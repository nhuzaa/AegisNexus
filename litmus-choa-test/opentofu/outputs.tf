output "vm_public_ip" {
  description = "Public IP address of the virtual machine"
  value       = azurerm_public_ip.main.ip_address
  sensitive   = false
}

output "vm_private_ip" {
  description = "Private IP address of the virtual machine"
  value       = azurerm_network_interface.main.private_ip_address
  sensitive   = false
}

output "vm_name" {
  description = "Name of the virtual machine"
  value       = azurerm_linux_virtual_machine.main.name
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = data.azurerm_resource_group.main.name
}

output "vm_fqdn" {
  description = "Fully qualified domain name of the VM"
  value       = azurerm_public_ip.main.fqdn
}

output "ssh_connection_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh -i ~/.ssh/id_rsa ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
  sensitive   = false
}

output "ansible_inventory_entry" {
  description = "Ansible inventory entry for this VM"
  value       = "${azurerm_public_ip.main.ip_address} ansible_user=${var.admin_username} ansible_ssh_private_key_file=~/.ssh/id_rsa"
  sensitive   = false
}

output "service_urls" {
  description = "URLs for accessing deployed services"
  value = {
    grafana_dashboard    = "http://${azurerm_public_ip.main.ip_address}:3000"
    prometheus          = "http://${azurerm_public_ip.main.ip_address}:9090"
    litmus_portal       = "http://${azurerm_public_ip.main.ip_address}:8080"
    nginx_app          = "http://${azurerm_public_ip.main.ip_address}:8081"
    kubernetes_dashboard = "Access via: minikube dashboard --url"
  }
}

output "security_group_rules" {
  description = "List of security group rules created"
  value = {
    ssh                = "Port 22 - SSH Access"
    http              = "Port 80 - HTTP"
    https             = "Port 443 - HTTPS"
    grafana           = "Port 3000 - Grafana Dashboard"
    litmus_portal     = "Port 8080 - Litmus Chaos Portal"
    nginx_app         = "Port 8081 - Nginx Sample App"
    prometheus        = "Port 9090 - Prometheus"
    kubernetes_api    = "Port 6443 - Kubernetes API Server"
    nodeport_range    = "Ports 30000-32767 - Kubernetes NodePort Services"
    monitoring_ports  = "Ports 9091,9093,9100,3100 - Additional Monitoring"
    all_tcp_inbound   = "All TCP Ports - Development Access (Restrict in Production)"
  }
}

output "deployment_instructions" {
  description = "Instructions for deploying the infrastructure"
  value = <<-EOT
    
    ====================================
    🎉 INFRASTRUCTURE DEPLOYED SUCCESSFULLY!
    ====================================
    
    VM Details:
    - Name: ${azurerm_linux_virtual_machine.main.name}
    - Public IP: ${azurerm_public_ip.main.ip_address}
    - Resource Group: ${data.azurerm_resource_group.main.name}
    - Location: ${data.azurerm_resource_group.main.location}
    
    Next Steps:
    1. Update your Ansible inventory:
       echo "${azurerm_public_ip.main.ip_address} ansible_user=${var.admin_username} ansible_ssh_private_key_file=~/.ssh/id_rsa" > inventory.ini
    
    2. Test SSH connectivity:
       ssh -i ~/.ssh/id_rsa ${var.admin_username}@${azurerm_public_ip.main.ip_address}
    
    3. Deploy Kubernetes infrastructure:
       ./deploy.sh
    
    4. Access services after deployment:
       - Grafana: http://${azurerm_public_ip.main.ip_address}:3000 (admin/admin)
       - Prometheus: http://${azurerm_public_ip.main.ip_address}:9090
       - Litmus Portal: http://${azurerm_public_ip.main.ip_address}:8080
       - Nginx App: http://${azurerm_public_ip.main.ip_address}:8081
    
    Security: All required ports are open for development.
    For production, restrict source IPs in the NSG rules.
    
  EOT
}

output "cleanup_instructions" {
  description = "Instructions for cleaning up resources"
  value = <<-EOT
    To clean up all resources:
    1. Run rollback on the VM: ./rollback.sh
    2. Destroy infrastructure: tofu destroy
    
    Or use: terraform destroy (if using Terraform instead of OpenTofu)
  EOT
}

output "vm_password" {
  description = "Randomly generated password for the VM"
  value       = random_password.vm_password.result
  sensitive   = true
}
