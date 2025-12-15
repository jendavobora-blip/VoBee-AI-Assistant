# VoBee AI Assistant - QA Testing Framework

## Overview

Comprehensive Quality Assurance (QA) testing framework for the VoBee AI Assistant system. This framework is designed to perform extensive testing including stress testing (up to 50,000 operations), functional testing, load testing, and edge case testing to ensure system robustness, stability, and scalability.

## Features

### 🔥 Stress Testing
- **Up to 50,000 operations**: Simulates extreme load conditions
- **Concurrent request handling**: Tests system behavior under high concurrency
- **Resource monitoring**: Tracks CPU, memory usage during tests
- **Sustained load testing**: 5-minute continuous high-load scenarios
- **Burst traffic patterns**: Tests resilience to sudden traffic spikes

### ✅ Functional Testing
- **API Gateway validation**: Health checks, status, metrics endpoints
- **Image Generation**: Tests various prompts, styles, and parameters
- **Video Generation**: Validates video creation workflows
- **Crypto Prediction**: Tests price predictions and sentiment analysis
- **Orchestrator**: Validates task orchestration and workflow management
- **Fraud Detection**: Tests transaction analysis capabilities
- **End-to-end workflows**: Complete user journey testing

### 📊 Load Testing
- **Concurrent users**: Tests up to 1000+ simultaneous users
- **Response time analysis**: Measures latency under various loads
- **Ramp-up scenarios**: Gradual load increase (100-1000 users)
- **Sustained high load**: 2-minute continuous load tests
- **Peak capacity testing**: Identifies maximum system capacity
- **Response time distribution**: Analyzes consistency and percentiles

### 🎯 Edge Case Testing
- **Invalid inputs**: Malformed JSON, missing fields, type mismatches
- **Security**: SQL injection, XSS, path traversal attempts
- **Resource limits**: Memory leak detection, connection cycling
- **Timeout handling**: Graceful timeout and recovery
- **Boundary values**: Zero, negative, extremely large values
- **System resilience**: Recovery after failures, cascading timeouts

## Installation

1. Navigate to the tests directory:
```bash
cd tests
```

2. Install test dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run quick validation tests (recommended first):
```bash
python run_tests.py quick
```

### Run All Tests
```bash
python run_tests.py all
```

### Run Specific Test Categories

**Stress Testing (50,000 operations):**
```bash
python run_tests.py stress --iterations 50000
```

**Functional Testing:**
```bash
python run_tests.py functional
```

**Load Testing:**
```bash
python run_tests.py load --users 1000
```

**Edge Case Testing:**
```bash
python run_tests.py edge_cases
```

### Advanced Options

**Verbose output with coverage:**
```bash
python run_tests.py functional --verbose
```

**Custom stress test iterations:**
```bash
python run_tests.py stress --iterations 100000
```

**Custom concurrent users:**
```bash
python run_tests.py load --users 2000
```

**Parallel execution:**
```bash
python run_tests.py all --workers 8
```

**List available test categories:**
```bash
python run_tests.py --list
```

## Test Categories

### 1. Stress Testing (`tests/stress/`)
- `test_api_gateway_health_stress`: 50,000 health check requests
- `test_orchestrator_stress`: 10,000 orchestration requests
- `test_varied_workload_stress`: 20,000 mixed request types
- `test_sustained_load_stress`: 5-minute continuous load
- `test_burst_traffic_stress`: 10 bursts × 1000 requests
- `test_quick_stress_validation`: Quick 1000-request smoke test

### 2. Functional Testing (`tests/functional/`)
- API Gateway: Health, status, metrics endpoints
- Image Generation: Various prompts, styles, parameters
- Video Generation: Basic and advanced scenarios
- Crypto Prediction: Multiple symbols, timeframes
- Sentiment Analysis: Cryptocurrency sentiment
- Orchestrator: Single/multiple task workflows, priorities
- Fraud Detection: Transaction analysis
- End-to-end: Complete workflow validation

### 3. Load Testing (`tests/load/`)
- `test_concurrent_users_load`: 1000 simultaneous users
- `test_ramp_up_load`: Gradual increase 100-1000 users
- `test_sustained_high_load`: 2-minute continuous load
- `test_peak_load_capacity`: Maximum capacity identification
- `test_mixed_endpoint_load`: Load across multiple endpoints
- `test_response_time_distribution`: Latency analysis

### 4. Edge Cases (`tests/edge_cases/`)
- Invalid endpoints and malformed payloads
- Oversized requests and special characters
- Security injection attempts (XSS, SQL, path traversal)
- Memory leak detection
- Timeout handling
- Service communication failures
- Data validation edge cases
- System resilience and recovery

## Configuration

### Environment Variables

Configure tests via environment variables:

