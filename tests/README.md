# VOBee AI Assistant - Testing Framework

Comprehensive testing framework for validating VOBee system stability and performance under realistic load conditions.

## Overview

This testing framework provides:

- **Functional Testing**: Validates all service endpoints and basic functionality
- **Load Testing**: Tests system under 300 concurrent users
- **Stress Testing**: Executes 5000 operations across all services
- **Integration Testing**: Validates service-to-service communication
- **Quick Smoke Tests**: Fast health checks (30 seconds)

## Installation

### Prerequisites

- Python 3.8+
- All VOBee services running (see main README)
- Required Python packages

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- pytest>=7.4.0
- pytest-asyncio>=0.21.0
- aiohttp>=3.8.0
- requests>=2.31.0
- psutil>=5.9.0

## Services Tested

The framework tests all 8 core VOBee services:

1. **Supreme Brain** (Port 5010) - Core consciousness
2. **Agent Ecosystem** (Port 5011) - 2000+ AI agents
3. **Media Factory** (Port 5012) - Media generation
4. **Marketing Brain** (Port 5013) - Marketing intelligence
5. **Tech Scouting** (Port 5020) - Technology discovery
6. **Hyper-Learning** (Port 5030) - Knowledge processing
7. **Simulation** (Port 5040) - Parallel testing
8. **Cost Guard** (Port 5050) - Cost optimization

## Usage

### Quick Start

Run a quick smoke test (30 seconds):

```bash
python tests/run_all_tests.py quick
```

### Individual Test Suites

**Functional Tests** - Test all service endpoints:
```bash
python tests/run_all_tests.py functional
```

**Load Tests** - 300 concurrent users for 5 minutes:
```bash
python tests/run_all_tests.py load
```

**Stress Tests** - 5000 operations:
```bash
python tests/run_all_tests.py stress
```

**Integration Tests** - Service communication:
```bash
python tests/run_all_tests.py integration
```

### Run All Tests

Execute complete test suite:
```bash
python tests/run_all_tests.py all
```

With HTML report generation:
```bash
python tests/run_all_tests.py all --report
```

### Run Individual Test Files

You can also run individual test modules directly:

```bash
# Functional tests
python tests/functional_testing/test_all_services.py

# Load tests
python tests/load_testing/test_300_users.py

# Stress tests
python tests/stress_testing/test_5k_operations.py

# Integration tests
python tests/integration_testing/test_service_communication.py
```

## Test Results

### Output Locations

All test results are saved to `test_results/` directory:

```
test_results/
├── functional_test_report.html      # Functional test results
├── load_test_report.html            # Load test charts
├── stress_test_report.html          # Stress test statistics
├── integration_test_report.html     # Integration test results
├── functional_test_results.json     # Raw functional data
├── load_test_results.json           # Raw load data
├── stress_test_results.json         # Raw stress data
├── integration_test_results.json    # Raw integration data
└── summary.json                     # Overall summary
```

### Console Output

Tests provide real-time progress output:

```
======================================================================
  VOBee Functional Testing Suite
======================================================================

Testing supreme_brain...
----------------------------------------------------------------------
  ✓ PASS - health_check: Health check passed (0.012s)
  ✓ PASS - root_endpoint: Root endpoint valid (0.015s)
  ✓ PASS - basic_functionality: Chat endpoint working (0.234s)
  → All tests passed for supreme_brain
...
```

### HTML Reports

HTML reports include:
- Interactive charts and visualizations
- Detailed metrics and statistics
- Pass/fail summaries
- Service-specific breakdowns

View reports by opening HTML files in a browser:
```bash
open test_results/functional_test_report.html
```

## Success Criteria

Tests are considered successful when they meet these criteria:

| Metric | Requirement |
|--------|-------------|
| Error Rate | < 5% |
| Success Rate | > 95% |
| P95 Response Time | < 3 seconds |
| P99 Response Time | < 5 seconds |
| Service Crashes | 0 |
| Functional Tests | 100% pass |
| Integration Tests | 100% pass |

### Load Test Criteria

**300 Concurrent Users Test**:
- Gradual ramp-up: 0 → 100 → 200 → 300 users
- Sustained duration: 5 minutes at 300 users
- Measures: P50, P95, P99 response times
- Throughput: requests/second
- Success/error rates

### Stress Test Criteria

**5000 Operations Test**:
- Distribution across all 8 services
- 50 concurrent workers
- Tracks failures, timeouts, errors
- Monitors CPU and memory usage

## Configuration

