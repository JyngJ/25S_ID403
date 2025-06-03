# runThis.py
# This script is the entry point for using the Frame2Prompt system.
# Follow the steps below to analyze a video using GPT-4o.
# GPT-4o를 활용해 영상에서 프레임을 분석하는 자동화된 메인 스크립트입니다.

# -------------------------------
# ✨ How to Run (Usage Summary)
#
# 1. 터미널에서 가사환경 활성화:
#    Activate virtual environment in terminal:
#        source venv/bin/activate
#
# 2. 실행:
#    Run:
#        python runThis.py
#
# 이 스크립트는 다음 과정을 자동으로 수행합니다:
# This script will automatically perform the following steps:
#   - ./vid 폴더에 있는 비디오로부터 프레임 추출
#     Extract frames from the video in the ./vid folder
#   - GPT-4o에 이미지 + 프론프트 전송 (그룹 단위)
#     Send grouped images with a prompt to GPT-4o
#   - 마지막에 종합 질문을 던지고 결과 출력
#     Ask a final summarizing question and print the result
#
# 설정은 상단의 변수(video_path, interval_seconds 등)을 수정하여 조정할 수 있습니다.
# You can modify parameters like video_path and interval_seconds at the top of the file.
# -------------------------------

# -------------------------------
# Step 1: Put your target video in the ./vid directory
# Example: ./vid/my_video.mp4
# 분석할 비디오 파일을 ./vid 폴더에 넣고 아래 경로를 해당 파일명으로 수정하세요.
video_path = "./vid/111.mov"  # Change this to your video file name

# -------------------------------
# Step 2: Set the interval (in seconds) for extracting frames from the video
# 영상에서 몇 초마다 프레임을 추출할지 설정합니다. (예: 1 = 1초마다 프레임 추출)
interval_seconds = 10  # e.g., 1 = extract one frame per second

# -------------------------------
# Step 3: Set the group size and prompt used for each image group
# 이미지를 몇 장씩 하나의 그룹으로 무기여, 각 그룹에 보내는 프롬프트를 설정합니다.
group_size = 2 # e.g., 2 = send 2 images per GPT message
group_prompt = "From all the images you analyzed, count or estimate how many unique cars appear in the video. Include any assumptions you make (e.g., whether the same car appears in multiple frames), and mention if you saw trucks, motorcycles, or other vehicles too."

# -------------------------------
# Step 4: Set the final follow-up questions asked after all groups are analyzed
# 전체 그룹 분석이 끝난 후 GPT에게 던지는 추가 질문 목록을 작성합니다.
final_questions = [
    "Describe what you see in each of these images. In particular, mention any vehicles (cars, buses, motorcycles, etc.) you observe.",
    "Do you see any patterns or notable features in the vehicles?",
    "Are there any unusual or interesting aspects of the video that stand out to you?"
]

# -------------------------------
# DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING
# It will run all processing steps in order
# 아래 코드는 자동 처리되므로 특별한 경우가 아니면 수정하지 마세요.

import os
import json
from extract_frames import extract_frames
from run_conversation import run_conversation, ask_followup_question

trial_name = os.path.splitext(os.path.basename(video_path))[0] + "_trial"

# Step A: Extract frames
extract_frames(video_path, trial_name, interval_seconds)

# Step B: Run GPT conversation
messages = run_conversation(trial_name, interval_seconds, group_size, group_prompt)

# Step C: Ask final follow-up questions (multiple allowed)
answers = []
for q in final_questions:
    answer = ask_followup_question(messages, q)
    answers.append((q, answer))

# Step D: Write to log file
os.makedirs("log", exist_ok=True)
log_data = {
    "video_name": os.path.basename(video_path),
    "interval_seconds": interval_seconds,
    "group_size": group_size,
    "group_prompt": group_prompt,
    "final_questions": [q for q, _ in answers],
    "responses": [a for _, a in answers]
}
log_path = os.path.join("log", f"{trial_name}_log.json")
with open(log_path, "w") as f:
    json.dump(log_data, f, indent=2, ensure_ascii=False)
print(f"\n✅ Log saved to {log_path}")