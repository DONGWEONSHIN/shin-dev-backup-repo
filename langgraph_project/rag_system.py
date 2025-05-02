"""
RAG system implementation using LangGraph.
"""

from typing import Annotated, Sequence, List, Dict, Any
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
)
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.graph import END, StateGraph
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load environment variables
load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")


# State definition
class GraphState(TypedDict):
    """State definition for the RAG system graph."""

    messages: Annotated[Sequence[BaseMessage], "Chat messages"]
    context: Annotated[list[Document], "Retrieved documents"]
    next_step: Annotated[str, "Next step in the pipeline"]
    query: Annotated[str, "User query"]


# Initialize components
llm = ChatOllama(
    model=OLLAMA_MODEL,
    temperature=0,
    system="""당신은 도움이 되는 AI 어시스턴트입니다. 모든 답변을 한국어로 해주세요. 
전문적이고 정중한 어투를 사용해주세요.

답변 과정:
1. <think> 태그 안에서 질문에 대한 생각을 정리하세요.
   - 주요 개념 파악
   - 관련 정보 회상
   - 논리적 구조화
   - 중요 포인트 확인
2. 정리된 생각을 바탕으로 명확하고 구조화된 답변을 작성하세요.
3. 필요한 경우 예시나 실제 사례를 포함하세요.""",
)

embeddings = OllamaEmbeddings(
    model=OLLAMA_MODEL,
)

