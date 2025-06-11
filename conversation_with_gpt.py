import os
import openai
import base64
import time
from dotenv import load_dotenv
from PIL import Image
import io

# Load OpenAI API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class RequestManager:
    def __init__(self, requests_before_pause=3, pause_duration=30):
        self.request_count = 0
        self.requests_before_pause = requests_before_pause
        self.pause_duration = pause_duration
        self.last_pause_time = time.time()

    def check_and_wait(self):
        self.request_count += 1
        current_time = time.time()

        if self.request_count >= self.requests_before_pause:
            time_since_last_pause = current_time - self.last_pause_time
            if time_since_last_pause < self.pause_duration:
                wait_time = self.pause_duration - time_since_last_pause
                print(f"\n💤 Pausing for {int(wait_time)} seconds to manage rate limits... ({self.request_count} requests processed)")
                time.sleep(wait_time)

            self.request_count = 0
            self.last_pause_time = time.time()
            print("▶️ Resuming requests...\n")

def resize_image(image_path, max_size=800):
    """Resize image to reduce token usage while maintaining quality"""
    with Image.open(image_path) as img:
        # Calculate new size maintaining aspect ratio
        ratio = min(max_size / max(img.size[0], img.size[1]), 1.0)
        new_size = tuple(int(dim * ratio) for dim in img.size)

        if ratio < 1.0:  # Only resize if image is larger than max_size
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85, optimize=True)
        return buffer.getvalue()

def _to_base64(file_path: str) -> str:
    # Use resize_image instead of reading directly
    image_data = resize_image(file_path)
    return base64.b64encode(image_data).decode("utf-8")

def start_conversation_with_images(folder_name: str, group_size: int, prompt: str, rate_limiter=None, model: str = "gpt-4.1-mini"):
    """
    Sends grouped images with prompt to GPT and accumulates responses.
    """
    folder_path = os.path.join("output", folder_name)
    image_paths = sorted([
        os.path.join(folder_path, fname)
        for fname in os.listdir(folder_path)
        if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])
    if not image_paths:
        raise ValueError(f"No image files found in folder: {folder_path}")

    grouped = [image_paths[i:i + group_size] for i in range(0, len(image_paths), group_size)]

    message_history = []
    summaries = []
    total = len(grouped)

    # Initialize request manager
    request_mgr = RequestManager(requests_before_pause=8, pause_duration=60)

    for idx, group in enumerate(grouped):
        percent = int((idx + 1) / total * 100)
        print(f"📤 Sending group {idx + 1}/{total} ({percent}%) to GPT...")

        group_prompt = {"type": "text", "text": prompt}
        group_images = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_to_base64(p)}"}}
            for p in group
        ]
        user_message = {"role": "user", "content": [group_prompt] + group_images}
        message_history.append(user_message)

        # Check if we need to pause
        request_mgr.check_and_wait()

        try:
            response = openai.chat.completions.create(
                model=model,
                messages=message_history,
                temperature=0.3,
                max_tokens=1000
            )
            reply = response.choices[0].message
            message_history.append({"role": "assistant", "content": reply.content})
            summaries.append(reply.content)
        except openai.RateLimitError as e:
            print(f"\n⚠️ Rate limit hit. Pausing for 2 minutes...")
            time.sleep(120)  # Wait for 2 minutes on rate limit error
            print("▶️ Retrying request...\n")
            # Retry the request
            response = openai.chat.completions.create(
                model=model,
                messages=message_history,
                temperature=0.3,
                max_tokens=1000
            )
            reply = response.choices[0].message
            message_history.append({"role": "assistant", "content": reply.content})
            summaries.append(reply.content)

    return message_history, summaries


def ask_followup_question(message_history, followup_questions, rate_limiter=None, model: str = "gpt-4.1-mini"):
    """
    Asks one or more follow-up questions based on the existing chat history.

    Parameters:
        - message_history: list of previous chat messages
        - followup_questions: list of strings (questions)
        - rate_limiter: optional RateLimiter instance for managing API calls
        - model: model name to use for completion

    Returns:
        - List of (question, response) tuples
    """
    results = []
    request_mgr = RequestManager(requests_before_pause=8, pause_duration=60)

    for question in followup_questions:
        print(f"💬 Asking follow-up: {question}")
        message_history.append({"role": "user", "content": question})

        request_mgr.check_and_wait()

        try:
            response = openai.chat.completions.create(
                model=model,
                messages=message_history,
                temperature=0.3,
                max_tokens=1000
            )
            reply = response.choices[0].message
            message_history.append({"role": "assistant", "content": reply.content})
            results.append((question, reply.content))
        except openai.RateLimitError as e:
            print(f"\n⚠️ Rate limit hit. Pausing for 2 minutes...")
            time.sleep(120)
            print("▶️ Retrying request...\n")
            response = openai.chat.completions.create(
                model=model,
                messages=message_history,
                temperature=0.3,
                max_tokens=1000
            )
            reply = response.choices[0].message
            message_history.append({"role": "assistant", "content": reply.content})
            results.append((question, reply.content))

    return results