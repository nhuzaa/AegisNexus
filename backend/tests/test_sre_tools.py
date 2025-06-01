#!/usr/bin/env python3
"""
Test suite for SRE tools functionality
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.sre_tools import (
    SREToolsOrchestrator,
    PrometheusClient,
    GrafanaAPI,
    LokiClient,
    AlertmanagerClient,
    GitHubAPI,
    SlackAPI,
    TeamsAPI,
    OpenTelemetryClient,
    demo_sre_tools
)
from app.agents.sre_agent import SREAgent


class TestPrometheusClient:
    """Test Prometheus client functionality"""
    
    def test_prometheus_client_init(self):
        """Test Prometheus client initialization"""
        client = PrometheusClient()
        assert client.server_url == "http://prometheus:9090"
    
    def test_prometheus_query_cpu(self):
        """Test Prometheus CPU metrics query"""
        client = PrometheusClient()
        result = client.query("cpu_usage_percent")
        
        assert result["status"] == "success"
        assert "data" in result
        assert "result" in result["data"]
        assert len(result["data"]["result"]) == 2  # Mock returns 2 instances
    
    def test_prometheus_query_memory(self):
        """Test Prometheus memory metrics query"""
        client = PrometheusClient()
        result = client.query("memory_usage_percent")
        
        assert result["status"] == "success"
        assert "data" in result
        assert len(result["data"]["result"]) == 1  # Mock returns 1 instance
    
    def test_prometheus_query_range(self):
        """Test Prometheus range query"""
        client = PrometheusClient()
        result = client.query_range("cpu_usage_percent", "1h", "now", "1m")
        
        assert result["status"] == "success"
        assert result["data"]["resultType"] == "matrix"
        assert len(result["data"]["result"]) == 1


class TestGrafanaAPI:
    """Test Grafana API functionality"""
    
    def test_grafana_client_init(self):
        """Test Grafana client initialization"""
        client = GrafanaAPI()
        assert client.base_url == "http://grafana:3000"
        assert client.api_key == "mock-api-key"
    
    def test_get_dashboard(self):
        """Test getting dashboard"""
        client = GrafanaAPI()
        dashboard = client.get_dashboard("test-dashboard")
        
        assert dashboard["dashboard"]["uid"] == "test-dashboard"
        assert dashboard["dashboard"]["title"] == "Infrastructure Overview"
        assert len(dashboard["dashboard"]["panels"]) == 2
    
    def test_get_dashboard_annotations(self):
        """Test getting dashboard annotations"""
        client = GrafanaAPI()
        annotations = client.get_dashboard_annotations(1, 0, 999999999999)
        
        assert len(annotations) == 2
        assert annotations[0]["text"] == "Deployment started"
        assert annotations[1]["text"] == "High CPU alert triggered"


class TestLokiClient:
    """Test Loki client functionality"""
    
    def test_loki_client_init(self):
        """Test Loki client initialization"""
        client = LokiClient()
        assert client.base_url == "http://loki:3100"
    
    def test_query_logs(self):
        """Test log querying"""
        client = LokiClient()
        result = client.query_logs('{level="error"}', limit=5)
        
        assert result["status"] == "success"
        assert result["data"]["resultType"] == "streams"
        assert len(result["data"]["result"]) == 1
        
        stream = result["data"]["result"][0]
        assert stream["stream"]["job"] == "web-service"
        assert len(stream["values"]) <= 5
    
    def test_query_range(self):
        """Test log metrics range query"""
        client = LokiClient()
        result = client.query_range("rate({level=\"error\"}[5m])", "1h", "now")
        
        assert result["status"] == "success"
        assert result["data"]["resultType"] == "matrix"


class TestAlertmanagerClient:
    """Test Alertmanager client functionality"""
    
    def test_alertmanager_client_init(self):
        """Test Alertmanager client initialization"""
        client = AlertmanagerClient()
        assert client.base_url == "http://alertmanager:9093"
    
    def test_get_alerts(self):
        """Test getting alerts"""
        client = AlertmanagerClient()
        alerts = client.get_alerts()
        
        assert len(alerts) == 2
        assert alerts[0]["labels"]["alertname"] == "HighCPUUsage"
        assert alerts[1]["labels"]["alertname"] == "DiskSpaceLow"
        assert alerts[1]["labels"]["severity"] == "critical"
    
    def test_create_silence(self):
        """Test creating silence"""
        client = AlertmanagerClient()
        matchers = [{"name": "alertname", "value": "HighCPUUsage"}]
        result = client.create_silence(matchers, "1h", "Maintenance window")
        
        assert result["status"] == "success"
        assert "silenceID" in result


class TestGitHubAPI:
    """Test GitHub API functionality"""
    
    def test_github_client_init(self):
        """Test GitHub client initialization"""
        client = GitHubAPI()
        assert client.repo == "org/repo"
        assert client.token == "mock-github-token"
    
    def test_get_commits(self):
        """Test getting commits"""
        client = GitHubAPI()
        commits = client.get_commits(per_page=5)
        
        assert len(commits) == 5
        assert "sha" in commits[0]
        assert "commit" in commits[0]
        assert "message" in commits[0]["commit"]
    
    def test_create_rollback_pr(self):
        """Test creating rollback PR"""
        client = GitHubAPI()
        pr = client.create_rollback_pr("abc123000", "Rollback to stable version")
        
        assert pr["state"] == "open"
        assert "number" in pr
        assert "html_url" in pr
    
    def test_trigger_deployment(self):
        """Test triggering deployment"""
        client = GitHubAPI()
        deployment = client.trigger_deployment("production", "main")
        
        assert deployment["environment"] == "production"
        assert deployment["ref"] == "main"
        assert deployment["state"] == "pending"


class TestSlackAPI:
    """Test Slack API functionality"""
    
    def test_slack_client_init(self):
        """Test Slack client initialization"""
        client = SlackAPI()
        assert client.token == "mock-slack-token"
    
    def test_send_message(self):
        """Test sending message"""
        client = SlackAPI()
        result = client.send_message("test-channel", "Test message")
        
        assert result["ok"] is True
        assert result["channel"] == "test-channel"
        assert result["message"]["text"] == "Test message"
    
    def test_send_alert(self):
        """Test sending alert"""
        client = SlackAPI()
        result = client.send_alert("incidents", "critical", "HighCPU", "CPU usage above threshold")
        
        assert result["ok"] is True
        assert result["channel"] == "incidents"


class TestTeamsAPI:
    """Test Teams API functionality"""
    
    def test_teams_client_init(self):
        """Test Teams client initialization"""
        client = TeamsAPI()
        assert client.webhook_url == "mock-teams-webhook"
    
    def test_send_message(self):
        """Test sending message"""
        client = TeamsAPI()
        result = client.send_message("Test Title", "Test content")
        
        assert result["status"] == "success"
    
    def test_send_incident_card(self):
        """Test sending incident card"""
        client = TeamsAPI()
        result = client.send_incident_card("INC-123", "critical", "High CPU usage")
        
        assert result["status"] == "success"


class TestOpenTelemetryClient:
    """Test OpenTelemetry client functionality"""
    
    def test_otel_client_init(self):
        """Test OpenTelemetry client initialization"""
        client = OpenTelemetryClient()
        assert client.endpoint == "http://jaeger:14268"
    
    def test_get_traces(self):
        """Test getting traces"""
        client = OpenTelemetryClient()
        traces = client.get_traces("test-service")
        
        assert len(traces) == 5
        assert "traceID" in traces[0]
        assert "spans" in traces[0]
        assert len(traces[0]["spans"]) == 1
    
    def test_get_service_map(self):
        """Test getting service map"""
        client = OpenTelemetryClient()
        service_map = client.get_service_map()
        
        assert "services" in service_map
        assert "dependencies" in service_map
        assert len(service_map["services"]) == 5
        assert len(service_map["dependencies"]) == 5


class TestSREToolsOrchestrator:
    """Test SRE tools orchestrator"""
    
    def test_orchestrator_init(self):
        """Test orchestrator initialization"""
        orchestrator = SREToolsOrchestrator()
        
        assert hasattr(orchestrator, 'prometheus')
        assert hasattr(orchestrator, 'grafana')
        assert hasattr(orchestrator, 'loki')
        assert hasattr(orchestrator, 'alertmanager')
        assert hasattr(orchestrator, 'github')
        assert hasattr(orchestrator, 'slack')
        assert hasattr(orchestrator, 'teams')
        assert hasattr(orchestrator, 'otel')
    
    def test_health_check(self):
        """Test health check"""
        orchestrator = SREToolsOrchestrator()
        health_status = orchestrator.health_check()
        
        expected_tools = [
            "prometheus", "grafana", "loki", "alertmanager",
            "github", "slack", "teams", "opentelemetry"
        ]
        
        for tool in expected_tools:
            assert tool in health_status
            assert health_status[tool] == "healthy"
    
    def test_incident_response_workflow(self):
        """Test incident response workflow"""
        orchestrator = SREToolsOrchestrator()
        result = orchestrator.incident_response_workflow("HighCPU", "critical")
        
        assert "alerts" in result
        assert "metrics" in result
        assert "logs" in result
        assert "traces" in result
        assert "notifications" in result
        assert "rollback_candidates" in result  # Because severity is critical


class TestSREAgent:
    """Test SRE agent functionality"""
    
    def test_sre_agent_init(self):
        """Test SRE agent initialization"""
        agent = SREAgent()
        assert hasattr(agent, 'tools')
        assert isinstance(agent.tools, SREToolsOrchestrator)
    
    @patch('app.services.llm_service.send_to_langgraph')
    @patch('app.services.llm_service.send_to_llama_api')
    def test_ask_question_with_metrics(self, mock_llama, mock_langgraph):
        """Test asking question about metrics"""
        mock_langgraph.return_value = {"response": "Langgraph response"}
        mock_llama.return_value = {"response": "Llama response"}
        
        agent = SREAgent()
        result = agent.ask_question("What's the current CPU usage?")
        
        assert "langgraph" in result
        assert "llama" in result
        assert "tools_data" in result
        assert "enhanced_context" in result
        assert result["enhanced_context"] is True
        assert "prometheus_cpu" in result["tools_data"]
    
    @patch('app.services.llm_service.send_to_langgraph')
    @patch('app.services.llm_service.send_to_llama_api')
    def test_ask_question_with_logs(self, mock_llama, mock_langgraph):
        """Test asking question about logs"""
        mock_langgraph.return_value = {"response": "Langgraph response"}
        mock_llama.return_value = {"response": "Llama response"}
        
        agent = SREAgent()
        result = agent.ask_question("Show me recent error logs")
        
        assert "tools_data" in result
        assert "logs" in result["tools_data"]
        assert "traces" in result["tools_data"]
    
    @patch('app.services.llm_service.send_to_langgraph')
    def test_execute_incident_response(self, mock_langgraph):
        """Test incident response execution"""
        mock_langgraph.return_value = {"analysis": "AI analysis"}
        
        agent = SREAgent()
        result = agent.execute_incident_response("HighCPU", "critical")
        
        assert "incident_response" in result
        assert "ai_analysis" in result
        assert result["status"] == "completed"
    
    @patch('app.services.llm_service.send_to_llama_api')
    def test_get_system_health(self, mock_llama):
        """Test system health report"""
        mock_llama.return_value = {"assessment": "System is healthy"}
        
        agent = SREAgent()
        result = agent.get_system_health()
        
        assert "health_data" in result
        assert "ai_assessment" in result
        assert "timestamp" in result


class TestIntegration:
    """Integration tests for SRE tools"""
    
    def test_full_workflow_demo(self, capsys):
        """Test the full demo workflow"""
        # This test captures the output to verify the demo runs without errors
        try:
            demo_sre_tools()
            captured = capsys.readouterr()
            assert "🎬 Starting SRE Tools Demo" in captured.out
            assert "🎉 SRE Tools Demo completed successfully!" in captured.out
        except Exception as e:
            pytest.fail(f"Demo failed with error: {str(e)}")
    
    def test_tools_integration(self):
        """Test that all tools work together"""
        orchestrator = SREToolsOrchestrator()
        
        # Test that we can call multiple tools in sequence
        health = orchestrator.health_check()
        alerts = orchestrator.alertmanager.get_alerts()
        metrics = orchestrator.prometheus.query("cpu_usage_percent")
        logs = orchestrator.loki.query_logs('{level="error"}')
        
        assert len(health) == 8  # All 8 tools
        assert len(alerts) == 2  # Mock returns 2 alerts
        assert metrics["status"] == "success"
        assert logs["status"] == "success"


# Test fixtures
@pytest.fixture
def sre_orchestrator():
    """Fixture for SRE tools orchestrator"""
    return SREToolsOrchestrator()


@pytest.fixture
def sre_agent():
    """Fixture for SRE agent"""
    return SREAgent()


# Performance tests
class TestPerformance:
    """Performance tests for SRE tools"""
    
    def test_orchestrator_initialization_time(self):
        """Test that orchestrator initializes quickly"""
        import time
        start_time = time.time()
        orchestrator = SREToolsOrchestrator()
        end_time = time.time()
        
        initialization_time = end_time - start_time
        assert initialization_time < 1.0  # Should initialize in less than 1 second
    
    def test_health_check_performance(self, sre_orchestrator):
        """Test health check performance"""
        import time
        start_time = time.time()
        health_status = sre_orchestrator.health_check()
        end_time = time.time()
        
        check_time = end_time - start_time
        assert check_time < 0.5  # Should complete in less than 0.5 seconds
        assert len(health_status) == 8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
