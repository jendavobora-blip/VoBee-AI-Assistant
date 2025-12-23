#!/usr/bin/env python3
"""
VoBee AI Assistant - Factory Integration Examples

This script demonstrates the usage of the factory skeletons including:
- Media Factory (Image, Video, Voice workflows)
- Research Factory (Market Analysis, Research Agents)
- Core Orchestration (Multi-factory workflows, task routing)

Note: This is a demonstration script showing the skeleton interfaces.
In production, these would connect to actual services and process real tasks.
"""

import sys
from typing import Dict, Any

# Add current directory to path for imports
sys.path.insert(0, '.')

from factories.media import MediaFactoryRegistry, MediaType
from factories.research import ResearchFactoryRegistry, ResearchType
from core.orchestration import (
    OrchestrationEngine,
    WorkflowCoordinator,
    WorkflowTemplate,
    WorkflowStep,
    FactoryType,
    TaskRouter,
    RoutingStrategy
)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subsection(title: str):
    """Print a formatted subsection header"""
    print(f"\n{title}")
    print("-" * 70)


def example_media_factory():
    """Demonstrate Media Factory capabilities"""
    print_section("MEDIA FACTORY EXAMPLES")
    
    # Example 1: Image Generation
    print_subsection("1. Image Generation Workflow")
    image_workflow = MediaFactoryRegistry.get_workflow(MediaType.IMAGE)
    
    task = image_workflow.process({
        "prompt": "A futuristic city with flying cars at sunset",
        "style": "realistic",
        "resolution": "1024x1024",
        "hdr": True,
        "pbr": True,
        "model": "stable-diffusion"
    })
    
    print(f"Created image generation task: {task.task_id}")
    print(f"  Status: {task.status.value}")
    print(f"  Parameters: {task.parameters.get('prompt')}")
    print(f"  Model: {task.metadata.get('model')}")
    
    # Batch processing
    print_subsection("2. Batch Image Processing")
    batch_tasks = image_workflow.batch_process([
        {"prompt": "Mountain landscape", "style": "realistic"},
        {"prompt": "Abstract geometric art", "style": "modern"},
        {"prompt": "Character portrait", "style": "anime"}
    ])
    print(f"Created {len(batch_tasks)} batch tasks")
    
    # Example 2: Video Generation
    print_subsection("3. Video Generation Workflow")
    video_workflow = MediaFactoryRegistry.get_workflow(MediaType.VIDEO)
    
    video_task = video_workflow.process({
        "prompt": "Flying through clouds at golden hour",
        "duration": 10,
        "resolution": "4K",
        "fps": 60,
        "use_nerf": True,
        "style": "cinematic"
    })
    
    print(f"Created video generation task: {video_task.task_id}")
    print(f"  Duration: {video_task.metadata.get('duration')}s")
    print(f"  FPS: {video_task.metadata.get('fps')}")
    
    # Example 3: Voice/Audio Processing
    print_subsection("4. Voice Processing Workflow")
    voice_workflow = MediaFactoryRegistry.get_workflow(MediaType.VOICE)
    
    tts_task = voice_workflow.text_to_speech(
        text="Welcome to the VoBee AI Assistant. Your intelligent companion for creative tasks.",
        voice="professional",
        language="en"
    )
    
    print(f"Created text-to-speech task: {tts_task.task_id}")
    print(f"  Language: {tts_task.metadata.get('language')}")
    print(f"  Voice: {tts_task.metadata.get('voice')}")
    
    # Get capabilities
    print_subsection("5. Media Factory Capabilities")
    image_caps = image_workflow.get_capabilities()
    print(f"Image workflow features: {', '.join(image_caps['features'])}")
    
    video_caps = video_workflow.get_capabilities()
    print(f"Video workflow features: {', '.join(video_caps['features'])}")


def example_research_factory():
    """Demonstrate Research Factory capabilities"""
    print_section("RESEARCH FACTORY EXAMPLES")
    
    # Example 1: Market Analysis
    print_subsection("1. Competitive Analysis")
    market_workflow = ResearchFactoryRegistry.get_workflow(ResearchType.MARKET_ANALYSIS)
    
    analysis_task = market_workflow.analyze_competitors(
        market_sector="technology",
        competitors=["OpenAI", "Anthropic", "Google DeepMind"],
        metrics=["innovation", "market_share", "product_quality"]
    )
    
    print(f"Created competitive analysis task: {analysis_task.task_id}")
    print(f"  Market: {analysis_task.metadata.get('market_sector')}")
    print(f"  Priority: {analysis_task.priority.value}")
    print(f"  Analysis Type: {analysis_task.metadata.get('analysis_type')}")
    
    # Example 2: Trend Analysis
    print_subsection("2. Market Trend Identification")
    trend_task = market_workflow.identify_trends(
        market_sector="artificial-intelligence",
        timeframe="1Y"
    )
    
    print(f"Created trend analysis task: {trend_task.task_id}")
    print(f"  Timeframe: 1 Year")
    
    # Example 3: Research Agent - Technology Discovery
    print_subsection("3. Technology Discovery Agent")
    agent_workflow = ResearchFactoryRegistry.get_workflow(ResearchType.RESEARCH_AGENT)
    
    discovery_task = agent_workflow.discover_technology(
        query="generative AI frameworks 2024",
        filters={"language": "python", "min_stars": 1000}
    )
    
    print(f"Created technology discovery task: {discovery_task.task_id}")
    print(f"  Query: {discovery_task.metadata.get('query')}")
    print(f"  Agent Type: {discovery_task.metadata.get('agent_type')}")
    print(f"  Max Results: {discovery_task.metadata.get('max_results')}")
    
    # Example 4: Research Paper Analysis
    print_subsection("4. Research Paper Analysis")
    paper_task = agent_workflow.analyze_research_papers(
        topic="transformer architectures in computer vision",
        max_results=20
    )
    
    print(f"Created paper analysis task: {paper_task.task_id}")
    print(f"  Sources: {', '.join(paper_task.metadata.get('sources', []))}")
    
    # Get capabilities
    print_subsection("5. Research Factory Capabilities")
    market_caps = market_workflow.get_capabilities()
    print(f"Market analysis types: {', '.join(market_caps['analysis_types'])}")
    
    agent_caps = agent_workflow.get_capabilities()
    print(f"Research agent features: {', '.join(agent_caps['features'][:5])}...")


