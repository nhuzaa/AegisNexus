#!/bin/bash

# Quick environment status checker
# This script helps verify the chaos engineering environment setup

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Chaos Engineering Environment Status Check${NC}"
echo "=============================================="

# Check if running on Azure VM
if command -v curl &> /dev/null; then
    echo -n "Getting Azure VM metadata... "
    AZURE_METADATA=$(curl -s -H "Metadata:true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01" 2>/dev/null)
    if [ $? -eq 0 ] && echo "$AZURE_METADATA" | grep -q "publicIpAddress"; then
        PUBLIC_IP=$(echo "$AZURE_METADATA" | jq -r '.network.interface[0].ipv4.ipAddress[0].publicIpAddress' 2>/dev/null)
        PRIVATE_IP=$(echo "$AZURE_METADATA" | jq -r '.network.interface[0].ipv4.ipAddress[0].privateIpAddress' 2>/dev/null)
        LOCATION=$(echo "$AZURE_METADATA" | jq -r '.compute.location' 2>/dev/null)
        
        echo -e "${GREEN}✅ Running on Azure VM${NC}"
        echo -e "${YELLOW}Public IP:${NC} $PUBLIC_IP"
        echo -e "${YELLOW}Private IP:${NC} $PRIVATE_IP"
        echo -e "${YELLOW}Location:${NC} $LOCATION"
    else
        echo -e "${YELLOW}⚠️ Not running on Azure VM or metadata unavailable${NC}"
        PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || echo "Unable to determine")
        echo -e "${YELLOW}External IP:${NC} $PUBLIC_IP"
    fi
else
    echo -e "${RED}❌ curl not available${NC}"
fi

echo ""

# Check if Minikube is running
echo -n "Checking Minikube status... "
if command -v minikube &> /dev/null; then
    if minikube status | grep -q "Running"; then
        echo -e "${GREEN}✅ Running${NC}"
        MINIKUBE_IP=$(minikube ip 2>/dev/null)
        echo -e "${YELLOW}Minikube IP:${NC} $MINIKUBE_IP"
    else
        echo -e "${RED}❌ Not running${NC}"
    fi
else
    echo -e "${RED}❌ Minikube not installed${NC}"
fi

echo ""

# Check Kubernetes services
echo -e "${YELLOW}Kubernetes Services Status:${NC}"
if command -v kubectl &> /dev/null; then
    kubectl get services --all-namespaces -o wide | grep -E "(LoadBalancer|NodePort)" || echo "No exposed services found"
else
    echo -e "${RED}❌ kubectl not available${NC}"
fi

echo ""

# Check if key services are accessible
echo -e "${YELLOW}Service Accessibility Test:${NC}"
if [ ! -z "$PRIVATE_IP" ]; then
    TEST_IP="$PRIVATE_IP"
elif [ ! -z "$MINIKUBE_IP" ]; then
    TEST_IP="$MINIKUBE_IP"
else
    TEST_IP="localhost"
fi

services=(
    "Grafana:3000"
    "Prometheus:9090"
    "AlertManager:9093"
    "Loki:3100"
    "Nginx:80"
    "Litmus:9091"
)

for service in "${services[@]}"; do
    name="${service%:*}"
    port="${service#*:}"
    echo -n "  $name ($TEST_IP:$port): "
    
    if timeout 3 bash -c "</dev/tcp/$TEST_IP/$port" 2>/dev/null; then
        echo -e "${GREEN}✅ Accessible${NC}"
    else
        echo -e "${RED}❌ Not accessible${NC}"
    fi
done

echo ""

# Display access URLs
echo -e "${BLUE}🔗 Access URLs (replace with your public IP if needed):${NC}"
DISPLAY_IP=${PUBLIC_IP:-$PRIVATE_IP}
DISPLAY_IP=${DISPLAY_IP:-$TEST_IP}

echo "📊 Grafana Dashboard:    http://$DISPLAY_IP:3000 (admin/admin123)"
echo "📈 Prometheus Metrics:   http://$DISPLAY_IP:9090"
echo "🚨 AlertManager:         http://$DISPLAY_IP:9093"
echo "📋 Loki Logs:            http://$DISPLAY_IP:3100"
echo "🌐 Test Application:     http://$DISPLAY_IP:80"
echo "⚡ Litmus Chaos Portal:  http://$DISPLAY_IP:9091"

echo ""
echo -e "${BLUE}💡 Next Steps:${NC}"
echo "1. Ensure Azure NSG allows inbound traffic on these ports"
echo "2. Run: ./verify-external-access.sh for detailed checks"
echo "3. Start chaos experiments: ./chaos-runner-discord.sh list"
echo "4. Test Discord integration: ./chaos-runner-discord.sh test-discord"
