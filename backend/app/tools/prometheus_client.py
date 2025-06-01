"""
Prometheus Client for SRE Tools
Provides integration with Prometheus for metrics collection and analysis.
"""

import os
import logging
import random
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrometheusClient:
    """Client for interacting with Prometheus API"""
    
    def __init__(self, url: Optional[str] = None):
        """Initialize Prometheus client"""
        self.prometheus_url = url or os.getenv('PROMETHEUS_URL', 
                                              'http://localhost:9090')
        self.mock_mode = os.getenv('MOCK_MODE', 'false').lower() == 'true'
        
        if not self.mock_mode:
            try:
                from prometheus_api_client import PrometheusConnect
                self.prom = PrometheusConnect(url=self.prometheus_url, 
                                            disable_ssl=True)
                logger.info(f"📊 Connected to Prometheus at "
                          f"{self.prometheus_url}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to connect to Prometheus: {e}")
                self.mock_mode = True
        
        if self.mock_mode:
            logger.info("🎭 Running in mock mode for Prometheus")
    
    def _generate_mock_data(self, metric_name: str, 
                          query: str) -> List[Dict[str, Any]]:
        """Generate mock data for testing"""
        mock_data = []
        current_time = time.time()
        
        # Generate mock time series data
        for i in range(5):
            timestamp = current_time - (i * 60)  # 1 minute intervals
            if 'cpu' in metric_name.lower():
                value = random.uniform(10, 80)
            elif 'memory' in metric_name.lower():
                value = random.uniform(20, 90)
            elif 'disk' in metric_name.lower():
                value = random.uniform(30, 70)
            elif 'up' in metric_name.lower():
                value = 1.0
            else:
                value = random.uniform(1, 100)
            
            mock_data.append({
                'metric': {
                    'instance': f'localhost:{9000 + i}',
                    'job': 'mock-service',
                    '__name__': metric_name
                },
                'value': [timestamp, str(value)]
            })
        
        return mock_data
    
    def query_prometheus(self, query: str) -> Dict[str, Any]:
        """Execute a PromQL query and return results"""
        try:
            if self.mock_mode:
                # Extract metric name from query for mock data
                metric_name = (query.split('(')[0] if '(' in query 
                             else query.split()[0])
                mock_data = self._generate_mock_data(metric_name, query)
                return {
                    'status': 'success',
                    'data': {
                        'resultType': 'vector',
                        'result': mock_data
                    },
                    'query': query,
                    'mock': True
                }
            
            # Real Prometheus query
            result = self.prom.custom_query(query=query)
            return {
                'status': 'success',
                'data': {
                    'resultType': 'vector',
                    'result': result
                },
                'query': query,
                'mock': False
            }
            
        except Exception as e:
            logger.error(f"❌ Error executing query '{query}': {e}")
            return {
                'status': 'error',
                'error': str(e),
                'query': query
            }
    
    def get_cpu_usage(self, instance: Optional[str] = None) -> Dict[str, Any]:
        """Get CPU usage metrics"""
        if instance:
            query = ('100 - (avg(rate(node_cpu_seconds_total'
                    f'{{mode="idle",instance="{instance}"}}[5m])) * 100)')
        else:
            query = ('100 - (avg(rate(node_cpu_seconds_total'
                    '{mode="idle"}[5m])) * 100)')
        
        result = self.query_prometheus(query)
        
        if result['status'] == 'success':
            return {
                'metric': 'cpu_usage_percentage',
                'query': query,
                'data': result['data']['result'],
                'summary': self._summarize_cpu_data(result['data']['result'])
            }
        return result
    
    def get_memory_usage(self, 
                        instance: Optional[str] = None) -> Dict[str, Any]:
        """Get memory usage metrics"""
        if instance:
            query = ('(1 - (node_memory_MemAvailable_bytes'
                    f'{{instance="{instance}"}} / '
                    f'node_memory_MemTotal_bytes{{instance="{instance}"}}))'
                    ' * 100')
        else:
            query = ('(1 - (node_memory_MemAvailable_bytes / '
                    'node_memory_MemTotal_bytes)) * 100')
        
        result = self.query_prometheus(query)
        
        if result['status'] == 'success':
            return {
                'metric': 'memory_usage_percentage',
                'query': query,
                'data': result['data']['result'],
                'summary': self._summarize_memory_data(
                    result['data']['result'])
            }
        return result
    
    def get_disk_usage(self, 
                      instance: Optional[str] = None) -> Dict[str, Any]:
        """Get disk usage metrics"""
        if instance:
            query = ('100 - ((node_filesystem_avail_bytes'
                    f'{{instance="{instance}",mountpoint="/"}} / '
                    f'node_filesystem_size_bytes{{instance="{instance}",'
                    'mountpoint="/"}}) * 100)')
        else:
            query = ('100 - ((node_filesystem_avail_bytes'
                    '{mountpoint="/"} / '
                    'node_filesystem_size_bytes{mountpoint="/"}) * 100)')
        
        result = self.query_prometheus(query)
        
        if result['status'] == 'success':
            return {
                'metric': 'disk_usage_percentage',
                'query': query,
                'data': result['data']['result'],
                'summary': self._summarize_disk_data(result['data']['result'])
            }
        return result
    
    def get_service_health(self, 
                          service_name: Optional[str] = None) -> Dict[str, Any]:
        """Get service health status"""
        if service_name:
            query = f'up{{job="{service_name}"}}'
        else:
            query = 'up'
        
        result = self.query_prometheus(query)
        
        if result['status'] == 'success':
            return {
                'metric': 'service_health',
                'query': query,
                'data': result['data']['result'],
                'summary': self._summarize_health_data(
                    result['data']['result'])
            }
        return result
    
    def get_http_requests_rate(self, 
                              service: Optional[str] = None) -> Dict[str, Any]:
        """Get HTTP request rate metrics"""
        if service:
            query = f'rate(http_requests_total{{service="{service}"}}[5m])'
        else:
            query = 'rate(http_requests_total[5m])'
        
        result = self.query_prometheus(query)
        
        if result['status'] == 'success':
            return {
                'metric': 'http_requests_per_second',
                'query': query,
                'data': result['data']['result'],
                'summary': self._summarize_rate_data(result['data']['result'])
            }
        return result
    
    def get_error_rate(self, service: Optional[str] = None) -> Dict[str, Any]:
        """Get error rate metrics"""
        if service:
            query = ('rate(http_requests_total'
                    f'{{service="{service}",status=~"5.."}}[5m]) / '
                    f'rate(http_requests_total{{service="{service}"}}[5m])'
                    ' * 100')
        else:
            query = ('rate(http_requests_total{status=~"5.."}[5m]) / '
                    'rate(http_requests_total[5m]) * 100')
        
        result = self.query_prometheus(query)
        
        if result['status'] == 'success':
            return {
                'metric': 'error_rate_percentage',
                'query': query,
                'data': result['data']['result'],
                'summary': self._summarize_error_data(result['data']['result'])
            }
        return result
    
    def _summarize_cpu_data(self, data: List[Dict]) -> str:
        """Summarize CPU usage data"""
        if not data:
            return "No CPU data available"
        
        values = [float(item['value'][1]) for item in data 
                 if len(item['value']) > 1]
        if not values:
            return "No valid CPU values"
        
        avg_cpu = sum(values) / len(values)
        max_cpu = max(values)
        min_cpu = min(values)
        
        return (f"CPU Usage - Avg: {avg_cpu:.1f}%, "
               f"Max: {max_cpu:.1f}%, Min: {min_cpu:.1f}%")
    
    def _summarize_memory_data(self, data: List[Dict]) -> str:
        """Summarize memory usage data"""
        if not data:
            return "No memory data available"
        
        values = [float(item['value'][1]) for item in data 
                 if len(item['value']) > 1]
        if not values:
            return "No valid memory values"
        
        avg_memory = sum(values) / len(values)
        max_memory = max(values)
        
        return (f"Memory Usage - Avg: {avg_memory:.1f}%, "
               f"Max: {max_memory:.1f}%")
    
    def _summarize_disk_data(self, data: List[Dict]) -> str:
        """Summarize disk usage data"""
        if not data:
            return "No disk data available"
        
        values = [float(item['value'][1]) for item in data 
                 if len(item['value']) > 1]
        if not values:
            return "No valid disk values"
        
        avg_disk = sum(values) / len(values)
        max_disk = max(values)
        
        return (f"Disk Usage - Avg: {avg_disk:.1f}%, "
               f"Max: {max_disk:.1f}%")
    
    def _summarize_health_data(self, data: List[Dict]) -> str:
        """Summarize service health data"""
        if not data:
            return "No health data available"
        
        up_services = sum(1 for item in data 
                         if len(item['value']) > 1 and 
                         float(item['value'][1]) == 1)
        total_services = len(data)
        
        return f"Service Health - {up_services}/{total_services} services up"
    
    def _summarize_rate_data(self, data: List[Dict]) -> str:
        """Summarize request rate data"""
        if not data:
            return "No request rate data available"
        
        values = [float(item['value'][1]) for item in data 
                 if len(item['value']) > 1]
        if not values:
            return "No valid rate values"
        
        total_rate = sum(values)
        avg_rate = total_rate / len(values)
        
        return (f"Request Rate - Total: {total_rate:.2f} req/s, "
               f"Avg: {avg_rate:.2f} req/s")
    
    def _summarize_error_data(self, data: List[Dict]) -> str:
        """Summarize error rate data"""
        if not data:
            return "No error rate data available"
        
        values = [float(item['value'][1]) for item in data 
                 if len(item['value']) > 1]
        if not values:
            return "Error rate: 0%"
        
        avg_error_rate = sum(values) / len(values)
        max_error_rate = max(values)
        
        return (f"Error Rate - Avg: {avg_error_rate:.2f}%, "
               f"Max: {max_error_rate:.2f}%")


def demo_prometheus_client():
    """Demonstrate Prometheus client functionality"""
    print("🎬 Starting Prometheus Client Demo")
    print("=" * 50)
    
    client = PrometheusClient()
    
    # Test different metrics
    metrics_to_test = [
        ("CPU Usage", lambda: client.get_cpu_usage()),
        ("Memory Usage", lambda: client.get_memory_usage()),
        ("Disk Usage", lambda: client.get_disk_usage()),
        ("Service Health", lambda: client.get_service_health()),
        ("HTTP Request Rate", lambda: client.get_http_requests_rate()),
        ("Error Rate", lambda: client.get_error_rate()),
    ]
    
    for metric_name, metric_func in metrics_to_test:
        print(f"\n📊 Testing {metric_name}:")
        try:
            result = metric_func()
            if result.get('status') == 'success':
                print(f"✅ {result.get('summary', 'No summary available')}")
                print(f"🔍 Query: {result.get('query', 'No query')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n🎉 Prometheus Client Demo completed!")


if __name__ == "__main__":
    demo_prometheus_client()
