"""
Intent Extraction Module
Extracts and parses user intent from natural language or structured inputs.
Modular design allows adding new parsers and intent types over time.
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import re
from datetime import datetime


class IntentType(Enum):
    """Supported intent types for application factory"""
    CREATE_APPLICATION = "create_application"
    ADD_FEATURE = "add_feature"
    MODIFY_ARCHITECTURE = "modify_architecture"
    GENERATE_COMPONENT = "generate_component"
    REFACTOR_CODE = "refactor_code"
    GENERATE_TESTS = "generate_tests"
    GENERATE_DOCS = "generate_docs"
    UNKNOWN = "unknown"


class IntentParser:
    """Base class for intent parsers - allows modular parser implementations"""
    
    def parse(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Parse user input to extract intent
        
        Args:
            user_input: Raw user input (natural language or structured)
            context: Additional context for parsing
            
        Returns:
            Dict containing parsed intent information
        """
        raise NotImplementedError("Subclasses must implement parse()")


class KeywordIntentParser(IntentParser):
    """Simple keyword-based intent parser - foundation for more sophisticated parsers"""
    
    def __init__(self):
        # Define keyword patterns for each intent type
        self.intent_patterns = {
            IntentType.CREATE_APPLICATION: [
                r'\b(create|build|generate|make)\s+(new\s+)?(app|application|project|system)\b',
                r'\bnew\s+(web|mobile|desktop|api)\s+(app|application)\b',
            ],
            IntentType.ADD_FEATURE: [
                r'\b(add|implement|create)\s+(a\s+|new\s+)?feature\b',
                r'\badd\s+.+\s+to\s+the\s+(app|application|project)\b',
            ],
            IntentType.MODIFY_ARCHITECTURE: [
                r'\b(modify|change|update|refactor)\s+(the\s+)?architecture\b',
                r'\brestructure\s+(the\s+)?(app|application|project)\b',
            ],
            IntentType.GENERATE_COMPONENT: [
                r'\b(create|generate|add)\s+(a\s+|new\s+)?(component|module|service)\b',
            ],
            IntentType.REFACTOR_CODE: [
                r'\brefactor\b',
                r'\b(clean\s+up|improve|optimize)\s+(the\s+)?code\b',
            ],
            IntentType.GENERATE_TESTS: [
                r'\b(create|generate|write)\s+(unit\s+)?tests?\b',
                r'\badd\s+test\s+coverage\b',
            ],
            IntentType.GENERATE_DOCS: [
                r'\b(create|generate|write)\s+(documentation|docs)\b',
                r'\bdocument\s+(the\s+)?(code|api|project)\b',
            ],
        }
        
        # Technology and framework detection patterns
        self.tech_patterns = {
            'backend': r'\b(backend|server|api|rest|graphql)\b',
            'frontend': r'\b(frontend|ui|interface|web\s+app|react|vue|angular)\b',
            'database': r'\b(database|db|postgres|mysql|mongodb)\b',
            'infrastructure': r'\b(infrastructure|deployment|kubernetes|docker|cloud)\b',
        }
    
    def parse(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Parse user input using keyword matching"""
        context = context or {}
        user_input_lower = user_input.lower()
        
        # Detect intent type
        detected_intent = IntentType.UNKNOWN
        confidence = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower, re.IGNORECASE):
                    detected_intent = intent_type
                    confidence = 0.8  # High confidence for keyword match
                    break
            if detected_intent != IntentType.UNKNOWN:
                break
        
        # Extract entities and technologies
        entities = self._extract_entities(user_input_lower)
        technologies = self._extract_technologies(user_input_lower)
        
        return {
            'intent_type': detected_intent.value,
            'confidence': confidence,
            'raw_input': user_input,
            'entities': entities,
            'technologies': technologies,
            'timestamp': datetime.utcnow().isoformat(),
            'context': context,
        }
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text - placeholder for more sophisticated NER"""
        entities = {
            'app_types': [],
            'features': [],
            'components': [],
        }
        
        # Simple pattern matching for app types
        app_type_patterns = {
            'web': r'\bweb\s+(app|application|site)\b',
            'mobile': r'\bmobile\s+(app|application)\b',
            'api': r'\b(rest|graphql)\s+api\b',
            'microservice': r'\bmicroservice',
        }
        
        for app_type, pattern in app_type_patterns.items():
            if re.search(pattern, text):
                entities['app_types'].append(app_type)
        
        return entities
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract mentioned technologies and frameworks"""
        technologies = []
        
        for tech, pattern in self.tech_patterns.items():
            if re.search(pattern, text):
                technologies.append(tech)
        
        # Extract specific tech stack mentions
        tech_stack_patterns = {
            'python': r'\bpython\b',
            'javascript': r'\b(javascript|js|node\.?js)\b',
            'react': r'\breact\b',
            'vue': r'\bvue(\.js)?\b',
            'docker': r'\bdocker\b',
            'kubernetes': r'\bkubernetes|k8s\b',
        }
        
        for tech, pattern in tech_stack_patterns.items():
            if re.search(pattern, text):
                technologies.append(tech)
        
        return list(set(technologies))  # Remove duplicates


class IntentExtractor:
    """
    Main intent extraction coordinator.
    Manages multiple parsers and provides unified interface.
    """
    
    def __init__(self):
        self.parsers = [
            KeywordIntentParser(),
            # Future parsers can be added here:
            # - MLIntentParser (using trained models)
            # - TemplateIntentParser (structured templates)
            # - ContextualIntentParser (uses conversation history)
        ]
    
    def extract_intent(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Extract intent from user input using available parsers
        
        Args:
            user_input: User's natural language input
            context: Optional context (conversation history, user preferences, etc.)
            
        Returns:
            Extracted intent with metadata
        """
        if not user_input or not user_input.strip():
            return {
                'intent_type': IntentType.UNKNOWN.value,
                'confidence': 0.0,
                'error': 'Empty input',
                'timestamp': datetime.utcnow().isoformat(),
            }
        
        # Try parsers in order of sophistication
        # For now, we only have keyword parser
        intent_result = self.parsers[0].parse(user_input, context)
        
        # Validate and enrich the result
        intent_result = self._validate_and_enrich(intent_result)
        
        return intent_result
    
    def _validate_and_enrich(self, intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate intent result and add additional metadata"""
        
        # Add suggestions based on detected intent
        intent_type = intent_result.get('intent_type')
        suggestions = self._generate_suggestions(intent_type, intent_result)
        
        intent_result['suggestions'] = suggestions
        intent_result['validated'] = True
        
        return intent_result
    
    def _generate_suggestions(self, intent_type: str, intent_result: Dict[str, Any]) -> List[str]:
        """Generate helpful suggestions based on detected intent"""
        suggestions = []
        
        if intent_type == IntentType.CREATE_APPLICATION.value:
            suggestions = [
                "Specify application type (web, mobile, api, etc.)",
                "Define primary technologies/frameworks",
                "Describe main features and functionality",
                "Specify deployment target (cloud, on-premise, etc.)",
            ]
        elif intent_type == IntentType.ADD_FEATURE.value:
            suggestions = [
                "Describe the feature functionality in detail",
                "Specify which part of the application (frontend, backend, etc.)",
                "List any dependencies or prerequisites",
            ]
        elif intent_type == IntentType.GENERATE_COMPONENT.value:
            suggestions = [
                "Specify component type (service, module, class, etc.)",
                "Define component interfaces and dependencies",
                "Describe component responsibility",
            ]
        elif intent_type == IntentType.UNKNOWN.value:
            suggestions = [
                "Try: 'Create a new web application'",
                "Try: 'Add authentication feature'",
                "Try: 'Generate REST API component'",
            ]
        
        return suggestions
    
    def add_parser(self, parser: IntentParser):
        """Add a new parser to the extraction pipeline"""
        self.parsers.append(parser)
        return self
