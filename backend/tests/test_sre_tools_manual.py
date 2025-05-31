#!/usr/bin/env python3
"""
Test runner for SRE tools - for manual testing and demonstrations
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.sre_tools import SREToolsOrchestrator, demo_sre_tools
from app.agents.sre_agent import SREAgent


def test_individual_tools():
    """Test each SRE tool individually"""
    print("🧪 Testing Individual SRE Tools")
    print("=" * 60)
    
    orchestrator = SREToolsOrchestrator()
    
    # Test Prometheus
    print("\n📊 Testing Prometheus...")
    cpu_data = orchestrator.prometheus.query("cpu_usage_percent")
    print(f"CPU query returned: {len(cpu_data['data']['result'])} metrics")
    
    # Test Grafana
    print("\n🎨 Testing Grafana...")
    dashboard = orchestrator.grafana.get_dashboard("test-dashboard")
    print(f"Dashboard '{dashboard['dashboard']['title']}' has {len(dashboard['dashboard']['panels'])} panels")
    
    # Test Loki
    print("\n📋 Testing Loki...")
    logs = orchestrator.loki.query_logs('{level="error"}', limit=5)
    log_count = len(logs['data']['result'][0]['values']) if logs['data']['result'] else 0
    print(f"Found {log_count} log entries")
    
    # Test Alertmanager
    print("\n🚨 Testing Alertmanager...")
    alerts = orchestrator.alertmanager.get_alerts()
    print(f"Found {len(alerts)} active alerts")
    
    # Test GitHub
    print("\n🐙 Testing GitHub...")
    commits = orchestrator.github.get_commits(per_page=3)
    print(f"Retrieved {len(commits)} recent commits")
    
    # Test Slack
    print("\n💬 Testing Slack...")
    slack_result = orchestrator.slack.send_message("test-channel", "Test message from SRE tools")
    print(f"Slack message sent: {slack_result['ok']}")
    
    # Test Teams
    print("\n🟦 Testing Teams...")
    teams_result = orchestrator.teams.send_message("Test Alert", "This is a test message")
    print(f"Teams message sent: {teams_result['status']}")
    
    # Test OpenTelemetry
    print("\n🔍 Testing OpenTelemetry...")
    traces = orchestrator.otel.get_traces("test-service")
    print(f"Retrieved {len(traces)} traces")
    
    service_map = orchestrator.otel.get_service_map()
    print(f"Service map has {len(service_map['services'])} services and {len(service_map['dependencies'])} dependencies")


def test_sre_agent():
    """Test the SRE agent with integrated tools"""
    print("\n🤖 Testing SRE Agent with Integrated Tools")
    print("=" * 60)
    
    agent = SREAgent()
    
    # Test different types of questions
    test_questions = [
        "What's the current CPU usage?",
        "Show me recent error logs",
        "Are there any active alerts?",
        "What's the system health status?",
        "Show me recent deployments"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        try:
            response = agent.ask_question(question)
            tools_used = len(response.get('tools_data', {}))
            print(f"   ✅ Response received, used {tools_used} tools")
            print(f"   📊 Enhanced context: {response.get('enhanced_context', False)}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")


def test_incident_response():
    """Test incident response workflow"""
    print("\n🚨 Testing Incident Response Workflow")
    print("=" * 60)
    
    agent = SREAgent()
    
    try:
        result = agent.execute_incident_response("HighCPUUsage", "critical")
        print(f"✅ Incident response completed: {result.get('status')}")
        workflow_steps = len(result.get('incident_response', {}))
        print(f"📋 Workflow executed {workflow_steps} steps")
    except Exception as e:
        print(f"❌ Incident response failed: {str(e)}")


def test_health_report():
    """Test system health report"""
    print("\n🏥 Testing System Health Report")
    print("=" * 60)
    
    agent = SREAgent()
    
    try:
        health_report = agent.get_system_health()
        tools_count = len(health_report.get('health_data', {}).get('tools_health', {}))
        alerts_count = len(health_report.get('health_data', {}).get('current_alerts', []))
        print(f"✅ Health report generated")
        print(f"🔧 Monitored tools: {tools_count}")
        print(f"🚨 Active alerts: {alerts_count}")
    except Exception as e:
        print(f"❌ Health report failed: {str(e)}")


def main():
    """Main test runner function"""
    print("🚀 SRE Tools Manual Test Suite")
    print("=" * 60)
    
    # Run the full demo first
    print("\n1️⃣ Running full SRE tools demo...")
    try:
        demo_sre_tools()
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    
    # Test individual components
    print("\n2️⃣ Testing individual tools...")
    test_individual_tools()
    
    print("\n3️⃣ Testing SRE agent integration...")
    test_sre_agent()
    
    print("\n4️⃣ Testing incident response...")
    test_incident_response()
    
    print("\n5️⃣ Testing health report...")
    test_health_report()
    
    print("\n🎉 All manual tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
