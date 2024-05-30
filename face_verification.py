import cv2
import os
import numpy as np


def compare_images(image1_path, image2_path):
    # Load images
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Check if images are loaded properly
    if img1 is None or img2 is None:
        raise ValueError("One of the images could not be loaded.")

    # Resize images to the same size (if necessary)
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Calculate Structural Similarity Index (SSI)
    score = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    (_, maxVal, _, _) = cv2.minMaxLoc(score)

    return maxVal


def is_image_valid(input_image_path, valid_users_folder, threshold=0.9):
    for filename in os.listdir(valid_users_folder):
        valid_image_path = os.path.join(valid_users_folder, filename)
        similarity = compare_images(input_image_path, valid_image_path)
        print(f"Comparing with {filename}, similarity: {similarity}")
        if similarity >= threshold:
            return True, filename
    return False, None


# Example usage:
# input_image_path = "test_user1.jpg"
# valid_users_folder = "verified_users"
#
# is_valid, matched_image = is_image_valid(input_image_path, valid_users_folder)
# if is_valid:
#     print(f"Image matches with {matched_image}, {is_valid}")
# else:
#     print(f"No match found {is_valid}")
