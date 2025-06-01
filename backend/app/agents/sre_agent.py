from app.services.llm_service import send_to_langgraph, send_to_llama_api
from app.tools.sre_tools import SRETool


class SREAgent:
    def __init__(self):
        self.tool = SRETool()

    def ask_question(self, question: str) -> dict:
        try:
            # Execute tool and get summary
            tool_result = self.tool.execute(question)
            
            # Generate LLM thought about the question
            llm_thought = f"Analyzing SRE question: '{question}' - {tool_result['tool_summary']}"
            
            # Get LLM responses
            langgraph_response = send_to_langgraph(question)
            llama_response = send_to_llama_api(question)

            return {
                "tool_summary": tool_result["tool_summary"],
                "natural_summary": tool_result["natural_summary"],
                "tools_used": tool_result["tools_used"],
                "llm_thought": llm_thought,
                "langgraph": langgraph_response,
                "llama": llama_response
            }
        except Exception as e:
            return {
                "tool_summary": "Error occurred during tool execution",
                "tools_used": ["error_handler"],
                "llm_thought": f"Error processing question: {str(e)}",
                "langgraph": {"error": "Failed to get response"},
                "llama": {"error": "Failed to get response"}
            }
