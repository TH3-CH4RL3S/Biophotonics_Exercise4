# Using IDS Peak (IDS Camera)

import ids_peak
import cv2
import time
import os

# Parameters
output_dir = "recorded_frames"
record_duration = 10  # Record for 10 seconds
frame_rate = 120

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Initialize the camera
system_manager = ids_peak.SystemManager()
system_manager.initialize()
camera_list = system_manager.create_device_list()
camera = camera_list[0]
camera.open()

# Set camera parameters
camera.nodemap['ExposureTime'].value = 1000  # Exposure in microseconds
camera.nodemap['AcquisitionFrameRate'].value = frame_rate
camera.nodemap['PixelFormat'].value = 'Mono8'

# Start recording
start_time = time.time()
frame_count = 0

print("Recording started...")
while time.time() - start_time < record_duration:
    frame = camera.get_frame(timeout=1000)  # Timeout in milliseconds
    if frame.image is not None:
        # Save each frame
        cv2.imwrite(f"{output_dir}/frame_{frame_count:04d}.png", frame.image)
        frame_count += 1

camera.close()
print(f"Recording completed. {frame_count} frames saved to '{output_dir}'.")
