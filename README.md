# Biophotonics_Exercise4

## Libraries:

- PyPylon: https://github.com/basler/pypylon/tree/master 
- IDS Peak: https://pypi.org/project/ids-peak/ 
- openCV: https://pypi.org/project/opencv-python/

## Scripts:

### perfusion.py
`perfusion.py` is used for calculating the perfusion metrics, including mean, standard deviation, and total values. The results are exported into the `lsci_outputs_perfusion_processed` folder, which contains both the processed images and a JSON file with the perfusion metrics.

### Recording Scripts
- `rec_basler.py`: Script for recording using the Basler camera.
- `rec_ids.py`: Script for recording using the IDS camera.

### LSCI Calculation
- `LSCI_convertion.py`: This script performs the normal LSCI calculation and outputs the results to the `LSCI_outputs` folder.
- `LSCI_convertion_filtering_windows.py`: This script performs LSCI calculation with temporal filtering and outputs the results to the `\Temporal Filtering\X` folder, where `X` represents the specific sequence used for filtering.