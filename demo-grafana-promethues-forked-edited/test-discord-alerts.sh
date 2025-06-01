#!/bin/bash

echo "🚀 Testing Discord Alert Configuration..."

# Test Discord webhook directly
echo "📡 Testing Discord webhook connection..."
curl -X POST "https://discord.com/api/webhooks/1378468656245117059/y2NYQi4z6clqKxnk4aywPkmYX8Ot_o_7Do4Hcj1Ye0ZWsQJpMB4HBBhAuUSyzxZv7TRA/slack" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "🧪 **Test Alert from E-commerce Monitoring**\n\n✅ Discord webhook is working correctly!\n⏰ Test sent at: '"$(date)"'\n🔗 System: Prometheus + Alertmanager"
  }'

echo -e "\n\n🔄 Restarting monitoring stack..."
docker compose alertmanager down
docker compose alertmanager up -d

echo -e "\n⏳ Waiting for services to start up..."
sleep 15

echo -e "\n📊 Checking service status..."
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000"
echo "E-commerce App: http://localhost:3001"
echo "Alertmanager: http://localhost:9093"

echo -e "\n🎯 To trigger test alerts, visit: http://localhost:3001"
echo "Click on scenario buttons to generate metrics that may trigger alerts"

echo -e "\n📈 Alert Rules Configured:"
echo "  🔥 High CPU Usage: >80% for 30s"
echo "  💾 High Memory Usage: >85% for 30s" 
echo "  👥 High Login Rate: >10 logins in 10s"
echo "  💳 High Payment Rate: >5 payments in 5s"
echo "  🚨 Service Down: App unavailable for 10s"
echo "  ⏱️ High Response Time: >2000ms for 1m"

echo -e "\n✅ Setup complete! Discord alerts are configured."
