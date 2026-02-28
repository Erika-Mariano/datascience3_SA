import cv2
import os

def extract_frames(video_path, output_folder, fps_rate=1):
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Could not open {video_path}")
        print("Make sure the file exists and the path is correct.")
        return 0

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / video_fps
    frame_interval = int(video_fps / fps_rate)

    print(f"\nVideo:    {os.path.basename(video_path)}")
    print(f"Duration: {duration/60:.1f} minutes")
    print(f"Video FPS: {video_fps}")
    print(f"Extracting at: {fps_rate} fps (1 frame every {frame_interval} original frames)")
    print(f"Expected output: ~{int(duration * fps_rate)} frames")
    print("Extracting", end="", flush=True)

    count = 0
    saved = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            filename = os.path.join(output_folder, f"frame_{saved:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
            if saved % 50 == 0:
                print(".", end="", flush=True)
        count += 1

    cap.release()
    print(f"\nDone! Saved {saved} frames to: {output_folder}\n")
    return saved


# ============================================================
# YOUR VIDEO PATHS - edit only if your filenames change
# ============================================================

base = r"C:\Users\Erika\Desktop\SA1 Data Sci"

videos = [
    (
        os.path.join(base, "Location1_Morning.mp4"),
        os.path.join(base, "frames", "Location1_Morning"),
        1  # 1 fps
    ),
    (
        os.path.join(base, "Location1_Afternoon.mov"),
        os.path.join(base, "frames", "Location1_Afternoon"),
        1  # 1 fps
    ),
    (
        os.path.join(base, "Location2_Afternoon.mov"),
        os.path.join(base, "frames", "Location2_Afternoon"),
        1  # 1 fps
    ),
]

# ============================================================
# RUN EXTRACTION
# ============================================================

print("=" * 55)
print("SA1 Traffic Dataset - Frame Extraction")
print("=" * 55)

total = 0
for video_path, output_folder, fps in videos:
    total += extract_frames(video_path, output_folder, fps)

print("=" * 55)
print(f"ALL DONE!")
print(f"Total frames extracted: {total}")
print(f"Estimated after 3x augmentation in Roboflow: ~{total * 3}")
print(f"\nFrames saved to: {base}\\frames\\")
print("=" * 55)