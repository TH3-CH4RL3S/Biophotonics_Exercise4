import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


def detect_roi_coordinates(frame_path):
    """
    Detect ROI coordinates for blue and red rectangles in a given frame.

    Parameters:
        frame_path (str): Path to the reference frame (PNG file).

    Returns:
        dict: Coordinates for blue and red ROIs as dictionaries.
    """
    # Read the frame
    image = cv2.imread(frame_path)

    # Extract color channels
    blue_channel = image[:, :, 0]
    red_channel = image[:, :, 2]

    # Detect blue ROI
    _, blue_thresh = cv2.threshold(blue_channel, 200, 255, cv2.THRESH_BINARY)
    blue_contours, _ = cv2.findContours(blue_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_roi = [cv2.boundingRect(c) for c in blue_contours if cv2.contourArea(c) > 100][0]

    # Detect red ROI
    _, red_thresh = cv2.threshold(red_channel, 200, 255, cv2.THRESH_BINARY)
    red_contours, _ = cv2.findContours(red_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_roi = [cv2.boundingRect(c) for c in red_contours if cv2.contourArea(c) > 100][0]

    return {
        "blue": {"x": blue_roi[0], "y": blue_roi[1], "w": blue_roi[2], "h": blue_roi[3]},
        "red": {"x": red_roi[0], "y": red_roi[1], "w": red_roi[2], "h": red_roi[3]},
    }


def load_frames_from_folder(folder_path):
    """
    Load all PNG frames from a specified folder.

    Parameters:
        folder_path (str): Path to the folder containing PNG frames.

    Returns:
        list: List of 2D arrays representing the frames.
    """
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frame_path = os.path.join(folder_path, filename)
            frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
            frames.append(frame)
    return frames


def calculate_temporal_lsci(sequence, window_size=5):
    """
    Calculate a simplified temporal LSCI map.

    Parameters:
        sequence (list): List of 2D arrays representing the frames.
        window_size (int): Number of frames in the temporal window.

    Returns:
        np.ndarray: Average LSCI map across all frames.
    """
    num_frames = len(sequence)
    height, width = sequence[0].shape

    # Convert the sequence into a 3D array for convenience: shape = (num_frames, height, width)
    stack = np.stack(sequence, axis=0)  # shape: (T, H, W)

    # We’ll compute an LSCI map for each valid temporal window, then average or pick one time point.
    half_window = window_size // 2

    # Output container for each time index t where we can apply the window
    lsci_results = []

    for t in range(half_window, num_frames - half_window):
        # Extract frames from t - half_window to t + half_window
        local_stack = stack[t - half_window: t + half_window + 1, :, :]

        # Compute standard deviation and mean across the temporal dimension
        local_std = np.std(local_stack, axis=0)
        local_mean = np.mean(local_stack, axis=0) + 1e-6  # small constant to avoid division by zero

        K = local_std / local_mean
        lsci_results.append(K)

    # For demonstration, we can take the average of these LSCI maps across all valid t
    lsci_map = np.mean(lsci_results, axis=0)

    return lsci_map


def visualize_and_save_lsci_map(lsci_map, output_path, title="LSCI Visualization"):
    """
    Displays and saves the LSCI map as a PNG.

    Parameters:
        lsci_map (np.ndarray): The LSCI map to visualize.
        output_path (str): Path to save the PNG file.
        title (str): Title for the visualization.
    """
    plt.figure(figsize=(6, 6))
    plt.imshow(lsci_map, cmap='jet')
    plt.colorbar(label='LSCI value')
    plt.title(title)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def plot_comparison(baseline_image, filtered_images, window_sizes, output_path):
    num_images = len(filtered_images) + 1
    fig, axes = plt.subplots(1, num_images, figsize=(15, 5))

    # Plot baseline image
    axes[0].imshow(baseline_image, cmap='gray')
    axes[0].set_title("Baseline")
    axes[0].axis('off')

    # Plot filtered images
    for i, (filtered_image, window_size) in enumerate(zip(filtered_images, window_sizes)):
        axes[i + 1].imshow(filtered_image, cmap='gray')
        axes[i + 1].set_title(f"Window Size {window_size}")
        axes[i + 1].axis('off')

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.show()


# Main script
if __name__ == "__main__":
    # Folder containing PNG frames
    folder_path = r"IDS\recorded_frames_COLD_left_HOT_right_final"  # Folder path to frames taken
    reference_frame_path = r"ROI_refrences\IDS_final_roi.png"  # Path to the reference frame

    # Detect ROI coordinates from the reference frame
    rois = detect_roi_coordinates(reference_frame_path)
    blue_roi = rois["blue"]
    red_roi = rois["red"]

    # Load all frames from the folder
    image_sequence = load_frames_from_folder(folder_path)

    # Calculate temporal LSCI maps for blue and red ROIs
    blue_sequence = [frame[blue_roi["y"]:blue_roi["y"] + blue_roi["h"], blue_roi["x"]:blue_roi["x"] + blue_roi["w"]]
                     for frame in image_sequence]
    red_sequence = [frame[red_roi["y"]:red_roi["y"] + red_roi["h"], red_roi["x"]:red_roi["x"] + red_roi["w"]]
                    for frame in image_sequence]

    # Define a range of window sizes for temporal filtering
    window_sizes = [3, 5, 7, 9]

    # Create output directory if it doesn't exist
    output_dir = r"Temporal Filtering\LSCI_outputs_temporal_filtering_initial_IDS"
    os.makedirs(output_dir, exist_ok=True)

    blue_filtered_images = []
    red_filtered_images = []

    for window_size in window_sizes:
        # Calculate LSCI maps for each window size
        blue_lsci_map = calculate_temporal_lsci(blue_sequence, window_size=window_size)
        red_lsci_map = calculate_temporal_lsci(red_sequence, window_size=window_size)

        # Collect filtered images for plotting
        blue_filtered_images.append(blue_lsci_map)
        red_filtered_images.append(red_lsci_map)

        # Define output paths
        blue_output = os.path.join(output_dir, f"blue_output_window_{window_size}.png")
        red_output = os.path.join(output_dir, f"red_output_window_{window_size}.png")

        # Save the LSCI maps as PNGs
        visualize_and_save_lsci_map(blue_lsci_map, blue_output, title=f"Blue ROI Temporal LSCI Map (Window Size {window_size})")
        visualize_and_save_lsci_map(red_lsci_map, red_output, title=f"Red ROI Temporal LSCI Map (Window Size {window_size})")

    # Optionally, visualize the baseline sequence for comparison
    baseline_blue_output = os.path.join(output_dir, "blue_output_baseline.png")
    baseline_red_output = os.path.join(output_dir, "red_output_baseline.png")
    visualize_and_save_lsci_map(blue_sequence[0], baseline_blue_output, title="Blue ROI Baseline Sequence")
    visualize_and_save_lsci_map(red_sequence[0], baseline_red_output, title="Red ROI Baseline Sequence")

    # Plot comparison for blue ROI
    comparison_output_path_blue = os.path.join(output_dir, "blue_comparison.png")
    plot_comparison(blue_sequence[0], blue_filtered_images, window_sizes, comparison_output_path_blue)

    # Plot comparison for red ROI
    comparison_output_path_red = os.path.join(output_dir, "red_comparison.png")
    plot_comparison(red_sequence[0], red_filtered_images, window_sizes, comparison_output_path_red)
