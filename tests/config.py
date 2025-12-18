"""
Test Configuration for VOBee AI Assistant Testing Framework

Defines service endpoints, test parameters, and success criteria.
"""

# Service endpoints
SERVICES = {
    'supreme_brain': 'http://localhost:5010',
    'agent_ecosystem': 'http://localhost:5011',
    'media_factory': 'http://localhost:5012',
    'marketing_brain': 'http://localhost:5013',
    'tech_scouting': 'http://localhost:5020',
    'hyper_learning': 'http://localhost:5030',
    'simulation': 'http://localhost:5040',
    'cost_guard': 'http://localhost:5050'
}

# Load testing config
LOAD_TEST_CONFIG = {
    'max_users': 300,
    'ramp_up_steps': [100, 200, 300],
    'sustained_duration_seconds': 300,  # 5 minutes
    'timeout_seconds': 30
}

# Stress testing config
STRESS_TEST_CONFIG = {
    'total_operations': 5000,
    'concurrent_workers': 50,
    'timeout_seconds': 60,
    'distribution': {
        'supreme_brain': 1000,
        'agent_ecosystem': 1000,
        'media_factory': 500,
        'marketing_brain': 500,
        'tech_scouting': 500,
        'hyper_learning': 500,
        'simulation': 500,
        'cost_guard': 500
    }
}

# Success criteria
SUCCESS_CRITERIA = {
    'max_error_rate': 0.05,  # 5%
    'min_success_rate': 0.95,  # 95%
    'max_p95_response_time': 3.0,  # 3 seconds
    'max_p99_response_time': 5.0  # 5 seconds
}

# Test timeout settings
TIMEOUT_SETTINGS = {
    'health_check': 5,
    'quick_test': 10,
    'functional_test': 30,
    'integration_test': 60
}

# Report settings
REPORT_SETTINGS = {
    'output_dir': 'test_results',
    'html_reports': True,
    'json_summary': True,
    'console_output': True
}
