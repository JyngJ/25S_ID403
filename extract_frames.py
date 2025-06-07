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

def extract_frames(video_path, trial_name, interval_sec, segementation=False, class_id=None):

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

    if segementation:
        # Load YOLO segmentation model
        model = YOLO("yolo11n-seg.pt")
        print(f"▶️ Starting frame extraction and segmentation every {interval_sec}s ({frame_interval} frames).")

    while success:
        if frame_id % frame_interval == 0:

            if segementation:
                # Run YOLOv8 inference (segmentation) on this frame
                results = model(image)

                # Create a copy for annotation
                annotated = image.copy()
                masks = results[0].masks
                boxes = results[0].boxes

                if masks is not None and boxes is not None:
                    for mask, box in zip(masks.data, boxes.data.cpu().numpy()):
                        cls_id = int(box[5])

                        if class_id is None:
                            annotated = overlay_segmentation(image, annotated, mask, box, width, height)
                        else:
                            if cls_id in class_id:
                                annotated = overlay_segmentation(image, annotated, mask, box, width, height)

                # Save the annotated frame
                image = annotated

            timestamp_sec = int(frame_id / fps)
            filename = f"frame_{timestamp_sec:04d}.jpg"
            filepath = os.path.join(output_folder, filename)
            cv2.imwrite(filepath, image)
            saved_count += 1

            if segementation:
                cv2.imshow("Extracted Frame", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        success, image = vidcap.read()
        frame_id += 1

    vidcap.release()
    print(f"✅ Done: Saved {saved_count} frames to '{output_folder}'.")

def overlay_segmentation(image, annotated, mask, box, width, height):
    # Convert mask to uint8 and scale
    mask_img = (mask.cpu().numpy().astype(np.uint8) * 255)
    # Resize mask to frame size (if model does resizing under the hood, this ensures alignment)
    mask_resized = cv2.resize(mask_img, (width, height), interpolation=cv2.INTER_NEAREST)

    # Create a colored overlay (red)
    mask_colored = np.zeros_like(image)
    mask_colored[:, :, 2] = mask_resized

    # Blend on top of annotated image
    annotated = cv2.addWeighted(annotated, 1.0, mask_colored, 0.5, 0)

    # Draw bounding box
    x1, y1, x2, y2 = map(int, box[:4])
    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
    label = f"Person {box[4]:.2f}"
    cv2.putText(
        annotated,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2,
    )

    return annotated



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video every N seconds.")
    parser.add_argument("video_path", help="Path to input video file (e.g., sample.mov or sample.mp4)")
    parser.add_argument("trial_name", help="Name of the trial (used in output folder naming)")
    parser.add_argument("interval_sec", type=int, help="Interval in seconds between frames")

    args = parser.parse_args()
    extract_frames(args.video_path, args.trial_name, args.interval_sec)