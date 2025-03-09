import cv2
import numpy as np

# Load image
folder_path = "./DATA_SET/"
image = cv2.imread(f"{folder_path}1.jpg")
image = cv2.resize(image, (500, 500))

# Function to apply selected effect
def apply_filter(mode):
    if mode == 0:
        return image  # Original
    elif mode == 1:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Grayscale
    elif mode == 2:
        return cv2.Canny(image, 50, 150)  # Edge Detection
    elif mode == 3:
        return cv2.GaussianBlur(image, (15, 15), 0)  # Blur

# Callback function for trackbar
def trackbar_callback(value):
    filtered_img = apply_filter(value)
    cv2.imshow("Image", filtered_img)

# Create OpenCV window
cv2.namedWindow("Image")

# Create a trackbar (acts as a dropdown)
cv2.createTrackbar("Mode", "Image", 0, 3, trackbar_callback)

# Initial display
trackbar_callback(0)

# Wait for user input
cv2.waitKey(0)
cv2.destroyAllWindows()
