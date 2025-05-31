#!/bin/bash

# Quick setup script for the chaos engineering environment
# Run this script after updating the inventory.ini file

set -e

echo "🚀 Setting up Chaos Engineering Environment..."

# Check if Ansible is installed
if ! command -v ansible &> /dev/null; then
    echo "❌ Ansible is not installed. Please install Ansible first."
    echo "   On macOS: brew install ansible"
    echo "   On Ubuntu: sudo apt install ansible"
    exit 1
fi

# Install required Python packages
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install required Ansible collections
echo "📦 Installing Ansible collections..."
ansible-galaxy collection install -r requirements.yml

# Check if inventory file has been updated
if grep -q "your-azure-vm-ip" inventory.ini; then
    echo "⚠️  Please update the inventory.ini file with your Azure VM IP address"
    echo "   Edit inventory.ini and replace 'your-azure-vm-ip' with your actual VM IP"
    exit 1
fi

# Test connectivity to the target host
echo "🔍 Testing connectivity to target host..."
ansible all -i inventory.ini -m ping

if [ $? -eq 0 ]; then
    echo "✅ Connectivity test passed!"
    
    # Run the main playbook
    echo "🚀 Running the main playbook..."
    ansible-playbook -i inventory.ini ansible-playbook.yml
    
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "To get the Minikube IP and access URLs:"
    echo "1. SSH into your VM: ssh ubuntu@<your-vm-ip>"
    echo "2. Run: minikube ip"
    echo "3. Access services using the URLs in the README.md"
    echo ""
    echo "📚 Read the README.md for detailed chaos engineering experiments!"
else
    echo "❌ Connectivity test failed. Please check:"
    echo "   - VM IP address in inventory.ini"
    echo "   - SSH key configuration"
    echo "   - Network connectivity"
fi
