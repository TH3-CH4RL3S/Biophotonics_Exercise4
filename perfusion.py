import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import json

def load_image(image_path):
    """
    Load the image and convert it to grayscale.

    Parameters:
        image_path (str): Path to the image.

    Returns:
        ndarray: Grayscale image array.

    Raises:
        FileNotFoundError: If the image cannot be loaded.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}. Please check the path.")
    return image

def calculate_perfusion(image):
    """
    Calculate perfusion metrics (mean, total, and standard deviation) for the entire image.

    Parameters:
        image (ndarray): Grayscale image (LSCI).

    Returns:
        dict: Dictionary containing "mean", "total", and "std" perfusion values.
    """
    mean_perfusion = np.mean(image)
    total_perfusion = np.sum(image)
    std_perfusion = np.std(image)

    return {
        "mean": mean_perfusion,
        "total": total_perfusion,
        "std": std_perfusion
    }

def visualize_perfusion(image, metrics, output_path1="perfusion_mean_std.png", output_path2="perfusion_total.png"):
    """
    Create visual representations of the perfusion metrics.

    Parameters:
        image (ndarray): The original grayscale image.
        metrics (dict): Calculated perfusion metrics.
        output_path1 (str): Path to save the mean and std visualization.
        output_path2 (str): Path to save the total perfusion visualization.
    """
    # --- Plot 1: Mean and Std ---
    plt.figure(figsize=(8, 5))
    plt.title("Perfusion Metrics (Mean and Std)")
    labels = ["Mean", "Std"]
    values = [metrics["mean"], metrics["std"]]
    bar_container = plt.bar(labels, values, color="green")
    plt.ylabel("Values")

    # Annotate bar values
    for rect, val in zip(bar_container, values):
        height = rect.get_height()
        plt.text(
            rect.get_x() + rect.get_width() / 2,
            height,
            f"{val:.2f}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()
    plt.savefig(output_path1, dpi=150)
    #plt.show()

    # --- Plot 2: Total Perfusion ---
    plt.figure(figsize=(8, 5))
    plt.title("Perfusion Metric (Total)")
    plt.bar(["Total"], [metrics["total"]], color="blue")
    plt.ylabel("Values")

    # Annotate the bar value
    plt.text(
        0,
        metrics["total"],
        f"{metrics['total']:.2f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

    plt.tight_layout()
    plt.savefig(output_path2, dpi=150)
    #plt.show()

def process_images_in_folder(folder_path, output_folder):
    # Get all image files in the folder
    image_files = glob.glob(os.path.join(folder_path, "*.png"))  # Adjust the extension if needed

    # Dictionary to store perfusion metrics for each image
    perfusion_metrics_dict = {}

    for image_path in image_files:
        # Extract the filename from the image path
        filename = os.path.basename(image_path)
        # Create output paths based on the input image filename
        output_path1 = os.path.join(output_folder, f"output_mean_std_{filename}")
        output_path2 = os.path.join(output_folder, f"output_total_{filename}")

        # Process each image
        print(f"Processing {image_path} with output {output_path1} and {output_path2}")
        # 1. Load the image
        lsci_image = load_image(image_path)

        # 2. Calculate perfusion metrics
        perfusion_metrics = calculate_perfusion(lsci_image)

        # Convert NumPy data types to standard Python data types
        perfusion_metrics = {k: (v.tolist() if isinstance(v, np.ndarray) else int(v) if isinstance(v, np.integer) else v)
                             for k, v in perfusion_metrics.items()}

        # Store the perfusion metrics in the dictionary
        perfusion_metrics_dict[filename] = perfusion_metrics

        # 3. Visualize and save results
        visualize_perfusion(lsci_image, perfusion_metrics, output_path1, output_path2)

    # Save the perfusion metrics dictionary to a JSON file
    json_output_path = os.path.join(output_folder, "perfusion_metrics.json")
    with open(json_output_path, 'w') as json_file:
        json.dump(perfusion_metrics_dict, json_file, indent=4)

def main():
    # Replace with your actual folder paths
    input_folder_path = r"LSCI_outputs"
    output_folder_path = r"LSCI_outputs_perfusion_processed"
    process_images_in_folder(input_folder_path, output_folder_path)

if __name__ == "__main__":
    main()
