from app.services.llm_service import send_to_langgraph, send_to_llama_api
from app.tools.sre_tools import SREToolsOrchestrator


class SREAgent:
    def __init__(self):
        self.tools = SREToolsOrchestrator()

    def ask_question(self, question: str) -> dict:
        try:
            # First, execute any relevant SRE tool operations
            tool_data = self._execute_tools_for_question(question)
            
            # Enhance the question with tool data for better LLM context
            enhanced_question = self._enhance_question_with_tools(question, tool_data)
            
            langgraph_response = send_to_langgraph(enhanced_question)
            llama_response = send_to_llama_api(enhanced_question)

            return {
                "langgraph": langgraph_response,
                "llama": llama_response,
                "tools_data": tool_data,
                "enhanced_context": True
            }
        except Exception as e:
            return {
                "error": f"Error processing question: {str(e)}",
                "langgraph": {"error": "Failed to get response"},
                "llama": {"error": "Failed to get response"},
                "tools_data": None,
                "enhanced_context": False
            }
    
    def _execute_tools_for_question(self, question: str) -> dict:
        """Execute relevant SRE tools based on the question content"""
        tool_data = {}
        question_lower = question.lower()
        
        try:
            # Check for metrics-related queries
            if any(keyword in question_lower for keyword in ['cpu', 'memory', 'metrics', 'performance']):
                print("🔍 Detected metrics query - fetching Prometheus data")
                tool_data['prometheus_cpu'] = self.tools.prometheus.query("cpu_usage_percent")
                tool_data['prometheus_memory'] = self.tools.prometheus.query("memory_usage_percent")
            
            # Check for log-related queries
            if any(keyword in question_lower for keyword in ['logs', 'errors', 'debug', 'trace']):
                print("📋 Detected log query - fetching Loki data")
                tool_data['logs'] = self.tools.loki.query_logs('{level="error"}', limit=20)
                tool_data['traces'] = self.tools.otel.get_traces("web-service", lookback="1h")
            
            # Check for alert-related queries
            if any(keyword in question_lower for keyword in ['alert', 'incident', 'problem', 'issue']):
                print("🚨 Detected alert query - fetching Alertmanager data")
                tool_data['alerts'] = self.tools.alertmanager.get_alerts()
            
            # Check for deployment-related queries
            if any(keyword in question_lower for keyword in ['deploy', 'rollback', 'release', 'commit']):
                print("🚀 Detected deployment query - fetching GitHub data")
                tool_data['recent_commits'] = self.tools.github.get_commits(per_page=10)
            
            # Check for dashboard-related queries
            if any(keyword in question_lower for keyword in ['dashboard', 'graph', 'visualization']):
                print("📊 Detected dashboard query - fetching Grafana data")
                tool_data['dashboard'] = self.tools.grafana.get_dashboard("infrastructure-overview")
            
            # Always include health check for system status questions
            if any(keyword in question_lower for keyword in ['health', 'status', 'system', 'overview']):
                print("🏥 Detected health query - running health check")
                tool_data['health_status'] = self.tools.health_check()
                tool_data['service_map'] = self.tools.otel.get_service_map()
                
        except Exception as e:
            print(f"⚠️ Error executing tools: {str(e)}")
            tool_data['tool_error'] = str(e)
        
        return tool_data
    
    def _enhance_question_with_tools(self, question: str, tool_data: dict) -> str:
        """Enhance the question with context from SRE tools"""
        if not tool_data:
            return question
        
        context_parts = [question, "\n\nSRE Tools Context:"]
        
        if 'prometheus_cpu' in tool_data:
            context_parts.append("- CPU metrics retrieved from Prometheus")
        
        if 'logs' in tool_data:
            log_count = len(tool_data['logs'].get('data', {}).get('result', []))
            context_parts.append(f"- {log_count} recent log entries analyzed")
        
        if 'alerts' in tool_data:
            alert_count = len(tool_data['alerts'])
            context_parts.append(f"- {alert_count} active alerts found")
        
        if 'recent_commits' in tool_data:
            commit_count = len(tool_data['recent_commits'])
            context_parts.append(f"- {commit_count} recent commits available for rollback")
        
        if 'health_status' in tool_data:
            healthy_tools = sum(1 for status in tool_data['health_status'].values() if status == 'healthy')
            context_parts.append(f"- {healthy_tools} SRE tools are healthy and operational")
        
        return "\n".join(context_parts)
    
    def execute_incident_response(self, alert_name: str, severity: str) -> dict:
        """Execute a complete incident response workflow"""
        try:
            print(f"🚨 Executing incident response for {alert_name} (severity: {severity})")
            workflow_result = self.tools.incident_response_workflow(alert_name, severity)
            
            # Generate LLM analysis of the incident
            incident_summary = f"""
            Incident Response Summary:
            Alert: {alert_name}
            Severity: {severity}
            Tools Data Collected: {len(workflow_result)} data sources
            
            Please analyze this incident and provide recommendations.
            """
            
            analysis = send_to_langgraph(incident_summary)
            
            return {
                "incident_response": workflow_result,
                "ai_analysis": analysis,
                "status": "completed"
            }
        except Exception as e:
            return {
                "error": f"Incident response failed: {str(e)}",
                "status": "failed"
            }
    
    def get_system_health(self) -> dict:
        """Get comprehensive system health report"""
        try:
            print("🏥 Generating comprehensive system health report")
            
            health_data = {
                "tools_health": self.tools.health_check(),
                "current_alerts": self.tools.alertmanager.get_alerts(),
                "service_map": self.tools.otel.get_service_map(),
                "recent_metrics": {
                    "cpu": self.tools.prometheus.query("cpu_usage_percent"),
                    "memory": self.tools.prometheus.query("memory_usage_percent")
                }
            }
            
            # Generate AI health assessment
            health_summary = f"""
            System Health Report:
            - Tools Status: {len([t for t, s in health_data['tools_health'].items() if s == 'healthy'])} healthy tools
            - Active Alerts: {len(health_data['current_alerts'])} alerts
            - Services Monitored: {len(health_data['service_map']['services'])} services
            
            Please provide a health assessment and recommendations.
            """
            
            ai_assessment = send_to_llama_api(health_summary)
            
            return {
                "health_data": health_data,
                "ai_assessment": ai_assessment,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        except Exception as e:
            return {
                "error": f"Health check failed: {str(e)}",
                "status": "failed"
            }