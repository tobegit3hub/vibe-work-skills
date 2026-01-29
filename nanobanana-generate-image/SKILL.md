---
name: nanobanana-generate-image
description: Generate images from text prompts or transform existing images using Gemini 3 Pro Image Preview model via Zenmux API. Use when the user wants to create AI-generated images, translate text in images, modify images with AI, or work with image generation tasks.
---

# Nanobanana Generate Image

Generate and transform images using Google Gemini 3 Pro Image Preview model through the Zenmux API gateway.

## Capabilities

1. **Text-to-Image Generation**: Create images from text descriptions
2. **Image-to-Image Transformation**: Modify existing images (e.g., translate text, inpaint, edit)

## Prerequisites

- **ZENMUX_API_KEY**: Environment variable must be set with your Zenmux API key
- **Python packages**: `google-genai`, `Pillow`

Install dependencies:
```bash
pip install google-genai Pillow
```

## Instructions

### Text-to-Image Generation

Use `scripts/generate_image_from_text.py` as reference:

```python
import os
from google import genai
from google.genai import types

api_key = os.getenv("ZENMUX_API_KEY")
if not api_key:
    raise ValueError("ZENMUX_API_KEY environment variable is not set")

client = genai.Client(
    api_key=api_key,
    vertexai=True,
    http_options=types.HttpOptions(api_version='v1', base_url='https://zenmux.ai/api/vertex-ai')
)

prompt = "Your image description here"

response = client.models.generate_content(
    model="google/gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
        print("Image saved as generated_image.png")
```

### Image-to-Image Transformation

Use `scripts/generate_image_from_image.py` as reference:

```python
import os
from google import genai
from google.genai import types
from PIL import Image

api_key = os.getenv("ZENMUX_API_KEY")
if not api_key:
    raise ValueError("ZENMUX_API_KEY environment variable is not set")

client = genai.Client(
    api_key=api_key,
    vertexai=True,
    http_options=types.HttpOptions(api_version='v1', base_url='https://zenmux.ai/api/vertex-ai')
)

# Load local image
local_image = Image.open("input_image.png")

prompt = "Your transformation instructions here"

response = client.models.generate_content(
    model="google/gemini-3-pro-image-preview",
    contents=[prompt, local_image],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    )
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
        print("Image saved as generated_image.png")
```

## Key Configuration

| Parameter | Value |
|-----------|-------|
| Model | `google/gemini-3-pro-image-preview` |
| API Base URL | `https://zenmux.ai/api/vertex-ai` |
| API Version | `v1` |

## Response Modalities

- `["TEXT", "IMAGE"]`: Get both text explanation and generated image
- `["IMAGE"]`: Get only the generated image
- `["TEXT"]`: Get only text response

## Examples

### Generate a creative image
```python
prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
```

### Translate text in an image
```python
language = "English"
prompt = f"Identify and translate the text in this image to {language}. Use inpainting to seamlessly replace the original text while preserving the visual context."
```

### Edit an image
```python
prompt = "Change the background color to blue while keeping the main subject intact"
```

## Reference Scripts

- [scripts/generate_image_from_text.py](scripts/generate_image_from_text.py): Text-to-image generation example
- [scripts/generate_image_from_image.py](scripts/generate_image_from_image.py): Image transformation example

## Troubleshooting

1. **ZENMUX_API_KEY not set**: Export the environment variable before running
   ```bash
   export ZENMUX_API_KEY="your-api-key"
   ```

2. **Missing packages**: Install required dependencies
   ```bash
   pip install google-genai Pillow
   ```

3. **Image not saving**: Ensure you have write permissions in the output directory
