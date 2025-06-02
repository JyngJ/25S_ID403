# 25S_ID403

# Frame2Prompt: Automated Frame Analysis from Video using GPT-4o

This repository contains a pipeline for extracting image frames from a video at fixed intervals, analyzing each frame using GPT-4o with a predefined prompt, and generating a final summary based on the results.

---

## 📌 Key Features

1. **Video to Image Frame Extraction**  
   Converts a video into image frames at user-defined time intervals (e.g., every 5 seconds).

2. **Image + Prompt Analysis via ChatGPT**  
   Sends each extracted frame with a textual prompt to GPT-4o, utilizing its multimodal capabilities.

3. **Final Summary or Post-analysis Prompting**  
   Combines individual analysis results and sends a final prompt to receive a summary or further insights.

---

## ✅ Ready to Run

### 1. Set Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 2. Set up Python Virtual Environment (Recommended)

It is **strongly recommended** to use a virtual environment:

```bash
# Create (only once)
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Install Dependencies

All required packages are listed in `requirements.txt`, including:

- `openai`
- `python-dotenv`
- `opencv-python`
- `tqdm`

To install them:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage Steps

### 1. Extract Frames from Video

```bash
python extract_frames.py input.mp4 trial_name 5
```

- `input.mp4`: Path to your input video
- `trial_name`: Name used to create output folder (e.g., `output/trial_name_5s/`)
- `5`: Frame extraction interval in seconds

---

### 2. Start a Visual Conversation with GPT-4o

```bash
python run_conversation.py
```

- Sends image frames in groups (default: 5 images per group)
- Uses a default prompt like: _"Describe what you see in each of these images."_
- Builds a message history across all groups

---

### 3. Ask a Follow-up Question (Optional)

After all groups are processed, you may ask a summarizing question:

```python
ask_followup_question(messages, "Overall, what kind of video do you think this is?")
```

- Can be added to `run_conversation.py` after analysis

---
