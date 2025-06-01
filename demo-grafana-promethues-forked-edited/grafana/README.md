# Grafana Configuration

## Login Credentials

**Default Admin Account:**
- Username: `admin`
- Password: `admin123`

## Dashboard Overview

This setup includes three pre-configured dashboards:

### 1. Home Dashboard (Default)
- **URL**: http://localhost:3000/d/home/home-dashboard
- **Purpose**: Overview of system health and quick navigation
- **Features**:
  - Service status summary
  - Active alerts count
  - Average CPU usage
  - Response time metrics
  - Quick links to other dashboards

### 2. Application Monitoring Dashboard
- **URL**: http://localhost:3000/d/app_monitoring/application-monitoring-dashboard
- **Purpose**: Detailed application performance metrics
- **Features**:
  - CPU usage over time
  - Memory usage trends
  - K6 HTTP request rates
  - Response time percentiles
  - HTTP status code distribution
  - Service health status

### 3. Alerts Dashboard
- **URL**: http://localhost:3000/d/alerts_dashboard/alerts-dashboard
- **Purpose**: Alert management and monitoring
- **Features**:
  - Active alerts timeline
  - Alert distribution by type
  - Detailed alert information table

## Data Sources

The following data sources are pre-configured:

- **Prometheus**: Primary metrics source (http://prometheus:9090)
- **Loki**: Log aggregation (http://loki:3100)
- **External Alertmanager**: Alert management (http://alertmanager:9093)
- **Postgres**: Database metrics (postgres:5432)

## Security Notes

⚠️ **Important**: The default credentials are for development/testing only. In production:

1. Change the admin password immediately
2. Set up proper user management
3. Configure HTTPS/TLS
4. Review and update security settings in `grafana.ini`

## Configuration Files

- `grafana/grafana.ini`: Main Grafana configuration
- `grafana/datasources/datasource.yaml`: Data source definitions
- `grafana/dashboards/dashboard.yaml`: Dashboard provisioning config
- `grafana/dashboards/*.json`: Dashboard definitions

## Starting the Stack

```bash
docker-compose up -d
```

Then access Grafana at: http://localhost:3000

## Customization

You can modify the dashboards by:

1. Editing the JSON files in `grafana/dashboards/`
2. Using the Grafana UI (changes will persist in the container)
3. Adding new dashboard JSON files to the dashboards directory

## Troubleshooting

If you encounter issues:

1. Check container logs: `docker-compose logs grafana`
2. Verify data source connectivity in Grafana UI
3. Ensure Prometheus and other services are running
4. Check file permissions on configuration files
