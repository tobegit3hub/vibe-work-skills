#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
local_image = Image.open("poster_images/poster2.png")

language = "英语"

# Image Generation with local image input
prompt = f"自动识别并翻译现有图片内的文本。利用重绘技术技术将译文完美融入原图，无痕回填背景，完美保留原图的视觉语境，实现无损替换。 识别图片的中文内容，翻译成{language}，然后输出生成的图片。"

response = client.models.generate_content(
    model="google/gemini-3-pro-image-preview",
    contents=[prompt, local_image],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
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
    

