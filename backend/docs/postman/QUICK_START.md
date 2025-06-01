# Postman Collection Quick Start Guide

## Overview
This guide provides step-by-step instructions for using the AegisNexus SRE Agent API Postman collection.

## Quick Setup (5 Minutes)

### 1. Import Files into Postman
1. Open Postman desktop app or web version
2. Click **Import** button (top left)
3. Drag and drop these files or click **Upload Files**:
   - `AegisNexus-SRE-API.postman_collection.json`
   - `development.postman_environment.json`
4. Click **Import**

### 2. Select Development Environment
1. In top-right corner, click environment dropdown
2. Select **"AegisNexus SRE Development"**
3. Verify `base_url` shows `http://127.0.0.1:8000`

### 3. Start Local Server
```bash
# In your terminal, navigate to the backend directory
cd /Users/nhz/Documents/code/meta-hacakthon/AegisNexus/backend

# Start the server
uv run uvicorn app.main:app --reload
```

### 4. Test the Connection
1. In Postman, expand **"Health Check"** folder
2. Click **"API Health Check"**
3. Click **Send** button
4. Verify you get a `200 OK` response

## Common API Testing Scenarios

### Scenario 1: Basic Health Check
**Request:** `GET /`
```
Expected Response:
{
  "message": "AegisNexus SRE Agent API is running",
  "status": "healthy",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

### Scenario 2: Ask About CPU Usage
**Request:** `POST /sre/ask`
```json
{
  "question": "What's the current CPU usage?"
}
```
This will trigger Prometheus metrics collection and provide AI analysis.

### Scenario 3: Trigger Incident Response
**Request:** `POST /sre/incident-response`
```json
{
  "alert_name": "HighCPUUsage",
  "severity": "critical"
}
```
This will execute a complete incident response workflow.

### Scenario 4: System Health Report
**Request:** `GET /sre/health`
Returns comprehensive system health including tools status and metrics.

## Folder Structure in Collection

```
📁 Health Check
  ├── API Health Check (GET /)
  ├── System Health Report (GET /sre/health)
  └── SRE Tools Health Check (GET /sre/tools/health)

📁 SRE Questions
  ├── Ask General SRE Question
  ├── Ask About CPU Usage
  ├── Ask About Memory Usage
  ├── Ask About Error Logs
  ├── Ask About Active Alerts
  ├── Ask About Recent Deployments
  └── Ask About System Overview

📁 Incident Response
  ├── Trigger High CPU Incident
  ├── Trigger Critical Memory Alert
  ├── Trigger Disk Space Alert
  ├── Trigger Network Connectivity Issue
  └── Trigger Database Performance Alert

📁 Tools & Demos
  └── Run SRE Tools Demo
```

## Environment Variables Explained

### Development Environment Variables
- `base_url`: `http://127.0.0.1:8000` - Local server URL
- `server_host`: `127.0.0.1` - Localhost
- `server_port`: `8000` - Default FastAPI port
- `protocol`: `http` - No SSL for local development

### How to Switch Environments
1. Click environment dropdown (top-right)
2. Select desired environment:
   - **Development**: Local testing
   - **Staging**: Pre-production testing  
   - **Production**: Live environment

## Testing Tips

### 1. Monitor Response Times
- Each request automatically tests response time < 30 seconds
- Check **Test Results** tab after sending requests

### 2. Check Server Logs
- Watch terminal where you started `uvicorn` for detailed logs
- Look for error messages, stack traces, request details

### 3. Use Pre-request Scripts
- Collection automatically sets timestamps
- Variables are available in `{{variable_name}}` format

### 4. Automated Testing
Each request includes automatic tests for:
- Response format (JSON)
- Status codes (200, 404, 500)
- Response structure validation

## Advanced Usage

### Custom Variables
Add your own environment variables:
1. Click environment name in top-right
2. Click **Edit** (eye icon)
3. Add new variables as needed

### Request Chaining
Use response data in subsequent requests:
```javascript
// In Tests tab of a request
pm.globals.set("incident_id", pm.response.json().response.incident_id);

// In next request, use {{incident_id}}
```

### Bulk Testing
1. Select entire collection or folder
2. Click **Run** button
3. Choose environment and settings
4. Monitor automated test execution

## Troubleshooting

### ❌ "Could not get response" Error
**Solution:** Ensure local server is running
```bash
uv run uvicorn app.main:app --reload
```

### ❌ 404 Not Found
**Solutions:**
- Verify endpoint URL is correct
- Check that environment is set to "Development"
- Ensure `base_url` is `http://127.0.0.1:8000`

### ❌ 500 Internal Server Error
**Solutions:**
- Check server terminal logs for error details
- Verify `.env.local` file has required API keys
- Ensure all dependencies are installed: `uv sync`

### ❌ Connection Timeout
**Solutions:**
- Check if server port 8000 is available
- Try restarting the server
- Verify firewall/antivirus isn't blocking the connection

## API Key Configuration (Future Use)

For staging/production environments:
1. Edit environment variables
2. Add your API keys to:
   - `api_key` (if required)
   - `auth_token` (if required)
3. Requests will automatically use these in headers

## Response Examples

### Successful SRE Question Response
```json
{
  "response": {
    "langgraph": {
      "response": "Based on the Prometheus metrics...",
      "status": "success"
    },
    "llama": {
      "response": "The current CPU usage shows...",
      "status": "success"
    },
    "tools_data": {
      "prometheus_cpu": {
        "status": "success",
        "data": {...}
      }
    },
    "enhanced_context": true
  }
}
```

### Health Check Response
```json
{
  "response": {
    "health_data": {
      "tools_health": {
        "prometheus": "healthy",
        "grafana": "healthy",
        ...
      },
      "current_alerts": [...],
      "service_map": {...}
    },
    "ai_assessment": {
      "assessment": "System is operating normally..."
    },
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## Integration with Development Workflow

### 1. Feature Development
- Test new endpoints immediately after implementation
- Verify request/response formats
- Check error handling

### 2. Debugging
- Use Postman Console (View → Show Postman Console)
- Monitor request/response details
- Copy cURL commands for command-line testing

### 3. Documentation
- Export requests as code examples
- Generate API documentation from collection
- Share collection with team members

## Next Steps

1. ✅ **Complete Basic Setup** - Import collection and test health check
2. ✅ **Test Core Features** - Try SRE questions and incident response
3. ✅ **Explore Advanced Features** - Custom variables, automated testing
4. ✅ **Integrate with Development** - Use during feature development

For additional help, refer to the detailed `README.md` in this directory.
