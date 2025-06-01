const express = require('express');
const path = require('path');
const promClient = require('prom-client');
const os = require('os');
const app = express();
const port = process.env.PORT || 3001;

let highTrafficScenarioActive = false; // Flag to indicate if high traffic CPU simulation is active

// Prometheus metrics setup
const register = new promClient.Registry();

// Enable default system metrics (CPU, memory, etc.)
promClient.collectDefaultMetrics({
  register,
  prefix: 'ecommerce_app_',
  timeout: 5000,
  gcDurationBuckets: [0.001, 0.01, 0.1, 1, 2, 5],
});

// Custom business metrics
const httpRequestsTotal = new promClient.Counter({
  name: 'ecommerce_http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

const httpRequestDuration = new promClient.Histogram({
  name: 'ecommerce_http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10],
  registers: [register]
});

const businessMetricsCounters = {
  userRegistrations: new promClient.Counter({
    name: 'ecommerce_user_registrations_total',
    help: 'Total number of user registrations',
    registers: [register]
  }),
  userLogins: new promClient.Counter({
    name: 'ecommerce_user_logins_total',
    help: 'Total number of user logins',
    registers: [register]
  }),
  productViews: new promClient.Counter({
    name: 'ecommerce_product_views_total',
    help: 'Total number of product views',
    labelNames: ['product_id', 'product_name'],
    registers: [register]
  }),
  cartAdditions: new promClient.Counter({
    name: 'ecommerce_cart_additions_total',
    help: 'Total number of items added to cart',
    registers: [register]
  }),
  checkouts: new promClient.Counter({
    name: 'ecommerce_checkouts_total',
    help: 'Total number of checkouts',
    registers: [register]
  }),
  paymentProcessed: new promClient.Counter({
    name: 'ecommerce_payments_processed_total',
    help: 'Total number of successful payments',
    registers: [register]
  }),
  paymentErrors: new promClient.Counter({
    name: 'ecommerce_payment_errors_total',
    help: 'Total number of payment errors',
    registers: [register]
  }),
  errors: new promClient.Counter({
    name: 'ecommerce_errors_total',
    help: 'Total number of application errors',
    labelNames: ['service', 'error_type'],
    registers: [register]
  })
};

// System resource gauges
const systemGauges = {
  cpuUsage: new promClient.Gauge({
    name: 'ecommerce_cpu_usage_percent',
    help: 'CPU usage percentage',
    registers: [register]
  }),
  memoryUsage: new promClient.Gauge({
    name: 'ecommerce_memory_usage_bytes',
    help: 'Memory usage in bytes',
    labelNames: ['type'], // 'used', 'free', 'total', 'used_percent', 'load_1m', 'load_5m', 'load_15m', 'uptime_seconds'
    registers: [register]
  }),
  activeConnections: new promClient.Gauge({
    name: 'ecommerce_active_connections',
    help: 'Number of active connections',
    registers: [register]
  }),
  responseTime: new promClient.Gauge({
    name: 'ecommerce_avg_response_time_ms',
    help: 'Average response time in milliseconds',
    registers: [register]
  }),
  activeUsers: new promClient.Gauge({
    name: 'ecommerce_active_users',
    help: 'Number of currently active users',
    registers: [register]
  }),
  cartValue: new promClient.Gauge({
    name: 'ecommerce_avg_cart_value_dollars',
    help: 'Average cart value in dollars',
    registers: [register]
  })
};

// System monitoring function
let previousCpuTimes = null;

function updateSystemMetrics() {
  // CPU usage calculation with better accuracy
  const cpus = os.cpus();
  let totalIdle = 0;
  let totalTick = 0;
  
  cpus.forEach(cpu => {
    for (type in cpu.times) {
      totalTick += cpu.times[type];
    }
    totalIdle += cpu.times.idle;
  });
  
  if (previousCpuTimes) {
    const idleDifference = totalIdle - previousCpuTimes.idle;
    const totalDifference = totalTick - previousCpuTimes.total;
    // const cpuPercentage = 90; // Original hardcoded value
    
    let cpuPercentageToSet;
    if (highTrafficScenarioActive) {
        cpuPercentageToSet = 95; // Simulate high CPU usage (95%) during the scenario
    } else {
        cpuPercentageToSet = 40; // Simulate normal CPU usage (40%) otherwise
    }
    systemGauges.cpuUsage.set(Math.max(0, Math.min(100, cpuPercentageToSet)));
  }
  
  previousCpuTimes = { idle: totalIdle, total: totalTick };

  // Memory usage
  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const usedMemPercent = (usedMem / totalMem) * 100;
  
  systemGauges.memoryUsage.set({ type: 'total' }, totalMem);
  systemGauges.memoryUsage.set({ type: 'used' }, usedMem);
  systemGauges.memoryUsage.set({ type: 'free' }, freeMem);
  systemGauges.memoryUsage.set({ type: 'used_percent' }, usedMemPercent);

  // System load average (if available)
  try {
    const loadavg = os.loadavg();
    systemGauges.memoryUsage.set({ type: 'load_1m' }, loadavg[0]);
    systemGauges.memoryUsage.set({ type: 'load_5m' }, loadavg[1]);
    systemGauges.memoryUsage.set({ type: 'load_15m' }, loadavg[2]);
  } catch (e) {
    // Load average not available on all systems
  }

  // Uptime
  const uptime = os.uptime();
  systemGauges.memoryUsage.set({ type: 'uptime_seconds' }, uptime);
}

// Update system metrics every 2 seconds
setInterval(updateSystemMetrics, 2000);

// Update business metrics every 5 seconds
setInterval(() => {
  // Simulate active user count (random between 50-500)
  const activeUsers = Math.floor(Math.random() * 450) + 50;
  systemGauges.activeUsers.set(activeUsers);
  
  // Simulate average cart value (random between $25-$300)
  const avgCartValue = Math.floor(Math.random() * 275) + 25;
  systemGauges.cartValue.set(avgCartValue);
  
  // Simulate active connections (related to active users)
  const connections = Math.floor(activeUsers * (0.8 + Math.random() * 0.4));
  systemGauges.activeConnections.set(connections);
}, 5000);

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Request monitoring middleware
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route ? req.route.path : req.path;
    
    httpRequestsTotal.inc({
      method: req.method,
      route: route,
      status_code: res.statusCode
    });
    
    httpRequestDuration.observe({
      method: req.method,
      route: route,
      status_code: res.statusCode
    }, duration);
    
    systemGauges.responseTime.set(Date.now() - start);
  });
  
  next();
});

