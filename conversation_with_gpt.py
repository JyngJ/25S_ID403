import os
import openai
import base64
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def _to_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def start_conversation_with_images(prompt: str, folder_path: str, group_size: int, model: str = "gpt-4o"):
    """
    Sends image groups to GPT-4o and builds a message history for follow-up questions.
    Returns:
        - message_history: list of messages
        - summaries: list of string summaries from each group
    """
    image_paths = sorted([
        os.path.join(folder_path, fname)
        for fname in os.listdir(folder_path)
        if fname.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])
    if not image_paths:
        raise ValueError(f"No image files found in: {folder_path}")

    grouped = [image_paths[i:i + group_size] for i in range(0, len(image_paths), group_size)]

    message_history = []
    summaries = []

    for group in grouped:
        group_prompt = {"type": "text", "text": prompt}
        group_images = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{_to_base64(p)}"}}
            for p in group
        ]
        user_message = {"role": "user", "content": [group_prompt] + group_images}
        message_history.append(user_message)

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


def ask_followup_question(message_history, followup_question: str, model: str = "gpt-4o") -> str:
    """
    Sends a follow-up text-only question to GPT based on existing message history.
    """
    message_history.append({"role": "user", "content": followup_question})

    response = openai.chat.completions.create(
        model=model,
        messages=message_history,
        temperature=0.3,
        max_tokens=1000
    )

    reply = response.choices[0].message
    message_history.append({"role": "assistant", "content": reply.content})
    return reply.content