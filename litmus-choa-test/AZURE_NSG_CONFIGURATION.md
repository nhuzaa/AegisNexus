# Azure Network Security Group Configuration for Chaos Engineering

This document provides the necessary Azure Network Security Group (NSG) rules to expose the chaos engineering services to external access.

## Required Inbound Security Rules

Configure the following inbound security rules in your Azure NSG to allow external access to all services:

### Rule 1: SSH Access
- **Name**: SSH
- **Priority**: 100
- **Source**: IP Addresses (your IP or 0.0.0.0/0 for any - not recommended for production)
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 22
- **Protocol**: TCP
- **Action**: Allow

### Rule 2: HTTP Web Traffic
- **Name**: HTTP
- **Priority**: 110
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 80
- **Protocol**: TCP
- **Action**: Allow

### Rule 3: Grafana Dashboard
- **Name**: Grafana
- **Priority**: 120
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 3000
- **Protocol**: TCP
- **Action**: Allow

### Rule 4: Loki Logs
- **Name**: Loki
- **Priority**: 130
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 3100
- **Protocol**: TCP
- **Action**: Allow

### Rule 5: Kubernetes API
- **Name**: Kubernetes-API
- **Priority**: 140
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 8443
- **Protocol**: TCP
- **Action**: Allow

### Rule 6: Prometheus Metrics
- **Name**: Prometheus
- **Priority**: 150
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 9090
- **Protocol**: TCP
- **Action**: Allow

### Rule 7: Litmus Chaos Portal
- **Name**: Litmus
- **Priority**: 160
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 9091
- **Protocol**: TCP
- **Action**: Allow

### Rule 8: AlertManager
- **Name**: AlertManager
- **Priority**: 170
- **Source**: Any
- **Source Port**: *
- **Destination**: Any
- **Destination Port**: 9093
- **Protocol**: TCP
- **Action**: Allow

## Azure CLI Commands

You can configure these rules using Azure CLI:

```bash
# Set variables
RESOURCE_GROUP="your-resource-group"
NSG_NAME="your-nsg-name"

# SSH Access
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name SSH \
  --priority 100 \
  --destination-port-ranges 22 \
  --access Allow \
  --protocol Tcp

# HTTP Web Traffic
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name HTTP \
  --priority 110 \
  --destination-port-ranges 80 \
  --access Allow \
  --protocol Tcp

# Grafana Dashboard
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name Grafana \
  --priority 120 \
  --destination-port-ranges 3000 \
  --access Allow \
  --protocol Tcp

# Loki Logs
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name Loki \
  --priority 130 \
  --destination-port-ranges 3100 \
  --access Allow \
  --protocol Tcp

# Kubernetes API
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name Kubernetes-API \
  --priority 140 \
  --destination-port-ranges 8443 \
  --access Allow \
  --protocol Tcp

# Prometheus Metrics
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name Prometheus \
  --priority 150 \
  --destination-port-ranges 9090 \
  --access Allow \
  --protocol Tcp

# Litmus Chaos Portal
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name Litmus \
  --priority 160 \
  --destination-port-ranges 9091 \
  --access Allow \
  --protocol Tcp

# AlertManager
az network nsg rule create \
  --resource-group $RESOURCE_GROUP \
  --nsg-name $NSG_NAME \
  --name AlertManager \
  --priority 170 \
  --destination-port-ranges 9093 \
  --access Allow \
  --protocol Tcp
```

## PowerShell Commands

Alternatively, you can use PowerShell:

```powershell
# Set variables
$ResourceGroupName = "your-resource-group"
$NetworkSecurityGroupName = "your-nsg-name"

# SSH Access
New-AzNetworkSecurityRuleConfig -Name "SSH" -Priority 100 -Access Allow -Protocol Tcp -Direction Inbound -SourcePortRange * -SourceAddressPrefix * -DestinationPortRange 22 -DestinationAddressPrefix *

# HTTP Web Traffic
New-AzNetworkSecurityRuleConfig -Name "HTTP" -Priority 110 -Access Allow -Protocol Tcp -Direction Inbound -SourcePortRange * -SourceAddressPrefix * -DestinationPortRange 80 -DestinationAddressPrefix *

# Continue with other rules...
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Restrict Source IPs**: For production environments, replace `Any` with specific IP addresses or CIDR blocks that need access.

2. **Use HTTPS**: Consider setting up SSL/TLS certificates for production use.

3. **Authentication**: Ensure all services have proper authentication configured.

4. **Monitoring**: Monitor access logs for suspicious activity.

5. **Least Privilege**: Only open ports that are actually needed for your use case.

## Verification

After configuring the NSG rules:

1. Run the status check script: `./quick-status.sh`
2. Run the verification script: `./verify-external-access.sh`
3. Access the services using your Azure VM's public IP address

## Troubleshooting

If services are not accessible:

1. Check NSG rules are applied to the correct subnet/NIC
2. Verify the VM's local firewall (UFW) allows the traffic
3. Check if services are running: `kubectl get services --all-namespaces`
4. Verify LoadBalancer services have external IPs assigned
5. Test from inside the VM first: `curl localhost:3000`