// E-commerce Metrics
let metrics = {
  requestCount: 0,
  errorCount: 0,
  userRegistrations: 0,
  userLogins: 0,
  productViews: 0,
  cartAdditions: 0,
  checkouts: 0,
  paymentProcessed: 0,
  paymentErrors: 0,
  inventoryChecks: 0,
  inventoryLow: 0,
  shippingRequests: 0,
  ordersFulfilled: 0,
  customerSupport: 0
};

// Sample data for scenarios
const products = [
  { id: 1, name: 'iPhone 15', price: 999, stock: 50 },
  { id: 2, name: 'MacBook Pro', price: 2499, stock: 25 },
  { id: 3, name: 'AirPods Pro', price: 249, stock: 100 },
  { id: 4, name: 'iPad Air', price: 599, stock: 75 },
  { id: 5, name: 'Apple Watch', price: 399, stock: 80 }
];

const users = ['john_doe', 'jane_smith', 'mike_johnson', 'sarah_wilson', 'tom_brown'];

// Utility function to generate random logs
function generateLog(level, service, message, userId = null, productId = null) {
  const timestamp = new Date().toISOString();
  const logData = {
    timestamp,
    level,
    service,
    message,
    userId,
    productId,
    sessionId: Math.random().toString(36).substring(7),
    requestId: Math.random().toString(36).substring(7)
  };
  
  console.log(`[${level.toUpperCase()}] [${service}] ${message} - ${JSON.stringify(logData)}`);
  return logData;
}

// Basic Routes
app.get('/api/health', (req, res) => {
    metrics.requestCount++;
    generateLog('info', 'health', 'Health check request received');
    res.json({ status: 'healthy', metrics });
});

app.get('/api/metrics', (req, res) => {
    generateLog('info', 'metrics', 'Metrics requested');
    res.json(metrics);
});

// Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
    try {
        res.set('Content-Type', register.contentType);
        const metricsData = await register.metrics();
        res.end(metricsData);
    } catch (error) {
        res.status(500).end(error);
    }
});

