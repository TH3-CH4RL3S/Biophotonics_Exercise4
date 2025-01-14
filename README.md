# Biophotonics_Exercise4

# Study Plan: Laser Speckle Imaging (LSI) Experiment

## 1. Baseline Measurement
- **Objective**: Record initial perfusion without any external stimulation to establish a baseline.
- **Procedure**:
  1. Position the subject’s hand (or desired skin area) under the camera.
  2. Ensure stable environmental conditions (e.g., lighting, temperature).
  3. Record a sequence of images for 10 seconds at 120 fps.

## 2. Stimulation of Tissue
- **Objective**: Increase skin perfusion using various stimuli.
- **Stimulation Options**:
  - Heating pad (localized heating).
  - Cooling pad (localized cooling).
  - Warming ointment (e.g., Finalgon or capsaicin cream).
  - Vibration device for mechanical stimulation.
- **Procedure**:
  1. Apply the chosen stimulation to the Region of Interest (ROI).
  2. Wait for the stimulation effect to develop:
     - **Heating pad**: 1–2 minutes.
     - **Cooling pad**: 1–2 minutes.
     - **Ointment**: 3–5 minutes.
     - **Vibration**: Immediate response.

## 3. Measurement After Stimulation
- **Objective**: Record perfusion changes immediately after stimulation.
- **Procedure**:
  1. Record another sequence of images for 10 seconds at 120 fps.
  2. Mark stimulated ROI and reference ROI for analysis.

## 4. Concluding Measurement
- **Objective**: Assess return to baseline or sustained changes in perfusion.
- **Procedure**:
  1. Record a final sequence after the effect dissipates (e.g., 10 minutes post-stimulation).

---

## Expected Reactions
- **Heating pad**: Increased perfusion (higher temporal contrast in LSI).
- **Cooling pad**: Decreased perfusion initially, followed by normalization.
- **Ointment**: Localized hyperemia (reddening due to increased blood flow).
- **Vibration**: Immediate, short-term perfusion increase.

---

## Procedure Instructions for the Patient
### 1. Preparation
- Avoid caffeine or physical exercise 30 minutes prior to the experiment.
- Clean the skin area to remove lotions or oils.

### 2. During the Experiment
- Remain still during measurements to avoid motion artifacts.
- Communicate if discomfort occurs during stimulation.

### 3. Post-Experiment
- Remove any applied substances (e.g., ointment) with a wet cloth.

---

## Camera Configuration
- **Frame rate**: 120 fps.
- **Exposure time**: 1000–5000 µs (adjust based on lighting conditions).
- **Pixel format**: Monochrome for optimal contrast.
- **Region of Interest (ROI)**: Define ROIs for stimulated and reference areas.
- **Trigger Mode**: Continuous acquisition.

---

## Python Implementation Outline
### 1. Initialize Camera
- Detect and configure the camera using PyPylon or IDS peak.

### 2. Record Baseline
```python
from pypylon import pylon
import cv2

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.StartGrabbing()

# Record sequence
frames = []
for _ in range(1200):  # 10 seconds at 120 fps
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grab_result.GrabSucceeded():
        frames.append(grab_result.Array)
    grab_result.Release()

camera.Close()
```

## Libraries:

- PyPylon: https://github.com/basler/pypylon/tree/master 
- IDS Peak: https://pypi.org/project/ids-peak/ 
- openCV: https://pypi.org/project/opencv-python/