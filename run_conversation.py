from conversation_with_gpt import start_conversation_with_images, ask_followup_question

# Step 1: Start conversation and build history
messages, group_summaries = start_conversation_with_images(
    prompt="Describe what you see in each of these images.",
    folder_path="output/trial_sea1_5s",
    group_size=1
)

# Step 2: Ask a follow-up question based on entire history
followup = "Overall, based on all the images you've seen, what kind of video do you think this is?"
final_answer = ask_followup_question(messages, followup)

print("\n=== Summary per group ===")
for i, s in enumerate(group_summaries):
    print(f"[Group {i+1}] {s}")

print("\n=== Final overall analysis ===")
print(final_answer)