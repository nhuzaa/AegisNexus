#!/bin/bash

# OpenTofu/Terraform Destruction Script for Azure Infrastructure
# This script destroys all Azure resources created by the infrastructure

set -e

echo "=========================================="
echo "🧹 Azure Infrastructure Destruction"
echo "=========================================="
echo

# Check if we're in the right directory
if [ ! -f "main.tf" ]; then
    echo "❌ Error: main.tf not found!"
    echo "Please run this script from the opentofu directory."
    exit 1
fi

# Check if OpenTofu or Terraform is available
TERRAFORM_CMD=""
if command -v tofu &> /dev/null; then
    TERRAFORM_CMD="tofu"
elif command -v terraform &> /dev/null; then
    TERRAFORM_CMD="terraform"
else
    echo "❌ Error: Neither OpenTofu nor Terraform is installed!"
    exit 1
fi

# Check if state file exists
if [ ! -f "terraform.tfstate" ]; then
    echo "⚠️  No terraform.tfstate found - no infrastructure to destroy"
    exit 0
fi

# Get current infrastructure info
echo "🔍 Current Infrastructure:"
if $TERRAFORM_CMD output vm_public_ip &> /dev/null; then
    VM_IP=$($TERRAFORM_CMD output -raw vm_public_ip 2>/dev/null || echo "Unknown")
    VM_NAME=$($TERRAFORM_CMD output -raw vm_name 2>/dev/null || echo "Unknown") 
    RG_NAME=$($TERRAFORM_CMD output -raw resource_group_name 2>/dev/null || echo "Unknown")
    
    echo "  VM Name: $VM_NAME"
    echo "  VM IP: $VM_IP"
    echo "  Resource Group: $RG_NAME"
else
    echo "  No active infrastructure found in state"
fi

echo
echo "⚠️  WARNING: This will permanently destroy:"
echo "   - Virtual Machine and all data"
echo "   - Virtual Network and subnets"
echo "   - Network Security Group"
echo "   - Public IP address"
echo "   - Storage account"
echo "   - Resource Group (if empty)"
echo
echo "💾 Make sure you have:"
echo "   - Backed up any important data"
echo "   - Run ./rollback.sh to clean applications first"
echo "   - Saved any configuration you need"
echo

read -p "Are you sure you want to destroy the infrastructure? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Destruction cancelled."
    exit 0
fi

echo
read -p "This action cannot be undone. Type 'DESTROY' to confirm: " confirm
if [ "$confirm" != "DESTROY" ]; then
    echo "Destruction cancelled."
    exit 0
fi

echo
echo "⏳ Planning destruction..."
$TERRAFORM_CMD plan -destroy -out=destroy.tfplan

echo
echo "🧨 Destroying infrastructure..."
$TERRAFORM_CMD apply destroy.tfplan

echo
echo "🧹 Cleaning up local files..."
rm -f destroy.tfplan
rm -f terraform.tfstate.backup

# Clean up inventory file
INVENTORY_PATH="../inventory.ini"
if [ -f "$INVENTORY_PATH" ]; then
    echo "🗑️  Cleaning up Ansible inventory..."
    cat > "$INVENTORY_PATH" << EOF
# Azure VM Inventory for Kubernetes Infrastructure Setup
# Infrastructure destroyed on $(date)
# Run 'cd opentofu && ./deploy-infra.sh' to recreate

[azure_vm]
# No VMs currently deployed

[azure_vm:vars]
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF
    echo "✅ Updated $INVENTORY_PATH"
fi

echo
echo "=========================================="
echo "✅ DESTRUCTION COMPLETED SUCCESSFULLY!"
echo "=========================================="
echo
echo "All Azure resources have been removed:"
echo "  ✓ Virtual Machine destroyed"
echo "  ✓ Network resources removed"
echo "  ✓ Storage account deleted"
echo "  ✓ Resource group cleaned up"
echo "  ✓ Local state cleaned"
echo
echo "📊 Cost savings: ~\$120-200/month"
echo
echo "To redeploy infrastructure:"
echo "  ./deploy-infra.sh"
echo
echo "🎉 Infrastructure destruction completed!"
