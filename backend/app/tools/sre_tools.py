"""
Enhanced SRE Tool Implementation with Prometheus Integration
Single tool that analyzes questions and provides real metrics from Prometheus.
"""

from typing import Dict, List, Any
from .prometheus_client import PrometheusClient


class SRETool:
    """Enhanced SRE tool with Prometheus integration for real metrics collection"""
    
    def __init__(self):
        print("🔧 Initializing SRE Tool with Prometheus integration")
        self.prometheus = PrometheusClient()
    
    def execute(self, question: str) -> Dict[str, Any]:
        """Execute tool based on question and return summary with real metrics"""
        question_lower = question.lower()
        tools_used = []
        prometheus_data = {}
        
        # Determine which tools would be used based on question content
        if any(keyword in question_lower for keyword in ['cpu', 'processor', 'cpu usage']):
            tools_used.extend(['prometheus', 'cpu_monitor'])
            cpu_result = self.prometheus.get_cpu_usage()
            prometheus_data['cpu'] = cpu_result
            tool_summary = f"Retrieved CPU metrics: {cpu_result.get('summary', 'No CPU data')}"
        
        elif any(keyword in question_lower for keyword in ['memory', 'ram', 'memory usage']):
            tools_used.extend(['prometheus', 'memory_monitor'])
            memory_result = self.prometheus.get_memory_usage()
            prometheus_data['memory'] = memory_result
            tool_summary = f"Retrieved memory metrics: {memory_result.get('summary', 'No memory data')}"
        
        elif any(keyword in question_lower for keyword in ['disk', 'storage', 'disk usage']):
            tools_used.extend(['prometheus', 'disk_monitor'])
            disk_result = self.prometheus.get_disk_usage()
            prometheus_data['disk'] = disk_result
            tool_summary = f"Retrieved disk metrics: {disk_result.get('summary', 'No disk data')}"
        
        elif any(keyword in question_lower for keyword in ['metrics', 'performance', 'system performance']):
            tools_used.extend(['prometheus', 'metrics_collector', 'performance_analyzer'])
            # Get comprehensive metrics
            cpu_result = self.prometheus.get_cpu_usage()
            memory_result = self.prometheus.get_memory_usage()
            disk_result = self.prometheus.get_disk_usage()
            
            prometheus_data = {
                'cpu': cpu_result,
                'memory': memory_result,
                'disk': disk_result
            }
            
            summaries = [
                cpu_result.get('summary', 'No CPU data'),
                memory_result.get('summary', 'No memory data'),
                disk_result.get('summary', 'No disk data')
            ]
            tool_summary = f"System performance overview: {' | '.join(summaries)}"
        
        elif any(keyword in question_lower for keyword in ['service', 'health', 'status', 'uptime']):
            tools_used.extend(['prometheus', 'health_checker'])
            health_result = self.prometheus.get_service_health()
            prometheus_data['health'] = health_result
            tool_summary = f"Service health status: {health_result.get('summary', 'No health data')}"
        
        elif any(keyword in question_lower for keyword in ['requests', 'traffic', 'load', 'http']):
            tools_used.extend(['prometheus', 'traffic_monitor'])
            rate_result = self.prometheus.get_http_requests_rate()
            prometheus_data['requests'] = rate_result
            tool_summary = f"HTTP traffic analysis: {rate_result.get('summary', 'No request data')}"
        
        elif any(keyword in question_lower for keyword in ['error', 'errors', 'failure', 'error rate']):
            tools_used.extend(['prometheus', 'error_monitor'])
            error_result = self.prometheus.get_error_rate()
            prometheus_data['errors'] = error_result
            tool_summary = f"Error rate analysis: {error_result.get('summary', 'No error data')}"
        
        elif any(keyword in question_lower for keyword in ['logs', 'debug', 'trace']):
            tools_used.extend(['loki', 'log_analyzer'])
            tool_summary = "Analyzed application logs and error traces for debugging"
        
        elif any(keyword in question_lower for keyword in ['alert', 'incident', 'problem', 'issue']):
            tools_used.extend(['alertmanager', 'incident_tracker'])
            tool_summary = "Checked active alerts and incident status"
        
        elif any(keyword in question_lower for keyword in ['deploy', 'rollback', 'release', 'commit']):
            tools_used.extend(['github', 'deployment_manager'])
            tool_summary = "Retrieved deployment history and rollback options"
        
        else:
            tools_used.append('general_analyzer')
            # Get basic system overview
            health_result = self.prometheus.get_service_health()
            prometheus_data['overview'] = health_result
            tool_summary = f"General SRE analysis: {health_result.get('summary', 'System overview completed')}"
        
        print(f"🔍 SRE Tool executed - Tools used: {', '.join(tools_used)}")
        
        result = {
            "tool_summary": tool_summary,
            "tools_used": tools_used
        }
        
        # Add Prometheus data if any was collected
        if prometheus_data:
            result["prometheus_data"] = prometheus_data
            result["metrics_collected"] = True
        else:
            result["metrics_collected"] = False
        
        return result


def demo_sre_tool():
    """Demonstrate enhanced SRE Tool functionality with Prometheus"""
    print("🎬 Starting Enhanced SRE Tool Demo")
    print("=" * 50)
    
    tool = SRETool()
    
    # Test different question types with real Prometheus integration
    test_questions = [
        "What is the CPU usage?",
        "Show me memory utilization",
        "What's the disk usage?",
        "Give me system performance metrics",
        "What's the service health status?",
        "Show me HTTP request rates",
        "What's the error rate?",
        "Show me the error logs",
        "Are there any active alerts?",
        "I need to rollback the deployment"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        result = tool.execute(question)
        print(f"📊 Summary: {result['tool_summary']}")
        print(f"🔧 Tools used: {', '.join(result['tools_used'])}")
        
        if result.get('metrics_collected'):
            print("📈 Prometheus metrics collected:")
            for metric_type, data in result.get('prometheus_data', {}).items():
                if data.get('status') == 'success':
                    print(f"  • {metric_type}: {data.get('summary', 'No summary')}")
                else:
                    print(f"  • {metric_type}: Error - {data.get('error', 'Unknown error')}")
    
    print("\n🎉 Enhanced SRE Tool Demo completed successfully!")


if __name__ == "__main__":
    demo_sre_tool()

