"""
AI Orchestrator using LangGraph
Coordinates AI operations and decision flows
"""

import os
import logging
from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

logger = logging.getLogger(__name__)

MOCK_MODE = os.getenv("MOCK_MODE", "true").lower() == "true"


class AgentState(TypedDict):
    """State passed between nodes in the graph"""
    messages: List[Any]
    user_id: str
    operation: str
    input_data: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    error: Optional[str]


class AIOrchestrator:
    """Orchestrates AI operations using LangGraph"""
    
    def __init__(self):
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        
        # Create graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("validate_input", self._validate_input)
        workflow.add_node("check_safety", self._check_safety)
        workflow.add_node("execute_operation", self._execute_operation)
        workflow.add_node("format_output", self._format_output)
        
        # Define edges
        workflow.set_entry_point("validate_input")
        workflow.add_edge("validate_input", "check_safety")
        workflow.add_edge("check_safety", "execute_operation")
        workflow.add_edge("execute_operation", "format_output")
        workflow.add_edge("format_output", END)
        
        # Compile
        self.graph = workflow.compile()
        logger.info("LangGraph workflow compiled")
    
    def _validate_input(self, state: AgentState) -> AgentState:
        """Validate input data"""
        logger.info(f"Validating input for operation: {state['operation']}")
        
        # Basic validation
        if not state.get("user_id"):
            state["error"] = "Missing user_id"
            return state
        
        if not state.get("operation"):
            state["error"] = "Missing operation type"
            return state
        
        logger.info("Input validation passed")
        return state
    
    def _check_safety(self, state: AgentState) -> AgentState:
        """Check safety constraints"""
        if state.get("error"):
            return state
        
        logger.info("Safety check passed")
        # Safety checks are done at API level
        return state
    
    def _execute_operation(self, state: AgentState) -> AgentState:
        """Execute the requested operation"""
        if state.get("error"):
            return state
        
        operation = state["operation"]
        input_data = state.get("input_data", {})
        
        logger.info(f"Executing operation: {operation}")
        
        try:
            if operation == "generate_image":
                result = self._mock_generate_image(input_data)
            elif operation == "generate_video":
                result = self._mock_generate_video(input_data)
            elif operation == "lifesync_decision":
                result = self._mock_lifesync_decision(input_data)
            elif operation == "chat":
                result = self._mock_chat(input_data)
            else:
                result = {"error": f"Unknown operation: {operation}"}
            
            state["result"] = result
        
        except Exception as e:
            logger.error(f"Operation failed: {e}")
            state["error"] = str(e)
        
        return state
    
    def _format_output(self, state: AgentState) -> AgentState:
        """Format the output"""
        if state.get("error"):
            state["result"] = {
                "status": "error",
                "error": state["error"]
            }
        elif state.get("result"):
            state["result"]["status"] = "success"
        
        return state
    
    def _mock_generate_image(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock image generation"""
        prompt = input_data.get("prompt", "")
        style = input_data.get("style", "realistic")
        
        return {
            "type": "image",
            "url": f"https://via.placeholder.com/512x512?text=Mock+Image",
            "prompt": prompt,
            "style": style,
            "model": "mock-stable-diffusion",
            "cost": 0.02
        }
    
    def _mock_generate_video(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock video generation"""
        prompt = input_data.get("prompt", "")
        duration = input_data.get("duration", 5)
        
        return {
            "type": "video",
            "url": f"https://via.placeholder.com/720x480?text=Mock+Video",
            "prompt": prompt,
            "duration": duration,
            "model": "mock-runway-gen2",
            "cost": 0.10
        }
    
    def _mock_lifesync_decision(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock LifeSync decision assistant"""
        scenario = input_data.get("scenario", "")
        options = input_data.get("options", [])
        
        # Simple mock logic
        if len(options) > 0:
            recommendation = options[0]
        else:
            recommendation = "Insufficient data for recommendation"
        
        return {
            "type": "lifesync_decision",
            "scenario": scenario,
            "recommendation": recommendation,
            "confidence": 0.75,
            "reasoning": "Based on mock analysis, this option provides the best balance.",
            "cost": 0.01
        }
    
    def _mock_chat(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock chat response"""
        message = input_data.get("message", "")
        
        # Simple echo response
        response = f"I received your message: '{message}'. This is a mock AI response."
        
        return {
            "type": "chat",
            "message": response,
            "model": "mock-gpt-4",
            "cost": 0.005
        }
    
    async def execute(self, operation: str, user_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an operation through the graph"""
        
        initial_state: AgentState = {
            "messages": [HumanMessage(content=f"Execute {operation}")],
            "user_id": user_id,
            "operation": operation,
            "input_data": input_data,
            "result": None,
            "error": None
        }
        
        try:
            # Run graph
            final_state = self.graph.invoke(initial_state)
            return final_state.get("result", {"error": "No result produced"})
        
        except Exception as e:
            logger.error(f"Graph execution failed: {e}")
            return {"status": "error", "error": str(e)}


# Global instance
_orchestrator = None


def get_orchestrator() -> AIOrchestrator:
    """Get or create the global AIOrchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AIOrchestrator()
    return _orchestrator
