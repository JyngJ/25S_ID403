# runThis.py
# This script is the entry point for using the Frame2Prompt system.
# GPT-4o를 활용해 영상에서 프레임을 분석하는 자동화된 메인 스크립트입니다.

# -------------------------------
# ✨ How to Run (Usage Summary)
#
# 1. Activate the virtual environment in terminal:
#    (터미널에서 가상환경 활성화)
#       source venv/bin/activate
#
# 2. Run the main pipeline:
#    (메인 스크립트 실행)
#       python runThis.py
#
# 🪄 What this script does:
#    - Extracts frames from a video in the ./vid folder (skips if already exists)
#    - Sends image groups and prompts to GPT-4o for visual analysis
#    - Asks follow-up questions after all frames are analyzed
#    - Saves the conversation log including metadata and execution time
# -------------------------------

# -------------------------------
# Step 1: Video Input
# Set your target video path under ./vid
# 분석할 비디오 파일 경로를 지정하세요 (예: ./vid/my_video.mp4)
video_path = "./vid/my_video.mp4"

# -------------------------------
# Step 2: Frame Extraction Interval
# Set how frequently to extract frames from the video (in seconds)
# 프레임을 몇 초 간격으로 추출할지 설정합니다
interval_seconds = 1

# -------------------------------
# Step 2.5: Optional Frame Extraction Settings
# If you want to extract frames with detection or segmentation, set these flags
#  프레임 추출 시 바운딩 박스나 세그멘테이션 마스크를 추가하려면 아래 설정을 변경하세요
set_detection = True  # Enable bounding box detection
set_segmentation = True  # Enable segmentation masks

# If you want to segment specific classes, set class_id to a list of class IDs
# class_id = [0]  # Only segment humans
# class_id = [0, 1]  # Segment humans and another class (e.g., cars)
# If you want to segment all classes, set class_id to None
# 세그멘테이션을 특정 클래스에 대해서만 적용하려면 class_id를 해당 클래스 ID의 리스트로 설정하세요
class_id = None  # Segment all classes (default)

# -------------------------------
# Step 3: Image Grouping & Prompt
# Set how many images to include per prompt, and what prompt to use
# 이미지 묶음 크기 및 GPT에게 보낼 그룹별 프롬프트 설정
group_size = 5
# group_prompt = (
#     "You will be shown a sequence of images. These images are consecutive frames extracted from a video, maintaining their original temporal order."
#     "There are three categories of people: 1 person == a single person, 2 people == couple, and more than or equal to three people == family/friends."
#     "Your task is to observe and categorize groups of people based on their relation using distance, touch, orientation, and synchrony."
#     "Output the count for each group."
#     "If a group is already counted in previous frames or groups, do not count them again."
#     "The green bounding boxes is there to help you identify the humans in the image."
#     "What is the total count in each group so far?"
# )

# group_prompt = (
#     "You will be shown a sequence of images. These images are frames extracted from a video, maintaining their original temporal order."
#     "Your task is to observe and estimate the age group distribution ratio among them based on visual cues (e.g., body size, posture, clothing)."
#     # "For your assistance, the background is grayscaled to help you focus on the people."
#     "Use the following age groups: Child (0–10 years), Teen (11–20 years), 20–30 years, 30–40 years, 40–50 years, 50–60 years, 60+ years)"
#     "Output the estimated percentage ratio for each group, adding up to approximately 100%."
#     "Format your output like this: [5%, 15%, 40%, 20%, 10%, 5%, 5%]"
#     "What is the total number of each category of people so far?"
# )

group_prompt = (
    "You will be shown a sequence of images. These images are consecutive frames extracted from a video, maintaining their original temporal order."
    "Your task is to observe ... "
)

# -------------------------------x
# Step 4: Final Follow-Up Questions
# After all image groups are analyzed, ask GPT some summary questions
# GPT 분석 후 던질 종합 질문 리스트
final_questions = [
    "Summarize the your findings."
]

# -------------------------------
# DO NOT MODIFY BELOW UNLESS NECESSARY
# 아래 코드는 전체 파이프라인을 자동으로 실행합니다
# -------------------------------

import os
import json
import time
from extract_frames import extract_frames
from run_conversation import run_conversation
from conversation_with_gpt import ask_followup_question

# 📌 Rate Limiting Setup
class RateLimiter:
    def __init__(self, requests_per_minute=20):
        self.requests_per_minute = requests_per_minute
        self.interval = 60.0 / requests_per_minute
        self.last_request_time = 0

    def wait(self):
        current_time = time.time()
        wait_time = self.interval - (current_time - self.last_request_time)
        if wait_time > 0:
            time.sleep(wait_time)
        self.last_request_time = time.time()

rate_limiter = RateLimiter(requests_per_minute=20)  # Adjust as needed

# ⏱ Execution timer start
start_time = time.time()

# 🎯 Define output folder name
data_name = os.path.splitext(os.path.basename(video_path))[0]
trial_name = data_name + "_trial"
folder_name = f"{trial_name}_{interval_seconds}s"
output_path = os.path.join("output", folder_name)

# 🖼 Step A: Extract frames (Skip if already exists)
if os.path.exists(output_path):
    print(f"📂 Found existing frame folder: {output_path}")
    print("🔁 Skipping frame extraction step.")
else:
    print("🎞 Extracting frames...")
    extract_frames(video_path, data_name, trial_name, interval_seconds, set_detection, set_segmentation, class_id)

# 💬 Step B: Start GPT image conversation
print("🤖 Starting GPT conversation...")
messages, summaries = run_conversation(
    trial_name=trial_name,
    interval_seconds=interval_seconds,
    group_size=group_size,
    prompt=group_prompt,
    rate_limiter=rate_limiter
)

# 🧠 Step C: Ask follow-up questions
print("\n=== Final overall analysis ===")
answers = ask_followup_question(messages, final_questions, rate_limiter=rate_limiter)

# 🖥 Print results to terminal
for q, a in answers:
    print(f"\n[Q] {q}\n[A] {a.strip()}")

# 📝 Step D: Write to log file
os.makedirs("log", exist_ok=True)
log_data = {
    "video_name": os.path.basename(video_path),
    "interval_seconds": interval_seconds,
    "group_size": group_size,
    "group_prompt": group_prompt,
    "final_questions": [q for q, _ in answers],
    "responses": [a for _, a in answers],
    "execution_time_seconds": round(time.time() - start_time, 2)
}

# 🗃 Generate log file name without conflict
base_log_path = os.path.join("log", f"{trial_name}_log.json")
log_path = base_log_path
count = 1
while os.path.exists(log_path):
    log_path = os.path.join("log", f"{trial_name}_log_{count}.json")
    count += 1

with open(log_path, "w") as f:
    json.dump(log_data, f, indent=2, ensure_ascii=False)

print(f"\n✅ Log saved to {log_path}")