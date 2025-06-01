# OpenTofu Infrastructure for Kubernetes Chaos Engineering

This directory contains OpenTofu (Terraform-compatible) infrastructure as code for deploying Azure VMs with comprehensive Network Security Group rules for Kubernetes, monitoring, and chaos engineering tools.

## 🏗️ Infrastructure Components

### Azure Resources Created
- **Resource Group**: Container for all resources
- **Virtual Network**: Isolated network environment
- **Subnet**: Network segment for VMs
- **Public IP**: Static IP for external access
- **Network Security Group**: Comprehensive firewall rules
- **Network Interface**: VM network connection
- **Linux Virtual Machine**: Ubuntu 20.04 LTS with cloud-init
- **Storage Account**: For diagnostics and boot diagnostics

### Network Security Group Rules
- **SSH (22)**: Remote access
- **HTTP (80)**: Web traffic
- **HTTPS (443)**: Secure web traffic
- **Grafana (3000)**: Dashboard access
- **Litmus Portal (8080)**: Chaos engineering interface
- **Nginx App (8081)**: Sample application
- **Prometheus (9090)**: Metrics collection
- **Kubernetes API (6443)**: Cluster management
- **NodePort Range (30000-32767)**: Kubernetes services
- **Monitoring Ports (9091,9093,9100,3100)**: Additional tools
- **All TCP Inbound**: Development mode (restrict for production)

## 🚀 Quick Start

### Prerequisites

1. **OpenTofu or Terraform** installed:
   ```bash
   # OpenTofu (recommended)
   brew install opentofu
   
   # Or Terraform
   brew install terraform
   ```

2. **Azure CLI** installed and authenticated:
   ```bash
   az login
   az account set --subscription "your-subscription-id"
   ```

3. **SSH Key Pair** (will be auto-generated if missing)

### Deployment

1. **Deploy Infrastructure**:
   ```bash
   chmod +x deploy-infra.sh
   ./deploy-infra.sh
   ```

2. **Customize Configuration** (optional):
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your preferences
   ```

3. **Deploy Kubernetes Stack**:
   ```bash
   cd .. && ./deploy.sh
   ```

### Manual Deployment

If you prefer manual control:

```bash
# Initialize
tofu init

# Plan deployment
tofu plan

# Apply changes
tofu apply

# Get outputs
tofu output
```

## 📊 Configuration Options

### VM Sizes (via terraform.tfvars)
- `Standard_B2s`: 2 vCPU, 4GB RAM (minimal)
- `Standard_D4s_v3`: 4 vCPU, 16GB RAM (recommended)
- `Standard_D8s_v3`: 8 vCPU, 32GB RAM (performance)

### Security Options
```hcl
# Restrict access to specific IPs (recommended for production)
allowed_source_ips = ["YOUR_PUBLIC_IP/32"]

# Or allow all (development only)
allowed_source_ips = []
```

### VM Configuration
```hcl
vm_size              = "Standard_D4s_v3"
disk_size_gb         = 128
enable_accelerated_networking = true
enable_boot_diagnostics      = true
```

## 🔧 File Structure

```
opentofu/
├── main.tf                    # Main infrastructure definition
├── variables.tf               # Input variables
├── outputs.tf                 # Output values
├── cloud-init.yml            # VM initialization script
├── terraform.tfvars.example  # Configuration template
├── deploy-infra.sh           # Deployment script
├── destroy-infra.sh          # Destruction script
└── README.md                 # This file
```

## 📋 Outputs

After deployment, you'll get:

```bash
# VM connection info
vm_public_ip              = "40.117.xxx.xxx"
ssh_connection_command    = "ssh -i ~/.ssh/id_rsa azureuser@40.117.xxx.xxx"
ansible_inventory_entry   = "40.117.xxx.xxx ansible_user=azureuser ..."

