"""
Application Factory Service
Main service coordinating intent extraction, specification generation,
architecture scaffolding, and parallel code generation workflows.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
from typing import Dict, Any, List
import json
import os
from uuid import uuid4

# Import Application Factory modules
from intent_extractor import IntentExtractor
from spec_generator import SpecificationGenerator
from architecture_scaffolder import ArchitectureScaffolder
from code_generators.backend_generator import BackendGenerator
from code_generators.frontend_generator import FrontendGenerator
from code_generators.infrastructure_generator import InfrastructureGenerator
from code_generators.qa_generator import QAGenerator
from code_generators.docs_generator import DocsGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


class ApplicationFactory:
    """
    Application Factory orchestrator.
    Coordinates the entire workflow from intent to code generation.
    """
    
    def __init__(self):
        # Initialize modules
        self.intent_extractor = IntentExtractor()
        self.spec_generator = SpecificationGenerator()
        self.architecture_scaffolder = ArchitectureScaffolder()
        
        # Initialize code generators
        self.backend_generator = BackendGenerator()
        self.frontend_generator = FrontendGenerator()
        self.infrastructure_generator = InfrastructureGenerator()
        self.qa_generator = QAGenerator()
        self.docs_generator = DocsGenerator()
        
        # Store for workflows (in-memory for now)
        self.workflows = {}
        
        logger.info("Application Factory initialized successfully")
    
    def process_workflow(
        self,
        user_input: str,
        context: Dict[str, Any] = None,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process complete workflow from user input to code generation
        
        Args:
            user_input: Natural language description of intent
            context: Optional context information
            preferences: Optional user preferences
            
        Returns:
            Complete workflow result with all generated artifacts
        """
        workflow_id = str(uuid4())
        context = context or {}
        preferences = preferences or {}
        
        logger.info(f"Starting workflow {workflow_id}")
        
        workflow = {
            'id': workflow_id,
            'status': 'processing',
            'created_at': datetime.utcnow().isoformat(),
            'stages': {},
        }
        
        try:
            # Stage 1: Intent Extraction
            logger.info(f"Workflow {workflow_id}: Extracting intent")
            intent = self.intent_extractor.extract_intent(user_input, context)
            workflow['stages']['intent'] = {
                'status': 'completed',
                'result': intent,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            # Stage 2: Specification Generation
            logger.info(f"Workflow {workflow_id}: Generating specification")
            specification = self.spec_generator.generate_specification(intent, preferences)
            workflow['stages']['specification'] = {
                'status': 'completed',
                'result': specification,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            # Stage 3: Architecture Scaffolding
            logger.info(f"Workflow {workflow_id}: Scaffolding architecture")
            architecture = self.architecture_scaffolder.generate_architecture(
                specification, preferences
            )
            workflow['stages']['architecture'] = {
                'status': 'completed',
                'result': architecture,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            # Stage 4: Parallel Code Generation (stubs for now)
            logger.info(f"Workflow {workflow_id}: Generating code (parallel stubs)")
            code_generation = self._parallel_code_generation(
                specification, architecture, preferences
            )
            workflow['stages']['code_generation'] = {
                'status': 'completed',
                'result': code_generation,
                'timestamp': datetime.utcnow().isoformat(),
            }
            
            workflow['status'] = 'completed'
            workflow['completed_at'] = datetime.utcnow().isoformat()
            
        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            workflow['status'] = 'failed'
            workflow['error'] = str(e)
            workflow['failed_at'] = datetime.utcnow().isoformat()
        
        # Store workflow
        self.workflows[workflow_id] = workflow
        
        return workflow
    
    def _parallel_code_generation(
        self,
        specification: Dict[str, Any],
        architecture: Dict[str, Any],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Coordinate parallel code generation across all generators.
        Currently executes sequentially but structured for parallel execution.
        """
        results = {
            'backend': None,
            'frontend': None,
            'infrastructure': None,
            'qa': None,
            'docs': None,
        }
        
        # Backend generation
        try:
            backend_framework = preferences.get('backend_framework', 'fastapi')
            backend_generator = BackendGenerator(backend_framework)
            results['backend'] = backend_generator.generate(
                specification, architecture, preferences
            )
        except Exception as e:
            logger.error(f"Backend generation failed: {str(e)}")
            results['backend'] = {'status': 'failed', 'error': str(e)}
        
        # Frontend generation
        try:
            frontend_framework = preferences.get('frontend_framework', 'react')
            frontend_generator = FrontendGenerator(frontend_framework)
            results['frontend'] = frontend_generator.generate(
                specification, architecture, preferences
            )
        except Exception as e:
            logger.error(f"Frontend generation failed: {str(e)}")
            results['frontend'] = {'status': 'failed', 'error': str(e)}
        
        # Infrastructure generation
        try:
            results['infrastructure'] = self.infrastructure_generator.generate(
                specification, architecture, preferences
            )
        except Exception as e:
            logger.error(f"Infrastructure generation failed: {str(e)}")
            results['infrastructure'] = {'status': 'failed', 'error': str(e)}
        
        # QA generation
        try:
            results['qa'] = self.qa_generator.generate(
                specification, architecture, results.get('backend', {}), preferences
            )
        except Exception as e:
            logger.error(f"QA generation failed: {str(e)}")
            results['qa'] = {'status': 'failed', 'error': str(e)}
        
        # Documentation generation
        try:
            results['docs'] = self.docs_generator.generate(
                specification, architecture, results, preferences
            )
        except Exception as e:
            logger.error(f"Documentation generation failed: {str(e)}")
            results['docs'] = {'status': 'failed', 'error': str(e)}
        
        return results


# Initialize factory
factory = ApplicationFactory()


# API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'application-factory',
        'timestamp': datetime.utcnow().isoformat(),
    }), 200


@app.route('/api/v1/factory/process', methods=['POST'])
def process_application():
    """
    Main endpoint to process application generation workflow
    
    Request body:
    {
        "input": "Create a REST API for user management",
        "context": {},
        "preferences": {
            "backend_framework": "fastapi",
            "frontend_framework": "react"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing required field: input'
            }), 400
        
        user_input = data.get('input')
        context = data.get('context', {})
        preferences = data.get('preferences', {})
        
        # Process workflow
        result = factory.process_workflow(user_input, context, preferences)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        return jsonify({
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat(),
        }), 500


@app.route('/api/v1/factory/intent', methods=['POST'])
def extract_intent():
    """
    Extract intent from user input
    
    Request body:
    {
        "input": "Build a web application",
        "context": {}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'input' not in data:
            return jsonify({
                'error': 'Missing required field: input'
            }), 400
        
        user_input = data.get('input')
        context = data.get('context', {})
        
        intent = factory.intent_extractor.extract_intent(user_input, context)
        
        return jsonify(intent), 200
        
    except Exception as e:
        logger.error(f"Error extracting intent: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/v1/factory/specification', methods=['POST'])
def generate_specification():
    """
    Generate specification from intent
    
    Request body:
    {
        "intent": {...},
        "preferences": {}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'intent' not in data:
            return jsonify({
                'error': 'Missing required field: intent'
            }), 400
        
        intent = data.get('intent')
        preferences = data.get('preferences', {})
        
        spec = factory.spec_generator.generate_specification(intent, preferences)
        
        return jsonify(spec), 200
        
    except Exception as e:
        logger.error(f"Error generating specification: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/v1/factory/architecture', methods=['POST'])
def generate_architecture():
    """
    Generate architecture from specification
    
    Request body:
    {
        "specification": {...},
        "preferences": {}
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'specification' not in data:
            return jsonify({
                'error': 'Missing required field: specification'
            }), 400
        
        specification = data.get('specification')
        preferences = data.get('preferences', {})
        
        architecture = factory.architecture_scaffolder.generate_architecture(
            specification, preferences
        )
        
        return jsonify(architecture), 200
        
    except Exception as e:
        logger.error(f"Error generating architecture: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/v1/factory/workflow/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """Get workflow status and results"""
    workflow = factory.workflows.get(workflow_id)
    
    if not workflow:
        return jsonify({
            'error': 'Workflow not found'
        }), 404
    
    return jsonify(workflow), 200


@app.route('/api/v1/factory/workflows', methods=['GET'])
def list_workflows():
    """List all workflows"""
    workflows = [
        {
            'id': wf_id,
            'status': wf['status'],
            'created_at': wf['created_at'],
        }
        for wf_id, wf in factory.workflows.items()
    ]
    
    return jsonify({
        'workflows': workflows,
        'total': len(workflows),
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5009))
    app.run(host='0.0.0.0', port=port, debug=False)
