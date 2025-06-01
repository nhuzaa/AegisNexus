variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "test_kube"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "East US 2"
  
  validation {
    condition = contains([
      "East US", "East US 2", "West US", "West US 2", "West US 3",
      "Central US", "North Central US", "South Central US",
      "West Central US", "Canada Central", "Canada East",
      "North Europe", "West Europe", "UK South", "UK West",
      "France Central", "Germany West Central", "Switzerland North",
      "Norway East", "Sweden Central"
    ], var.location)
    error_message = "The location must be a valid Azure region."
  }
}

variable "vm_name" {
  description = "Name of the virtual machine"
  type        = string
  default     = "kubetester"
  
  validation {
    condition     = length(var.vm_name) >= 1 && length(var.vm_name) <= 64
    error_message = "VM name must be between 1 and 64 characters."
  }
}

variable "vm_size" {
  description = "Size of the virtual machine"
  type        = string
  default     = "Standard_D4s_v3"
  
  validation {
    condition = contains([
      "Standard_B2s", "Standard_B2ms", "Standard_B4ms",
      "Standard_D2s_v3", "Standard_D4s_v3", "Standard_D8s_v3",
      "Standard_DS2_v2", "Standard_DS3_v2", "Standard_DS4_v2",
      "Standard_E2s_v3", "Standard_E4s_v3", "Standard_E8s_v3"
    ], var.vm_size)
    error_message = "VM size must be a valid Azure VM size suitable for Kubernetes workloads."
  }
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
  
  validation {
    condition     = length(var.admin_username) >= 1 && length(var.admin_username) <= 32
    error_message = "Admin username must be between 1 and 32 characters."
  }
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key file"
  type        = string
  default     = "/Users/nhz/Documents/code/meta-hacakthon/keys/kubetestkey.pub"
  
  validation {
    condition     = can(regex(".*\\.pub$", var.ssh_public_key_path))
    error_message = "SSH public key path should end with .pub extension."
  }
}

variable "disk_size_gb" {
  description = "Size of the OS disk in GB"
  type        = number
  default     = 128
  
  validation {
    condition     = var.disk_size_gb >= 30 && var.disk_size_gb <= 2048
    error_message = "Disk size must be between 30 and 2048 GB."
  }
}

variable "allowed_source_ips" {
  description = "List of IP addresses allowed to access the VM (empty list means allow all)"
  type        = list(string)
  default     = []
  
  validation {
    condition = alltrue([
      for ip in var.allowed_source_ips : can(regex("^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}(?:/[0-9]{1,2})?$", ip))
    ])
    error_message = "All IP addresses must be in valid CIDR format (e.g., 192.168.1.1/32 or 10.0.0.0/24)."
  }
}

variable "environment" {
  description = "Environment name for tagging"
  type        = string
  default     = "development"
  
  validation {
    condition = contains([
      "development", "staging", "production", "test"
    ], var.environment)
    error_message = "Environment must be one of: development, staging, production, test."
  }
}

variable "enable_accelerated_networking" {
  description = "Enable accelerated networking for better performance"
  type        = bool
  default     = true
}

variable "enable_boot_diagnostics" {
  description = "Enable boot diagnostics for troubleshooting"
  type        = bool
  default     = true
}

variable "use_existing_resource_group" {
  description = "Whether to use an existing resource group instead of creating a new one"
  type        = bool
  default     = true
}
