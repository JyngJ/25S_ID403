# Used for checking gpt calling is working
# Not gonna be used in the final code

import os
import openai
from typing import List
from dotenv import load_dotenv
load_dotenv()

def send_images_to_gpt(prompt: str, folder_path: str, group_size: int, model: str = "gpt-4o") -> List[str]:
    """
    Sends groups of images from a folder to the OpenAI GPT-4o model along with a prompt.
    Args:
        prompt: The prompt text to send with each group of images.
        folder_path: Directory containing image files (.jpg, .jpeg, .png).
        group_size: Number of images per API call.
        model: Model name (default: "gpt-4o").
    Returns:
        List of responses from GPT-4o, one per group of images.
    """
    # Make sure your OpenAI API key is set
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Gather image paths from the directory
    image_paths = sorted([
        os.path.join(folder_path, fname)
        for fname in os.listdir(folder_path)
        if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])
    if not image_paths:
        raise ValueError(f"No image files found in: {folder_path}")

    # Group image paths
    grouped = [
        image_paths[i:i + group_size]
        for i in range(0, len(image_paths), group_size)
    ]

    results = []

    for i, group in enumerate(grouped):
        # Compose the message
        messages = [
            {"role": "user", "content": [{"type": "text", "text": prompt}] + [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_to_base64(img_path)}"}}
                for img_path in group
            ]}
        ]

        # Call the OpenAI Chat API
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )

        content = response.choices[0].message.content
        results.append(content)

    return results


# Helper: encode image to base64
import base64

def _to_base64(file_path: str) -> str:
    """
    Converts an image file to a base64-encoded string.
    """
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")