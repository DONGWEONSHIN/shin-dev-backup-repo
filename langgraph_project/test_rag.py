from rag_system import process_message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_rag():
    # Test questions about King Jangsu
    questions = [
        "고구려의 장수왕은 어떤 정책을 통해 영토를 확장했는가?",
        # "장수왕의 평양 천도는 언제 이루어졌으며, 그 목적은 무엇이었나?",
        # "장수왕은 백제와의 전투에서 어떤 성과를 거두었는가?",
        # "장수왕의 행정 제도 개혁의 주요 내용은 무엇인가?",
        # "장수왕 치세의 역사적 의의는 무엇인가?",
    ]

    print("\nRAG 시스템 테스트를 시작합니다...\n")

    # Process each question
    chat_history = []
    for question in questions:
        print(f"\nQuery: {question}\n")
        print("Processing...\n")
        chat_history = process_message(question, chat_history)
        print(chat_history[-1].content)  # Print the last response
        print("\n" + "=" * 80 + "\n")  # Separator


if __name__ == "__main__":
    test_rag()