# Service URLs (after Kubernetes deployment)
service_urls = {
  grafana_dashboard = "http://40.117.xxx.xxx:3000"
  prometheus       = "http://40.117.xxx.xxx:9090"
  litmus_portal    = "http://40.117.xxx.xxx:8080"
  nginx_app        = "http://40.117.xxx.xxx:8081"
}
```

## 🔄 Management Commands

### View Current State
```bash
tofu show
tofu output
```

### Update Infrastructure
```bash
# Modify terraform.tfvars or .tf files
tofu plan
tofu apply
```

### Destroy Infrastructure
```bash
./destroy-infra.sh
# or manually: tofu destroy
```

## 🛡️ Security Considerations

### Development vs Production

**Development Mode (default)**:
- All TCP ports open from any source
- Simple for testing and development
- **Not suitable for production**

**Production Mode**:
```hcl
# In terraform.tfvars
allowed_source_ips = ["YOUR_OFFICE_IP/32", "YOUR_HOME_IP/32"]
```

### SSH Key Management
- Keys auto-generated if missing
- Stored in `~/.ssh/id_rsa` (private) and `~/.ssh/id_rsa.pub` (public)
- Password authentication disabled
- Root login disabled

### Resource Tagging
All resources tagged with:
- Environment: development/staging/production
- Project: KubernetesChaosInfra
- CreatedBy: OpenTofu

## 💰 Cost Estimation

### Standard_D4s_v3 (recommended)
- **VM**: ~$140/month
- **Storage**: ~$15/month
- **Networking**: ~$5/month
- **Total**: ~$160/month

### Cost Optimization
- Use `Standard_B2s` for testing (~$30/month)
- Enable auto-shutdown schedules
- Use spot instances for development
- Monitor with Azure Cost Management

## 🔧 Troubleshooting

### Common Issues

1. **SSH Key Errors**:
   ```bash
   chmod 600 ~/.ssh/id_rsa
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
   ```

2. **Azure Authentication**:
   ```bash
   az login
   az account list
   az account set --subscription "subscription-id"
   ```

3. **Resource Conflicts**:
   ```bash
   # Check existing resources
   az group list
   az vm list
   
   # Clean up if needed
   tofu destroy
   ```

4. **Network Connectivity**:
   ```bash
   # Test from local machine
   telnet VM_IP 22
   nmap -p 22,3000,8080,8081,9090 VM_IP
   ```

### Logs and Diagnostics

```bash
# Check cloud-init logs on VM
ssh azureuser@VM_IP "sudo tail -f /var/log/cloud-init-output.log"

# Check boot diagnostics in Azure Portal
# VM -> Boot diagnostics -> Serial log
```

## 🤝 Integration with Ansible

The OpenTofu deployment automatically:
1. Creates and updates `../inventory.ini`
2. Tests SSH connectivity
3. Provides next steps for Ansible deployment

Manual integration:
```bash
# Get VM IP
VM_IP=$(tofu output -raw vm_public_ip)

# Update inventory
echo "$VM_IP ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/id_rsa" > ../inventory.ini

# Deploy Kubernetes stack
cd .. && ansible-playbook -i inventory.ini setup-infrastructure.yml
```

## 📈 Advanced Configuration

### Multiple VMs
```hcl
# In main.tf, use count or for_each
resource "azurerm_linux_virtual_machine" "main" {
  count = var.vm_count
  name  = "${var.vm_name}-${count.index + 1}"
  # ... rest of configuration
}
```

### Custom Images
```hcl
source_image_reference {
  publisher = "Canonical"
  offer     = "0001-com-ubuntu-server-focal"
  sku       = "20_04-lts-gen2"
  version   = "latest"
}
```

### Additional Disks
```hcl
resource "azurerm_managed_disk" "data" {
  name                 = "${var.vm_name}-data-disk"
  location             = azurerm_resource_group.main.location
  resource_group_name  = azurerm_resource_group.main.name
  storage_account_type = "Premium_LRS"
  create_option        = "Empty"
  disk_size_gb         = 500
}
```

## 📄 License

MIT License - see parent directory for details.

---

**Note**: This infrastructure is designed for development and testing. For production deployments, implement additional security measures, monitoring, backup strategies, and cost controls.
