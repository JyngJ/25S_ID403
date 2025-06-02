# runThis.py
# This script is the entry point for using the Frame2Prompt system.
# Follow the steps below to analyze a video using GPT-4o.
# GPT-4o를 활용해 영상에서 프레임을 분석하는 자동화된 메인 스크립트입니다.

# -------------------------------
# Step 1: Put your target video in the ./vid directory
# Example: ./vid/my_video.mp4
# 분석할 비디오 파일을 ./vid 폴더에 넣고 아래 경로를 해당 파일명으로 수정하세요.
video_path = "./vid/IMG_0582.MOV"  # Change this to your video file name

# -------------------------------
# Step 2: Set the interval (in seconds) for extracting frames from the video
# 영상에서 몇 초마다 프레임을 추출할지 설정합니다. (예: 1 = 1초마다 프레임 추출)
interval_seconds = 1  # e.g., 1 = extract one frame per second

# -------------------------------
# Step 3: Set the group size and prompt used for each image group
# 이미지를 몇 장씩 하나의 그룹으로 묶을지, 각 그룹에 보낼 프롬프트를 설정합니다.
group_size = 2 # e.g., 2 = send 2 images per GPT message
group_prompt = "Describe what you see in each of these images."

# -------------------------------
# Step 4: Set the final follow-up question asked after all groups are analyzed
# 전체 그룹 분석이 끝난 후 GPT에게 던질 추가 질문을 작성합니다.
final_question = "Overall, what kind of video do you think this is?"

# -------------------------------
# DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING
# It will run all processing steps in order
# 아래 코드는 자동 처리되므로 특별한 경우가 아니면 수정하지 마세요.

import os
from extract_frames import extract_frames
from run_conversation import run_conversation, ask_followup_question

# Generate trial name from video name (e.g., my_video -> my_video_trial)
# 비디오 파일 이름을 기반으로 고유한 trial 이름을 생성합니다.
trial_name = os.path.splitext(os.path.basename(video_path))[0] + "_trial"

# Step A: Extract frames
# Step A: 비디오에서 프레임 추출
extract_frames(video_path, trial_name, interval_seconds)

# Step B: Run GPT conversation
# Step B: 프레임 그룹을 GPT-4o와 대화 형태로 전송하여 분석 받기
messages = run_conversation(trial_name, interval_seconds, group_size, group_prompt)

# Step C: Ask final follow-up question
# Step C: 전체 분석 후 추가 질문을 통해 GPT의 통합적인 판단 받기
ask_followup_question(messages, final_question)