Test configuration is in `tests/config.py`:

```python
# Service endpoints
SERVICES = {
    'supreme_brain': 'http://localhost:5010',
    'agent_ecosystem': 'http://localhost:5011',
    # ... other services
}

# Load test settings
LOAD_TEST_CONFIG = {
    'max_users': 300,
    'ramp_up_steps': [100, 200, 300],
    'sustained_duration_seconds': 300,  # 5 minutes
}

# Success criteria
SUCCESS_CRITERIA = {
    'max_error_rate': 0.05,  # 5%
    'min_success_rate': 0.95,  # 95%
    'max_p95_response_time': 3.0,  # 3 seconds
    'max_p99_response_time': 5.0  # 5 seconds
}
```

You can modify these settings to adjust test parameters.

## Troubleshooting

### Common Issues

**1. Services Not Running**

Error: `Service not reachable (connection refused)`

Solution:
```bash
# Check if services are running
docker compose ps

# Start services if needed
docker compose up -d

# Wait for services to be ready
sleep 10
```

**2. Port Conflicts**

Error: `Connection refused on port 5010`

Solution:
```bash
# Check what's using the port
lsof -i :5010

# Update config.py if services are on different ports
```

**3. Timeout Errors**

Error: `Health check timed out`

Solution:
- Increase timeout in `config.py`
- Check service logs: `docker compose logs <service-name>`
- Restart slow services

**4. High Error Rates**

If tests show >5% error rate:
- Check service logs for errors
- Verify system resources (CPU, memory)
- Reduce concurrent load
- Check network connectivity

**5. Memory Issues**

If load/stress tests fail with memory errors:
```bash
# Check system memory
free -h

# Reduce concurrent workers in config.py
STRESS_TEST_CONFIG = {
    'concurrent_workers': 25  # Reduced from 50
}
```

### Debug Mode

Run tests with verbose output:
```bash
python tests/run_all_tests.py functional -v
```

View individual service logs:
```bash
docker compose logs -f supreme-brain
docker compose logs -f agent-ecosystem
```

### Test-Specific Troubleshooting

**Load Tests**:
- Start with smaller user counts (50, 100)
- Reduce sustained duration for quick tests
- Monitor system resources during test

**Stress Tests**:
- Reduce concurrent workers if overwhelming services
- Check for rate limiting or throttling
- Monitor service resource usage

**Integration Tests**:
- Ensure all dependent services are healthy first
- Run functional tests before integration tests
- Check service discovery and networking

## Performance Benchmarks

Expected performance on standard hardware:

| Test Type | Duration | Operations | Expected Result |
|-----------|----------|------------|-----------------|
| Quick | 30s | ~100 | All services healthy |
| Functional | 1-2 min | ~24 tests | 100% pass |
| Load | 5-7 min | ~10,000+ requests | <5% errors, P95 <3s |
| Stress | 2-5 min | 5,000 ops | >95% success |
| Integration | 30-60s | 5 workflows | 100% pass |
| All | 10-15 min | Combined | All criteria met |

## Best Practices

1. **Run Quick Tests First**: Start with `quick` to verify services are healthy
2. **Monitor Resources**: Keep an eye on CPU/memory during load tests
3. **Sequential Testing**: Run functional → integration → load → stress
4. **Clean State**: Restart services between major test runs if needed
5. **Save Reports**: Keep HTML reports for historical comparison
6. **CI Integration**: Integrate quick/functional tests into CI pipeline

## CI/CD Integration

### GitHub Actions Example

```yaml
name: VOBee Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Start services
        run: docker compose up -d
      - name: Wait for services
        run: sleep 30
      - name: Run quick tests
        run: python tests/run_all_tests.py quick
      - name: Run functional tests
        run: python tests/run_all_tests.py functional
```

## Advanced Usage

### Custom Test Scenarios

Create custom test scenarios by modifying test files or creating new ones:

```python
# custom_test.py
from tests.config import SERVICES
import requests

def test_custom_workflow():
    # Your custom test logic
    response = requests.get(f"{SERVICES['supreme_brain']}/health")
    assert response.status_code == 200
```

### Parallel Test Execution

Run multiple test suites in parallel:
```bash
# Terminal 1
python tests/functional_testing/test_all_services.py &

# Terminal 2
python tests/integration_testing/test_service_communication.py &

# Wait for both
wait
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review service logs: `docker compose logs`
3. Check test results in `test_results/`
4. Review `summary.json` for detailed metrics

## License

Part of VOBee AI Assistant project.
