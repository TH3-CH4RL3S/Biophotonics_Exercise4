# Using PyPylon (Basler Camera)

from pypylon import pylon
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
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Set camera parameters
camera.ExposureTime.SetValue(1000)  # Exposure in microseconds
camera.AcquisitionFrameRateEnable.SetValue(True)
camera.AcquisitionFrameRate.SetValue(frame_rate)
camera.PixelFormat.SetValue("Mono8")

# Start recording
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
start_time = time.time()
frame_count = 0

print("Recording started...")
while camera.IsGrabbing() and time.time() - start_time < record_duration:
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grab_result.GrabSucceeded():
        frame = grab_result.Array  # Extract the image data
        # Save each frame
        cv2.imwrite(f"{output_dir}/frame_{frame_count:04d}.png", frame)
        frame_count += 1
    grab_result.Release()

camera.StopGrabbing()
camera.Close()
print(f"Recording completed. {frame_count} frames saved to '{output_dir}'.")
