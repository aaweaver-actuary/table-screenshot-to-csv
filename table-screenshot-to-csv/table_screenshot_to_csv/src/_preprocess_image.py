from PIL import Image, ImageFilter, ImageOps
import numpy as np
import cv2

def preprocess_image(image_path:str) -> Image:
    """Preprocess the input image for better OCR recognition.
    
    This function performs the following steps:
    1. Convert the image to grayscale.
    2. Apply thresholding to binarize the image.
    3. Resize the image to a standard size.
    4. Reduce noise in the image.
    5. Deskew the image.

    Parameters
    ----------
    image_path : str
        The path to the input image file.

    Returns
    -------
    Image
        Preprocessed image ready for OCR.
    """   
    image = Image.open(image_path)      # Load the image
    image = ImageOps.grayscale(image)   # Convert to grayscale
    
    # Apply thresholding to binarize the image
    thresholded_image = image.point(lambda x: 0 if x<128 else 255, "1")
    
    
    standard_size = (1000, 1000) # Resize the image to a standard size if needed
    resized_image = thresholded_image.resize(standard_size, Image.ANTIALIAS)
    
    # Noise reduction - using a median filter here
    image_np = np.array(resized_image) # Convert image to np.array for filtering
    denoised_image_np = cv2.medianBlur(image_np, 5) # Apply median filter
    
    # Return the deskewed image
    return deskew_image(Image.fromarray(denoised_image_np))

def deskew_image(image: Image) -> Image:
    """Deskew the given PIL image.
    
    Uses edge detection and line finding to determine skew.

    Steps:
    1. Detect edges in the image using Canny edge detection.
    2. Use Hough transform to detect lines in the image.
    3. Calculate the average angle of the lines.
    4. Rotate the image to deskew it.
        
    Parameters
    ----------
    image : Image
        The input image to deskew.

    Returns
    -------
    Image
        Deskewed image.
    """
    image_np = np.array(image) # Convert to numpy
    edges = cv2.Canny(image_np, 50, 150, apertureSize=3) # Detect edges
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200) # Hough transform
    
    if lines is not None:
        # Calculate the average angle of the lines
        average_angle_rad = np.mean([theta for _, theta in lines[:, 0]])
        angle_degrees = average_angle_rad * (180/np.pi)
        
        # Adjust angle to be relative to the image axes
        skew_angle = angle_degrees - 90
        
        # Rotate the image to deskew it
        center = tuple(np.array(image_np.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(center, skew_angle, 1.0)
        result_np = cv2.warpAffine(image_np, rot_mat, image_np.shape[1::-1], flags=cv2.INTER_LINEAR)
        
        # Convert back to PIL image
        result_image = Image.fromarray(result_np)
    else:
        # If no lines are detected, return the original image
        result_image = image
    
    return result_image