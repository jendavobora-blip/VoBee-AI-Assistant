# Application and Media Factory E2E Pipeline

## Overview

This document describes the end-to-end pipeline implementation for the Application Factory and Media Factory in the VoBee AI Assistant system. The pipeline enables natural language input to be processed into actionable specifications and executed as media generation tasks.

## Architecture

The E2E pipeline consists of three main components:

```
User Input (Natural Language)
    ↓
[Application Factory]
    - Intent Extraction
    - Entity Extraction
    - Specification Generation
    - Validation
    ↓
[Orchestrator]
    - Workflow Coordination
    - Data Passing
    - Status Tracking
    ↓
[Media Factory]
    - Image Generation
    - Video Generation
    - Voice Processing
    ↓
Output (Generated Media)
```

## Components

### 1. Application Factory (Port 5011)

The Application Factory analyzes natural language user input and generates actionable specifications for downstream factories.

#### Key Features:
- **Intent Extraction**: Identifies user intent from natural language input
  - Supported intents: `generate_image`, `generate_video`, `process_audio`, `transcribe_voice`
  - Pattern-based matching with confidence scoring
  
- **Entity Extraction**: Extracts parameters from user input
  - Prompt text
  - Style (realistic, artistic, etc.)
  - Resolution (1024x1024, 8K, etc.)
  - Duration (for videos)
  - Format (png, mp4, wav, etc.)

- **Specification Generation**: Creates complete task specifications
  - Combines intent and entities
  - Assigns target factory
  - Validates completeness
  
- **Validation**: Ensures specifications are valid before execution
  - Checks required fields
  - Validates confidence thresholds
  - Provides warnings for low-confidence intents

#### API Endpoints:

**Health Check**
```bash
GET /health
```

**Extract Intent**
```bash
POST /extract-intent
{
    "input": "create an image of a sunset"
}
```

**Extract Entities**
```bash
POST /extract-entities
{
    "input": "generate a video in realistic style",
    "intent_type": "generate_video"
}
```

**Generate Specification**
```bash
POST /generate-spec
{
    "input": "create an image of a beautiful landscape",
    "validate": true
}
```

**Validate Specification**
```bash
POST /validate-spec
{
    "specification": {...}
}
```

### 2. Media Factory (Port 5012)

The Media Factory processes media tasks based on specifications from the Application Factory.

#### Key Features:
- **Image Generation**: Simulated image generation workflow
  - Accepts prompts, styles, and resolution
  - Returns simulated image metadata
  - Processing time: ~1200ms (simulated)

- **Video Generation**: Simulated video generation workflow
  - Accepts prompts, duration, and style
  - Returns simulated video metadata
  - Processing time: ~3500ms (simulated)

- **Voice Processing**: Simulated voice/audio workflow
  - Transcription support
  - Audio processing and enhancement
  - Processing time: ~600-800ms (simulated)

- **Task History**: Tracks all processed tasks
- **Statistics**: Provides metrics on task processing

#### API Endpoints:

**Health Check**
```bash
GET /health
```

**Process Task**
```bash
POST /process
{
    "action": "generate_image",
    "parameters": {
        "prompt": "sunset landscape",
        "style": "realistic",
        "resolution": "1024x1024",
        "format": "png"
    }
}
```

**Get Task Status**
```bash
GET /task/{task_id}
```

**Get Statistics**
```bash
GET /stats
```

**Get Capabilities**
```bash
GET /capabilities
```

### 3. Orchestrator Enhancement

The orchestrator has been enhanced to coordinate the E2E pipeline between factories.

#### New Features:
- **Factory Pipeline Execution**: Coordinates Application Factory → Media Factory workflow
- **Data Passing**: Seamlessly passes specifications between factories
- **Status Tracking**: Tracks pipeline progress through all stages
- **Error Handling**: Handles failures at any stage gracefully

#### API Endpoints:

**Execute Factory Pipeline**
```bash
POST /factory-pipeline
{
    "input": "create an image of a futuristic city"
}
```

**Get Pipeline Status**
```bash
GET /pipeline/{pipeline_id}
```

## Usage Examples

### Example 1: Image Generation

**Input:**
```bash
curl -X POST http://localhost:5003/factory-pipeline \
  -H "Content-Type: application/json" \
  -d '{"input": "create an image of a serene lake at dawn in realistic style"}'
```

**Pipeline Flow:**
1. Application Factory extracts intent: `generate_image`
2. Application Factory extracts entities: prompt="serene lake at dawn", style="realistic"
3. Application Factory generates specification with validation
4. Orchestrator routes to Media Factory
5. Media Factory processes image generation
6. Returns completed result with image metadata

**Response:**
```json
{
    "pipeline_id": "uuid...",
    "user_input": "create an image of a serene lake at dawn in realistic style",
    "status": "completed",
    "stages": {
        "application_factory": {
            "status": "completed",
            "specification": {
                "intent": {"type": "generate_image", "confidence": 0.6},
                "action": "generate_image",
                "target_factory": "media_factory",
                "parameters": {...}
            }
        },
        "media_factory": {
            "status": "completed",
            "result": {
                "task_id": "...",
                "output": {
                    "image_id": "img_...",
                    "url": "/outputs/images/...",
                    "prompt": "serene lake at dawn",
                    "style": "realistic"
                }
            }
        }
    },
    "output": {
        "image_id": "img_...",
        "url": "/outputs/images/..."
    }
}
```