# Initialize vector store
vectorstore = Chroma(
    collection_name="rag_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)


def rerank_documents(
    query: str, docs: List[Document], scores: List[float], k: int = 5
) -> List[Document]:
    """Rerank documents using a more sophisticated approach."""
    # 1. Calculate query embedding
    query_embedding = embeddings.embed_query(query)

    # 2. Get document embeddings
    doc_embeddings = [embeddings.embed_query(doc.page_content) for doc in docs]

    # 3. Calculate semantic similarity scores
    semantic_scores = cosine_similarity([query_embedding], doc_embeddings)[0]

    # 4. Calculate content length scores (normalize by max length)
    lengths = [len(doc.page_content.split()) for doc in docs]
    max_length = max(lengths) if lengths else 1
    length_scores = [length / max_length for length in lengths]

    # 5. Calculate metadata relevance scores
    metadata_scores = []
    for doc in docs:
        score = 0
        if doc.metadata:
            # Add score for having metadata
            score += 0.2
            # Add score for specific metadata fields
            if "source" in doc.metadata:
                score += 0.3
            if "page" in doc.metadata:
                score += 0.3
        metadata_scores.append(score)

    # 6. Combine scores with weights
    final_scores = []
    for i in range(len(docs)):
        score = (
            0.5 * semantic_scores[i]  # Semantic similarity
            + 0.2 * scores[i]  # Original similarity
            + 0.2 * length_scores[i]  # Content length
            + 0.1 * metadata_scores[i]  # Metadata presence
        )
        final_scores.append(score)

    # 7. Sort and return top k documents
    ranked_pairs = sorted(zip(final_scores, docs), reverse=True)
    return [doc for _, doc in ranked_pairs[:k]]


def filter_similar_chunks(
    docs: List[Document], threshold: float = 0.8
) -> List[Document]:
    """Filter out very similar document chunks."""
    if not docs:
        return []

    # Get embeddings for all documents
    embeddings_list = [embeddings.embed_query(doc.page_content) for doc in docs]

    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(embeddings_list)

    # Keep track of documents to remove
    to_remove = set()

    # Check each pair of documents
    for i in range(len(docs)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(docs)):
            if j in to_remove:
                continue
            if similarity_matrix[i][j] > threshold:
                # Keep the longer document
                if len(docs[i].page_content) < len(docs[j].page_content):
                    to_remove.add(i)
                else:
                    to_remove.add(j)

    # Return filtered documents
    return [doc for i, doc in enumerate(docs) if i not in to_remove]


# Retrieval function
def retrieve(state: GraphState) -> GraphState:
    """Retrieve relevant documents based on the user query."""
    query = state["query"]
    print(f"\n[검색 중...] 질문: {query}")

    # 1. Initial search with high k value
    search_results = vectorstore.similarity_search_with_score(
        query, k=15  # Get more initial results
    )

    print("\n[디버그] 검색 결과 상세:")
    docs_with_scores = []
    for doc, score in search_results:
        similarity = 1 - score  # Convert distance to similarity
        if similarity > 0.2:  # Lower threshold for initial filtering
            print(f"\n문서 유사도: {similarity:.2%}")
            # Extract source filename from path if available
            source = doc.metadata.get("source", "문서 출처 없음")
            if isinstance(source, str) and "/" in source:
                source = source.split("/")[-1]  # Get just the filename
            page = doc.metadata.get("page", "페이지 정보 없음")
            print(f"출처: {source}")
            print(f"페이지: {page}")
            print(f"내용 미리보기: {doc.page_content[:200]}...")
            docs_with_scores.append((doc, similarity))

    if not docs_with_scores:
        print("\n[주의] 관련성 높은 문서를 찾지 못했습니다.")
        state["context"] = []
        return state

    # 2. Filter similar chunks
    docs = [doc for doc, _ in docs_with_scores]
    scores = [score for _, score in docs_with_scores]
    filtered_docs = filter_similar_chunks(docs)

    # 3. Rerank documents
    reranked_docs = rerank_documents(query, filtered_docs, scores)

    if reranked_docs:
        print(f"\n[검색 완료] {len(reranked_docs)}개의 관련 문서를 찾았습니다.")
        state["context"] = reranked_docs
    else:
        print("\n[주의] 필터링 후 관련성 높은 문서가 없습니다.")
        state["context"] = []

    return state


# Decide next step function
def decide(state: GraphState) -> GraphState:
    """Decide the next step in the conversation."""
    # If we've already retrieved context, move to respond
    if state["context"]:
        state["next_step"] = "respond"
        return state

    # If no context was found, try to determine if we should retry
    messages = state["messages"]
    last_message = messages[-1].content if messages else ""

    # Ask LLM if we should try another search or end
    response = llm.invoke(
        [
            *messages[:-1],  # Previous context
            HumanMessage(content=last_message),  # Last user message
            (
                "system",
                """대화를 분석하고 다음 단계를 결정하세요:
1. 'retrieve': 다음 경우에 선택
   - 질문이 구체적인 정보나 사실을 요구하는 경우
   - 이전 검색 결과가 불충분한 경우
   - 다른 관점이나 추가 정보가 필요한 경우
2. 'end': 다음 경우에 선택
   - 일반적인 대화나 인사인 경우
   - 충분한 정보가 이미 제공된 경우
   - 더 이상의 검색이 도움되지 않을 경우

'retrieve' 또는 'end' 중 하나로만 답변하세요.""",
            ),
        ]
    )

    next_step = response.content.strip().lower()
    if next_step not in ["retrieve", "end"]:
        next_step = "end"  # Default to end if unclear

    state["next_step"] = next_step
    return state


# Generate response function
def generate_response(state: GraphState) -> GraphState:
    """Generate a response based on the context and conversation history."""
    # Format context with source information
    context_texts = []
    if state["context"]:
        print("\n[컨텍스트] 사용할 문서:")
        for i, doc in enumerate(state["context"], 1):
            # Extract source filename from path if available
            source = doc.metadata.get("source", "문서 출처 없음")
            if isinstance(source, str) and "/" in source:
                source = source.split("/")[-1]  # Get just the filename
            page_num = doc.metadata.get("page", "페이지 정보 없음")

            # Add document relevance information
            relevance_info = "관련도: 높음" if i <= 3 else "관련도: 중간"

            context_text = (
                f"문서 {i} (출처: {source}, "
                f"페이지: {page_num}, {relevance_info}):\n{doc.page_content}\n"
            )
            context_texts.append(context_text)
            print(f"\n{context_text}")

    context_text = "\n".join(context_texts)

    system_msg = (
        "당신은 도움이 되는 AI 어시스턴트입니다. 다음 지침을 엄격히 따라주세요:\n\n"
        "1. 제공된 컨텍스트에서 직접적으로 찾을 수 있는 정보만 사용하세요.\n"
        "2. 컨텍스트에 명시적으로 언급되지 않은 정보는 절대 포함하지 마세요.\n"
        "3. 연도, 날짜, 수치 등은 컨텍스트에서 직접 인용된 것만 사용하세요.\n"
        "4. 컨텍스트에서 정보를 찾을 수 없다면, '죄송합니다. 제공된 문서에서 해당 질문에 대한 "
        "정보를 찾을 수 없습니다.'라고 답변하세요.\n"
        "5. 일반적인 지식이나 추론을 통한 답변은 하지 마세요.\n\n"
        "답변 과정:\n"
        "1. <think> 태그 안에서 다음을 수행하세요:\n"
        "   - 제공된 컨텍스트를 자세히 분석\n"
        "   - 질문과 관련된 정보 식별\n"
        "   - 정보의 직접적인 관련성 확인\n"
        "   - 불확실하거나 추론이 필요한 정보 제외\n"
        "2. 컨텍스트에서 찾은 정보만으로 답변을 작성하세요.\n"
        "3. 답변 마지막에 '[참고 문서]' 섹션을 추가하고, 실제로 정보를 찾은 문서만 나열하세요.\n"
        "4. 정보가 부족하거나 불확실한 경우, 솔직하게 그 사실을 인정하세요.\n"
    )

    # Generate response with enhanced context handling
    response = llm.invoke(
        [
            ("system", system_msg),
            *state["messages"][:-1],  # Chat history
            ("system", f"컨텍스트: {context_text}"),
            state["messages"][-1],  # Last message
        ]
    )

    # Format response with source information
    if not state["context"]:
        response_content = (
            f"{response.content}\n\n"
            "이 답변은 일반적인 지식을 바탕으로 생성되었습니다."
        )
    else:
        # Add source information with relevance indicators
        sources = []
        for i, doc in enumerate(state["context"], 1):
            source = doc.metadata.get("source", "문서 출처 없음")
            if isinstance(source, str) and "/" in source:
                source = source.split("/")[-1]
            relevance = "높음" if i <= 3 else "중간"
            sources.append(f"- 문서 {i} (출처: {source}, 관련도: {relevance})")

        response_content = (
            f"{response.content}\n\n" "[참고 문서]\n" f"{chr(10).join(sources)}"
        )

    state["messages"].append(AIMessage(content=response_content))
    return state


# Create the graph
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("decide", decide)
workflow.add_node("generate_response", generate_response)

# Add edges
workflow.add_edge("retrieve", "decide")
workflow.add_edge("decide", "generate_response")
workflow.add_edge("generate_response", END)

# Set entry point
workflow.set_entry_point("retrieve")

# Compile the graph
app = workflow.compile()


def process_message(
    message: str, chat_history: list[BaseMessage] = None
) -> list[BaseMessage]:
    """Process a message through the RAG system."""
    if chat_history is None:
        chat_history = []

    msg = HumanMessage(content=message)
    messages = chat_history + [msg]
    result = app.invoke(
        {"messages": messages, "context": [], "next_step": "retrieve", "query": message}
    )
    return result["messages"]


if __name__ == "__main__":
    # Example usage
    response = process_message("What can you tell me about LangGraph?")
    print(response[-1].content)
