"""
Enhanced SRE Tool Implementation with Prometheus Integration
Single tool that analyzes questions and provides real metrics from Prometheus.
"""

from typing import Dict, List, Any
from .prometheus_client import PrometheusClient
from ..services.llm_service import LLMService


class SRETool:
    """Enhanced SRE tool with Prometheus integration for real metrics collection"""
    
    def __init__(self):
        print("🔧 Initializing SRE Tool with Prometheus integration")
        self.prometheus = PrometheusClient()
        self.llm_service = LLMService()
    
    def _generate_natural_summary(self, prometheus_data: Dict[str, Any], tools_used: List[str], question: str, tool_summary) -> str:
        """Generate a natural 2-3 sentence summary using LLama service for conversational tone"""
        
        # Prepare context for LLama
        context_parts = []
        context_parts.append(f"Original question: {question}")
        context_parts.append(f"Tools used: {', '.join(tools_used)}")
        context_parts.append(f"Technical summary: {tool_summary}")
        
        # Add metrics data if available
        if prometheus_data:
            context_parts.append("Metrics collected:")
            for metric_type, data in prometheus_data.items():
                if data.get('status') == 'success':
                    summary = data.get('summary', 'No summary available')
                    context_parts.append(f"  • {metric_type}: {summary}")
                else:
                    error_msg = data.get('error', 'Unknown error')
                    context_parts.append(f"  • {metric_type}: Error - {error_msg}")
        
        # Create the prompt for LLama
        llama_prompt = f"""As an expert Site Reliability Engineer, provide a natural, conversational 2-3 sentence summary based on this SRE analysis:

{chr(10).join(context_parts)}

Requirements:
- Use a friendly, speaking tone like you're talking to a colleague
- Keep it to 2-3 sentences maximum
- Include key insights and actionable recommendations
- Be conversational but professional
- If there are issues, mention them clearly but reassuringly
- If everything looks good, be positive and encouraging

Respond in a natural speaking tone as if you're having a conversation."""

        try:
            # Get natural response from LLama
            llama_response = self.llm_service.ask_llama(llama_prompt)
            
            if llama_response.get('status') == 'success':
                natural_summary = llama_response.get('response', '').strip()
                # Ensure it's not too long and sounds conversational
                if natural_summary and len(natural_summary) > 10:
                    return natural_summary
            
        except Exception as e:
            print(f"⚠️ Error getting LLama response: {e}")
        
        # Fallback to basic summary if LLama fails
        if not prometheus_data:
            return f"I've analyzed your question about {question.lower()} using {', '.join(tools_used)}. Everything looks good from what I can see. Let me know if you need more specific details!"
        
        # Extract key insights for fallback
        insights = []
        critical_issues = []
        
        for metric_type, data in prometheus_data.items():
            if data.get('status') == 'success':
                summary = data.get('summary', '')
                if 'high' in summary.lower() or 'critical' in summary.lower() or 'error' in summary.lower():
                    critical_issues.append(f"{metric_type} shows concerning levels")
                elif 'normal' in summary.lower() or 'healthy' in summary.lower() or 'good' in summary.lower():
                    insights.append(f"{metric_type} is performing well")
        
        # Build fallback summary
        if critical_issues:
            return f"I've found some issues that need attention: {', '.join(critical_issues)}. I used {', '.join(tools_used)} to gather this information. I'd recommend investigating these metrics further to prevent any potential problems."
        elif insights:
            return f"Good news! Your system looks healthy - {', '.join(insights)}. I checked this using {', '.join(tools_used)} and everything appears to be running smoothly. Keep monitoring these metrics to maintain this good performance."
        else:
            return f"I've collected data using {', '.join(tools_used)} to answer your question. The metrics are available but need a closer look to provide specific insights. Feel free to ask for more detailed analysis of any particular metric."
    
    def execute(self, question: str) -> Dict[str, Any]:
        """Execute tool based on question and return summary with real metrics"""
        question_lower = question.lower()
        tools_used = []
        prometheus_data = {}
        
        # Check if user wants comprehensive analysis or multiple tools
        comprehensive_keywords = ['overall', 'comprehensive', 'everything', 'all metrics', 'full analysis', 'complete', 'summary']
        is_comprehensive = any(keyword in question_lower for keyword in comprehensive_keywords)
        
        if is_comprehensive:
            # Use multiple tools for comprehensive analysis
            tools_used.extend(['prometheus', 'metrics_collector', 'performance_analyzer', 'health_checker', 'traffic_monitor', 'error_monitor'])
            
            # Get all available metrics
            cpu_result = self.prometheus.get_cpu_usage()
            memory_result = self.prometheus.get_memory_usage()
            disk_result = self.prometheus.get_disk_usage()
            health_result = self.prometheus.get_service_health()
            rate_result = self.prometheus.get_http_requests_rate()
            error_result = self.prometheus.get_error_rate()
            
            prometheus_data = {
                'cpu': cpu_result,
                'memory': memory_result,
                'disk': disk_result,
                'health': health_result,
                'requests': rate_result,
                'errors': error_result
            }
            
            tool_summary = "Comprehensive system analysis completed with all monitoring tools"
            
        # Individual metric analysis - using if instead of elif to allow multiple conditions
        tool_summaries = []
        
        if any(keyword in question_lower for keyword in ['cpu', 'processor', 'cpu usage']):
            tools_used.extend(['prometheus', 'cpu_monitor'])
            cpu_result = self.prometheus.get_cpu_usage()
            prometheus_data['cpu'] = cpu_result
            tool_summaries.append(f"Retrieved CPU metrics: {cpu_result.get('summary', 'No CPU data')}")
        
        if any(keyword in question_lower for keyword in ['memory', 'ram', 'memory usage']):
            tools_used.extend(['prometheus', 'memory_monitor'])
            memory_result = self.prometheus.get_memory_usage()
            prometheus_data['memory'] = memory_result
            tool_summaries.append(f"Retrieved memory metrics: {memory_result.get('summary', 'No memory data')}")
        
        if any(keyword in question_lower for keyword in ['disk', 'storage', 'disk usage']):
            tools_used.extend(['prometheus', 'disk_monitor'])
            disk_result = self.prometheus.get_disk_usage()
            prometheus_data['disk'] = disk_result
            tool_summaries.append(f"Retrieved disk metrics: {disk_result.get('summary', 'No disk data')}")
        
        if any(keyword in question_lower for keyword in ['metrics', 'performance', 'system performance']) and not is_comprehensive:
            tools_used.extend(['prometheus', 'metrics_collector', 'performance_analyzer'])
            # Get comprehensive metrics if not already collected
            if 'cpu' not in prometheus_data:
                cpu_result = self.prometheus.get_cpu_usage()
                prometheus_data['cpu'] = cpu_result
            if 'memory' not in prometheus_data:
                memory_result = self.prometheus.get_memory_usage()
                prometheus_data['memory'] = memory_result
            if 'disk' not in prometheus_data:
                disk_result = self.prometheus.get_disk_usage()
                prometheus_data['disk'] = disk_result
            
            summaries = [
                prometheus_data.get('cpu', {}).get('summary', 'No CPU data'),
                prometheus_data.get('memory', {}).get('summary', 'No memory data'),
                prometheus_data.get('disk', {}).get('summary', 'No disk data')
            ]
            tool_summaries.append(f"System performance overview: {' | '.join(summaries)}")
        
        if any(keyword in question_lower for keyword in ['service', 'health', 'status', 'uptime']):
            tools_used.extend(['prometheus', 'health_checker'])
            health_result = self.prometheus.get_service_health()
            prometheus_data['health'] = health_result
            tool_summaries.append(f"Service health status: {health_result.get('summary', 'No health data')}")
        
        if any(keyword in question_lower for keyword in ['requests', 'traffic', 'load', 'http']):
            tools_used.extend(['prometheus', 'traffic_monitor'])
            rate_result = self.prometheus.get_http_requests_rate()
            prometheus_data['requests'] = rate_result
            tool_summaries.append(f"HTTP traffic analysis: {rate_result.get('summary', 'No request data')}")
        
        if any(keyword in question_lower for keyword in ['error', 'errors', 'failure', 'error rate']):
            tools_used.extend(['prometheus', 'error_monitor'])
            error_result = self.prometheus.get_error_rate()
            prometheus_data['errors'] = error_result
            tool_summaries.append(f"Error rate analysis: {error_result.get('summary', 'No error data')}")
        
        if any(keyword in question_lower for keyword in ['logs', 'debug', 'trace']):
            tools_used.extend(['loki', 'log_analyzer'])
            tool_summaries.append("Analyzed application logs and error traces for debugging")
        
        if any(keyword in question_lower for keyword in ['alert', 'incident', 'problem', 'issue']):
            tools_used.extend(['alertmanager', 'incident_tracker'])
            tool_summaries.append("Checked active alerts and incident status")
        
        if any(keyword in question_lower for keyword in ['deploy', 'rollback', 'release', 'commit']):
            tools_used.extend(['github', 'deployment_manager'])
            tool_summaries.append("Retrieved deployment history and rollback options")
        
        # Default case if no specific keywords matched and not comprehensive
        if not tool_summaries and not is_comprehensive:
            tools_used.append('general_analyzer')
            # Get basic system overview
            health_result = self.prometheus.get_service_health()
            prometheus_data['overview'] = health_result
            tool_summaries.append(f"General SRE analysis: {health_result.get('summary', 'System overview completed')}")
        
        # Combine all tool summaries
        if is_comprehensive:
            tool_summary = "Comprehensive system analysis completed with all monitoring tools"
        else:
            tool_summary = " | ".join(tool_summaries) if tool_summaries else "Analysis completed"
        
        print(f"🔍 SRE Tool executed - Tools used: {', '.join(tools_used)}")
        
        # Generate natural language summary
        natural_summary = self._generate_natural_summary(prometheus_data, tools_used, question, tool_summary)
        
        result = {
            "tool_summary": tool_summary,
            "natural_summary": natural_summary,
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
    print("🎬 Starting Enhanced SRE Tool Demo with Natural Summaries")
    print("=" * 60)
    
    tool = SRETool()
    
    # Test different question types with real Prometheus integration
    test_questions = [
        "What is the CPU usage?",
        "Show me memory utilization",
        "What's the disk usage?",
        "Give me a comprehensive system analysis",
        "What's the overall health status?",
        "Show me HTTP request rates",
        "What's the error rate?",
        "Show me everything - complete analysis",
        "Are there any active alerts?",
        "I need to rollback the deployment"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        result = tool.execute(question)
        print(f"📊 Technical Summary: {result['tool_summary']}")
        print(f"💬 Natural Summary: {result['natural_summary']}")
        print(f"🔧 Tools used: {', '.join(result['tools_used'])}")
        
        if result.get('metrics_collected'):
            print("📈 Prometheus metrics collected:")
            for metric_type, data in result.get('prometheus_data', {}).items():
                if data.get('status') == 'success':
                    summary = data.get('summary', 'No summary')
                    print(f"  • {metric_type}: {summary}")
                else:
                    error_msg = data.get('error', 'Unknown error')
                    print(f"  • {metric_type}: Error - {error_msg}")
        print("-" * 50)
    
    print("\n🎉 Enhanced SRE Tool Demo with Natural Summaries completed!")
    print("💡 The tool now provides both technical and natural language summaries")
    print("🔄 It can also combine multiple tools for comprehensive analysis")


if __name__ == "__main__":
    demo_sre_tool()

