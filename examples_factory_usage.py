#!/usr/bin/env python3
"""
Factory Skeletons Usage Examples

Demonstrates how to use the Media Factory, Research Factory, 
and Project-Level Orchestration.
"""

import sys
sys.path.insert(0, '.')

from factories.media import MediaFactory
from factories.research import ResearchFactory
from core.orchestration import ProjectOrchestrator


def example_media_factory():
    """Example: Using the Media Factory"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Media Factory Usage")
    print("=" * 60)
    
    # Initialize Media Factory
    media = MediaFactory(config={
        'image': {'quality': 'high', 'default_model': 'stable-diffusion'},
        'video': {'fps': 60, 'resolution': '8K'},
        'voice': {'language': 'en', 'default_voice': 'neural'}
    })
    
    print(f"\n✓ Media Factory initialized")
    print(f"  Status: {media.get_status()}")
    
    # Create image
    image_result = media.create_media('image', {
        'prompt': 'A futuristic city with flying cars',
        'style': 'realistic',
        'resolution': '1024x1024'
    })
    print(f"\n✓ Image creation request:")
    print(f"  {image_result}")
    
    # Create video
    video_result = media.create_media('video', {
        'prompt': 'Flying through clouds at sunset',
        'duration': 5,
        'fps': 60
    })
    print(f"\n✓ Video creation request:")
    print(f"  {video_result}")
    
    # Create voice
    voice_result = media.create_media('voice', {
        'text': 'Hello, this is a voice synthesis test',
        'voice_id': 'neural-en-us'
    })
    print(f"\n✓ Voice creation request:")
    print(f"  {voice_result}")


def example_research_factory():
    """Example: Using the Research Factory"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Research Factory Usage")
    print("=" * 60)
    
    # Initialize Research Factory
    research = ResearchFactory(config={
        'market': {'data_sources': ['binance', 'coingecko']},
        'collaboration': {'sources': ['arxiv', 'github']}
    })
    
    print(f"\n✓ Research Factory initialized")
    print(f"  Status: {research.get_status()}")
    
    # Analyze market
    market_result = research.analyze_market({
        'symbol': 'BTC',
        'timeframe': '1h',
        'analysis_type': 'trend',
        'include_sentiment': True
    })
    print(f"\n✓ Market analysis request:")
    print(f"  {market_result}")
    
    # Initiate research collaboration
    research_result = research.initiate_research({
        'topic': 'Latest AI/ML trends in image generation',
        'sources': ['arxiv', 'github'],
        'collaboration_type': 'discovery'
    })
    print(f"\n✓ Research collaboration request:")
    print(f"  {research_result}")


def example_orchestration():
    """Example: Using Project-Level Orchestration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Project-Level Orchestration")
    print("=" * 60)
    
    # Initialize components
    orchestrator = ProjectOrchestrator()
    media = MediaFactory()
    research = ResearchFactory()
    
    # Register factories
    orchestrator.register_factory('media', media)
    orchestrator.register_factory('research', research)
    
    print(f"\n✓ Orchestrator initialized with 2 factories")
    print(f"  Status: {orchestrator.get_status()}")
    
    # Create a sequential workflow
    workflow_id = orchestrator.create_workflow('content_creation_pipeline', {
        'steps': [
            {
                'factory': 'research',
                'action': 'analyze_market',
                'params': {
                    'symbol': 'ETH',
                    'timeframe': '4h'
                }
            },
            {
                'factory': 'media',
                'action': 'create_media',
                'params': {
                    'media_type': 'image',
                    'prompt': 'ETH market trends visualization'
                }
            }
        ],
        'factories': ['research', 'media'],
        'parallel': False
    })
    
    print(f"\n✓ Created workflow: {workflow_id}")
    
    # Execute workflow
    result = orchestrator.execute_workflow(workflow_id)
    print(f"\n✓ Workflow execution completed:")
    print(f"  Status: {result['status']}")
    print(f"  Steps executed: {len(result['result']['results'])}")
    
    # Create a parallel workflow
    parallel_workflow_id = orchestrator.create_workflow('parallel_media_generation', {
        'steps': [
            {
                'factory': 'media',
                'action': 'create_media',
                'params': {'media_type': 'image', 'prompt': 'Sunset landscape'}
            },
            {
                'factory': 'media',
                'action': 'create_media',
                'params': {'media_type': 'video', 'prompt': 'Ocean waves'}
            },
            {
                'factory': 'media',
                'action': 'create_media',
                'params': {'media_type': 'voice', 'text': 'Welcome message'}
            }
        ],
        'factories': ['media'],
        'parallel': True
    })
    
    print(f"\n✓ Created parallel workflow: {parallel_workflow_id}")
    
    # Execute parallel workflow
    parallel_result = orchestrator.execute_workflow(parallel_workflow_id)
    print(f"\n✓ Parallel workflow execution completed:")
    print(f"  Status: {parallel_result['status']}")
    print(f"  Parallel steps executed: {len(parallel_result['result']['results'])}")


def example_advanced_integration():
    """Example: Advanced integration with all factories"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Advanced Multi-Factory Integration")
    print("=" * 60)
    
    orchestrator = ProjectOrchestrator()
    media = MediaFactory()
    research = ResearchFactory()
    
    orchestrator.register_factory('media', media)
    orchestrator.register_factory('research', research)
    
    # Create a complex workflow
    complex_workflow = orchestrator.create_workflow('research_and_content_pipeline', {
        'steps': [
            {
                'factory': 'research',
                'action': 'analyze_market',
                'params': {'symbol': 'BTC', 'timeframe': '1d'}
            },
            {
                'factory': 'research',
                'action': 'initiate_research',
                'params': {'topic': 'BTC technical analysis', 'sources': ['arxiv']}
            },
            {
                'factory': 'media',
                'action': 'create_media',
                'params': {'media_type': 'image', 'prompt': 'BTC analysis chart'}
            },
            {
                'factory': 'media',
                'action': 'create_media',
                'params': {'media_type': 'voice', 'text': 'BTC analysis summary'}
            }
        ],
        'factories': ['research', 'media'],
        'parallel': False
    })
    
    print(f"\n✓ Created complex multi-factory workflow")
    
    result = orchestrator.execute_workflow(complex_workflow)
    print(f"\n✓ Complex workflow completed:")
    print(f"  Status: {result['status']}")
    print(f"  Total steps: {len(result['result']['results'])}")
    
    # Check orchestrator status
    final_status = orchestrator.get_status()
    print(f"\n✓ Final orchestrator status:")
    print(f"  Active workflows: {final_status['active_workflows']}")
    print(f"  Completed workflows: {final_status['completed_workflows']}")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("VoBee AI Assistant - Factory Skeletons Examples")
    print("=" * 60)
    
    try:
        example_media_factory()
        example_research_factory()
        example_orchestration()
        example_advanced_integration()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
