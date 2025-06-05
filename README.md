# 25S_ID403

# Frame2Prompt: Automated Frame Analysis from Video using GPT-4o

This repository contains a pipeline for extracting image frames from a video at fixed intervals, analyzing each frame using GPT-4o with a predefined prompt, and generating a final summary based on the results.

---

## 📌 Key Features

1. **Video to Image Frame Extraction**  
   Converts a video into image frames at user-defined time intervals (e.g., every 5 seconds).  
   ➤ If frames already exist with the same interval, extraction is skipped automatically.

2. **Image + Prompt Analysis via ChatGPT**  
   Sends each extracted frame (in groups) with a textual prompt to GPT-4o, utilizing its multimodal capabilities.

3. **Final Summary or Post-analysis Prompting**  
   After all image groups are analyzed, you can ask one or more follow-up questions.  
   These are answered using the accumulated chat context.

4. **Execution Logging**  
   The results, configuration, and execution time are saved to a log file under the `log/` folder.  
   File names are deduplicated if conflicts exist (e.g., `_log_1.json`).

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
