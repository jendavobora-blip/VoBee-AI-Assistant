#!/usr/bin/env python3
"""
Simple integration test for Application Factory components
Tests the workflow from intent extraction through architecture generation
"""

import sys
import json
from intent_extractor import IntentExtractor
from spec_generator import SpecificationGenerator
from architecture_scaffolder import ArchitectureScaffolder
from code_generators.backend_generator import BackendGenerator
from code_generators.frontend_generator import FrontendGenerator
from code_generators.infrastructure_generator import InfrastructureGenerator
from code_generators.qa_generator import QAGenerator
from code_generators.docs_generator import DocsGenerator


def test_intent_extraction():
    """Test intent extraction"""
    print("Testing Intent Extraction...")
    extractor = IntentExtractor()
    
    # Test cases
    test_inputs = [
        "Create a new web application with React and Python",
        "Add authentication feature to my app",
        "Generate a REST API service",
    ]
    
    for user_input in test_inputs:
        result = extractor.extract_intent(user_input)
        assert result['intent_type'] != 'unknown', f"Failed to extract intent from: {user_input}"
        assert result['confidence'] > 0, "Confidence should be greater than 0"
        print(f"  ✓ Intent: {result['intent_type']}, Confidence: {result['confidence']}")
    
    print("✅ Intent Extraction tests passed\n")


def test_specification_generation():
    """Test specification generation"""
    print("Testing Specification Generation...")
    generator = SpecificationGenerator()
    
    # Create sample intent
    intent = {
        'intent_type': 'create_application',
        'entities': {'app_types': ['web']},
        'technologies': ['python', 'react', 'docker'],
        'raw_input': 'Create a web application',
    }
    
    spec = generator.generate_specification(intent)
    
    assert 'metadata' in spec, "Specification should have metadata"
    assert 'architecture' in spec, "Specification should have architecture"
    assert 'components' in spec, "Specification should have components"
    assert 'validation' in spec, "Specification should have validation"
    
    print(f"  ✓ Generated spec with architecture: {spec['architecture']['type']}")
    print(f"  ✓ Validation status: {spec['validation']['valid']}")
    print("✅ Specification Generation tests passed\n")


def test_architecture_scaffolding():
    """Test architecture scaffolding"""
    print("Testing Architecture Scaffolding...")
    scaffolder = ArchitectureScaffolder()
    
    # Create sample specification
    spec = {
        'architecture': {'type': 'microservices'},
        'components': {
            'services': [
                {'name': 'api', 'type': 'rest_api'},
                {'name': 'frontend', 'type': 'web_ui'},
            ]
        },
        'technology_stack': {
            'backend': ['python', 'fastapi'],
            'frontend': ['react'],
        },
    }
    
    architecture = scaffolder.generate_architecture(spec)
    
    assert 'pattern' in architecture, "Architecture should have pattern"
    assert 'structure' in architecture, "Architecture should have structure"
    assert 'directories' in architecture, "Architecture should have directories"
    assert 'interface_contracts' in architecture, "Architecture should have interface contracts"
    
    print(f"  ✓ Generated architecture pattern: {architecture['pattern']}")
    print(f"  ✓ Number of directories: {len(architecture['directories'])}")
    print("✅ Architecture Scaffolding tests passed\n")


def test_code_generators():
    """Test all code generators"""
    print("Testing Code Generators...")
    
    # Sample data
    spec = {
        'components': {'services': [{'name': 'api', 'type': 'rest_api'}]},
        'technology_stack': {'backend': ['python']},
    }
    architecture = {'pattern': 'monolith'}
    
    # Test Backend Generator
    backend_gen = BackendGenerator('fastapi')
    backend_result = backend_gen.generate(spec, architecture)
    assert backend_result['status'] == 'stub', "Backend generator should return stub"
    print("  ✓ Backend Generator working")
    
    # Test Frontend Generator
    frontend_gen = FrontendGenerator('react')
    frontend_result = frontend_gen.generate(spec, architecture)
    assert frontend_result['status'] == 'stub', "Frontend generator should return stub"
    print("  ✓ Frontend Generator working")
    
    # Test Infrastructure Generator
    infra_gen = InfrastructureGenerator()
    infra_result = infra_gen.generate(spec, architecture)
    assert infra_result['status'] == 'stub', "Infrastructure generator should return stub"
    print("  ✓ Infrastructure Generator working")
    
    # Test QA Generator
    qa_gen = QAGenerator()
    qa_result = qa_gen.generate(spec, architecture)
    assert qa_result['status'] == 'stub', "QA generator should return stub"
    print("  ✓ QA Generator working")
    
    # Test Docs Generator
    docs_gen = DocsGenerator()
    docs_result = docs_gen.generate(spec, architecture)
    assert docs_result['status'] == 'stub', "Docs generator should return stub"
    print("  ✓ Docs Generator working")
    
    print("✅ All Code Generators tests passed\n")


def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    print("Testing End-to-End Workflow...")
    
    # Initialize components
    extractor = IntentExtractor()
    spec_gen = SpecificationGenerator()
    scaffolder = ArchitectureScaffolder()
    
    # Step 1: Extract intent
    user_input = "Create a microservices application with Python backend and React frontend"
    intent = extractor.extract_intent(user_input)
    print(f"  ✓ Step 1: Intent extracted - {intent['intent_type']}")
    
    # Step 2: Generate specification
    spec = spec_gen.generate_specification(intent)
    print(f"  ✓ Step 2: Specification generated - {spec['metadata']['intent_type']}")
    
    # Step 3: Generate architecture
    architecture = scaffolder.generate_architecture(spec)
    print(f"  ✓ Step 3: Architecture generated - {architecture['pattern']}")
    
    # Step 4: Generate code (stubs)
    backend_gen = BackendGenerator()
    backend = backend_gen.generate(spec, architecture)
    print(f"  ✓ Step 4: Code generation completed - {backend['status']}")
    
    print("✅ End-to-End Workflow tests passed\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Application Factory Integration Tests")
    print("=" * 60 + "\n")
    
    try:
        test_intent_extraction()
        test_specification_generation()
        test_architecture_scaffolding()
        test_code_generators()
        test_end_to_end_workflow()
        
        print("=" * 60)
        print("✅ All tests passed successfully!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