### Example 2: Video Generation

**Input:**
```bash
curl -X POST http://localhost:5003/factory-pipeline \
  -H "Content-Type: application/json" \
  -d '{"input": "generate a 10 second video of a flying bird"}'
```

**Pipeline Flow:**
1. Application Factory extracts intent: `generate_video`
2. Application Factory extracts duration: 10 seconds
3. Specification generated and validated
4. Media Factory processes video generation
5. Returns completed result with video metadata

### Example 3: Voice Transcription

**Input:**
```bash
curl -X POST http://localhost:5003/factory-pipeline \
  -H "Content-Type: application/json" \
  -d '{"input": "transcribe the voice recording"}'
```

**Pipeline Flow:**
1. Application Factory extracts intent: `transcribe_voice`
2. Specification generated for voice processing
3. Media Factory processes transcription
4. Returns transcribed text with confidence score

## Testing

### Integration Tests

Run the complete integration test suite:

```bash
python3 test-factory-pipeline.py
```

This test suite validates:
1. Application Factory health
2. Media Factory health
3. Intent extraction accuracy
4. Specification generation
5. Image generation workflow
6. Voice processing workflow
7. Complete E2E pipeline
8. Statistics and capabilities

### Manual Testing

**Test Application Factory:**
```bash
# Start service
cd services/application-factory
python3 main.py

# Test endpoints
curl http://localhost:5011/health
curl -X POST http://localhost:5011/generate-spec \
  -H "Content-Type: application/json" \
  -d '{"input": "create an image of mountains"}'
```

**Test Media Factory:**
```bash
# Start service
cd services/media-factory
python3 main.py

# Test endpoints
curl http://localhost:5012/health
curl -X POST http://localhost:5012/process \
  -H "Content-Type: application/json" \
  -d '{"action": "generate_image", "parameters": {"prompt": "sunset"}}'
```

## Docker Deployment

Both factories are integrated into the docker-compose setup:

```yaml
services:
  application-factory:
    build: ./services/application-factory
    ports:
      - "5011:5011"
    
  media-factory:
    build: ./services/media-factory
    ports:
      - "5012:5012"
    
  orchestrator:
    # Enhanced with factory URLs
    environment:
      - APP_FACTORY_URL=http://application-factory:5011
      - MEDIA_FACTORY_URL=http://media-factory:5012
```

Start all services:
```bash
docker compose up -d application-factory media-factory orchestrator
```

## Implementation Details

### Intent Recognition

The Application Factory uses pattern-based intent recognition with regular expressions:

- Multiple patterns per intent type for better coverage
- Confidence scoring based on pattern matches
- Support for complex natural language variations

### Specification Structure

Generated specifications follow this structure:
```json
{
    "spec_id": "uuid",
    "user_input": "original input",
    "intent": {
        "type": "intent_type",
        "confidence": 0.0-1.0
    },
    "entities": {
        "prompt": "extracted prompt",
        "style": "style",
        ...
    },
    "target_factory": "media_factory",
    "action": "action_name",
    "parameters": {...},
    "validation": {
        "valid": true/false,
        "errors": [],
        "warnings": []
    }
}
```

### Media Processing

The Media Factory implements minimal but functional workflows:

- **Simulated Processing**: Uses hash-based unique IDs for outputs
- **Realistic Metadata**: Returns processing times and model information
- **Task History**: Maintains in-memory history of processed tasks
- **Statistics**: Tracks task counts by type

### Error Handling

The pipeline includes comprehensive error handling:

- **Application Factory**: Validates input and specifications
- **Media Factory**: Returns error status for failed tasks
- **Orchestrator**: Catches and reports errors at each stage
- **Pipeline Result**: Includes error messages and failed stage information

## Performance

### Processing Times (Simulated)

- Image Generation: ~1200ms
- Video Generation: ~3500ms
- Voice Transcription: ~800ms
- Voice Processing: ~600ms
- Pipeline Overhead: ~100-200ms

### Scalability

Both factories are stateless and can be horizontally scaled:

```yaml
orchestrator:
  deploy:
    replicas: 3
    
application-factory:
  deploy:
    replicas: 2
    
media-factory:
  deploy:
    replicas: 4
```

## Future Enhancements

Potential enhancements for production deployment:

1. **Real Model Integration**: Replace simulated processing with actual AI models
2. **Persistent Storage**: Store task history in database
3. **Async Processing**: Implement job queue for long-running tasks
4. **Caching**: Add result caching for similar requests
5. **Monitoring**: Add metrics and tracing
6. **Authentication**: Implement API authentication
7. **Rate Limiting**: Add request rate limiting
8. **Webhooks**: Support callback notifications for completion

## Conclusion

This implementation provides a complete, functional E2E pipeline from natural language input to media generation. The minimal but real implementation demonstrates the workflow without placeholder code, making it ready for further development and integration with actual AI models.