// E-commerce Scenario Routes
app.post('/api/scenarios/user-registration', (req, res) => {
    const count = req.body.count || 10;
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        metrics.userRegistrations++;
        businessMetricsCounters.userRegistrations.inc();
        generateLog('info', 'auth', `User registration successful`, userId);
        
        // Simulate some registration errors
        if (Math.random() < 0.1) {
            metrics.errorCount++;
            businessMetricsCounters.errors.inc({ service: 'auth', error_type: 'registration_failed' });
            generateLog('error', 'auth', `User registration failed - email already exists`, userId);
        }
    }
    res.json({ message: `Generated ${count} user registration events`, metrics });
});

app.post('/api/scenarios/user-login', (req, res) => {
    const count = req.body.count || 15;
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        metrics.userLogins++;
        businessMetricsCounters.userLogins.inc();
        generateLog('info', 'auth', `User login successful`, userId);
        
        // Simulate login failures
        if (Math.random() < 0.15) {
            metrics.errorCount++;
            businessMetricsCounters.errors.inc({ service: 'auth', error_type: 'login_failed' });
            generateLog('warn', 'auth', `Failed login attempt - invalid credentials`, userId);
        }
    }
    res.json({ message: `Generated ${count} user login events`, metrics });
});

app.post('/api/scenarios/product-browsing', (req, res) => {
    const count = req.body.count || 25;
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        const product = products[Math.floor(Math.random() * products.length)];
        metrics.productViews++;
        businessMetricsCounters.productViews.inc({ 
            product_id: product.id.toString(), 
            product_name: product.name 
        });
        generateLog('info', 'catalog', `Product viewed: ${product.name}`, userId, product.id);
        
        // Simulate product search
        if (Math.random() < 0.3) {
            generateLog('info', 'search', `Product search performed for: ${product.name}`, userId);
        }
    }
    res.json({ message: `Generated ${count} product browsing events`, metrics });
});

app.post('/api/scenarios/shopping-cart', (req, res) => {
    const count = req.body.count || 20;
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        const product = products[Math.floor(Math.random() * products.length)];
        metrics.cartAdditions++;
        businessMetricsCounters.cartAdditions.inc();
        generateLog('info', 'cart', `Product added to cart: ${product.name}`, userId, product.id);
        
        // Simulate cart errors
        if (Math.random() < 0.05) {
            metrics.errorCount++;
            businessMetricsCounters.errors.inc({ service: 'cart', error_type: 'session_expired' });
            generateLog('error', 'cart', `Failed to add product to cart - session expired`, userId, product.id);
        }
    }
    res.json({ message: `Generated ${count} shopping cart events`, metrics });
});

app.post('/api/scenarios/checkout-payment', (req, res) => {
    const count = req.body.count || 12;
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        
        // Checkout process
        metrics.checkouts++;
        businessMetricsCounters.checkouts.inc();
        generateLog('info', 'checkout', `Checkout process started`, userId);
        
        // Payment processing
        if (Math.random() < 0.8) {
            metrics.paymentProcessed++;
            businessMetricsCounters.paymentProcessed.inc();
            const amount = Math.floor(Math.random() * 1000) + 50;
            generateLog('info', 'payment', `Payment processed successfully - $${amount}`, userId);
        } else {
            metrics.paymentErrors++;
            metrics.errorCount++;
            businessMetricsCounters.paymentErrors.inc();
            businessMetricsCounters.errors.inc({ service: 'payment', error_type: 'insufficient_funds' });
            generateLog('error', 'payment', `Payment failed - insufficient funds`, userId);
        }
    }
    res.json({ message: `Generated ${count} checkout and payment events`, metrics });
});

app.post('/api/scenarios/inventory-management', (req, res) => {
    const count = req.body.count || 15;
    for (let i = 0; i < count; i++) {
        const product = products[Math.floor(Math.random() * products.length)];
        metrics.inventoryChecks++;
        generateLog('info', 'inventory', `Inventory check for: ${product.name} - Stock: ${product.stock}`, null, product.id);
        
        // Simulate low inventory warnings
        if (product.stock < 30) {
            metrics.inventoryLow++;
            generateLog('warn', 'inventory', `Low inventory warning for: ${product.name} - Stock: ${product.stock}`, null, product.id);
        }
        
        // Simulate inventory errors
        if (Math.random() < 0.08) {
            metrics.errorCount++;
            businessMetricsCounters.errors.inc({ service: 'inventory', error_type: 'database_connection_failed' });
            generateLog('error', 'inventory', `Inventory system error - database connection failed`, null, product.id);
        }
    }
    res.json({ message: `Generated ${count} inventory management events`, metrics });
});

