# Chaos Engineering Environment Setup

This repository contains Ansible playbooks to set up a complete chaos engineering environment on an Azure Ubuntu VM with Kubernetes (Minikube), LitmusChaos, Prometheus, Grafana, Loki, and AlertManager.

## Prerequisites

1. **Azure VM**: Ubuntu 20.04 or later with at least 8GB RAM and 4 vCPUs
2. **Ansible**: Installed on your local machine
3. **SSH Access**: SSH key-based access to the Azure VM
4. **Required Ansible Collections**:
   ```bash
   ansible-galaxy collection install kubernetes.core
   ansible-galaxy collection install community.kubernetes
   ```

## Quick Setup

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd litmus-chaos-test
   ```

2. **Update inventory file**:
   Edit `inventory.ini` and replace `your-azure-vm-ip` with your actual Azure VM IP address.

3. **Install required Ansible collections**:
   ```bash
   ansible-galaxy collection install kubernetes.core
   ansible-galaxy collection install community.kubernetes
   pip3 install kubernetes pyyaml
   ```

4. **Run the playbook**:
   ```bash
   ansible-playbook -i inventory.ini ansible-playbook.yml
   ```

## What Gets Installed

### Core Infrastructure
- **Docker**: Container runtime
- **Minikube**: Local Kubernetes cluster
- **kubectl**: Kubernetes CLI tool
- **Helm**: Kubernetes package manager

### Monitoring Stack
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation system
- **AlertManager**: Alert routing and management

### Chaos Engineering
- **LitmusChaos**: Chaos engineering platform
- **Sample Applications**: Nginx deployment with 10 replicas for testing

## Service URLs

After successful deployment, services will be available at:

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | `http://<minikube-ip>:30080` | admin/admin123 |
| Prometheus | `http://<minikube-ip>:30090` | - |
| AlertManager | `http://<minikube-ip>:30093` | - |
| Loki | `http://<minikube-ip>:30031` | - |
| Sample Nginx App | `http://<minikube-ip>:30082` | - |
| Litmus Frontend | `http://<minikube-ip>:30091` | - |

To get the Minikube IP, SSH into your VM and run:
```bash
minikube ip
```

## Basic Chaos Engineering Experiments

### 1. Pod Delete Experiment

This experiment randomly deletes pods from the nginx deployment:

```bash
# SSH into your Azure VM
ssh ubuntu@<your-azure-vm-ip>

# Apply the pod delete experiment
kubectl apply -f ~/chaos-experiments/pod-delete-experiment.yaml

# Monitor the experiment
kubectl get chaosengines -n chaos-apps
kubectl describe chaosengine nginx-pod-delete -n chaos-apps

# Watch pods being deleted and recreated
kubectl get pods -n chaos-apps -w
```

### 2. Network Chaos Experiment

This experiment introduces network packet loss:

```bash
# Apply network chaos experiment
kubectl apply -f ~/chaos-experiments/network-chaos-experiment.yaml

# Monitor the experiment
kubectl get chaosengines -n chaos-apps
kubectl describe chaosengine nginx-network-loss -n chaos-apps
```

### 3. Monitoring During Chaos

1. **Access Grafana** at `http://<minikube-ip>:30080`
   - Username: `admin`
   - Password: `admin123`

2. **Import Kubernetes dashboards**:
   - Go to "+" → Import
   - Use dashboard ID: `315` (Kubernetes cluster monitoring)
   - Use dashboard ID: `8588` (Kubernetes Deployment metrics)

3. **Monitor metrics in Prometheus** at `http://<minikube-ip>:30090`
   - Query: `kube_pod_status_phase{namespace="chaos-apps"}`
   - Query: `rate(container_cpu_usage_seconds_total[5m])`

### 4. Creating Custom Chaos Experiments

Create your own chaos experiments using LitmusChaos hub:

```bash
# List available experiments
kubectl get chaosexperiments -n litmus

# Get experiment YAML from LitmusChaos hub
curl -o my-experiment.yaml https://hub.litmuschaos.io/api/chaos/3.0.0?file=charts/generic/node-cpu-hog/experiment.yaml

# Customize and apply
kubectl apply -f my-experiment.yaml -n litmus
```

### 5. Advanced Monitoring Setup

#### Configure Grafana Data Sources

1. **Add Prometheus data source**:
   - URL: `http://prometheus-stack-kube-prom-prometheus:9090`

2. **Add Loki data source**:
   - URL: `http://loki:3100`

#### Set up Alerts in AlertManager

1. Access AlertManager at `http://<minikube-ip>:30093`
2. Configure notification channels (Slack, email, etc.)
3. Create alert rules in Prometheus for chaos experiments

## Useful Commands

### Kubernetes Operations
```bash
# Get all resources in all namespaces
kubectl get all --all-namespaces

# Check cluster status
kubectl cluster-info

# Get detailed pod information
kubectl describe pod <pod-name> -n <namespace>

# View logs
kubectl logs <pod-name> -n <namespace>
```

### Chaos Engineering Commands
```bash
# List all chaos engines
kubectl get chaosengines --all-namespaces

# Get chaos results
kubectl get chaosresults --all-namespaces

# Delete a chaos experiment
kubectl delete chaosengine <engine-name> -n <namespace>
```

### Monitoring Commands
```bash
# Port forward for local access (if needed)
kubectl port-forward -n monitoring service/prometheus-stack-grafana 3000:80
kubectl port-forward -n monitoring service/prometheus-stack-kube-prom-prometheus 9090:9090

# Check metrics server
kubectl top nodes
kubectl top pods --all-namespaces
```

## Troubleshooting

### Common Issues

1. **Minikube won't start**:
   ```bash
   minikube delete
   minikube start --driver=docker --cpus=4 --memory=8192
   ```

2. **Services not accessible**:
   ```bash
   # Check service status
   kubectl get services --all-namespaces
   
   # Check if minikube tunnel is needed
   minikube tunnel
   ```

3. **Pods stuck in pending state**:
   ```bash
   # Check node resources
   kubectl describe nodes
   
   # Check events
   kubectl get events --sort-by='.lastTimestamp'
   ```

4. **Chaos experiments not running**:
   ```bash
   # Check Litmus operator status
   kubectl get pods -n litmus
   
   # Check RBAC permissions
   kubectl describe clusterrolebinding litmus-admin
   ```

## Cleanup

To clean up the environment:

```bash
# Delete chaos experiments
kubectl delete chaosengines --all --all-namespaces

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Security Considerations

- Default passwords are used for demo purposes (Grafana: admin/admin123)
- Change default passwords in production
- Implement proper RBAC for chaos experiments
- Use network policies to isolate namespaces
- Enable audit logging for compliance

## Next Steps

1. **Integrate with CI/CD**: Set up automated chaos testing in your pipeline
2. **Custom Experiments**: Create domain-specific chaos experiments
3. **Advanced Monitoring**: Set up custom metrics and dashboards
4. **Chaos Scheduling**: Use CronChaos for scheduled experiments
5. **Multi-cluster**: Extend to test distributed systems

## Resources

- [LitmusChaos Documentation](https://docs.litmuschaos.io/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Chaos Engineering Principles](https://principlesofchaos.org/)
