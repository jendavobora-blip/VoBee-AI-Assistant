"""
Application Factory Service
Handles intent extraction and specification generation for downstream factories
"""

from flask import Flask, request, jsonify
import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class IntentType(Enum):
    """Supported intent types"""
    GENERATE_IMAGE = "generate_image"
    GENERATE_VIDEO = "generate_video"
    PROCESS_AUDIO = "process_audio"
    TRANSCRIBE_VOICE = "transcribe_voice"
    UNKNOWN = "unknown"


class ApplicationFactory:
    """
    Application Factory for intent extraction and specification generation.
    Analyzes user input and generates actionable specifications for downstream factories.
    """
    
    def __init__(self):
        logger.info("Initializing Application Factory")
        self.intent_patterns = self._initialize_intent_patterns()
        self.entity_extractors = self._initialize_entity_extractors()
    
    def _initialize_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """Initialize intent recognition patterns"""
        return {
            IntentType.GENERATE_IMAGE: [
                r'(?:create|generate|make|produce)\s+(?:an?\s+)?image',
                r'(?:create|generate|make|produce)\s+(?:a\s+)?picture',
                r'(?:create|generate|make|produce)\s+(?:a\s+)?photo',
                r'image\s+(?:of|with|showing)',
                r'picture\s+(?:of|with|showing)',
            ],
            IntentType.GENERATE_VIDEO: [
                r'(?:create|generate|make|produce)\s+(?:a\s+)?video',
                r'(?:create|generate|make|produce)\s+(?:an?\s+)?animation',
                r'video\s+(?:of|with|showing)',
                r'animate',
            ],
            IntentType.PROCESS_AUDIO: [
                r'(?:process|enhance|edit)\s+(?:the\s+)?audio',
                r'(?:process|enhance|edit)\s+(?:the\s+)?sound',
                r'audio\s+(?:processing|enhancement|editing)',
            ],
            IntentType.TRANSCRIBE_VOICE: [
                r'(?:transcribe|convert)\s+(?:the\s+)?(?:voice|speech|audio)',
                r'speech\s+to\s+text',
                r'voice\s+to\s+text',
                r'(?:listen|hear)\s+(?:to\s+)?(?:the\s+)?audio',
            ],
        }
    
    def _initialize_entity_extractors(self) -> Dict[str, str]:
        """Initialize entity extraction patterns"""
        return {
            'prompt': r'(?:of|showing|with|depicting)\s+["\']?([^"\']+?)["\']?(?:\s+in|\s+with|\s+as|\.|$)',
            'style': r'(?:in|with)\s+(?:a\s+)?([a-zA-Z\-]+)\s+style',
            'duration': r'(\d+)\s*(?:second|sec|minute|min)s?',
            'resolution': r'(\d+x\d+|\d+k|4k|8k|hd|fullhd|uhd)',
            'format': r'(?:in|as)\s+(mp4|avi|mov|png|jpg|jpeg|wav|mp3)',
        }
    
    def extract_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Extract user intent from natural language input
        
        Args:
            user_input: Raw user input text
            
        Returns:
            Dictionary containing intent type and confidence score
        """
        user_input_lower = user_input.lower()
        intent_scores = {}
        
        # Match patterns for each intent type
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    score += 1
            
            if score > 0:
                intent_scores[intent_type] = score
        
        # Determine primary intent
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)
            confidence = min(intent_scores[primary_intent] / len(self.intent_patterns[primary_intent]), 1.0)
        else:
            primary_intent = IntentType.UNKNOWN
            confidence = 0.0
        
        logger.info(f"Intent extracted: {primary_intent.value} (confidence: {confidence:.2f})")
        
        return {
            'type': primary_intent.value,
            'confidence': confidence,
            'matched_patterns': len(intent_scores),
            'all_intents': {k.value: v for k, v in intent_scores.items()}
        }
    
    def extract_entities(self, user_input: str, intent_type: str) -> Dict[str, Any]:
        """
        Extract entities from user input based on intent type
        
        Args:
            user_input: Raw user input text
            intent_type: Detected intent type
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        # Extract common entities
        for entity_name, pattern in self.entity_extractors.items():
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                entities[entity_name] = match.group(1).strip()
        
        # Extract prompt if not found by pattern
        if 'prompt' not in entities:
            # Use entire input as prompt, cleaned up
            entities['prompt'] = user_input
        
        logger.info(f"Entities extracted: {list(entities.keys())}")
        
        return entities
    
    def generate_specification(self, user_input: str) -> Dict[str, Any]:
        """
        Generate actionable specification from user input
        Combines intent and entity extraction to create complete specification
        
        Args:
            user_input: Raw user input text
            
        Returns:
            Complete specification for downstream factories
        """
        spec_id = str(uuid4())
        
        # Extract intent
        intent_data = self.extract_intent(user_input)
        intent_type = intent_data['type']
        
        # Extract entities
        entities = self.extract_entities(user_input, intent_type)
        
        # Generate specification based on intent type
        specification = {
            'spec_id': spec_id,
            'user_input': user_input,
            'intent': intent_data,
            'entities': entities,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'generated',
        }
        
        # Add target factory and parameters
        if intent_type == IntentType.GENERATE_IMAGE.value:
            specification['target_factory'] = 'media_factory'
            specification['action'] = 'generate_image'
            specification['parameters'] = {
                'prompt': entities.get('prompt', user_input),
                'style': entities.get('style', 'realistic'),
                'resolution': entities.get('resolution', '1024x1024'),
                'format': entities.get('format', 'png'),
            }
        
        elif intent_type == IntentType.GENERATE_VIDEO.value:
            specification['target_factory'] = 'media_factory'
            specification['action'] = 'generate_video'
            specification['parameters'] = {
                'prompt': entities.get('prompt', user_input),
                'style': entities.get('style', 'realistic'),
                'duration': self._parse_duration(entities.get('duration', '5')),
                'resolution': entities.get('resolution', '1920x1080'),
                'format': entities.get('format', 'mp4'),
            }
        
        elif intent_type in [IntentType.PROCESS_AUDIO.value, IntentType.TRANSCRIBE_VOICE.value]:
            specification['target_factory'] = 'media_factory'
            specification['action'] = 'process_voice'
            specification['parameters'] = {
                'task': intent_type,
                'format': entities.get('format', 'wav'),
            }
        
        else:
            specification['target_factory'] = None
            specification['action'] = 'unknown'
            specification['parameters'] = {}
        
        logger.info(f"Specification generated: {spec_id} -> {specification['target_factory']}/{specification['action']}")
        
        return specification
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse duration string to seconds"""
        try:
            # Extract number
            num = int(re.search(r'\d+', str(duration_str)).group())
            # Check if minutes
            if 'min' in str(duration_str).lower():
                return num * 60
            return num
        except:
            return 5  # Default 5 seconds
    
    def validate_specification(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate specification before sending to downstream factories
        
        Args:
            specification: Generated specification
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check required fields
        required_fields = ['spec_id', 'intent', 'target_factory', 'action', 'parameters']
        for field in required_fields:
            if field not in specification:
                errors.append(f"Missing required field: {field}")
        
        # Check intent confidence
        if specification.get('intent', {}).get('confidence', 0) < 0.3:
            warnings.append("Low confidence in intent detection")
        
        # Check target factory
        valid_factories = ['media_factory', None]
        if specification.get('target_factory') not in valid_factories:
            errors.append(f"Invalid target factory: {specification.get('target_factory')}")
        
        # Check parameters
        if specification.get('action') != 'unknown':
            if not specification.get('parameters'):
                errors.append("Parameters are required for known actions")
            elif not specification.get('parameters', {}).get('prompt'):
                warnings.append("No prompt found in parameters")
        
        is_valid = len(errors) == 0
        
        logger.info(f"Specification validation: valid={is_valid}, errors={len(errors)}, warnings={len(warnings)}")
        
        return {
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'validated_at': datetime.utcnow().isoformat()
        }


# Initialize the factory
factory = ApplicationFactory()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "application-factory",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/extract-intent', methods=['POST'])
def extract_intent():
    """Extract intent from user input"""
    try:
        data = request.get_json()
        
        if 'input' not in data:
            return jsonify({"error": "Input is required"}), 400
        
        result = factory.extract_intent(data['input'])
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in extract-intent endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/extract-entities', methods=['POST'])
def extract_entities():
    """Extract entities from user input"""
    try:
        data = request.get_json()
        
        if 'input' not in data:
            return jsonify({"error": "Input is required"}), 400
        
        intent_type = data.get('intent_type', 'unknown')
        result = factory.extract_entities(data['input'], intent_type)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in extract-entities endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/generate-spec', methods=['POST'])
def generate_specification():
    """Generate actionable specification from user input"""
    try:
        data = request.get_json()
        
        if 'input' not in data:
            return jsonify({"error": "Input is required"}), 400
        
        specification = factory.generate_specification(data['input'])
        
        # Optionally validate
        if data.get('validate', True):
            validation = factory.validate_specification(specification)
            specification['validation'] = validation
        
        return jsonify(specification), 200
        
    except Exception as e:
        logger.error(f"Error in generate-spec endpoint: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/validate-spec', methods=['POST'])
def validate_specification():
    """Validate a specification"""
    try:
        data = request.get_json()
        
        if 'specification' not in data:
            return jsonify({"error": "Specification is required"}), 400
        
        validation = factory.validate_specification(data['specification'])
        
        return jsonify(validation), 200
        
    except Exception as e:
        logger.error(f"Error in validate-spec endpoint: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=False)
