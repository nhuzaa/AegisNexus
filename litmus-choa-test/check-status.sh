#!/bin/bash

# Monitoring script to check the status of all services
# Run this script on the Azure VM after setup

echo "🔍 Chaos Engineering Environment Status Check"
echo "=============================================="

# Get Minikube IP
MINIKUBE_IP=$(minikube ip 2>/dev/null)

if [ -z "$MINIKUBE_IP" ]; then
    echo "❌ Minikube is not running or not accessible"
    echo "   Try running: minikube start"
    exit 1
fi

echo "📍 Minikube IP: $MINIKUBE_IP"
echo ""

# Check cluster status
echo "🔍 Cluster Status:"
kubectl cluster-info --request-timeout=10s

echo ""
echo "🔍 Node Status:"
kubectl get nodes

echo ""
echo "🔍 Namespace Status:"
kubectl get namespaces

echo ""
echo "🔍 Pod Status (All Namespaces):"
kubectl get pods --all-namespaces

echo ""
echo "🔍 Service Status:"
kubectl get services --all-namespaces

echo ""
echo "🔍 Chaos Engines:"
kubectl get chaosengines --all-namespaces

echo ""
echo "🌐 Service URLs:"
echo "=================="
echo "📊 Grafana:        http://$MINIKUBE_IP:30080 (admin/admin123)"
echo "📈 Prometheus:     http://$MINIKUBE_IP:30090"
echo "🚨 AlertManager:   http://$MINIKUBE_IP:30093"
echo "📝 Loki:           http://$MINIKUBE_IP:30031"
echo "🌐 Nginx App:      http://$MINIKUBE_IP:30082"
echo "🔬 Litmus Frontend: http://$MINIKUBE_IP:30091"

echo ""
echo "🧪 Test Connectivity:"
echo "======================"

# Test each service
services=("30080:Grafana" "30090:Prometheus" "30093:AlertManager" "30031:Loki" "30082:Nginx" "30091:Litmus")

for service in "${services[@]}"; do
    port=$(echo $service | cut -d: -f1)
    name=$(echo $service | cut -d: -f2)
    
    if curl -s --connect-timeout 5 http://$MINIKUBE_IP:$port > /dev/null; then
        echo "✅ $name (port $port) - Accessible"
    else
        echo "❌ $name (port $port) - Not accessible"
    fi
done

echo ""
echo "📊 Resource Usage:"
echo "=================="
kubectl top nodes 2>/dev/null || echo "Metrics server not ready yet"
kubectl top pods --all-namespaces 2>/dev/null || echo "Metrics server not ready yet"

echo ""
echo "🔍 Recent Events:"
echo "=================="
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -10

echo ""
echo "✅ Status check completed!"
echo ""
echo "💡 Tips:"
echo "   - Access Grafana at http://$MINIKUBE_IP:30080 with admin/admin123"
echo "   - Run chaos experiments from ~/chaos-experiments/"
echo "   - Monitor with 'kubectl get pods -w' during experiments"
