import numpy as np
import pytest
from PIL import Image
from table_screenshot_to_csv.src._preprocess_image import preprocess_image

@pytest.fixture
def sample_image_path():
    return "/app/screenshot.png"

def test_preprocess_image_output_type(sample_image_path):
    """Test if the preprocessing function returns an Image object."""
    result = preprocess_image(sample_image_path)
    assert isinstance(result, Image.Image), "The output should be a PIL Image object."

def test_preprocess_image_grayscale(sample_image_path):
    """Test if the preprocessing function converts the image to grayscale."""
    result = preprocess_image(sample_image_path)
    assert result.mode == "L", "The image should be converted to grayscale (mode 'L')."

def test_preprocess_image_thresholding(sample_image_path):
    """Test if the preprocessing function applies thresholding to binarize the image."""
    result = preprocess_image(sample_image_path)
    # Assuming here that thresholding means the image should only contain two colors
    num_colors = len(result.getcolors())
    assert num_colors == 2, "The image should be thresholded to two colors."

def frequency_filter(image, threshold):
    """Filter high-frequency noise from the image.
    
    Helper function that returns the proportion of high-frequency components.
    """
    # Convert image to grayscale if not already
    if image.mode != "L":
        image = image.convert("L")

    # Perform the 2D Fourier Transform using the numpy FFT module
    image_fft = np.fft.fft2(image)

    # Filter out the high-frequency noise
    rows, cols = image.size
    crow, ccol = int(rows / 2), int(cols / 2)
    
    # Remove frequencies beyond a certain distance from the center
    mask = np.zeros((rows, cols), np.uint8)
    center_square = np.array((slice(crow-threshold, crow+threshold), slice(ccol-threshold, ccol+threshold)))
    mask[center_square] = 1

    # Calculate the proportion of high-frequency components
    high_freq_magnitude = np.abs(image_fft * (1 - mask))
    return np.sum(high_freq_magnitude) / np.sum(np.abs(image_fft))

def test_preprocess_image_noise_reduction(sample_image_path):
    """Test if the preprocessing function reduces noise by comparing the proportion of high-frequency components."""
    image = Image.open(sample_image_path)
    before_prop = frequency_filter(image, threshold=20)
    preprocessed_image = preprocess_image(sample_image_path)
    after_prop = frequency_filter(preprocessed_image, threshold=20)
    
    assert after_prop < before_prop, "The preprocessing should reduce the proportion of high-frequency components."
