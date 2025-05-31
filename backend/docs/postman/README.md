# AegisNexus SRE Agent API - Postman Collection

This directory contains Postman collection and environment files for testing the AegisNexus SRE Agent API.

## Files

### Collection
- `AegisNexus-SRE-API.postman_collection.json` - Complete Postman collection with all API endpoints

### Environments
- `development.postman_environment.json` - Local development environment (http://127.0.0.1:8000)
- `staging.postman_environment.json` - Staging environment
- `production.postman_environment.json` - Production environment

## Import Instructions

### 1. Import Collection
1. Open Postman
2. Click **Import** button
3. Drag and drop `AegisNexus-SRE-API.postman_collection.json` or click **Upload Files**
4. Click **Import**

### 2. Import Environment
1. In Postman, click **Import** button
2. Import the desired environment file:
   - `development.postman_environment.json` for local testing
   - `staging.postman_environment.json` for staging
   - `production.postman_environment.json` for production
3. Click **Import**

### 3. Select Environment
1. In the top-right corner of Postman, click the environment dropdown
2. Select the appropriate environment (Development, Staging, or Production)

## API Endpoints

### Health Check Endpoints
- **GET** `/` - Basic API health check
- **GET** `/sre/health` - Comprehensive system health report
- **GET** `/sre/tools/health` - SRE tools health status

### SRE Question Endpoints
- **POST** `/sre/ask` - Ask questions to the SRE agent

### Incident Response Endpoints
- **POST** `/sre/incident-response` - Trigger incident response workflows

### Tools & Demo Endpoints
- **GET** `/sre/tools/demo` - Run SRE tools demonstration

## Sample Requests

### Ask a General SRE Question
```json
POST /sre/ask
{
  "question": "What is Site Reliability Engineering?"
}
```

### Ask About System Metrics
```json
POST /sre/ask
{
  "question": "What's the current CPU usage?"
}
```

### Trigger Incident Response
```json
POST /sre/incident-response
{
  "alert_name": "HighCPUUsage",
  "severity": "critical"
}
```

## Pre-configured Question Types

The collection includes pre-configured requests for common SRE scenarios:

### Monitoring Questions
- CPU usage analysis
- Memory usage trends  
- Error log analysis
- Active alerts status
- Recent deployments
- System overview

### Incident Response Scenarios
- High CPU usage (warning/critical)
- High memory usage (critical)
- Low disk space (critical)
- Network connectivity issues
- Database performance problems

## Environment Variables

### Development Environment
- `base_url`: http://127.0.0.1:8000
- `server_host`: 127.0.0.1
- `server_port`: 8000
- `protocol`: http

### Staging/Production Environments
- `base_url`: Environment-specific URL
- `server_host`: Environment-specific host
- `server_port`: 443 (HTTPS)
- `protocol`: https
- `api_key`: API key (if required)
- `auth_token`: Authentication token (if required)

## Testing Features

### Automated Tests
Each request includes automated tests that verify:
- Response time is reasonable (< 30 seconds)
- Response format is JSON
- Status codes are correct
- Response structure validation

### Pre-request Scripts
- Automatic timestamp generation
- Environment variable validation

## Starting the Local Server

Before testing with the development environment, start the local server:

```bash
# Using uv (recommended)
uv run uvicorn app.main:app --reload

# Or using Python directly
python -m uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000` by default.

## Troubleshooting

### Common Issues

1. **Connection refused**
   - Ensure the local server is running
   - Check the correct port (8000 for development)
   - Verify the environment is set correctly

2. **404 Not Found**
   - Verify the endpoint URL is correct
   - Check that all routes are properly configured in the FastAPI app

3. **500 Internal Server Error**
   - Check server logs for detailed error messages
   - Verify environment variables are properly set (`.env.local` file)
   - Ensure all dependencies are installed

### Server Logs
Monitor server logs for detailed error information:
```bash
# The server logs will show in the terminal where you started uvicorn
# Look for error messages, stack traces, and request details
```

### Environment Variables
Ensure your `.env.local` file contains the required API keys:
```bash
LANGGRAPH_API_URL=your_langgraph_api_url_here
LANGGRAPH_API_KEY=your_langgraph_api_key_here
LLAMA_API_KEY=your_llama_api_key_here
```

## Collection Features

### Organized Structure
- **Health Check**: API and system health endpoints
- **SRE Questions**: Various question types with AI responses
- **Incident Response**: Different incident scenarios
- **Tools & Demos**: SRE tools demonstrations

### Dynamic Variables
- Timestamp generation for unique requests
- Environment-specific URLs and settings
- Configurable timeouts and retry logic

### Response Validation
- Automatic response time checking
- JSON format validation
- Status code verification
- Custom test assertions

## API Response Examples

### Successful SRE Question Response
```json
{
  "response": {
    "langgraph": {
      "response": "LangGraph response about SRE...",
      "status": "success"
    },
    "llama": {
      "response": "Llama API response about SRE...",
      "status": "success"
    },
    "tools_data": {
      "prometheus_cpu": {...},
      "health_status": {...}
    },
    "enhanced_context": true
  }
}
```

### Incident Response Example
```json
{
  "response": {
    "incident_response": {
      "alerts": [...],
      "metrics": {...},
      "logs": {...},
      "traces": {...},
      "notifications": {...}
    },
    "ai_analysis": {
      "analysis": "AI-generated incident analysis..."
    },
    "status": "completed"
  }
}
```

## Contributing

When adding new endpoints:
1. Add the endpoint to the collection
2. Include appropriate request examples
3. Add test assertions
4. Update this documentation
5. Test across all environments

## Support

For issues with the Postman collection or API:
1. Check the troubleshooting section above
2. Review server logs for detailed error information
3. Verify environment configuration
4. Ensure all dependencies are properly installed
