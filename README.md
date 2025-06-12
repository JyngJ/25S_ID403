# 🛰️ SPATIA: System for Spatial Behavior Analysis using ChatGPT

### SPATIA : Spatial Planning Assisted by Tracking and Interpreting Activity

This repository contains an experimental pipeline designed to analyze human behavior in physical spaces using video data and GPT-4o.
It was developed as part of the “Spatia” project, which explores how multimodal large language models (MLLMs) can support spatial design evaluation through human-AI collaboration.

---

## 📌 Key Features

1. **🎞️ Frame Extraction from Video**
   • Automatically extracts image frames from a video at user-defined time intervals.
   • Skips extraction if preprocessed frames already exist.

2. **🤖 Multimodal Analysis with ChatGPT**
   • Sends grouped image frames with a textual prompt to ChatGPT API for behavior or spatial understanding.

3. **🧠 Post-analysis with Summary Questions**
   • After all frame groups are processed, the system asks one or more follow-up questions based on the full image context.

4. **🗃️ Structured Logging**
   • Saves full results, prompts, configuration, and execution time as a .json + .txt log in the log/ folder.

---

🌐 Use Case Example

This pipeline was used in experiments to:
• Detect risky behaviors (e.g., jaywalking) in urban footage
• Simulate accessibility evaluations using visual scenes
• Observe spatial behavior in real-world settings
• Generate design feedback through visual interpretation

---

## ✅ Setup Instructions

### 1. Set Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 2. Set up Python Virtual Environment (Recommended)

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

---

## 🚀 Usage

### Option A: [Recommended] One-Step Execution with `runThis.py`

```bash
python runThis.py
```

This will:

- Extract frames from `./vid/your_video.mp4` (if not already extracted)
- Send grouped image prompts to GPT-4o
- Ask one or more post-analysis questions (defined in the script)
- Save the results + metadata in a log file

You can configure:

- `video_path`: input video location (e.g., `"./vid/111.mov"`)
- `interval_seconds`: how frequently to sample frames
- `set_detection`: whether to perform instance detection on extracted frames
- `set_segmentation`: whether to perform instance segmentation on extracted frames
- `class_id` : list of class ids for object detection
- `group_size`: number of images per GPT request
- `group_prompt`: the main prompt used for each image group
- `final_questions`: list of follow-up questions asked after all images are processed

> Log files are saved to `/log` and include full responses + metadata + execution time.

---

### Option B: Manual Step-by-Step (For development / customization)

#### 1. Extract Frames from Video

```bash
python extract_frames.py input.mp4 trial_name 5
```

- `input.mp4`: path to your video
- `trial_name`: name used in folder `output/{trial_name}_5s`
- `5`: interval in seconds between frames

#### 2. Start a Visual Conversation with GPT-4o

```bash
python run_conversation.py
```

- Sends image groups with prompts to GPT-4o
- Maintains message history for contextual understanding

#### 3. Ask a Follow-up Question (Optional)

Inside Python:

```python
ask_followup_question(messages, "Overall, what kind of video is this?")
```

> Use after image analysis to gather a high-level insight.

---

## 📁 Folder Structure

```
.
├── runThis.py                # Main entry script (automated pipeline)
├── extract_frames.py        # Frame extraction logic
├── run_conversation.py      # GPT conversation logic
├── conversation_with_gpt.py # Low-level OpenAI image/prompt interactions
├── /vid                     # Input video folder
├── /output                  # Extracted frame folders
├── /log                     # Result logs (JSON)
├── requirements.txt
└── .env
```

---

## 🔒 Notes

- GPT-4o image input is used in **base64** encoding.
- To avoid rate limiting, internal throttling is added (adjustable in `RateLimiter`).
- Each run is fully reproducible if the video and config stay the same.
  """

readme_path = Path("README.md")
readme_path.write_text(readme_content.strip(), encoding="utf-8")
readme_path.name
