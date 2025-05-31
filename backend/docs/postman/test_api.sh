#!/bin/bash

# API Test Runner for AegisNexus SRE Agent
# This script tests all API endpoints to ensure they're working correctly

set -e  # Exit on any error

# Configuration
BASE_URL="http://127.0.0.1:8000"
TEST_OUTPUT_DIR="docs/postman/test_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create test results directory
mkdir -p "$TEST_OUTPUT_DIR"

echo -e "${BLUE}🚀 AegisNexus SRE Agent API Test Runner${NC}"
echo -e "${BLUE}=====================================${NC}"
echo "Base URL: $BASE_URL"
echo "Timestamp: $TIMESTAMP"
echo ""

# Function to test endpoint
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    local expected_status=${5:-200}
    
    echo -e "${YELLOW}Testing: $description${NC}"
    echo "  $method $endpoint"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$BASE_URL$endpoint" -H "Content-Type: application/json")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
                   -H "Content-Type: application/json" \
                   -d "$data")
    fi
    
    # Extract status code (last line) and body (all but last line)
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$status_code" -eq "$expected_status" ]; then
        echo -e "  ${GREEN}✅ PASS${NC} (Status: $status_code)"
        
        # Save successful response to file
        echo "$body" | jq '.' > "$TEST_OUTPUT_DIR/${endpoint//\//_}_${method,,}_$TIMESTAMP.json" 2>/dev/null || \
        echo "$body" > "$TEST_OUTPUT_DIR/${endpoint//\//_}_${method,,}_$TIMESTAMP.txt"
    else
        echo -e "  ${RED}❌ FAIL${NC} (Expected: $expected_status, Got: $status_code)"
        echo "  Response: $body"
        return 1
    fi
    echo ""
}

# Function to check if server is running
check_server() {
    echo -e "${YELLOW}Checking if server is running...${NC}"
    if curl -s "$BASE_URL" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Server is running${NC}"
    else
        echo -e "${RED}❌ Server is not running at $BASE_URL${NC}"
        echo -e "${YELLOW}Please start the server with: uv run uvicorn app.main:app --reload${NC}"
        exit 1
    fi
    echo ""
}

# Main test execution
main() {
    check_server
    
    local passed=0
    local failed=0
    
    echo -e "${BLUE}Running API Tests...${NC}"
    echo ""
    
    # Health Check Tests
    echo -e "${BLUE}=== Health Check Tests ===${NC}"
    
    if test_endpoint "GET" "/" "" "API Root Health Check"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "GET" "/sre/health" "" "System Health Report"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "GET" "/sre/tools/health" "" "SRE Tools Health Check"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    # SRE Question Tests
    echo -e "${BLUE}=== SRE Question Tests ===${NC}"
    
    if test_endpoint "POST" "/sre/ask" '{"question": "What is Site Reliability Engineering?"}' "General SRE Question"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "POST" "/sre/ask" '{"question": "What is the current CPU usage?"}' "CPU Usage Question"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "POST" "/sre/ask" '{"question": "Show me recent error logs"}' "Error Logs Question"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "POST" "/sre/ask" '{"question": "Are there any active alerts?"}' "Active Alerts Question"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    # Incident Response Tests
    echo -e "${BLUE}=== Incident Response Tests ===${NC}"
    
    if test_endpoint "POST" "/sre/incident-response" '{"alert_name": "HighCPUUsage", "severity": "warning"}' "High CPU Incident (Warning)"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "POST" "/sre/incident-response" '{"alert_name": "HighMemoryUsage", "severity": "critical"}' "High Memory Incident (Critical)"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    # Tools & Demo Tests
    echo -e "${BLUE}=== Tools & Demo Tests ===${NC}"
    
    if test_endpoint "GET" "/sre/tools/demo" "" "SRE Tools Demo"; then
        ((passed++))
    else
        ((failed++))
    fi
    
    # Error Handling Tests
    echo -e "${BLUE}=== Error Handling Tests ===${NC}"
    
    if test_endpoint "POST" "/sre/ask" '{}' "Invalid Request Body (Missing question)" 422; then
        ((passed++))
    else
        ((failed++))
    fi
    
    if test_endpoint "GET" "/nonexistent" "" "Non-existent Endpoint" 404; then
        ((passed++))
    else
        ((failed++))
    fi
    
    # Test Summary
    echo -e "${BLUE}=== Test Summary ===${NC}"
    local total=$((passed + failed))
    echo "Total Tests: $total"
    echo -e "Passed: ${GREEN}$passed${NC}"
    echo -e "Failed: ${RED}$failed${NC}"
    echo "Success Rate: $((passed * 100 / total))%"
    echo ""
    echo "Test results saved to: $TEST_OUTPUT_DIR/"
    
    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}❌ Some tests failed. Check the output above for details.${NC}"
        exit 1
    fi
}

# CLI help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -u, --url URL  Set custom base URL (default: http://127.0.0.1:8000)"
    echo "  -q, --quiet    Suppress detailed output"
    echo ""
    echo "Examples:"
    echo "  $0                           # Run tests against local server"
    echo "  $0 -u https://api.example.com # Run tests against remote server"
    echo ""
    echo "This script tests all AegisNexus SRE Agent API endpoints to ensure"
    echo "they are working correctly. Make sure the server is running before"
    echo "executing the tests."
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -u|--url)
            BASE_URL="$2"
            shift 2
            ;;
        -q|--quiet)
            QUIET=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check dependencies
if ! command -v curl &> /dev/null; then
    echo -e "${RED}❌ curl is required but not installed${NC}"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️ jq is not installed - JSON responses won't be formatted${NC}"
fi

# Run the tests
main
