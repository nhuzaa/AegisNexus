#!/bin/bash

# Pre-deployment verification script
# Checks if all prerequisites are met before running the chaos engineering setup

echo "🔍 Pre-deployment Verification"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

checks_passed=0
checks_total=0

# Check 1: Ansible installation
print_check "Checking Ansible installation..."
((checks_total++))
if command -v ansible &> /dev/null; then
    ansible_version=$(ansible --version | head -n1)
    print_pass "Ansible is installed: $ansible_version"
    ((checks_passed++))
else
    print_fail "Ansible is not installed. Install with: pip install ansible"
fi

# Check 2: Python installation
print_check "Checking Python installation..."
((checks_total++))
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    print_pass "Python3 is installed: $python_version"
    ((checks_passed++))
else
    print_fail "Python3 is not installed"
fi

# Check 3: SSH key exists
print_check "Checking SSH key configuration..."
((checks_total++))
ssh_key_path=$(grep "ansible_ssh_private_key_file" inventory.ini | sed 's/.*ansible_ssh_private_key_file=//' | tr -d ' ')
if [[ "$ssh_key_path" == *"~"* ]]; then
    ssh_key_path="${ssh_key_path/#\~/$HOME}"
fi

if [[ -f "$ssh_key_path" ]]; then
    print_pass "SSH key exists: $ssh_key_path"
    ((checks_passed++))
else
    print_fail "SSH key not found: $ssh_key_path"
fi

# Check 4: Inventory configuration
print_check "Checking inventory configuration..."
((checks_total++))
vm_ip=$(grep -E '^[^;#]*ansible_user' inventory.ini | awk '{print $1}' | head -1)
if [[ "$vm_ip" != "your-azure-vm-ip" && -n "$vm_ip" ]]; then
    print_pass "VM IP configured: $vm_ip"
    ((checks_passed++))
else
    print_fail "VM IP not configured in inventory.ini"
fi

# Check 5: Discord webhook configuration
print_check "Checking Discord webhook configuration..."
((checks_total++))
discord_webhook=$(grep "discord_webhook_url:" ansible-playbook.yml | grep -o 'https://[^"]*')
if [[ "$discord_webhook" != *"YOUR_WEBHOOK"* && -n "$discord_webhook" ]]; then
    print_pass "Discord webhook configured"
    ((checks_passed++))
else
    print_warn "Discord webhook not configured (optional)"
    ((checks_passed++))  # Count as pass since it's optional
fi

# Check 6: Required files exist
print_check "Checking required files..."
((checks_total++))
required_files=("ansible-playbook.yml" "inventory.ini" "requirements.yml")
all_files_exist=true

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        all_files_exist=false
    fi
done

if $all_files_exist; then
    print_pass "All required files present"
    ((checks_passed++))
else
    print_fail "Some required files are missing"
fi

# Summary
echo
echo "📋 Verification Summary"
echo "======================"
echo "Checks passed: $checks_passed/$checks_total"

if [[ $checks_passed -eq $checks_total ]]; then
    print_pass "All checks passed! Ready to deploy."
    echo
    echo "🚀 Next steps:"
    echo "  1. Run: ./configure-and-run.sh"
    echo "  2. Or manually run: ansible-playbook -i inventory.ini ansible-playbook.yml"
else
    print_fail "Some checks failed. Please fix the issues above before deploying."
    echo
    echo "💡 Common fixes:"
    echo "  • Install Ansible: pip install ansible"
    echo "  • Configure VM IP in inventory.ini"
    echo "  • Check SSH key path and permissions"
    echo "  • Set up Discord webhook (optional)"
fi

echo
echo "📁 Available scripts:"
echo "  • ./configure-and-run.sh    - Interactive setup and deployment"
echo "  • ./check-status.sh         - Check service status after deployment"
echo "  • ./chaos-runner-discord.sh - Run chaos experiments with Discord alerts"
echo "  • ./test-discord-alert.sh   - Test Discord webhook integration"