app.post('/api/scenarios/shipping-fulfillment', (req, res) => {
    const count = req.body.count || 18;
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        
        // Shipping request
        metrics.shippingRequests++;
        const trackingNumber = Math.random().toString(36).substring(2, 15).toUpperCase();
        generateLog('info', 'shipping', `Shipping label created - Tracking: ${trackingNumber}`, userId);
        
        // Order fulfillment
        if (Math.random() < 0.9) {
            metrics.ordersFulfilled++;
            generateLog('info', 'fulfillment', `Order fulfilled and shipped - Tracking: ${trackingNumber}`, userId);
        } else {
            metrics.errorCount++;
            businessMetricsCounters.errors.inc({ service: 'shipping', error_type: 'carrier_unavailable' });
            generateLog('error', 'shipping', `Shipping error - carrier service unavailable`, userId);
        }
    }
    res.json({ message: `Generated ${count} shipping and fulfillment events`, metrics });
});

app.post('/api/scenarios/customer-support', (req, res) => {
    const count = req.body.count || 8;
    const supportIssues = [
        'Order not received',
        'Product defective',
        'Refund request',
        'Account access issues',
        'Payment inquiry',
        'Shipping delay complaint'
    ];
    
    for (let i = 0; i < count; i++) {
        const userId = users[Math.floor(Math.random() * users.length)];
        const issue = supportIssues[Math.floor(Math.random() * supportIssues.length)];
        metrics.customerSupport++;
        
        const ticketId = Math.random().toString(36).substring(2, 10).toUpperCase();
        generateLog('info', 'support', `Support ticket created: ${issue} - Ticket: ${ticketId}`, userId);
        
        // Simulate escalated issues
        if (Math.random() < 0.2) {
            generateLog('warn', 'support', `Support ticket escalated - Ticket: ${ticketId}`, userId);
        }
    }
    res.json({ message: `Generated ${count} customer support events`, metrics });
});

app.post('/api/scenarios/system-errors', (req, res) => {
    const count = req.body.count || 5;
    const errorTypes = [
        { service: 'database', message: 'Database connection timeout' },
        { service: 'payment', message: 'Payment gateway unavailable' },
        { service: 'inventory', message: 'Inventory service timeout' },
        { service: 'shipping', message: 'Carrier API rate limit exceeded' },
        { service: 'auth', message: 'Authentication service down' }
    ];
    
    for (let i = 0; i < count; i++) {
        const error = errorTypes[Math.floor(Math.random() * errorTypes.length)];
        metrics.errorCount++;
        businessMetricsCounters.errors.inc({ service: error.service, error_type: 'system_error' });
        generateLog('error', error.service, error.message);
    }
    res.json({ message: `Generated ${count} system error events`, metrics });
});

app.post('/api/scenarios/high-traffic', (req, res) => {
    const duration = req.body.duration || 30; // seconds
    let eventCount = 0;
    
    highTrafficScenarioActive = true; // Activate high CPU simulation flag
    
    const interval = setInterval(() => {
        // Simulate high traffic with multiple concurrent actions
        for (let i = 0; i < 5; i++) {
            const userId = users[Math.floor(Math.random() * users.length)];
            const product = products[Math.floor(Math.random() * products.length)];
            
            metrics.productViews++;
            businessMetricsCounters.productViews.inc({ 
                product_id: product.id.toString(), 
                product_name: product.name 
            });
            generateLog('info', 'catalog', `High traffic - Product viewed: ${product.name}`, userId, product.id);
            eventCount++;
        }
    }, 1000);
    
    setTimeout(() => {
        clearInterval(interval);
        highTrafficScenarioActive = false; // Deactivate high CPU simulation flag
    }, duration * 1000);
    
    res.json({ message: `Started high traffic simulation for ${duration} seconds`, metrics });
});

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
    console.log(`[INFO] Server running on port ${port}`);
});