# 25S_ID403

# 🎬 Frame2Prompt: Automated Frame Analysis from Video using GPT-4o

This repository contains a pipeline for extracting image frames from a video at fixed intervals, analyzing each frame using ChatGPT (GPT-4o) with a predefined prompt, and generating a final summary based on the results.

## 📌 Key Features

### 1. Video to Image Frame Extraction

Converts a video into image frames at user-defined time intervals (e.g., every 5 seconds).

### 2. Image + Prompt Analysis via ChatGPT

Sends each extracted frame with a textual prompt to GPT-4o, utilizing its multimodal capabilities.

### 3. Final Summary or Post-analysis Prompting

Combines individual analysis results and sends a final prompt to receive a summary or further insights.

---

##

### Set Environment Variables

Create a .env file in the root directory to store your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

⸻

### Install Dependencies

Make sure all Python dependencies are installed. You can install them using:

pip install openai python-dotenv opencv-python tqdm

> This will automatically install all required packages listed in requirements.txt:

    •	openai
    •	python-dotenv
    •	opencv-python
    •	tqdm

---

## 🚀 Usage Steps

### 1. Extract Frames from Video

> Convert a video into images every n seconds and save them in an organized output folder.

python extract_frames.py input.mp4 trial_name 5
• input.mp4: Path to your input video
• trial_name: Name used to create the output folder (e.g., output/trial_name_5s/)
• 5: Frame extraction interval in seconds

⸻

### 2. Start a Visual Conversation with GPT-4o

> Analyze the image frames with a specified prompt. GPT will respond to each group and maintain conversational context.

python run_conversation.py
• Sends image frames in groups (default: 5 images per group)
• Uses a default prompt like: “Describe what you see in each of these images.”
• Builds up a message history across all groups

⸻

### 3. Ask a Follow-up Question (Optional)

> After GPT has seen all image groups, you can ask a final summary question like:

ask_followup_question(messages, “Overall, what kind of video do you think this is?”)
• This can be added to run_conversation.py after the image analysis is done

⸻
