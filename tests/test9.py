import cv2
import numpy as np
import os
import glob
from tkinter import *
import sys
sys.path.append("./")
from dropdown import MyDropDown


# Define HSV range for green
lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

reducing_factor = 500


folder_path = os.path.join(".", "DATA_SET")
image_paths = glob.glob(f"{folder_path}/*.[jJpP][pPnN][gG]")  # Matches .jpg, .png, etc.
image__names = images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".png"))]

def liveFromCamera(camNo):
    # Open the camera
    cam = cv2.VideoCapture(camNo, cv2.CAP_DSHOW)

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
        print(f"{num_of_whites*100/total_pixels}%")

        # Display images using OpenCV (Much faster)
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

def fromDataset(image_path):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (reducing_factor, reducing_factor))
    hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    num_of_whites = np.count_nonzero(mask)
    total_pixels = len(mask) * len(mask[0])
    print(f"{num_of_whites*100/total_pixels}%")

    # Display images using OpenCV
    cv2.imshow('Original', resized_image)
    cv2.imshow('Mask', mask)

    # Return on pressing 'q'
    if cv2.waitKey(0) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        return
    if cv2.getWindowProperty('Original', cv2.WND_PROP_VISIBLE) < 1:
        cv2.destroyAllWindows()
        return
    if cv2.getWindowProperty('Mask', cv2.WND_PROP_VISIBLE) < 1:
        cv2.destroyAllWindows()
        return

def processNShow(e):
    # print(drop.get_selection())
    selected_opt = drop.get_selection()
    if selected_opt == "0: Default Cam":
        liveFromCamera(0);
    if selected_opt == "1: USB Cam":
        liveFromCamera(1);
    if selected_opt in image__names:
        fromDataset(image_paths[image__names.index(selected_opt)])

# liveFromCamera()
# fromDataset(image_paths[0])


root = Tk()
root.title("Leaf Image Extraction")

drop_list = image__names
drop_list.append("0: Default Cam")
drop_list.append("1: USB Cam")
drop = MyDropDown(image__names, root, bind_fun=processNShow, label_str="Choose Source: ", grid_loc=(0, 0))

root.mainloop()
