from conversation_with_gpt import start_conversation_with_images

def run_conversation(trial_name: str, interval_seconds: int, group_size: int, prompt: str, rate_limiter=None):
    """
    Runs the full visual conversation for the given image folder.

    Parameters:
        - trial_name: name of the video trial (used to construct folder path)
        - interval_seconds: frame extraction interval (used in folder naming)
        - group_size: number of images per GPT message
        - prompt: prompt for each group of images
        - rate_limiter: optional RateLimiter instance for managing API calls

    Returns:
        - messages: full chat history
        - summaries: list of GPT responses for each image group
    """
    folder_name = f"{trial_name}_{interval_seconds}s"

    # Step 1: Start conversation and build history from grouped images
    messages, summaries = start_conversation_with_images(
        folder_name=folder_name,
        group_size=group_size,
        prompt=prompt,
        rate_limiter=rate_limiter
    )

    # Step 2: Print all group summaries
    print("\n=== Summary per group ===")
    for i, s in enumerate(summaries):
        print(f"[Group {i+1}] {s}")

    # Return full message history and group-level responses
    return messages, summaries