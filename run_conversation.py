from conversation_with_gpt import start_conversation_with_images, ask_followup_question

def run_conversation(trial_name: str, interval_seconds: int, group_size: int, prompt: str):
    """
    Runs the full visual conversation for the given image folder.
    
    Parameters:
        - trial_name: name of the video trial (used to construct folder path)
        - interval_seconds: frame extraction interval (used in folder naming)
        - group_size: number of images per GPT message
        - prompt: prompt for each group of images

    Returns:
        - messages: full chat history
    """
    folder_name = f"{trial_name}_{interval_seconds}s"

    # Step 1: Start conversation and build history from grouped images
    messages, summaries = start_conversation_with_images(
        folder_name=folder_name,
        group_size=group_size,
        prompt=prompt
    )

    # Step 2: Ask a follow-up question based on entire history
    followup = "Overall, based on all the images you've seen, what kind of video do you think this is?"
    final_answer = ask_followup_question(messages, followup)

    # Step 3: Print the result to console
    print("\n=== Summary per group ===")
    for i, s in enumerate(summaries):
        print(f"[Group {i+1}] {s}")

    print("\n=== Final overall analysis ===")
    print(final_answer)

    return messages