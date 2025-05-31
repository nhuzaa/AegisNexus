# Kubernetes Connectivity Fixes

## Issue Addressed
The Ansible playbook was failing with "connection refused to 10.0.0.4:8443" when trying to create namespaces. This was happening because kubectl couldn't connect to the Kubernetes API server.

## Root Cause
1. Minikube startup was not properly waiting for full readiness
2. kubectl connectivity was not verified before proceeding with Kubernetes operations
3. Duplicate configuration blocks were causing YAML structure issues

## Fixes Applied

### 1. Improved Minikube Startup Process
- **Separated Minikube start from addon installation** to ensure proper initialization sequence
- **Added comprehensive readiness check** with 300-second timeout that verifies both:
  - Minikube status shows "Running"
  - kubectl can successfully connect to the cluster
- **Removed problematic kubectl server configuration** that was trying to bind to incorrect IP

### 2. Enhanced Connectivity Verification
```yaml
- name: Wait for Minikube to be ready and verify kubectl connectivity
  become_user: "{{ ubuntu_user }}"
  shell: |
    echo "Waiting for Minikube to be fully ready..."
    timeout=300
    elapsed=0
    
    while [ $elapsed -lt $timeout ]; do
      echo "Checking Minikube status... ($elapsed/$timeout seconds)"
      
      # Check if Minikube is running
      if minikube status | grep -q "Running"; then
        echo "Minikube is running, testing kubectl connectivity..."
        
        # Test kubectl connectivity
        if kubectl cluster-info >/dev/null 2>&1; then
          echo "✅ Minikube is ready and kubectl is connected!"
          exit 0
        else
          echo "Minikube running but kubectl not connected yet..."
        fi
      else
        echo "Minikube not yet running..."
      fi
      
      sleep 10
      elapsed=$((elapsed + 10))
    done
    
    echo "❌ Timeout waiting for Minikube to be ready"
    echo "Minikube status:"
    minikube status || true
    echo "kubectl cluster-info:"
    kubectl cluster-info || true
    exit 1
```

### 3. Fixed Configuration Issues
- **Removed duplicate Prometheus Stack installation task** that was causing confusion
- **Fixed incomplete AlertManager configuration** by removing partial/broken blocks
- **Standardized service exposure** using LoadBalancer with proper external IP binding

### 4. Better Error Handling
- Added timeout handling with clear error messages
- Included diagnostic output when failures occur
- Step-by-step verification before proceeding to namespace creation

## Expected Results
After these fixes:
1. Minikube will start properly and wait for full readiness
2. kubectl connectivity will be verified before any Kubernetes operations
3. Namespace creation should succeed without connection errors
4. All services will be properly exposed for external access

## Testing the Fix
Run the playbook with these improvements:
```bash
ansible-playbook -i inventory.ini ansible-playbook.yml
```

The playbook should now successfully:
1. Start Minikube without connectivity issues
2. Create all required namespaces
3. Install Prometheus, Grafana, Loki, and LitmusChaos
4. Expose all services for external access
5. Set up Discord integration for alerts

## Next Steps
1. Test the fixed playbook on your Azure VM
2. Verify external access to all services
3. Configure Azure NSG rules for the required ports
4. Test chaos experiments and Discord notifications
