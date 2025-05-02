import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# Load environment variables
load_dotenv()

# Constants
DOCUMENTS_DIR = "documents"
CHROMA_PERSIST_DIR = "./chroma_db"
CHUNK_SIZE = 500  # Reduced chunk size for better granularity
CHUNK_OVERLAP = 100  # Reduced overlap


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove excessive whitespace
    text = " ".join(text.split())
    # Remove special characters that might affect embedding quality
    text = text.replace("\u200b", "")  # Zero-width space
    text = text.replace("\ufeff", "")  # Zero-width no-break space
    return text


def enhance_metadata(doc: Document, file_path: str) -> Dict[str, Any]:
    """Enhance document metadata with additional information."""
    metadata = doc.metadata.copy()

    # Add source file information
    metadata["source"] = file_path
    metadata["filename"] = os.path.basename(file_path)

    # Add content statistics
    content = doc.page_content
    metadata["char_count"] = len(content)
    metadata["word_count"] = len(content.split())

    # Add chunk position information if available
    if "chunk" in metadata:
        metadata["chunk_index"] = metadata["chunk"]

    return metadata


def process_document(
    file_path: str, text_splitter: RecursiveCharacterTextSplitter
) -> List[Document]:
    """Process a single document with enhanced error handling and metadata."""
    try:
        # Load document
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Clean and enhance each document
        enhanced_docs = []
        for doc in documents:
            # Clean text
            doc.page_content = clean_text(doc.page_content)

            # Skip empty documents
            if not doc.page_content.strip():
                continue

            # Enhance metadata
            doc.metadata = enhance_metadata(doc, file_path)
            enhanced_docs.append(doc)

        # Split documents
        splits = text_splitter.split_documents(enhanced_docs)

        print(f"Successfully processed {file_path}:")
        print(f"- Original pages: {len(documents)}")
        print(f"- Generated chunks: {len(splits)}")

        return splits

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return []


def add_documents(directory_path: str):
    """Add documents from a directory to the vector store with improved processing."""
    # Initialize embeddings
    embeddings = OllamaEmbeddings(
        model="qwen3:30b-a3b", base_url="http://localhost:11434"
    )

    # Initialize text splitter with smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
    )

    # Create documents directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"\nCreated documents directory at {directory_path}")
        print("Please add PDF documents to this directory and run this command again.")
        return

    # Process documents
    all_splits = []
    pdf_files = []

    # First, collect all PDF files
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    if not pdf_files:
        print("No PDF documents found in the specified directory.")
        return

    print(f"\nFound {len(pdf_files)} PDF files to process.")

    # Process each document
    for file_path in pdf_files:
        splits = process_document(file_path, text_splitter)
        all_splits.extend(splits)

    if not all_splits:
        print("No valid content extracted from documents.")
        return

    print(f"\nTotal chunks created: {len(all_splits)}")

    # Initialize and update vector store
    print("\nUpdating vector store...")
    vectorstore = Chroma(
        collection_name="rag_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    # Clear existing documents
    vectorstore.delete_collection()
    vectorstore = Chroma(
        collection_name="rag_docs",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    # Add documents in batches
    batch_size = 50
    for i in range(0, len(all_splits), batch_size):
        batch = all_splits[i : i + batch_size]
        vectorstore.add_documents(batch)
        print(f"Added batch {i//batch_size + 1}/{(len(all_splits)-1)//batch_size + 1}")

    print(f"\nSuccessfully added {len(all_splits)} document chunks to the vector store")


if __name__ == "__main__":
    # Example usage
    docs_dir = "documents"  # Create this directory and add your documents
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        print(f"Created documents directory: {docs_dir}")
        print("Please add your PDF documents to this directory and run again")
    else:
        add_documents(docs_dir)
