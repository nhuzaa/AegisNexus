#!/bin/bash

# Chaos Engineering Environment Configuration and Deployment Script
# This script helps you configure and deploy the complete chaos engineering environment

set -e

echo "🚀 Chaos Engineering Environment Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Ansible is installed
if ! command -v ansible &> /dev/null; then
    print_error "Ansible is not installed. Please install it first:"
    echo "pip install ansible"
    exit 1
fi

print_success "Ansible is installed"

# Step 1: Configure Azure VM IP
echo
print_status "Step 1: Configure Azure VM IP Address"
echo "======================================="

current_ip=$(grep -E '^[^;]*ansible_user' inventory.ini | awk '{print $1}' | head -1)
if [[ "$current_ip" == "your-azure-vm-ip" ]]; then
    print_warning "Azure VM IP is not configured yet"
    echo
    echo "Please provide your Azure VM IP address:"
    read -p "Azure VM IP: " azure_vm_ip
    
    if [[ -z "$azure_vm_ip" ]]; then
        print_error "IP address cannot be empty"
        exit 1
    fi
    
    # Update inventory.ini
    sed -i.bak "s/your-azure-vm-ip/$azure_vm_ip/g" inventory.ini
    print_success "Updated inventory.ini with IP: $azure_vm_ip"
else
    print_success "Azure VM IP already configured: $current_ip"
fi

# Step 2: Configure Discord Webhook
echo
print_status "Step 2: Configure Discord Webhook"
echo "=================================="

current_webhook=$(grep "discord_webhook_url:" ansible-playbook.yml | grep -o 'https://[^"]*')
if [[ "$current_webhook" == *"YOUR_WEBHOOK"* ]]; then
    print_warning "Discord webhook is not configured yet"
    echo
    echo "Please provide your Discord webhook URL (or press Enter to skip Discord integration):"
    read -p "Discord Webhook URL: " discord_webhook
    
    if [[ -n "$discord_webhook" ]]; then
        # Update ansible-playbook.yml
        escaped_webhook=$(echo "$discord_webhook" | sed 's/[\/&]/\\&/g')
        sed -i.bak "s|discord_webhook_url: \"https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN\"|discord_webhook_url: \"$escaped_webhook\"|g" ansible-playbook.yml
        print_success "Updated Discord webhook URL"
    else
        print_warning "Skipping Discord integration - you can configure it later"
    fi
else
    print_success "Discord webhook already configured"
fi

# Step 3: Check SSH connectivity
echo
print_status "Step 3: Testing SSH Connectivity"
echo "================================="

ssh_key_path=$(grep "ansible_ssh_private_key_file" inventory.ini | awk -F'=' '{print $2}' | tr -d ' ')
vm_ip=$(grep -E '^[^;]*ansible_user' inventory.ini | awk '{print $1}' | head -1)

if [[ "$ssh_key_path" == *"~"* ]]; then
    ssh_key_path="${ssh_key_path/#\~/$HOME}"
fi

print_status "Testing SSH connection to $vm_ip with key $ssh_key_path"

if ssh -i "$ssh_key_path" -o ConnectTimeout=10 -o StrictHostKeyChecking=no ubuntu@"$vm_ip" "echo 'SSH connection successful'" &>/dev/null; then
    print_success "SSH connection to Azure VM is working"
else
    print_error "Cannot connect to Azure VM via SSH"
    echo "Please check:"
    echo "  1. VM IP address is correct"
    echo "  2. SSH key path is correct"
    echo "  3. VM is running and accessible"
    echo "  4. Security group allows SSH (port 22)"
    exit 1
fi

# Step 4: Run Ansible playbook
echo
print_status "Step 4: Deploy Chaos Engineering Environment"
echo "============================================="

echo "This will:"
echo "  • Install Docker, Minikube, kubectl, Helm"
echo "  • Deploy Prometheus, Grafana, Loki, AlertManager"
echo "  • Install LitmusChaos"
echo "  • Create sample application with 10 replicas"
echo "  • Configure Discord alerts (if webhook provided)"
echo

read -p "Do you want to proceed with the deployment? (y/N): " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
    print_status "Starting Ansible playbook deployment..."
    echo
    
    # Run the playbook with verbose output
    if ansible-playbook -i inventory.ini ansible-playbook.yml -v; then
        print_success "Deployment completed successfully!"
        echo
        echo "🎉 Your chaos engineering environment is ready!"
        echo
        echo "Access URLs (replace <minikube-ip> with your VM IP):"
        echo "  📊 Grafana:        http://$vm_ip:30080 (admin/admin123)"
        echo "  📈 Prometheus:     http://$vm_ip:30090"
        echo "  🚨 AlertManager:   http://$vm_ip:30093"
        echo "  📋 Loki:          http://$vm_ip:30031"
        echo "  🌐 Sample App:     http://$vm_ip:30082"
        echo "  🔥 Litmus Portal:  http://$vm_ip:30091"
        echo
        echo "Next steps:"
        echo "  1. Open Grafana and explore the chaos engineering dashboard"
        echo "  2. Access Litmus Portal to create chaos experiments"
        echo "  3. Check AlertManager for active alerts"
        echo "  4. Run: ./check-status.sh to verify all services"
        echo "  5. Run: ./chaos-runner-discord.sh to test chaos experiments"
        
    else
        print_error "Deployment failed. Check the output above for errors."
        exit 1
    fi
else
    print_warning "Deployment cancelled by user"
fi

echo
print_status "Configuration and deployment script completed"
