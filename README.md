# 25S_ID403

# 🎬 Frame2Prompt: Automated Frame Analysis from Video using GPT-4o

This repository contains a pipeline for extracting image frames from a video at fixed intervals, analyzing each frame using ChatGPT (GPT-4o) with a predefined prompt, and generating a final summary based on the results.

---

## 📌 Key Features

1. **Video to Image Frame Extraction**  
   Converts a video into image frames at user-defined time intervals (e.g., every 5 seconds).

2. **Image + Prompt Analysis via ChatGPT**  
   Sends each extracted frame with a textual prompt to GPT-4o, utilizing its multimodal capabilities.

3. **Final Summary or Post-analysis Prompting**  
   Combines individual analysis results and sends a final prompt to receive a summary or further insights.

---

## 🚀 Usage Steps

1. **Extract Frames from Video**  
   Run `extract_frames.py` with the following command:
   ```bash
   python extract_frames.py input.mp4 trialA 5
   ```
