"""
SRE Tools Mock Implementation
Provides mock implementations of various SRE tools for demonstration purposes.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random


class PrometheusClient:
    """Mock Prometheus client for metrics scraping"""
    
    def __init__(self, server_url: str = "http://prometheus:9090"):
        self.server_url = server_url
        print(f"🔍 Initializing Prometheus client connecting to {server_url}")
    
    def query(self, query: str) -> Dict[str, Any]:
        """Execute a PromQL query"""
        print(f"📊 Prometheus: Executing query '{query}'")
        
        # Mock different types of metrics based on query
        if "cpu_usage" in query.lower():
            result = {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [
                        {
                            "metric": {"instance": "web-server-1", "job": "node"},
                            "value": [time.time(), str(random.uniform(10, 95))]
                        },
                        {
                            "metric": {"instance": "web-server-2", "job": "node"},
                            "value": [time.time(), str(random.uniform(10, 95))]
                        }
                    ]
                }
            }
        elif "memory" in query.lower():
            result = {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [
                        {
                            "metric": {"instance": "web-server-1"},
                            "value": [time.time(), str(random.uniform(50, 90))]
                        }
                    ]
                }
            }
        else:
            result = {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": []
                }
            }
        
        print(f"✅ Prometheus: Query completed, returned {len(result['data']['result'])} metrics")
        return result
    
    def query_range(self, query: str, start: str, end: str, step: str) -> Dict[str, Any]:
        """Execute a range query"""
        print(f"📈 Prometheus: Executing range query '{query}' from {start} to {end}")
        
        # Generate mock time series data
        result = {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": [
                    {
                        "metric": {"instance": "web-server-1"},
                        "values": [
                            [time.time() - 3600, str(random.uniform(20, 80))],
                            [time.time() - 1800, str(random.uniform(20, 80))],
                            [time.time(), str(random.uniform(20, 80))]
                        ]
                    }
                ]
            }
        }
        
        print("✅ Prometheus: Range query completed")
        return result


class GrafanaAPI:
    """Mock Grafana API client for dashboard queries"""
    
    def __init__(self, base_url: str = "http://grafana:3000", api_key: str = "mock-api-key"):
        self.base_url = base_url
        self.api_key = api_key
        print(f"📊 Initializing Grafana API client for {base_url}")
    
    def get_dashboard(self, dashboard_uid: str) -> Dict[str, Any]:
        """Get dashboard by UID"""
        print(f"🎨 Grafana: Fetching dashboard {dashboard_uid}")
        
        dashboard = {
            "dashboard": {
                "id": 1,
                "uid": dashboard_uid,
                "title": "Infrastructure Overview",
                "tags": ["infrastructure", "monitoring"],
                "panels": [
                    {
                        "id": 1,
                        "title": "CPU Usage",
                        "type": "graph",
                        "targets": [{"expr": "cpu_usage_percent"}]
                    },
                    {
                        "id": 2,
                        "title": "Memory Usage",
                        "type": "singlestat",
                        "targets": [{"expr": "memory_usage_percent"}]
                    }
                ]
            },
            "meta": {
                "isStarred": False,
                "url": f"/d/{dashboard_uid}/infrastructure-overview"
            }
        }
        
        print(f"✅ Grafana: Dashboard '{dashboard['dashboard']['title']}' retrieved successfully")
        return dashboard
    
    def get_dashboard_annotations(self, dashboard_id: int, from_time: int, to_time: int) -> List[Dict]:
        """Get annotations for a dashboard"""
        print(f"📝 Grafana: Fetching annotations for dashboard {dashboard_id}")
        
        annotations = [
            {
                "id": 1,
                "time": int(time.time() * 1000) - 3600000,
                "text": "Deployment started",
                "tags": ["deployment"],
                "userId": 1
            },
            {
                "id": 2,
                "time": int(time.time() * 1000) - 1800000,
                "text": "High CPU alert triggered",
                "tags": ["alert", "cpu"],
                "userId": 1
            }
        ]
        
        print(f"✅ Grafana: Retrieved {len(annotations)} annotations")
        return annotations


class LokiClient:
    """Mock Loki client for log aggregation"""
    
    def __init__(self, base_url: str = "http://loki:3100"):
        self.base_url = base_url
        print(f"📋 Initializing Loki client for {base_url}")
    
    def query_logs(self, query: str, start: Optional[str] = None, end: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """Query logs using LogQL"""
        print(f"🔍 Loki: Querying logs with '{query}' (limit: {limit})")
        
        # Generate mock log entries
        log_entries = []
        for i in range(min(limit, 10)):  # Generate up to 10 mock entries
            timestamp = datetime.now() - timedelta(minutes=i*5)
            log_entries.append([
                str(int(timestamp.timestamp() * 1000000000)),  # nanosecond timestamp
                f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] INFO: Mock log entry {i+1} - Service operation completed"
            ])
        
        result = {
            "status": "success",
            "data": {
                "resultType": "streams",
                "result": [
                    {
                        "stream": {
                            "job": "web-service",
                            "instance": "web-server-1",
                            "level": "info"
                        },
                        "values": log_entries
                    }
                ]
            }
        }
        
        print(f"✅ Loki: Retrieved {len(log_entries)} log entries")
        return result
    
    def query_range(self, query: str, start: str, end: str, step: str = "1m") -> Dict[str, Any]:
        """Query log metrics over a time range"""
        print(f"📊 Loki: Querying log metrics '{query}' from {start} to {end}")
        
        result = {
            "status": "success",
            "data": {
                "resultType": "matrix",
                "result": [
                    {
                        "metric": {"level": "error"},
                        "values": [
                            [time.time() - 3600, "5"],
                            [time.time() - 1800, "3"],
                            [time.time(), "2"]
                        ]
                    }
                ]
            }
        }
        
        print("✅ Loki: Log metrics query completed")
        return result


class AlertmanagerClient:
    """Mock Alertmanager client for incident management"""
    
    def __init__(self, base_url: str = "http://alertmanager:9093"):
        self.base_url = base_url
        print(f"🚨 Initializing Alertmanager client for {base_url}")
    
    def get_alerts(self, active: bool = True, silenced: bool = False) -> List[Dict[str, Any]]:
        """Get current alerts"""
        print(f"🔔 Alertmanager: Fetching alerts (active: {active}, silenced: {silenced})")
        
        alerts = [
            {
                "labels": {
                    "alertname": "HighCPUUsage",
                    "instance": "web-server-1",
                    "severity": "warning"
                },
                "annotations": {
                    "summary": "High CPU usage detected",
                    "description": "CPU usage is above 80% for more than 5 minutes"
                },
                "state": "firing",
                "activeAt": datetime.now().isoformat(),
                "value": "85.5"
            },
            {
                "labels": {
                    "alertname": "DiskSpaceLow",
                    "instance": "web-server-2",
                    "severity": "critical"
                },
                "annotations": {
                    "summary": "Low disk space",
                    "description": "Disk space is below 10%"
                },
                "state": "firing",
                "activeAt": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "value": "8.2"
            }
        ]
        
        print(f"✅ Alertmanager: Retrieved {len(alerts)} alerts")
        return alerts
    
    def create_silence(self, matchers: List[Dict], duration: str, comment: str) -> Dict[str, Any]:
        """Create a silence for alerts"""
        print(f"🔇 Alertmanager: Creating silence for {duration} - {comment}")
        
        silence_id = f"silence-{int(time.time())}"
        result = {
            "silenceID": silence_id,
            "status": "success"
        }
        
        print(f"✅ Alertmanager: Silence {silence_id} created successfully")
        return result


class GitHubAPI:
    """Mock GitHub API client for code rollback operations"""
    
    def __init__(self, token: str = "mock-github-token", repo: str = "org/repo"):
        self.token = token
        self.repo = repo
        print(f"🐙 Initializing GitHub API client for repository {repo}")
    
    def get_commits(self, branch: str = "main", per_page: int = 10) -> List[Dict[str, Any]]:
        """Get recent commits"""
        print(f"📜 GitHub: Fetching {per_page} commits from {branch} branch")
        
        commits = []
        for i in range(per_page):
            commit_time = datetime.now() - timedelta(hours=i*2)
            commits.append({
                "sha": f"abc123{i:03d}",
                "commit": {
                    "message": f"Mock commit {i+1}: Fix issue #{i+100}",
                    "author": {
                        "name": "Developer",
                        "email": "dev@example.com",
                        "date": commit_time.isoformat()
                    }
                },
                "html_url": f"https://github.com/{self.repo}/commit/abc123{i:03d}"
            })
        
        print(f"✅ GitHub: Retrieved {len(commits)} commits")
        return commits
    
    def create_rollback_pr(self, target_commit: str, title: str) -> Dict[str, Any]:
        """Create a rollback pull request"""
        print(f"🔄 GitHub: Creating rollback PR to commit {target_commit}")
        
        pr_number = random.randint(100, 999)
        result = {
            "number": pr_number,
            "title": title,
            "html_url": f"https://github.com/{self.repo}/pull/{pr_number}",
            "state": "open",
            "created_at": datetime.now().isoformat()
        }
        
        print(f"✅ GitHub: Rollback PR #{pr_number} created successfully")
        return result
    
    def trigger_deployment(self, environment: str, ref: str) -> Dict[str, Any]:
        """Trigger a deployment"""
        print(f"🚀 GitHub: Triggering deployment to {environment} from {ref}")
        
        deployment_id = random.randint(1000, 9999)
        result = {
            "id": deployment_id,
            "environment": environment,
            "ref": ref,
            "state": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        print(f"✅ GitHub: Deployment {deployment_id} triggered successfully")
        return result


class SlackAPI:
    """Mock Slack API client for notifications"""
    
    def __init__(self, token: str = "mock-slack-token"):
        self.token = token
        print("💬 Initializing Slack API client")
    
    def send_message(self, channel: str, text: str, attachments: Optional[List] = None) -> Dict[str, Any]:
        """Send a message to a Slack channel"""
        print(f"📤 Slack: Sending message to #{channel}")
        print(f"📝 Message: {text}")
        
        result = {
            "ok": True,
            "channel": channel,
            "ts": str(time.time()),
            "message": {
                "text": text,
                "user": "U123SREBOT",
                "ts": str(time.time())
            }
        }
        
        print("✅ Slack: Message sent successfully")
        return result
    
    def send_alert(self, channel: str, severity: str, alert_name: str, description: str) -> Dict[str, Any]:
        """Send a formatted alert message"""
        color = {
            "critical": "danger",
            "warning": "warning",
            "info": "good"
        }.get(severity, "warning")
        
        print(f"🚨 Slack: Sending {severity} alert '{alert_name}' to #{channel}")
        
        attachment = {
            "color": color,
            "title": f"{severity.upper()}: {alert_name}",
            "text": description,
            "fields": [
                {"title": "Severity", "value": severity, "short": True},
                {"title": "Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "short": True}
            ]
        }
        
        return self.send_message(channel, f"Alert: {alert_name}", [attachment])


class TeamsAPI:
    """Mock Microsoft Teams API client for notifications"""
    
    def __init__(self, webhook_url: str = "mock-teams-webhook"):
        self.webhook_url = webhook_url
        print("🟦 Initializing Microsoft Teams API client")
    
    def send_message(self, title: str, text: str, color: str = "0078D4") -> Dict[str, Any]:
        """Send a message to Teams"""
        print(f"📤 Teams: Sending message '{title}'")
        print(f"📝 Content: {text}")
        
        result = {
            "status": "success",
            "message": "Message sent to Teams channel"
        }
        
        print("✅ Teams: Message sent successfully")
        return result
    
    def send_incident_card(self, incident_id: str, severity: str, description: str) -> Dict[str, Any]:
        """Send an incident notification card"""
        print(f"🚨 Teams: Sending incident card for {incident_id} (severity: {severity})")
        
        return self.send_message(
            f"Incident {incident_id}",
            f"**Severity:** {severity}\n**Description:** {description}",
            "FF0000" if severity == "critical" else "FFA500"
        )


class OpenTelemetryClient:
    """Mock OpenTelemetry client for application tracing"""
    
    def __init__(self, endpoint: str = "http://jaeger:14268"):
        self.endpoint = endpoint
        print(f"🔍 Initializing OpenTelemetry client for {endpoint}")
    
    def get_traces(self, service: str, operation: Optional[str] = None, lookback: str = "1h") -> List[Dict[str, Any]]:
        """Get traces for a service"""
        print(f"🕵️ OpenTelemetry: Fetching traces for service '{service}' (lookback: {lookback})")
        
        traces = []
        for i in range(5):  # Generate 5 mock traces
            trace_id = f"trace-{random.randint(100000, 999999)}"
            start_time = datetime.now() - timedelta(minutes=random.randint(1, 60))
            duration = random.randint(10, 5000)  # milliseconds
            
            traces.append({
                "traceID": trace_id,
                "spans": [
                    {
                        "spanID": f"span-{i+1}",
                        "operationName": operation or f"operation_{i+1}",
                        "startTime": int(start_time.timestamp() * 1000000),  # microseconds
                        "duration": duration * 1000,  # microseconds
                        "tags": [
                            {"key": "http.method", "value": "GET"},
                            {"key": "http.status_code", "value": "200"},
                            {"key": "service.name", "value": service}
                        ]
                    }
                ]
            })
        
        print(f"✅ OpenTelemetry: Retrieved {len(traces)} traces")
        return traces
    
    def get_service_map(self) -> Dict[str, Any]:
        """Get service dependency map"""
        print("🗺️ OpenTelemetry: Generating service dependency map")
        
        service_map = {
            "services": [
                {"name": "frontend", "type": "web"},
                {"name": "api-gateway", "type": "service"},
                {"name": "user-service", "type": "service"},
                {"name": "payment-service", "type": "service"},
                {"name": "database", "type": "database"}
            ],
            "dependencies": [
                {"source": "frontend", "target": "api-gateway", "callCount": 1500},
                {"source": "api-gateway", "target": "user-service", "callCount": 800},
                {"source": "api-gateway", "target": "payment-service", "callCount": 200},
                {"source": "user-service", "target": "database", "callCount": 600},
                {"source": "payment-service", "target": "database", "callCount": 150}
            ]
        }
        
        print("✅ OpenTelemetry: Service map generated")
        return service_map


class SREToolsOrchestrator:
    """Orchestrator for all SRE tools"""
    
    def __init__(self):
        print("🎯 Initializing SRE Tools Orchestrator")
        self.prometheus = PrometheusClient()
        self.grafana = GrafanaAPI()
        self.loki = LokiClient()
        self.alertmanager = AlertmanagerClient()
        self.github = GitHubAPI()
        self.slack = SlackAPI()
        self.teams = TeamsAPI()
        self.otel = OpenTelemetryClient()
        print("✅ All SRE tools initialized successfully")
    
    def health_check(self) -> Dict[str, str]:
        """Check the health of all integrated tools"""
        print("🏥 Running health check on all SRE tools...")
        
        tools_status = {
            "prometheus": "healthy",
            "grafana": "healthy", 
            "loki": "healthy",
            "alertmanager": "healthy",
            "github": "healthy",
            "slack": "healthy",
            "teams": "healthy",
            "opentelemetry": "healthy"
        }
        
        for tool, status in tools_status.items():
            print(f"  ✅ {tool}: {status}")
        
        return tools_status
    
    def incident_response_workflow(self, alert_name: str, severity: str) -> Dict[str, Any]:
        """Execute a complete incident response workflow"""
        print(f"🚨 Starting incident response workflow for '{alert_name}' (severity: {severity})")
        
        workflow_results = {}
        
        # 1. Get current alerts
        alerts = self.alertmanager.get_alerts()
        workflow_results["alerts"] = alerts
        
        # 2. Gather metrics
        cpu_metrics = self.prometheus.query("cpu_usage_percent")
        workflow_results["metrics"] = cpu_metrics
        
        # 3. Collect logs
        error_logs = self.loki.query_logs('{level="error"}', limit=50)
        workflow_results["logs"] = error_logs
        
        # 4. Get traces
        traces = self.otel.get_traces("web-service", lookback="30m")
        workflow_results["traces"] = traces
        
        # 5. Send notifications
        slack_result = self.slack.send_alert("incidents", severity, alert_name, "Automated incident response triggered")
        teams_result = self.teams.send_incident_card(f"INC-{int(time.time())}", severity, alert_name)
        workflow_results["notifications"] = {"slack": slack_result, "teams": teams_result}
        
        # 6. Prepare rollback if critical
        if severity == "critical":
            commits = self.github.get_commits(per_page=5)
            workflow_results["rollback_candidates"] = commits
        
        print("✅ Incident response workflow completed")
        return workflow_results


# Example usage function
def demo_sre_tools():
    """Demonstrate all SRE tools functionality"""
    print("🎬 Starting SRE Tools Demo")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = SREToolsOrchestrator()
    
    print("\n" + "=" * 50)
    print("🏥 Health Check")
    print("=" * 50)
    orchestrator.health_check()
    
    print("\n" + "=" * 50)
    print("🚨 Incident Response Demo")
    print("=" * 50)
    orchestrator.incident_response_workflow("HighMemoryUsage", "critical")
    
    print("\n🎉 SRE Tools Demo completed successfully!")


if __name__ == "__main__":
    demo_sre_tools()
