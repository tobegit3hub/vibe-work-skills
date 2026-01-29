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

# Text Generation
response = client.models.generate_content(
    model="google/gemini-3-pro-image-preview",
    contents="How does AI work?"
)
print(response.text);
    
# Image Generation  
# Streaming call: generate_content_stream
# Non-streaming call: generate_content
prompt = "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"

response = client.models.generate_content(
    model="google/gemini-3-pro-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    )
)

# Handle text and image responses
for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        # Save the generated image
        image = part.as_image()
        image.save("generated_image.png")
        print("Image saved as generated_image.png")
    

