import cv2
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

# Parameters
frame_folder = "recorded_frames_COLD_left_HOT_right_final"
window_size = 30  # Temporal window size

# Load frames
frames = []
for frame_file in sorted(glob.glob(os.path.join(frame_folder, "*.png"))):
    frame = cv2.imread(frame_file, cv2.IMREAD_GRAYSCALE)
    frames.append(frame)

# Calculate LSI
def calculate_lsi(frames, window_size):
    stack = np.stack(frames[:window_size], axis=0)
    mean_intensity = np.mean(stack, axis=0)
    std_intensity = np.std(stack, axis=0)
    lsi = std_intensity / mean_intensity
    return lsi

lsi_image = calculate_lsi(frames, window_size)

# Visualize LSI
plt.imshow(lsi_image, cmap='hot')
plt.colorbar(label="Temporal Contrast (LSI)")
plt.title("LSI Visualization")
plt.show()

# Save LSI Image
output_path = "lsi_image_final.png"
cv2.imwrite(output_path, (lsi_image * 255).astype(np.uint8))
print(f"LSI image saved to {output_path}.")

# Convert frames to video
output_video = "output2.avi"
height, width = frames[0].shape
video_writer = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'XVID'), 120, (width, height))

for frame in frames:
    video_writer.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))

video_writer.release()
print(f"Video saved to {output_video}.")

# Open the video file
cap = cv2.VideoCapture(output_video)

if not cap.isOpened():
    print(f"Error: Cannot open video file {output_video}")
    exit()

print("Playing video. Press 'q' to quit.")

# Play the video frame by frame
while True:
    ret, frame = cap.read()
    if not ret:
        print("Video playback completed.")
        break

    # Display the frame
    cv2.imshow("Video Playback", frame)

    # Wait for 25ms and check if 'q' is pressed to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        print("Playback interrupted by user.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

