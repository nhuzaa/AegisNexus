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

    def ask_langgraph(self, question: str, tools_used: list = None,
                      tool_summary: str = None, 
                      natural_summary: str = None) -> dict:
        try:
            # Build context-aware prompt including tool information
            enhanced_question = question
            
            # Add tool context if available
            if tools_used or tool_summary:
                context_parts = []
                if tools_used:
                    tools_list = ', '.join(tools_used)
                    context_parts.append(f"Tools used: {tools_list}")
                if tool_summary:
                    context_parts.append(f"Tool analysis: {tool_summary}")
                if natural_summary:
                    context_parts.append(f"Summary: {natural_summary}")

                tool_context = "\n".join(context_parts)
                enhanced_question = f"""Based on the following SRE tool analysis, please provide additional insights and recommendations:

{tool_context}

Original question: {question}

Please provide actionable SRE insights, potential root causes, and recommended next steps."""

            # This is a placeholder - adjust based on your LangGraph setup
            response = {
                "response": f"LangGraph response for: {enhanced_question}",
                "status": "success"
            }
            return response
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def ask_llama(self, question: str, tools_used: list = None,
                  tool_summary: str = None, 
                  natural_summary: str = None) -> dict:
        try:
            # Build context-aware prompt including tool information
            system_context = ("You are an expert Site Reliability Engineer "
                             "(SRE) assistant. You have access to various "
                             "monitoring and operational tools to help "
                             "diagnose and resolve system issues.")

            # Add tool context if available
            if tools_used or tool_summary:
                context_parts = []
                if tools_used:
                    tools_list = ', '.join(tools_used)
                    context_parts.append(f"Tools used: {tools_list}")
                if tool_summary:
                    context_parts.append(f"Tool analysis: {tool_summary}")
                if natural_summary:
                    context_parts.append(f"Summary: {natural_summary}")

                tool_context = "\n".join(context_parts)
                enhanced_question = f"""Based on the following SRE tool analysis, please provide additional insights and recommendations:

{tool_context}

Original question: {question}

Please provide actionable SRE insights, potential root causes, and recommended next steps."""
            else:
                enhanced_question = question

            messages = [
                {"role": "system", "content": system_context},
                {"role": "user", "content": enhanced_question}
            ]

            response = self.llama_api.chat.completions.create(
                messages=messages,
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
def send_to_langgraph(question: str, tools_used: list = None,
                      tool_summary: str = None,
                      natural_summary: str = None) -> dict:
    llm_service = LLMService()
    return llm_service.ask_langgraph(question, tools_used,
                                     tool_summary, natural_summary)


def send_to_llama_api(question: str, tools_used: list = None,
                      tool_summary: str = None,
                      natural_summary: str = None) -> dict:
    llm_service = LLMService()
    return llm_service.ask_llama(question, tools_used, tool_summary,
                                 natural_summary)