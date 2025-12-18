# VOBee Testing Framework - Quick Reference

This guide provides quick access to testing commands and common scenarios.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start services (if not already running)
docker compose up -d

# 3. Wait for services to be ready
sleep 30

# 4. Run quick smoke test
python tests/run_all_tests.py quick
```

## 📋 Test Commands

### Quick Tests

```bash
# Quick smoke test (30 seconds) - Check if services are healthy
python tests/run_all_tests.py quick

# Alternative: Use the interactive quickstart script
./tests/quickstart.sh
```

### Individual Test Suites

```bash
# Functional tests - Test all service endpoints
python tests/run_all_tests.py functional

# Load test - 300 concurrent users for 5 minutes
python tests/run_all_tests.py load

# Stress test - 5000 operations across services
python tests/run_all_tests.py stress

# Integration tests - Service communication
python tests/run_all_tests.py integration
```

### Complete Test Suite

```bash
# Run all tests (10-15 minutes)
python tests/run_all_tests.py all

# Run all tests with HTML reports
python tests/run_all_tests.py all --report
```

### Run Individual Test Files

```bash
# Functional tests only
python tests/functional_testing/test_all_services.py

# Load tests only
python tests/load_testing/test_300_users.py

# Stress tests only
python tests/stress_testing/test_5k_operations.py

# Integration tests only
python tests/integration_testing/test_service_communication.py
```

## 📊 Test Results

All test results are saved to `test_results/`:

```
test_results/
├── functional_test_report.html      # Service endpoint validation
├── load_test_report.html            # Performance metrics and charts  
├── stress_test_report.html          # Operation statistics
├── integration_test_report.html     # Service communication results
├── functional_test_results.json     # Raw functional data
├── load_test_results.json           # Raw load data
├── stress_test_results.json         # Raw stress data
├── integration_test_results.json    # Raw integration data
└── summary.json                     # Overall summary
```

### View Reports

```bash
# Open HTML reports in browser
open test_results/*.html

# Or individually
open test_results/functional_test_report.html
open test_results/load_test_report.html
open test_results/stress_test_report.html
open test_results/integration_test_report.html

# View JSON summary
cat test_results/summary.json | python -m json.tool
```

## ✅ Success Criteria

Tests pass when they meet these criteria:

| Metric | Requirement |
|--------|-------------|
| Error Rate | < 5% |
| Success Rate | > 95% |
| P95 Response Time | < 3 seconds |
| P99 Response Time | < 5 seconds |
| Service Crashes | 0 |
| Functional Tests | 100% pass |
| Integration Tests | 100% pass |

## 🎯 Common Scenarios

### Scenario 1: Pre-Deployment Validation

```bash
# Before deploying, run complete test suite
python tests/run_all_tests.py all --report

# Check results
cat test_results/summary.json
```

### Scenario 2: Quick Health Check

```bash
# Fast check if all services are running
python tests/run_all_tests.py quick
```

### Scenario 3: Performance Validation

```bash
# Test system under load
python tests/run_all_tests.py load

# Check response times in report
open test_results/load_test_report.html
```

### Scenario 4: Stress Testing

```bash
# Test system resilience
python tests/run_all_tests.py stress

# Review failure rates
cat test_results/stress_test_results.json
```

### Scenario 5: Service Integration Check

```bash
# Verify services communicate properly
python tests/run_all_tests.py integration
```

## 🔧 Configuration

Edit `tests/config.py` to customize:

```python
# Service endpoints
SERVICES = {
    'supreme_brain': 'http://localhost:5010',
    'agent_ecosystem': 'http://localhost:5011',
    # ... other services
}

# Load test settings
LOAD_TEST_CONFIG = {
    'max_users': 300,                    # Max concurrent users
    'ramp_up_steps': [100, 200, 300],    # Gradual ramp-up
    'sustained_duration_seconds': 300,   # 5 minutes
}

# Stress test settings
STRESS_TEST_CONFIG = {
    'total_operations': 5000,            # Total operations
    'concurrent_workers': 50,            # Concurrent workers
}
```

## 🐛 Troubleshooting

### Services Not Running

**Problem**: `Service not reachable (connection refused)`

**Solution**:
```bash
# Check services
docker compose ps

# Start services
docker compose up -d

# Wait for services to be ready
sleep 30

# Try again
python tests/run_all_tests.py quick
```

### Timeout Errors

**Problem**: `Health check timed out`

**Solution**:
```bash
# Check service logs
docker compose logs supreme-brain
docker compose logs agent-ecosystem

# Increase timeout in config.py
TIMEOUT_SETTINGS = {
    'health_check': 10,  # Increased from 5
}
```

### High Error Rates

**Problem**: Error rate > 5%

**Solution**:
1. Check service logs for errors
2. Verify system resources (CPU, memory)
3. Reduce concurrent load
4. Check network connectivity

```bash
# Check system resources
docker stats

# Check individual service
docker compose logs -f <service-name>
```

### Memory Issues

**Problem**: Tests fail with memory errors

**Solution**:
```bash
# Check system memory
free -h

# Reduce concurrent workers in config.py
STRESS_TEST_CONFIG = {
    'concurrent_workers': 25  # Reduced from 50
}
```

## 📈 Performance Benchmarks

Expected performance on standard hardware:

| Test Type | Duration | Operations | Expected Result |
|-----------|----------|------------|-----------------|
| Quick | 30s | ~100 | All services healthy |
| Functional | 1-2 min | ~24 tests | 100% pass |
| Load | 5-7 min | ~10,000+ requests | <5% errors, P95 <3s |
| Stress | 2-5 min | 5,000 ops | >95% success |
| Integration | 30-60s | 5 workflows | 100% pass |
| All | 10-15 min | Combined | All criteria met |

## 🔗 Additional Resources

- **[Detailed Testing Guide](tests/README.md)** - Complete documentation
- **[Configuration File](tests/config.py)** - Test settings
- **[Main README](README-new.md)** - Project overview

## 💡 Tips

1. **Start Small**: Run `quick` before running full test suite
2. **Monitor Resources**: Keep an eye on CPU/memory during load tests
3. **Sequential Testing**: Run functional → integration → load → stress
4. **Save Reports**: Keep HTML reports for historical comparison
5. **Clean State**: Restart services between major test runs if needed

## 🎓 Example Workflow

```bash
# 1. Ensure services are running
docker compose up -d
sleep 30

# 2. Quick health check
python tests/run_all_tests.py quick

# 3. If healthy, run functional tests
python tests/run_all_tests.py functional

# 4. If functional tests pass, run integration
python tests/run_all_tests.py integration

# 5. If integration passes, run performance tests
python tests/run_all_tests.py load
python tests/run_all_tests.py stress

# 6. Review reports
open test_results/load_test_report.html
open test_results/stress_test_report.html

# 7. Check summary
cat test_results/summary.json | python -m json.tool
```

---

**For detailed documentation, see [tests/README.md](tests/README.md)**
