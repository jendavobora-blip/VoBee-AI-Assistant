# Media Factory

The Media Factory provides modular, extensible interfaces for media-related workflows including image, video, and voice processing.

## Overview

The Media Factory is designed to:
- Provide a consistent interface for different media types
- Enable easy integration with existing services (image-generation, video-generation)
- Support future extensions for voice and other media types
- Maintain task tracking and status management
- Allow batch processing and parallel operations

## Architecture

```
media/
├── __init__.py          # Factory registry and exports
├── base.py              # Abstract base classes and interfaces
├── image.py             # Image workflow implementation
├── video.py             # Video workflow implementation
└── voice.py             # Voice workflow implementation (placeholder)
```

## Usage Examples

### Image Generation

```python
from factories.media import MediaFactoryRegistry, MediaType

# Get an image workflow instance
image_workflow = MediaFactoryRegistry.get_workflow(MediaType.IMAGE)

# Generate an image
task = image_workflow.process({
    "prompt": "A futuristic city with flying cars",
    "style": "realistic",
    "resolution": "1024x1024",
    "hdr": True,
    "model": "stable-diffusion"
})

# Check task status
print(f"Task ID: {task.task_id}")
print(f"Status: {task.status}")

# Batch processing
tasks = image_workflow.batch_process([
    {"prompt": "Sunset over mountains", "style": "realistic"},
    {"prompt": "Abstract geometric patterns", "style": "modern"}
])
```

### Video Generation

```python
from factories.media import MediaFactoryRegistry, MediaType

# Get a video workflow instance
video_workflow = MediaFactoryRegistry.get_workflow(MediaType.VIDEO)

# Generate a video
task = video_workflow.process({
    "prompt": "Flying through clouds at sunset",
    "duration": 10,
    "resolution": "8K",
    "fps": 60,
    "use_nerf": True
})

# Create video from images
task = video_workflow.create_from_images(
    image_sequence=["img1.png", "img2.png", "img3.png"],
    parameters={"fps": 30, "transitions": "fade"}
)
```

### Voice Processing

```python
from factories.media import MediaFactoryRegistry, MediaType

# Get a voice workflow instance
voice_workflow = MediaFactoryRegistry.get_workflow(MediaType.VOICE)

# Text-to-speech
task = voice_workflow.text_to_speech(
    text="Welcome to VoBee AI Assistant",
    voice="professional",
    language="en"
)

# Voice cloning (future feature)
task = voice_workflow.clone_voice(
    sample_audio="sample.wav",
    text="This is a cloned voice speaking"
)
```

## Core Components

### MediaFactory (Base Class)

Abstract base class that all media workflows inherit from. Provides:
- Task management (create, track, cancel)
- Parameter validation
- Status tracking
- Capability reporting

### MediaTask

Dataclass representing a media processing task with:
- Unique task ID
- Media type
- Processing status
- Parameters and configuration
- Results and metadata
- Error tracking

### MediaType Enum

Supported media types:
- `IMAGE` - Image generation and processing
- `VIDEO` - Video generation and processing
- `VOICE` - Voice/audio generation and processing

### ProcessingStatus Enum

Task status values:
- `PENDING` - Task created, awaiting processing
- `PROCESSING` - Task currently being processed
- `COMPLETED` - Task completed successfully
- `FAILED` - Task failed with error
- `CANCELLED` - Task cancelled by user

## Integration Points

### Image Generation Service
- Endpoint: `http://image-generation-service:5000`
- Models: Stable Diffusion, DALL-E, StyleGAN3, DreamBooth
- Features: HDR, PBR, style transfer

### Video Generation Service
- Endpoint: `http://video-generation-service:5001`
- Models: Runway ML Gen-2, NeRF
- Features: 8K resolution, HDR10+, dynamic camera

### Voice Service (Future)
- Endpoint: `http://voice-generation-service:5009`
- Models: TTS-1, TTS-HD, Voice Clone
- Features: Multi-language, emotion control, voice effects

## Extension Guidelines

To add a new media workflow:

1. Create a new file in `factories/media/`
2. Inherit from `MediaFactory` base class
3. Implement required abstract methods:
   - `_setup()` - Initialize resources
   - `validate_parameters()` - Validate inputs
   - `process()` - Main processing logic
   - `_get_supported_formats()` - List formats
   - `_get_features()` - List features

4. Register in `MediaFactoryRegistry` if needed
5. Update `__init__.py` exports

## Configuration

Each workflow accepts a configuration dictionary:

```python
config = {
    "service_endpoint": "http://custom-endpoint:5000",
    "default_model": "custom-model",
    "max_duration": 600,  # For video
    "timeout": 300
}

workflow = ImageWorkflow(config)
```

## Future Enhancements

- [ ] Async processing with callbacks
- [ ] Progress tracking for long-running tasks
- [ ] Result caching and retrieval
- [ ] Multi-step pipeline workflows
- [ ] Resource pool management
- [ ] Advanced error recovery
- [ ] Metrics and monitoring integration
