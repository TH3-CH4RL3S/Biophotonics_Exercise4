# USING BASLER

from pypylon import pylon
import os
from datetime import datetime
import cv2
import numpy as np

# Get the current timestamp
timestamp = datetime.now().strftime("%H_%M_%S")

# Use the timestamp as the folder name
folder_name = f"Basler_{timestamp}"

# Create folder with camera name and timestamp as name
os.mkdir(folder_name)

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
#camera.TriggerDelay.SetValue(0)
#camera.TriggerSelector.SetValue("FrameBurstStart")
#camera.TriggerSource.SetValue("Line4")
#camera.TriggerMode.SetValue("On")
#camera.TriggerActivation.SetValue('RisingEdge')
#camera.AcquisitionFrameRateEnable.SetValue(True)
#camera.AcquisitionFrameRateAbs.SetValue(200.0)

camera.PixelFormat.Value = "Mono8"
camera.AcquisitionFrameRate.Value = 100
camera.AcquisitionFrameRateEnable.Value = True
camera.ExposureTime.Value = 6500
camera.Gain.Value = 32
camera.DigitalShift.Value = 1
camera.BinningHorizontal.Value = 2
camera.BinningVertical.Value = 2
camera.BinningHorizontalMode.Value = "Average"
camera.BinningVerticalMode.Value = "Average"
camera.Width.Value = 1000
camera.Height.Value = 768

# demonstrate some feature access
# new_width = camera.Width.Value - camera.Width.Inc
# if new_width >= camera.Width.Min:
#    camera.Width.Value = new_width

numberOfImagesToGrab = 3000
camera.StartGrabbingMax(numberOfImagesToGrab)

# img_count = 0
img_timestamp = []
img_array = []
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        img_timestamp_string = datetime.now().strftime('%H_%M_%S_%f') # + "_" + datetime.now().microsecond // 1000:03d
        img_timestamp.append(img_timestamp_string) #(f"{img}_{datetime.now.microsecond // 1000:03d}")
        # Access the image data.
        #print("SizeX: ", grabResult.Width)
        #print("SizeY: ", grabResult.Height)
        #img = np.copy(grabResult.Array)
        img_array.append(grabResult.Array.copy())
        #print(f"Gray value of first pixel: {img[0, 0]}")
        #print(f"Timestamp: {img_timestamp[-1]} \n")
        #filename = f"{folder_name}/{img_timestamp_string}.png"
        #cv2.imwrite(filename, grabResult.Array.copy())

        #img_count += 1

    grabResult.Release()

print("Recording done!")

for i in range(len(img_array)):
    filename = f"{folder_name}/{i}_{img_timestamp[i]}.png"
    cv2.imwrite(filename, img_array[i][:,:])
    #print(img_array[i][:,:])
    #print("\n")
    #(img_array[i]).Save(pylon.ImageFileFormat_Png, filename)

camera.Close()

print("Images saved!")