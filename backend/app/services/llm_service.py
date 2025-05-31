from langgraph_sdk import get_client
from llama_api_client import LlamaAPIClient
import os
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('.env.local')


class LLMService:
    def __init__(self):
        self.langgraph_client = get_client(
            url=os.getenv("LANGGRAPH_API_URL"),
            api_key=os.getenv("LANGGRAPH_API_KEY")
        )
        self.llama_api = LlamaAPIClient(api_key=os.getenv("LLAMA_API_KEY"))

    def ask_langgraph(self, question: str) -> dict:
        try:
            # This is a placeholder - adjust based on your LangGraph setup
            response = {
                "response": f"LangGraph response for: {question}",
                "status": "success"
            }
            return response
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def ask_llama(self, question: str) -> dict:
        try:
            response = self.llama_api.chat.completions.create(
                messages=[
                    {"role": "user", "content": question}
                ],
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                stream=False
            )
            return {
                "response": response.completion_message.content.text,
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def format_response(self, langgraph_response: dict,
                        llama_response: dict) -> dict:
        return {
            "langgraph": langgraph_response,
            "llama": llama_response
        }


# Standalone functions for backward compatibility
def send_to_langgraph(question: str) -> dict:
    llm_service = LLMService()
    return llm_service.ask_langgraph(question)


def send_to_llama_api(question: str) -> dict:
    llm_service = LLMService()
    return llm_service.ask_llama(question)