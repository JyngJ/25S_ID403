import cv2
import os
import argparse
import subprocess
import shutil

def reencode_video(input_path):
    base, _ = os.path.splitext(input_path)
    output_path = base + "_converted.mp4"
    print(f"⚠️ Trying to re-encode video to: {output_path}")

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", output_path
    ]
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode != 0:
        print("❌ FFmpeg re-encoding failed. Check ffmpeg installation.")
        print(result.stderr.decode())
        exit(1)
    
    print("✅ Re-encoding successful.")
    return output_path

def extract_frames(video_path, trial_name, interval_sec):
    # Try loading video
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps == 0.0 or total_frames == 0:
        print(f"⚠️ Failed to read video '{video_path}', attempting re-encoding...")
        vidcap.release()
        video_path = reencode_video(video_path)
        vidcap = cv2.VideoCapture(video_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        if fps == 0.0 or total_frames == 0:
            print("❌ Could not open video even after re-encoding.")
            exit(1)

    frame_interval = int(fps * interval_sec)

    print(f"🎞 Video FPS: {fps}, Total frames: {total_frames}, Saving every {frame_interval} frames.")

    output_folder = os.path.join("output", f"{trial_name}_{interval_sec}s")
    os.makedirs(output_folder, exist_ok=True)

    success, image = vidcap.read()
    frame_id = 0
    saved_count = 0

    while success:
        if frame_id % frame_interval == 0:
            timestamp_sec = int(frame_id / fps)
            filename = f"frame_{timestamp_sec:04d}.jpg"
            filepath = os.path.join(output_folder, filename)
            cv2.imwrite(filepath, image)
            saved_count += 1
        success, image = vidcap.read()
        frame_id += 1

    vidcap.release()
    print(f"✅ Done: Saved {saved_count} frames to '{output_folder}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video every N seconds.")
    parser.add_argument("video_path", help="Path to input video file (e.g., sample.mov or sample.mp4)")
    parser.add_argument("trial_name", help="Name of the trial (used in output folder naming)")
    parser.add_argument("interval_sec", type=int, help="Interval in seconds between frames")

    args = parser.parse_args()
    extract_frames(args.video_path, args.trial_name, args.interval_sec)