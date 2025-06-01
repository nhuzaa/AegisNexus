# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

# Use existing resource group
data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

# Create a virtual network
resource "azurerm_virtual_network" "main" {
  name                = "${var.vm_name}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name

  tags = {
    Environment = "Development"
    Project     = "KubernetesChaosInfra"
  }
}

# Create a subnet
resource "azurerm_subnet" "main" {
  name                 = "${var.vm_name}-subnet"
  resource_group_name  = data.azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create public IP
resource "azurerm_public_ip" "main" {
  name                = "${var.vm_name}-pip"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = {
    Environment = "Development"
    Project     = "KubernetesChaosInfra"
  }
}

# Create Network Security Group with comprehensive rules
resource "azurerm_network_security_group" "main" {
  name                = "${var.vm_name}-nsg"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name

  # SSH Access
  security_rule {
    name                       = "SSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # HTTP
  security_rule {
    name                       = "HTTP"
    priority                   = 200
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # HTTPS
  security_rule {
    name                       = "HTTPS"
    priority                   = 300
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Grafana Dashboard
  security_rule {
    name                       = "Grafana"
    priority                   = 400
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "3000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Litmus Chaos Portal
  security_rule {
    name                       = "LitmusPortal"
    priority                   = 500
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8080"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Nginx Sample App
  security_rule {
    name                       = "NginxApp"
    priority                   = 600
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8081"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Prometheus
  security_rule {
    name                       = "Prometheus"
    priority                   = 700
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "9090"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Kubernetes API Server (if needed for external access)
  security_rule {
    name                       = "KubernetesAPI"
    priority                   = 800
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "6443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # NodePort range for Kubernetes services
  security_rule {
    name                       = "NodePortRange"
    priority                   = 900
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "30000-32767"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Additional monitoring ports
  security_rule {
    name                       = "MonitoringPorts"
    priority                   = 1000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["9091", "9093", "9100", "3100"]
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  # Allow all TCP inbound (for development - restrictive in production)
  security_rule {
    name                       = "AllowAllTCPInbound"
    priority                   = 4000
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = {
    Environment = "Development"
    Project     = "KubernetesChaosInfra"
  }
}

# Create network interface
resource "azurerm_network_interface" "main" {
  name                = "${var.vm_name}-nic"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }

  tags = {
    Environment = "Development"
    Project     = "KubernetesChaosInfra"
  }
}

# Associate Network Security Group to the network interface
resource "azurerm_network_interface_security_group_association" "main" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

# Enable password authentication and generate a random password
resource "random_password" "vm_password" {
  length           = 16
  special          = true
  override_special = "_@"
}

# Create virtual machine
resource "azurerm_linux_virtual_machine" "main" {
  name                = var.vm_name
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  size                = var.vm_size
  admin_username      = var.admin_username
  admin_password      = random_password.vm_password.result

  # Enable password authentication
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file("/Users/nhz/Documents/code/meta-hacakthon/keys/kubetestkey.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = var.disk_size_gb
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-focal"
    sku       = "20_04-lts-gen2"
    version   = "latest"
  }

  # Custom script to prepare the system
  custom_data = base64encode(templatefile("${path.module}/cloud-init.yml", {
    admin_username = var.admin_username
  }))

  tags = {
    Environment = "Development"
    Project     = "KubernetesChaosInfra"
    Purpose     = "KubernetesCluster"
  }
}

# Create storage account for diagnostics (optional)
resource "azurerm_storage_account" "diagnostics" {
  name                     = "${replace(var.vm_name, "-", "")}diag${random_string.storage_suffix.result}"
  resource_group_name      = data.azurerm_resource_group.main.name
  location                 = data.azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Environment = "Development"
    Project     = "KubernetesChaosInfra"
  }
}

# Random string for storage account name
resource "random_string" "storage_suffix" {
  length  = 6
  special = false
  upper   = false
}
