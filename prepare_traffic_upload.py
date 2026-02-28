import os
import shutil
import random

frames_root = "frames"
output_folder = "upload_to_roboflow"

# Clear output folder if it already exists
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

# 334 frames per video x 3 videos = ~1,002 total
# After 3x augmentation = ~3,006 frames (meets YOLO requirement)
FRAMES_PER_VIDEO = 334

print("=" * 55)
print("SA1 Traffic Dataset - Preparing Roboflow Upload")
print("=" * 55)

total_copied = 0

for video_folder in os.listdir(frames_root):
    folder_path = os.path.join(frames_root, video_folder)
    if not os.path.isdir(folder_path):
        continue

    frames = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]

    if len(frames) == 0:
        print(f"WARNING: No frames found in {video_folder}, skipping.")
        continue

    selected = random.sample(frames, min(FRAMES_PER_VIDEO, len(frames)))

    for fname in selected:
        src = os.path.join(folder_path, fname)
        new_name = f"{video_folder}_{fname}"
        dst = os.path.join(output_folder, new_name)
        shutil.copy(src, dst)

    total_copied += len(selected)
    print(f"  {video_folder}: {len(selected)} frames selected out of {len(frames)} available")

print()
print("=" * 55)
print(f"Total frames ready for Roboflow: {total_copied}")
print(f"After 3x augmentation in Roboflow: ~{total_copied * 3}")
print(f"Saved to: {os.path.abspath(output_folder)}")
print("=" * 55)
print("\nReady to upload to Roboflow!")