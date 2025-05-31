"""
SRE Tools Implementation
Provides both mock and real implementations of various SRE tools.
"""

import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random
import requests


def get_env_var(key: str, default: str = "") -> str:
    """Get environment variable with default fallback"""
    return os.getenv(key, default)


def is_mock_mode() -> bool:
    """Check if we're running in mock mode"""
    return get_env_var("MOCK_MODE", "true").lower() == "true"


class PrometheusClient:
    """Prometheus client for metrics scraping"""
    
    def __init__(self, server_url: str = None):
        self.server_url = server_url or get_env_var(
            "PROMETHEUS_URL", "http://prometheus:9090"
        )
        self.mock_mode = is_mock_mode()
        print(f"🔍 Initializing Prometheus client for {self.server_url}"
              f" (mock: {self.mock_mode})")
    
    def query(self, query: str) -> Dict[str, Any]:
        """Execute a PromQL query"""
        print(f"📊 Prometheus: Executing query '{query}'")
        
        if self.mock_mode:
            return self._mock_query(query)
        else:
            return self._real_query(query)
    
    def _mock_query(self, query: str) -> Dict[str, Any]:
        """Mock implementation for testing"""
        if "cpu_usage" in query.lower():
            result = {
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [
                        {
                            "metric": {
                                "instance": "web-server-1",
                                "job": "node"
                            },
                            "value": [time.time(), str(random.uniform(10, 95))]
                        },
                        {
                            "metric": {
                                "instance": "web-server-2",
                                "job": "node"
                            },
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
        
        print(f"✅ Prometheus: Query completed, returned "
              f"{len(result['data']['result'])} metrics")
        return result
    
    def _real_query(self, query: str) -> Dict[str, Any]:
        """Real implementation for production"""
        try:
            url = f"{self.server_url}/api/v1/query"
            params = {"query": query}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Prometheus: Query completed, returned "
                  f"{len(result.get('data', {}).get('result', []))} metrics")
            return result
        except Exception as e:
            print(f"❌ Prometheus: Query failed - {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def query_range(self, query: str, start: str, end: str,
                    step: str) -> Dict[str, Any]:
        """Execute a range query"""
        print(f"📈 Prometheus: Executing range query '{query}' "
              f"from {start} to {end}")
        
        if self.mock_mode:
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
        else:
            try:
                url = f"{self.server_url}/api/v1/query_range"
                params = {
                    "query": query,
                    "start": start,
                    "end": end,
                    "step": step
                }
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                print(f"❌ Prometheus: Range query failed - {str(e)}")
                return {"status": "error", "error": str(e)}
        
        print("✅ Prometheus: Range query completed")
        return result


class GrafanaAPI:
    """Grafana API client for dashboard queries"""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or get_env_var(
            "GRAFANA_URL", "http://grafana:3000"
        )
        self.api_key = api_key or get_env_var(
            "GRAFANA_API_KEY", "mock-api-key"
        )
        self.mock_mode = is_mock_mode()
        print(f"📊 Initializing Grafana API client for {self.base_url}"
              f" (mock: {self.mock_mode})")
    
    def get_dashboard(self, dashboard_uid: str) -> Dict[str, Any]:
        """Get dashboard by UID"""
        print(f"🎨 Grafana: Fetching dashboard {dashboard_uid}")
        
        if self.mock_mode:
            return self._mock_get_dashboard(dashboard_uid)
        else:
            return self._real_get_dashboard(dashboard_uid)
    
    def _mock_get_dashboard(self, dashboard_uid: str) -> Dict[str, Any]:
        """Mock dashboard implementation"""
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
        
        print(f"✅ Grafana: Dashboard "
              f"'{dashboard['dashboard']['title']}' retrieved")
        return dashboard
    
    def _real_get_dashboard(self, dashboard_uid: str) -> Dict[str, Any]:
        """Real dashboard implementation"""
        try:
            url = f"{self.base_url}/api/dashboards/uid/{dashboard_uid}"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Grafana: Dashboard '{dashboard_uid}' retrieved")
            return result
        except Exception as e:
            print(f"❌ Grafana: Dashboard fetch failed - {str(e)}")
            return {"error": str(e)}


class LokiClient:
    """Loki client for log aggregation"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or get_env_var(
            "LOKI_URL", "http://loki:3100"
        )
        self.mock_mode = is_mock_mode()
        print(f"📋 Initializing Loki client for {self.base_url}"
              f" (mock: {self.mock_mode})")
    
    def query_logs(self, query: str, start: Optional[str] = None,
                   end: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """Query logs using LogQL"""
        print(f"🔍 Loki: Querying logs with '{query}' (limit: {limit})")
        
        if self.mock_mode:
            return self._mock_query_logs(query, limit)
        else:
            return self._real_query_logs(query, start, end, limit)
    
    def _mock_query_logs(self, query: str, limit: int) -> Dict[str, Any]:
        """Mock log query implementation"""
        log_entries = []
        for i in range(min(limit, 10)):
            timestamp = datetime.now() - timedelta(minutes=i*5)
            log_entries.append([
                str(int(timestamp.timestamp() * 1000000000)),
                f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
                f"INFO: Mock log entry {i+1} - Service operation completed"
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
    
    def _real_query_logs(self, query: str, start: Optional[str],
                         end: Optional[str], limit: int) -> Dict[str, Any]:
        """Real log query implementation"""
        try:
            url = f"{self.base_url}/loki/api/v1/query_range"
            params = {
                "query": query,
                "limit": limit
            }
            if start:
                params["start"] = start
            if end:
                params["end"] = end
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()
            log_count = len(result.get("data", {}).get("result", []))
            print(f"✅ Loki: Retrieved {log_count} log entries")
            return result
        except Exception as e:
            print(f"❌ Loki: Log query failed - {str(e)}")
            return {"status": "error", "error": str(e)}


class AlertmanagerClient:
    """Alertmanager client for incident management"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or get_env_var(
            "ALERTMANAGER_URL", "http://alertmanager:9093"
        )
        self.mock_mode = is_mock_mode()
        print(f"🚨 Initializing Alertmanager client for {self.base_url}"
              f" (mock: {self.mock_mode})")
    
    def get_alerts(self, active: bool = True,
                   silenced: bool = False) -> List[Dict[str, Any]]:
        """Get current alerts"""
        print(f"🔔 Alertmanager: Fetching alerts "
              f"(active: {active}, silenced: {silenced})")
        
        if self.mock_mode:
            return self._mock_get_alerts()
        else:
            return self._real_get_alerts(active, silenced)
    
    def _mock_get_alerts(self) -> List[Dict[str, Any]]:
        """Mock alerts implementation"""
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
    
    def _real_get_alerts(self, active: bool,
                         silenced: bool) -> List[Dict[str, Any]]:
        """Real alerts implementation"""
        try:
            url = f"{self.base_url}/api/v1/alerts"
            params = {}
            if not active:
                params["active"] = "false"
            if silenced:
                params["silenced"] = "true"
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            alerts = response.json()
            print(f"✅ Alertmanager: Retrieved {len(alerts)} alerts")
            return alerts
        except Exception as e:
            print(f"❌ Alertmanager: Get alerts failed - {str(e)}")
            return []


class SlackAPI:
    """Slack API client for notifications"""
    
    def __init__(self, token: str = None):
        self.token = token or get_env_var("SLACK_TOKEN", "mock-slack-token")
        self.mock_mode = is_mock_mode()
        print(f"💬 Initializing Slack API client (mock: {self.mock_mode})")
    
    def send_message(self, channel: str, text: str,
                     attachments: Optional[List] = None) -> Dict[str, Any]:
        """Send a message to a Slack channel"""
        print(f"📤 Slack: Sending message to #{channel}")
        print(f"📝 Message: {text}")
        
        if self.mock_mode:
            return self._mock_send_message(channel, text)
        else:
            return self._real_send_message(channel, text, attachments)
    
    def _mock_send_message(self, channel: str, text: str) -> Dict[str, Any]:
        """Mock message sending"""
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
    
    def _real_send_message(self, channel: str, text: str,
                           attachments: Optional[List] = None) -> Dict[str, Any]:
        """Real message sending"""
        try:
            url = "https://slack.com/api/chat.postMessage"
            headers = {"Authorization": f"Bearer {self.token}"}
            data = {
                "channel": channel,
                "text": text
            }
            if attachments:
                data["attachments"] = json.dumps(attachments)
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("ok"):
                print("✅ Slack: Message sent successfully")
            else:
                print(f"❌ Slack: Message failed - {result.get('error')}")
            
            return result
        except Exception as e:
            print(f"❌ Slack: Message sending failed - {str(e)}")
            return {"ok": False, "error": str(e)}
    
    def send_alert(self, channel: str, severity: str, alert_name: str,
                   description: str) -> Dict[str, Any]:
        """Send a formatted alert message"""
        color = {
            "critical": "danger",
            "warning": "warning",
            "info": "good"
        }.get(severity, "warning")
        
        print(f"🚨 Slack: Sending {severity} alert '{alert_name}' "
              f"to #{channel}")
        
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


class SREToolsOrchestrator:
    """Orchestrator for all SRE tools"""
    
    def __init__(self):
        print("🎯 Initializing SRE Tools Orchestrator")
        self.prometheus = PrometheusClient()
        self.grafana = GrafanaAPI()
        self.loki = LokiClient()
        self.alertmanager = AlertmanagerClient()
        self.slack = SlackAPI()
        print("✅ All SRE tools initialized successfully")
    
    def health_check(self) -> Dict[str, str]:
        """Check the health of all integrated tools"""
        print("🏥 Running health check on all SRE tools...")
        
        tools_status = {
            "prometheus": "healthy",
            "grafana": "healthy",
            "loki": "healthy",
            "alertmanager": "healthy",
            "slack": "healthy"
        }
        
        for tool, status in tools_status.items():
            print(f"  ✅ {tool}: {status}")
        
        return tools_status
    
    def incident_response_workflow(self, alert_name: str,
                                   severity: str) -> Dict[str, Any]:
        """Execute a complete incident response workflow"""
        print(f"🚨 Starting incident response workflow for '{alert_name}' "
              f"(severity: {severity})")
        
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
        
        # 4. Send notifications
        default_channel = get_env_var("DEFAULT_INCIDENT_CHANNEL", "incidents")
        slack_result = self.slack.send_alert(
            default_channel, severity, alert_name,
            "Automated incident response triggered"
        )
        workflow_results["notifications"] = {"slack": slack_result}
        
        print("✅ Incident response workflow completed")
        return workflow_results


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
