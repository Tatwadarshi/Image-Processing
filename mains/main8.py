import cv2
import numpy as np

# Open the camera
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

show = True

# Define HSV range for green
lower_green = np.array([35, 40, 40])
upper_green = np.array([85, 255, 255])

if not cam.isOpened():
    print("Error: Camera not capturing frames!")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Faster way to count white pixels
    num_of_whites = np.count_nonzero(mask)
    total_pixels = len(mask) * len(mask[0])
    percentageGreenArea = num_of_whites*100/total_pixels
    print(f"{percentageGreenArea}%") 

    # Display images using OpenCV (Much faster)
    if show:
        cv2.imshow('Original', frame)
        cv2.imshow('Mask', mask)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty('Original', cv2.WND_PROP_VISIBLE) < 1:
            break
        if cv2.getWindowProperty('Mask', cv2.WND_PROP_VISIBLE) < 1:
            break

# Release resources
cam.release()
cv2.destroyAllWindows()