def example_orchestration():
    """Demonstrate Core Orchestration capabilities"""
    print_section("CORE ORCHESTRATION EXAMPLES")
    
    # Example 1: Factory Status
    print_subsection("1. Factory Status Monitoring")
    engine = OrchestrationEngine()
    status = engine.get_factory_status()
    
    for factory_name, factory_status in status.items():
        print(f"{factory_name.upper()} Factory:")
        print(f"  Status: {factory_status['status']}")
        print(f"  Workflows: {', '.join(factory_status['available_workflows'])}")
    
    # Example 2: Intelligent Task Routing
    print_subsection("2. Intelligent Task Routing")
    router = TaskRouter({"strategy": "CONTENT_BASED"})
    
    tasks = [
        {"type": "image_generation", "keywords": ["image", "photo"]},
        {"type": "market_research", "keywords": ["market", "analysis"]},
        {"type": "video_creation", "keywords": ["video", "animation"]},
        {"type": "technology_scan", "keywords": ["discover", "research"]}
    ]
    
    for task in tasks:
        factory = router.route(task)
        print(f"Task '{task['type']}' → routed to: {factory.upper()} factory")
    
    # Example 3: Multi-Factory Workflow
    print_subsection("3. Multi-Factory Workflow Coordination")
    coordinator = WorkflowCoordinator({
        "max_retries": 3,
        "parallel_execution": True
    })
    
    # Create a complex workflow
    template = coordinator.create_template(
        name="Product Launch Campaign",
        description="Generate marketing materials and conduct market research",
        steps=[
            {
                "name": "Market Research",
                "factory_type": "research",
                "action": "market_analysis",
                "parameters": {
                    "market_sector": "consumer_tech",
                    "analysis_type": "competitive",
                    "depth": "comprehensive"
                }
            },
            {
                "name": "Trend Discovery",
                "factory_type": "research",
                "action": "discover_trends",
                "parameters": {
                    "query": "emerging consumer tech trends"
                },
                "dependencies": []  # Runs in parallel with Market Research
            },
            {
                "name": "Product Hero Image",
                "factory_type": "media",
                "action": "generate_image",
                "parameters": {
                    "prompt": "Professional product hero shot",
                    "style": "realistic",
                    "resolution": "2048x2048"
                },
                "dependencies": ["step_0"]  # Wait for market research
            },
            {
                "name": "Product Demo Video",
                "factory_type": "media",
                "action": "generate_video",
                "parameters": {
                    "prompt": "Product demonstration and features",
                    "duration": 30,
                    "style": "professional"
                },
                "dependencies": ["step_2"]  # Wait for hero image
            },
            {
                "name": "Voiceover Narration",
                "factory_type": "media",
                "action": "text_to_speech",
                "parameters": {
                    "text": "Introducing our revolutionary new product...",
                    "voice": "professional",
                    "language": "en"
                },
                "dependencies": ["step_3"]  # Wait for video
            }
        ]
    )
    
    print(f"Created workflow template: {template.name}")
    print(f"  Workflow ID: {template.workflow_id}")
    print(f"  Total Steps: {len(template.steps)}")
    print(f"\nWorkflow Steps:")
    for i, step in enumerate(template.steps):
        deps = f" (depends on: {', '.join(step.dependencies)})" if step.dependencies else " (parallel)"
        print(f"  {i+1}. {step.name} [{step.factory_type}]{deps}")
    
    # Execute the workflow
    execution = coordinator.execute(template)
    print(f"\nWorkflow Execution Started:")
    print(f"  Execution ID: {execution.execution_id}")
    print(f"  Status: {execution.status.value}")


def main():
    """Main execution"""
    print("\n" + "=" * 70)
    print("  VoBee AI Assistant - Factory Integration Examples")
    print("=" * 70)
    print("\nThis demonstration showcases the modular factory architecture:")
    print("  • Media Factory: Image, Video, Voice workflows")
    print("  • Research Factory: Market Analysis, Research Agents")
    print("  • Core Orchestration: Multi-factory coordination & routing")
    
    try:
        # Run all examples
        example_media_factory()
        example_research_factory()
        example_orchestration()
        
        # Final summary
        print_section("SUMMARY")
        print("\n✅ All factory skeletons are operational and ready for extension")
        print("\nKey Features Demonstrated:")
        print("  • Modular factory architecture with clear interfaces")
        print("  • Task-based workflow management")
        print("  • Intelligent routing and load balancing")
        print("  • Multi-factory orchestration with dependencies")
        print("  • Extensible design for future enhancements")
        
        print("\nNext Steps:")
        print("  • Connect to actual service implementations")
        print("  • Add async processing capabilities")
        print("  • Implement result storage and retrieval")
        print("  • Add monitoring and metrics")
        print("  • Extend with additional factory types")
        
        print("\n" + "=" * 70)
        print("  End of Examples")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
