import cv2
import os
import argparse
import subprocess
import shutil
from ultralytics import YOLO
import numpy as np

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

def extract_frames(video_path, data_name, trial_name, interval_sec, detection = False, segmentation=False, class_id=None):

    # Try loading video
    vidcap = cv2.VideoCapture(video_path)
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
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

    if detection or segmentation:
        # Load YOLO model
        model = YOLO("yolo11n-seg.pt")
        print(f"▶️ Starting frame extraction and segmentation every {interval_sec}s ({frame_interval} frames).")

    while frame_id < total_frames:

        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        success, image = vidcap.read()

        if not success:
            print(f"⚠️ Failed to read frame {frame_id}")
            break

        if segmentation or detection:

            results = model(image)

            boxes = results[0].boxes.xyxy.cpu().numpy()
            confs = results[0].boxes.conf.cpu().numpy()
            masks = results[0].masks.data.cpu().numpy()
            labels = results[0].boxes.cls.cpu().numpy().astype(int)


            if segmentation:
                # Only include masks for labels in class_id (or all if class_id is None)
                if class_id is not None:
                    selected_masks = [mask for mask, label in zip(masks, labels) if label in class_id]
                else:
                    selected_masks = masks

                if selected_masks:
                    combined_mask = np.any(selected_masks, axis=0).astype(np.uint8)

                    mask_resized = cv2.resize(combined_mask, (width, height), interpolation=cv2.INTER_NEAREST)

                    # Create a 3-channel mask
                    mask_3ch = np.stack([mask_resized]*3, axis=-1)  # (H, W, 3)

                    # Convert original image to grayscale and make it darker
                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    # Scale pixel values to make it darker (e.g., 50% brightness)
                    dark_gray_image = (gray_image * 0.5).astype(np.uint8)
                    gray_image_3ch = cv2.cvtColor(dark_gray_image, cv2.COLOR_GRAY2BGR)

                    # Composite image: color where mask == 1, grayscale elsewhere
                    image = np.where(mask_3ch == 1, image, gray_image_3ch)

            if detection:
                if boxes is not None:
                    for box, conf, label in zip(boxes, confs, labels):
                        if class_id is None or label in class_id:
                            x1, y1, x2, y2 = map(int, box)
                            label_name = model.names[label]
                            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            # cv2.putText(image, f'{label_name} {conf:.2f}', (x1, y1 - 10),
                            #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            if boxes is None:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                dark_gray_image = (gray_image * 0.5).astype(np.uint8)
                image = cv2.cvtColor(dark_gray_image, cv2.COLOR_GRAY2BGR)


        timestamp_sec = int(frame_id / fps)
        filename = f"{data_name}_{timestamp_sec:04d}.jpg"
        filepath = os.path.join(output_folder, filename)
        cv2.imwrite(filepath, image)
        saved_count += 1

        if detection or segmentation:
            cv2.imshow("Extracted Frame", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        frame_id += frame_interval

    vidcap.release()
    print(f"✅ Done: Saved {saved_count} frames to '{output_folder}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video every N seconds.")
    parser.add_argument("video_path", help="Path to input video file (e.g., sample.mov or sample.mp4)")
    parser.add_argument("trial_name", help="Name of the trial (used in output folder naming)")
    parser.add_argument("interval_sec", type=int, help="Interval in seconds between frames")

    args = parser.parse_args()
    extract_frames(args.video_path, args.trial_name, args.interval_sec)