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

# General Workflow for Laser Speckle Imaging (LSI)

## **1. Initialize and Configure the Camera**
- Use **PyPylon** for Basler cameras or **IDS peak** for IDS cameras.
- Set the following parameters:
  - **Exposure time**: 1000–5000 µs (adjust as needed).
  - **Frame rate**: 120 fps.
  - **Pixel format**: Monochrome (e.g., `Mono8`).
  - Define the **Region of Interest (ROI)** if applicable.

---

## **2. Capture a Sequence of Frames**
- Record frames for different phases of the experiment:
  - **Baseline measurement**: Record for 10 seconds at 120 fps.
  - **During stimulation**: Record as the stimulation takes effect.
  - **Follow-up measurement**: Record after the stimulation effect dissipates.
- Save captured frames for further processing.

---

## **3. Process the Images**
- **Calculate Temporal Contrast for LSI**:
  - Use OpenCV and NumPy to process frames.
  - Compute the temporal contrast:
        $$LSI = \frac{\sigma}{\mu}$$
        Where:
        $\sigma$ is the standard deviation of intensity values and
        $\mu$ is the mean intensity value.
  - Generate the LSI image for visualization.
- **Convert Frames to Video**:
  - Save the captured frames as a video file for documentation or playback.

---

## **4. Analyze and Compare ROIs**
- Define two ROIs:
  - **Stimulated ROI**: Area where the stimulation was applied.
  - **Reference ROI**: Non-stimulated area for comparison.
- Calculate the mean perfusion for each ROI:
  - Compare perfusion changes between stimulated and reference areas.

---

## **5. Validate and Compare Results**
- Use provided software (e.g., **moor instruments**) to validate your LSI results.
- Compare:
  - Your calculated LSI images.
  - Perfusion changes in the stimulated and reference ROIs.

---

## **6. Document and Submit**
- Prepare documentation for the experiment:
  - Include the protocol and Python scripts.
  - Provide a README with setup instructions.
  - Record and submit results as per the guidelines.


## Libraries:

- PyPylon: https://github.com/basler/pypylon/tree/master 
- IDS Peak: https://pypi.org/project/ids-peak/ 
- openCV: https://pypi.org/project/opencv-python/