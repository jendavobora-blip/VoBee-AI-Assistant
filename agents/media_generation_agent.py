"""
Media Generation Agent - Content and media generation specialist.

Responsibilities:
- Generate images based on prompts
- Create video content
- Produce text content
- Manage media workflows
"""

from typing import Dict, List
from .base_agent import BaseAgent
from agents import register_agent


@register_agent
class MediaGenerationAgent(BaseAgent):
    """
    Media generation agent for content creation.
    
    Generates artifacts and specifications only - actual generation requires approval.
    """
    
    ROLE_ID = "media_generation"
    ROLE_NAME = "Media Generation Specialist"
    ROLE_DESCRIPTION = "Creates and manages media generation workflows"
    CAPABILITIES = [
        "generate_image_spec",
        "generate_video_spec",
        "create_content_plan",
        "recommend_styles",
        "optimize_prompts"
    ]
    
    def execute_task(self, task: Dict) -> Dict:
        """
        Execute a media generation task.
        
        Args:
            task: Task definition with type and parameters
            
        Returns:
            Result with generation specifications
        """
        task_type = task.get("type")
        
        self.logger.info(f"Executing media generation task: {task_type}")
        
        if task_type == "generate_image_spec":
            return self._generate_image_spec(task)
        elif task_type == "generate_video_spec":
            return self._generate_video_spec(task)
        elif task_type == "create_content_plan":
            return self._create_content_plan(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    def _generate_image_spec(self, task: Dict) -> Dict:
        """Generate image generation specification."""
        self.validate_action("generate_artifact")
        
        prompt = task.get("prompt", "")
        style = task.get("style", "realistic")
        requirements = task.get("requirements", {})
        
        spec = f"""
# Image Generation Specification

## Original Prompt
{prompt}

## Enhanced Prompt
TODO: AI-enhanced prompt optimization needed

**Suggested Enhancement:**
Consider adding:
- Specific lighting conditions
- Camera angle and perspective
- Artistic style details
- Color palette preferences
- Composition guidelines

## Generation Parameters

### Model Selection
- **Recommended Model**: {self._recommend_model(style)}
- **Alternative Models**: Stable Diffusion XL, DALL-E 3
- **Rationale**: Based on style requirement: {style}

### Technical Settings
```json
{{
  "prompt": "TODO: Enhanced prompt",
  "negative_prompt": "low quality, blurry, distorted, watermark",
  "style": "{style}",
  "resolution": "{requirements.get('resolution', '1024x1024')}",
  "guidance_scale": 7.5,
  "steps": 50,
  "seed": null,
  "hdr": {requirements.get('hdr', 'false')},
  "pbr": {requirements.get('pbr', 'false')}
}}
```

### Quality Settings
- **Resolution**: {requirements.get('resolution', '1024x1024')}
- **Sampling Steps**: 50 (balanced)
- **CFG Scale**: 7.5 (moderate guidance)

### Style Modifiers
- Primary Style: {style}
- Lighting: TODO - Specify lighting preference
- Mood: TODO - Define desired mood
- Color Palette: TODO - Choose color scheme

## Cost Estimate
- **Model**: {self._recommend_model(style)}
- **Estimated Cost**: $0.02 - $0.05 per image
- **Generation Time**: 10-30 seconds

## Review Requirements
- [ ] Prompt clarity verified
- [ ] Style appropriate for use case
- [ ] Resolution meets requirements
- [ ] Budget approved
- [ ] Human review of initial output

## Execution Plan
1. Review and approve specification
2. Execute generation with approved parameters
3. Review output quality
4. Iterate if needed (max 3 iterations recommended)

---
⚠️ This is a specification only. Human approval required before actual generation.
"""
        
        artifact_path = self.generate_artifact(
            "config",
            spec,
            metadata={"prompt": prompt, "style": style, "requirements": requirements}
        )
        
        return {
            "status": "completed",
            "artifact": artifact_path,
            "requires_approval": True,
            "next_actions": ["Review spec", "Approve generation", "Execute with approved params"]
        }
    
    def _generate_video_spec(self, task: Dict) -> Dict:
        """Generate video generation specification."""
        self.validate_action("generate_artifact")
        
        prompt = task.get("prompt", "")
        duration = task.get("duration", 5)
        style = task.get("style", "cinematic")
        
        spec = f"""
# Video Generation Specification

## Concept
{prompt}

## Enhanced Concept
TODO: Storyboard and scene breakdown needed

## Generation Parameters

### Model Selection
- **Recommended**: Runway ML Gen-2
- **Alternative**: NeRF for 3D scenes
- **Rationale**: {style} style best suited for Runway

### Technical Settings
```json
{{
  "prompt": "{prompt}",
  "duration": {duration},
  "resolution": "1920x1080",
  "fps": 30,
  "style": "{style}",
  "use_nerf": false,
  "camera_motion": "smooth",
  "transitions": "fade"
}}
```

### Scene Breakdown
1. **Scene 1 (0-{duration//3}s)**: TODO - Define opening
2. **Scene 2 ({duration//3}-{2*duration//3}s)**: TODO - Define middle
3. **Scene 3 ({2*duration//3}-{duration}s)**: TODO - Define conclusion

### Visual Style
- **Style**: {style}
- **Color Grading**: TODO
- **Lighting**: TODO
- **Camera Movement**: TODO

## Production Requirements
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 fps
- **Duration**: {duration} seconds
- **Format**: H.265/HEVC with HDR10+

## Cost Estimate
- **Model**: Runway ML Gen-2
- **Estimated Cost**: ${duration * 0.05:.2f} (approx $0.05/second)
- **Generation Time**: {duration * 20} seconds

## Review Checkpoints
1. Concept approval
2. Initial frame review
3. Full video review
4. Final approval

---
⚠️ Video generation is resource-intensive. Requires explicit approval and budget allocation.
"""
        
        artifact_path = self.generate_artifact(
            "config",
            spec,
            metadata={"prompt": prompt, "duration": duration, "style": style}
        )
        
        return {
            "status": "completed",
            "artifact": artifact_path,
            "requires_approval": True,
            "next_actions": ["Review concept", "Approve budget", "Execute generation"]
        }
    
    def _create_content_plan(self, task: Dict) -> Dict:
        """Create content generation plan."""
        self.validate_action("recommend")
        
        objectives = task.get("objectives", [])
        timeline = task.get("timeline", "1 month")
        
        plan = f"""
# Content Generation Plan

## Objectives
{self._format_list(objectives)}

## Timeline
{timeline}

## Content Calendar

### Week 1
- [ ] Content piece 1: TODO - Define topic and format
- [ ] Content piece 2: TODO - Define topic and format
- [ ] Review and approval checkpoint

### Week 2
- [ ] Content piece 3: TODO
- [ ] Content piece 4: TODO
- [ ] Mid-point review

### Week 3
- [ ] Content piece 5: TODO
- [ ] Content piece 6: TODO
- [ ] Quality assessment

### Week 4
- [ ] Content piece 7: TODO
- [ ] Final reviews
- [ ] Publishing preparation

## Content Types

### Visual Content
- Images: X per week
- Videos: Y per week
- Infographics: Z per week

### Written Content
- Blog posts: TODO
- Social media: TODO
- Documentation: TODO

## Quality Standards
- All content requires human review
- Brand guidelines compliance mandatory
- Accessibility requirements met
- SEO optimization applied

## Budget Allocation
- Image generation: $TODO
- Video generation: $TODO
- Text content: $TODO
- Total: $TODO

## Approval Workflow
1. Agent generates specification
2. Human reviews and approves concept
3. Generation executed
4. Human reviews output
5. Iteration if needed (max 2 rounds)
6. Final approval for publishing

---
⚠️ Content plan template. Requires human input to complete and approve.
"""
        
        artifact_path = self.generate_artifact(
            "plan",
            plan,
            metadata={"objectives": objectives, "timeline": timeline}
        )
        
        return {
            "status": "completed",
            "artifact": artifact_path,
            "requires_approval": True,
            "next_actions": ["Complete plan details", "Approve calendar", "Allocate budget"]
        }
    
    def _recommend_model(self, style: str) -> str:
        """Recommend model based on style."""
        model_map = {
            "realistic": "Stable Diffusion XL",
            "anime": "Stable Diffusion with Anime LoRA",
            "artistic": "DALL-E 3",
            "photographic": "Stable Diffusion XL + Refiner",
            "3d": "StyleGAN3"
        }
        return model_map.get(style.lower(), "Stable Diffusion XL")
    
    def _format_list(self, items: List) -> str:
        """Format list for markdown output."""
        if not items:
            return "- None specified"
        return "\n".join(f"- {item}" for item in items)
