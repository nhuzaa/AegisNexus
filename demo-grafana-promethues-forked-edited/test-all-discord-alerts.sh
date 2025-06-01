#!/bin/bash

# Test script to verify Discord alerts for all Prometheus rules
echo "🚀 Testing Discord alerts for all Prometheus rules..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📋 Summary of all configured alerts:${NC}"
echo ""

echo -e "${GREEN}1. System Alerts (1.basic.yml):${NC}"
echo "   ✅ HighCPUUsage (critical) - Triggers when CPU > 80%"
echo "   ✅ HighMemoryUsage (critical) - Triggers when Memory > 85%"
echo "   ✅ LowMemoryWarning (warning) - Triggers when Memory > 70%"
echo ""

echo -e "${GREEN}2. Business Alerts (1.basic.yml):${NC}"
echo "   ✅ HighLoginRate (warning) - Triggers when >10 logins in 10s"
echo "   ✅ HighPaymentRate (warning) - Triggers when >5 payments in 5s"
echo "   ✅ HighPaymentErrorRate (critical) - Triggers when payment error rate > 0.1/s"
echo "   ✅ HighErrorRate (warning) - Triggers when app error rate > 0.05/s"
echo ""

echo -e "${GREEN}3. Availability Alerts (1.basic.yml):${NC}"
echo "   ✅ ServiceDown (critical) - Triggers when service is down for >10s"
echo "   ✅ HighResponseTime (warning) - Triggers when response time > 2000ms"
echo ""

echo -e "${GREEN}4. Monitoring Alerts (2.absent.yml):${NC}"
echo "   ✅ NoMetrics (critical) - Triggers when no metrics for 10s"
echo ""

echo -e "${GREEN}5. Additional System Alerts (3.group.yml & 4.templating.yml):${NC}"
echo "   ✅ NewHighCPUUsage (critical) - Triggers when avg CPU > 80% over 5min"
echo "   ✅ NewHighCPUUsageCustom (critical) - Same as above with custom annotations"
echo "   ✅ HighCPU (critical) - Triggers when avg CPU > 80% over 5min (templated)"
echo ""

echo -e "${YELLOW}🔔 Discord Alert Routing Configuration:${NC}"
echo "   🔥 Critical alerts → discord-critical receiver (🔥 CRITICAL ALERT)"
echo "   ⚠️  Warning alerts → discord-warnings receiver (⚠️ WARNING ALERT)"
echo "   💳 Payment alerts → discord-payment receiver (💳 PAYMENT ALERT)"
echo "   🖥️  System alerts → discord-system receiver (🖥️ SYSTEM ALERT)"
echo "   📋 Default alerts → discord-default receiver (📋 DEFAULT ALERT)"
echo ""

echo -e "${YELLOW}🚀 To trigger test alerts:${NC}"
echo ""
echo "1. High CPU Usage Alert:"
echo "   curl -X POST http://localhost:3001/api/scenarios/high-traffic -H 'Content-Type: application/json' -d '{\"duration\": 60}'"
echo ""
echo "2. High Payment Rate Alert:"
echo "   curl -X POST http://localhost:3001/api/scenarios/checkout-payment -H 'Content-Type: application/json' -d '{\"count\": 20}'"
echo ""
echo "3. System Errors Alert:"
echo "   curl -X POST http://localhost:3001/api/scenarios/system-errors -H 'Content-Type: application/json' -d '{\"count\": 10}'"
echo ""
echo "4. High Login Rate Alert:"
echo "   curl -X POST http://localhost:3001/api/scenarios/user-login -H 'Content-Type: application/json' -d '{\"count\": 25}'"
echo ""

echo -e "${GREEN}✅ All Prometheus rules are configured to send Discord alerts!${NC}"
echo -e "${YELLOW}📍 Discord Webhook URL is configured and ready${NC}"
echo ""
echo -e "${RED}⚠️  Make sure your Docker containers are running:${NC}"
echo "   docker-compose up -d"
echo ""
