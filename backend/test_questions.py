#!/usr/bin/env python3
"""
Test script with appropriate questions for each SRE agent scenario
"""

import json
from app.agents.sre_agent import SREAgent

# Test questions organized by scenario
test_scenarios = {
    "comprehensive_analysis": [
        "Give me a comprehensive system analysis",
        "Show me everything - complete analysis", 
        "What's the overall health status?",
        "I need a full analysis of the system"
    ],
    
    "individual_metrics": {
        "cpu": [
            "What is the CPU usage?",
            "Show me CPU utilization",
            "How's the processor performance?"
        ],
        "memory": [
            "Show me memory utilization",
            "What's the RAM usage?",
            "Check memory consumption"
        ],
        "disk": [
            "What's the disk usage?",
            "Show me storage utilization",
            "Check disk space"
        ],
        "performance": [
            "Show me system performance",
            "What are the current metrics?",
            "Give me a performance overview"
        ],
        "health": [
            "What's the service health?",
            "Check system status",
            "Are all services running?"
        ],
        "traffic": [
            "Show me HTTP request rates",
            "What's the current traffic load?",
            "Check request volume"
        ],
        "errors": [
            "What's the error rate?",
            "Show me current failures",
            "Are there any error spikes?"
        ]
    },
    
    "operational": {
        "logs": [
            "Show me recent logs",
            "I need to debug something",
            "What do the logs show?"
        ],
        "alerts": [
            "Are there any active alerts?",
            "Show me current incidents",
            "What problems are we facing?"
        ],
        "deployment": [
            "I need to rollback the deployment",
            "Show me recent releases",
            "Check deployment history"
        ],
        "general": [
            "How is everything?",
            "Give me a general overview",
            "What's happening with the system?"
        ]
    }
}

def test_scenario(scenario_name, questions, agent):
    """Test a specific scenario with its questions"""
    print(f"\n🎯 Testing {scenario_name.upper()} Scenario")
    print("=" * 60)
    
    for i, question in enumerate(questions[:2], 1):  # Test first 2 questions
        print(f"\n❓ Question {i}: {question}")
        result = agent.ask_question(question)
        print(f"📊 Technical: {result['tool_summary']}")
        print(f"💬 Natural: {result['natural_summary']}")
        print(f"🔧 Tools: {', '.join(result['tools_used'])}")
        print("-" * 40)

def main():
    """Main test function"""
    print("🚀 SRE Agent Question Testing Suite")
    print("=" * 80)
    
    agent = SREAgent()
    
    # Test comprehensive analysis
    test_scenario("comprehensive_analysis", test_scenarios["comprehensive_analysis"], agent)
    
    # Test individual metrics
    for metric_type, questions in test_scenarios["individual_metrics"].items():
        test_scenario(f"individual_{metric_type}", questions, agent)
    
    # Test operational scenarios
    for op_type, questions in test_scenarios["operational"].items():
        test_scenario(f"operational_{op_type}", questions, agent)
    
    print("\n🎉 All scenario testing completed!")
    print("💡 Each scenario demonstrates different tool combinations and natural summaries")

if __name__ == "__main__":
    main()