```bash
# API endpoints
export API_GATEWAY_URL="http://localhost:8000"
export IMAGE_SERVICE_URL="http://localhost:5000"
export VIDEO_SERVICE_URL="http://localhost:5001"
export CRYPTO_SERVICE_URL="http://localhost:5002"
export ORCHESTRATOR_URL="http://localhost:5003"
export FRAUD_SERVICE_URL="http://localhost:5004"

# Test parameters
export STRESS_TEST_ITERATIONS=50000
export LOAD_TEST_USERS=1000
```

### Test Configuration File

Edit `conftest.py` to modify default test settings:
- Timeouts
- Retry policies
- Test data generators
- Resource thresholds

## Test Results

### HTML Reports

After each test run, HTML reports are generated in `tests/results/`:
- `report_<category>_<timestamp>.html`: Test execution report
- `coverage_<timestamp>/`: Code coverage report (with --verbose)

### Console Output

Tests provide real-time console output with:
- ✓ Passed tests with metrics
- ✗ Failed tests with error details
- Test summaries with performance metrics
- Resource usage statistics

### Example Output

```
================================================================================
TEST SUMMARY: API Gateway Health Stress Test (50,000 requests)
================================================================================

Request Statistics:
  Total Requests:       50000
  Successful:           49856
  Failed:               144
  Success Rate:         99.71%
  Total Time:           45.23s
  Requests/Second:      1105.18

Response Times (seconds):
  Average:              0.018
  Minimum:              0.005
  Maximum:              2.341
  Median:               0.015
  95th Percentile:      0.045
  99th Percentile:      0.089

Resource Usage:
  CPU Average:          45.23%
  CPU Peak:             78.45%
  Memory Average:       34.12%
  Memory Peak:          42.78%
================================================================================
```

## Prerequisites

### Running Services

Ensure the following services are running before testing:

**Docker Compose (Development):**
```bash
docker-compose up -d
```

**Kubernetes (Production):**
```bash
kubectl get pods -n ai-orchestration
```

### Service Health Check

Verify services are accessible:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/status
```

## Best Practices

### 1. Start with Quick Tests
Always run quick validation first:
```bash
python run_tests.py quick
```

### 2. Incremental Testing
Run tests in order of complexity:
1. Functional tests (basic validation)
2. Load tests (performance baseline)
3. Edge cases (robustness)
4. Stress tests (extreme conditions)

### 3. Resource Monitoring
Monitor system resources during tests:
```bash
# CPU and memory
top

# Docker containers
docker stats

# Kubernetes pods
kubectl top pods -n ai-orchestration
```

### 4. Baseline Establishment
Run tests multiple times to establish performance baselines.

### 5. Isolated Testing
Test one category at a time for accurate results.

## Troubleshooting

### Service Unavailable Errors

**Problem**: Tests fail with connection errors

**Solution**:
1. Verify services are running
2. Check service URLs in environment variables
3. Ensure network connectivity
4. Review service logs

### Timeout Errors

**Problem**: Tests timeout frequently

**Solution**:
1. Increase timeout values in `conftest.py`
2. Check service performance
3. Reduce concurrent request limits
4. Verify system resources

### Memory Issues

**Problem**: Out of memory during stress tests

**Solution**:
1. Reduce test iterations
2. Decrease concurrent workers
3. Increase system memory
4. Enable memory monitoring

### Failed Assertions

**Problem**: Tests fail assertion checks

**Solution**:
1. Review test output for details
2. Check service logs
3. Verify test data validity
4. Adjust assertion thresholds if needed

## CI/CD Integration

### GitHub Actions

Add to `.github/workflows/qa-tests.yml`:

```yaml
name: QA Tests

on: [push, pull_request]

jobs:
  qa-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd tests
          pip install -r requirements.txt
      
      - name: Start services
        run: docker-compose up -d
      
      - name: Wait for services
        run: sleep 30
      
      - name: Run QA tests
        run: |
          cd tests
          python run_tests.py quick
          python run_tests.py functional
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: tests/results/
```

## Performance Benchmarks

### Expected Performance Metrics

**API Gateway Health Endpoint:**
- Success Rate: > 99%
- Average Response Time: < 50ms
- P95 Response Time: < 100ms
- Throughput: > 1000 req/s

**Crypto Prediction:**
- Success Rate: > 95%
- Average Response Time: < 500ms
- P95 Response Time: < 1000ms

**Orchestration:**
- Success Rate: > 90%
- Average Response Time: < 2000ms
- Task Completion: > 95%

## Contributing

### Adding New Tests

1. Create test file in appropriate category directory
2. Follow existing test patterns
3. Use provided utilities from `utils/test_utils.py`
4. Add comprehensive docstrings
5. Update this README with new tests

### Test Structure

```python
import pytest
from utils.test_utils import make_request, TestMetrics

@pytest.mark.asyncio
async def test_new_feature(test_config):
    """Test description"""
    # Test implementation
    pass
```

## Support

For issues or questions:
1. Check troubleshooting section
2. Review test output and logs
3. Consult main project documentation
4. Open an issue on GitHub

## License

MIT License - Same as main project
