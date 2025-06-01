import { check, sleep } from "k6";
import http from "k6/http";
import { Counter, Gauge, Rate, Trend } from "k6/metrics";

// Custom metrics for e-commerce services
let errorCounter = new Counter('ecommerce_errors_total');
let responseTimeGauge = new Gauge('ecommerce_response_time');
let errorRate = new Rate('ecommerce_error_rate');
let requestDuration = new Trend('ecommerce_request_duration');

// E-commerce service endpoints simulation
const services = [
  { name: 'frontend', port: 3001, endpoints: ['/health', '/api/products', '/api/cart'] },
  { name: 'backend', port: 3002, endpoints: ['/health', '/api/orders', '/api/users'] },
  { name: 'payment', port: 3003, endpoints: ['/health', '/api/payments', '/api/refunds'] },
  { name: 'inventory', port: 3004, endpoints: ['/health', '/api/stock', '/api/warehouse'] },
  { name: 'shipping', port: 3005, endpoints: ['/health', '/api/shipments', '/api/tracking'] }
];

export let options = {
  vus: 5,
  duration: '30s',
  ext: {
    'experimental-prometheus-rw': {
      server: __ENV.K6_PROMETHEUS_RW_SERVER_URL || 'http://prometheus:9090/api/v1/write',
      pushInterval: '5s',
    },
  },
};

export default () => {
  // Randomly select a service and endpoint
  const service = services[Math.floor(Math.random() * services.length)];
  const endpoint = service.endpoints[Math.floor(Math.random() * service.endpoints.length)];
  
  // Simulate different error types
  const errorTypes = ['error', 'warn', 'info'];
  const errorLevel = errorTypes[Math.floor(Math.random() * errorTypes.length)];
  
  // Simulate HTTP request with random response times and errors
  const shouldError = Math.random() < 0.3; // 30% chance of error
  
  if (shouldError) {
    // Simulate error responses
    errorCounter.add(1, { 
      service: service.name, 
      endpoint: endpoint,
      error_level: errorLevel,
      status_code: Math.random() < 0.5 ? '500' : '404'
    });
    errorRate.add(true, { service: service.name });
    responseTimeGauge.add(Math.random() * 2000 + 500, { service: service.name }); // 500-2500ms for errors
  } else {
    // Simulate successful responses
    errorRate.add(false, { service: service.name });
    const responseTime = Math.random() * 200 + 50; // 50-250ms for success
    responseTimeGauge.add(responseTime, { service: service.name });
    requestDuration.add(responseTime, { service: service.name, endpoint: endpoint });
  }
  
  sleep(1);
};
