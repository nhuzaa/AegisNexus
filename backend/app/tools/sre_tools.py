"""
Simplified SRE Tool Implementation
Single tool that analyzes questions and provides summary and tools used.
"""

from typing import Dict, List, Any


class SRETool:
    """Single SRE tool that analyzes questions and provides basic responses"""
    
    def __init__(self):
        print("🔧 Initializing SRE Tool")
    
    def execute(self, question: str) -> Dict[str, Any]:
        """Execute tool based on question and return summary"""
        question_lower = question.lower()
        tools_used = []
        
        # Determine which tools would be used based on question content
        if any(keyword in question_lower for keyword in ['cpu', 'memory', 'metrics', 'performance']):
            tools_used.extend(['prometheus', 'metrics_collector'])
            tool_summary = "Retrieved system performance metrics and resource utilization data"
        
        elif any(keyword in question_lower for keyword in ['logs', 'errors', 'debug', 'trace']):
            tools_used.extend(['loki', 'log_analyzer'])
            tool_summary = "Analyzed application logs and error traces for debugging"
        
        elif any(keyword in question_lower for keyword in ['alert', 'incident', 'problem', 'issue']):
            tools_used.extend(['alertmanager', 'incident_tracker'])
            tool_summary = "Checked active alerts and incident status"
        
        elif any(keyword in question_lower for keyword in ['deploy', 'rollback', 'release', 'commit']):
            tools_used.extend(['github', 'deployment_manager'])
            tool_summary = "Retrieved deployment history and rollback options"
        
        elif any(keyword in question_lower for keyword in ['health', 'status', 'system', 'overview']):
            tools_used.extend(['health_checker', 'system_monitor'])
            tool_summary = "Performed system health check and service status verification"
        
        else:
            tools_used.append('general_analyzer')
            tool_summary = "Performed general SRE analysis and system overview"
        
        print(f"🔍 SRE Tool executed - Tools used: {', '.join(tools_used)}")
        
        return {
            "tool_summary": tool_summary,
            "tools_used": tools_used
        }


def demo_sre_tool():
    """Demonstrate SRE Tool functionality"""
    print("🎬 Starting SRE Tool Demo")
    print("=" * 50)
    
    tool = SRETool()
    
    # Test different question types
    test_questions = [
        "What is the CPU usage?",
        "Show me the error logs",
        "Are there any active alerts?",
        "I need to rollback the deployment",
        "What's the system health status?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        result = tool.execute(question)
        print(f"Summary: {result['tool_summary']}")
        print(f"Tools used: {', '.join(result['tools_used'])}")
    
    print("\n🎉 SRE Tool Demo completed successfully!")


if __name__ == "__main__":
    demo_sre_tool()

