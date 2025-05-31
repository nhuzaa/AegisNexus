# Discord AlertManager Integration Setup Guide

## 🎯 Overview
This guide helps you set up Discord notifications for your chaos engineering alerts from Prometheus AlertManager.

## 📝 Prerequisites
- Discord server where you have admin permissions
- The Ansible playbook ready to deploy

## 🔧 Setup Steps

### 1. Create Discord Webhook

1. **Open Discord** and go to your server
2. **Right-click on the channel** where you want alerts (e.g., #chaos-alerts)
3. **Select "Edit Channel"** → **"Integrations"** → **"Webhooks"**
4. **Click "Create Webhook"**
5. **Customize the webhook**:
   - Name: `Chaos Engineering Alerts`
   - Avatar: Choose an appropriate icon
6. **Copy the webhook URL** (format: `https://discord.com/api/webhooks/ID/TOKEN`)

### 2. Update Ansible Configuration

Edit your `ansible-playbook.yml` and update the Discord webhook URL:

```yaml
vars:
  # ... other vars ...
  discord_webhook_url: "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
```

**Example:**
```yaml
discord_webhook_url: "https://discord.com/api/webhooks/1234567890123456789/AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIjKlMnOpQrSt"
```

### 3. Deploy the Configuration

```bash
# Install required collections first
ansible-galaxy collection install -r requirements.yml
pip3 install -r requirements.txt

# Run the playbook
ansible-playbook -i inventory.ini ansible-playbook.yml
```

### 4. Test Discord Integration

SSH into your VM and test the webhook:

```bash
ssh ubuntu@<your-vm-ip>
./test-discord-alert.sh
```

You should see a test message in your Discord channel.

## 🚨 Alert Types

The setup includes these chaos engineering alerts:

### 🔴 Critical Alerts
- **PodNotReady**: Pods not ready for >5 minutes
- **ChaosExperimentFailed**: Litmus experiments failing

### 🟡 Warning Alerts  
- **PodCrashLooping**: Pods restarting frequently (>0 restarts in 15m)
- **HighCPUUsage**: CPU usage >80% for 2 minutes
- **HighMemoryUsage**: Memory usage >80% for 2 minutes
- **DeploymentReplicasMismatch**: Replica count issues

### 🔵 Info Alerts
- **ChaosExperimentRunning**: New chaos experiments started

## 🧪 Trigger Test Alerts

### 1. Create CPU Stress Alert:
```bash
./chaos-runner-discord.sh run cpu-stress-experiment
```

### 2. Create Pod Delete Alert:
```bash
./chaos-runner-discord.sh run pod-delete-experiment
```

### 3. Monitor Alerts:
```bash
# Check AlertManager web UI
echo "AlertManager: http://$(minikube ip):30093"

# Check active alerts via API
curl -s "http://$(minikube ip):30093/api/v1/alerts" | jq .
```

## 📊 Discord Alert Format

Alerts will appear in Discord with rich embeds containing:

- 🚨 **Alert Title** with emoji indicators
- 📝 **Description** of the issue  
- ⚡ **Severity** level (critical/warning/info)
- 🎯 **Chaos Type** (pod_failure, resource_stress, experiment_status, etc.)
- 🖥️ **Instance** or pod affected
- ⏰ **Timestamps** for start and end times
- 📊 **Status** (firing/resolved)

**Example Alert:**
```
🚨 Chaos Engineering Alert 🚨

🔥 Alert: Pod nginx-deployment-abc123 is crash looping
📝 Description: Pod nginx-deployment-abc123 in namespace chaos-apps is restarting frequently
⚡ Severity: warning
🖥️ Instance: minikube
📊 Status: firing
⏰ Started: 2025-05-31 14:30:15
🎯 Chaos Type: pod_failure
```

## 🔧 Troubleshooting

### Test Webhook Manually:
```bash
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"content": "🧪 Test from chaos engineering!"}' \
     "YOUR_DISCORD_WEBHOOK_URL"
```

### Check AlertManager Config:
```bash
# View AlertManager configuration
kubectl get secret -n monitoring alertmanager-prometheus-stack-kube-prom-alertmanager -o jsonpath='{.data.alertmanager\.yml}' | base64 -d

# Check AlertManager pod logs
kubectl logs -n monitoring -l app.kubernetes.io/name=alertmanager
```

### View Alert Status:
```bash
# Check firing alerts
curl -s "http://$(minikube ip):30093/api/v1/alerts" | jq '.data[] | select(.status.state=="active")'

# Check AlertManager status  
curl -s "http://$(minikube ip):30093/api/v1/status"

# Check Prometheus rules
curl -s "http://$(minikube ip):30090/api/v1/rules" | jq '.data.groups[].rules[] | select(.type=="alerting")'
```

### Common Issues:

1. **Webhook URL Invalid**: Ensure the URL is complete and valid
2. **Network Issues**: Check that the VM can reach Discord (port 443)
3. **YAML Formatting**: Ensure proper YAML indentation in the playbook
4. **AlertManager Not Ready**: Wait for all pods to be running

## 🎯 Advanced Configuration

### Custom Alert Rules:
Add custom rules to the Prometheus configuration in the playbook:

```yaml
- alert: CustomChaosAlert
  expr: your_custom_metric > threshold
  for: 1m
  labels:
    severity: warning
    chaos_type: custom
  annotations:
    summary: "Custom chaos condition detected"
    description: "Your custom description"
```

### Discord Formatting Customization:
Modify the AlertManager webhook configuration to change Discord message format:

```yaml
text: |
  {{ range .Alerts }}
  **🔥 Alert:** {{ .Annotations.summary }}
  **📝 Description:** {{ .Annotations.description }}
  **⚡ Severity:** {{ .Labels.severity }}
  {{ end }}
```

### Multiple Discord Channels:
Create different receivers for different alert types:

```yaml
receivers:
- name: 'discord-critical'
  webhook_configs:
  - url: 'https://discord.com/api/webhooks/CRITICAL_CHANNEL_WEBHOOK'
- name: 'discord-warning'
  webhook_configs:
  - url: 'https://discord.com/api/webhooks/WARNING_CHANNEL_WEBHOOK'
```

## 📈 Monitoring Dashboard

Access Grafana at `http://<minikube-ip>:30080` to view:
- Real-time chaos experiment metrics
- Alert status dashboard
- Resource usage during chaos tests
- Historical experiment data

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

## 🚀 Usage Examples

### Start Chaos with Discord Notifications:
```bash
# List available experiments
./chaos-runner-discord.sh list

# Run pod delete experiment
./chaos-runner-discord.sh run pod-delete-experiment

# Check status
./chaos-runner-discord.sh status

# Stop experiment
./chaos-runner-discord.sh stop pod-delete-experiment
```

### Monitor in Real-time:
```bash
# Watch pods during chaos
kubectl get pods -n chaos-apps -w

# Monitor AlertManager
watch "curl -s http://$(minikube ip):30093/api/v1/alerts | jq '.data | length' && echo ' active alerts'"
```

## 📚 Additional Resources

- [Prometheus AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Discord Webhooks Guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- [LitmusChaos Documentation](https://docs.litmuschaos.io/)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)
