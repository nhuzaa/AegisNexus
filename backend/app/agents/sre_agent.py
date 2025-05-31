from app.services.llm_service import send_to_langgraph, send_to_llama_api


class SREAgent:
    def __init__(self):
        pass

    def ask_question(self, question: str) -> dict:
        try:
            langgraph_response = send_to_langgraph(question)
            llama_response = send_to_llama_api(question)

            return {
                "langgraph": langgraph_response,
                "llama": llama_response
            }
        except Exception as e:
            return {
                "error": f"Error processing question: {str(e)}",
                "langgraph": {"error": "Failed to get response"},
                "llama": {"error": "Failed to get response"}
            }