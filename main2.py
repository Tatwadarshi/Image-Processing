import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import glob
from dropdown import MyDropDown
from tkinter import *
import os

reducing_factor = 750

lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

folder_path = "./DATA_SET/"
image_paths = glob.glob(f"{folder_path}/*.[jJpP][pPnN][gG]")  # Matches .jpg, .png, etc.

def processImage(image_path, reducing_factor=reducing_factor):
    global lower_green, upper_green
    
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (reducing_factor, reducing_factor))

    # Convert to HSV color space
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(resized_image, cv2.COLOR_RGB2HSV)

    # Create a mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Fix: Ensure the mask has the correct shape for bitwise operation
    mask_3ch = cv2.merge([mask, mask, mask])  # Convert (750,750) to (750,750,3)

    # Extract the leaf using bitwise AND
    result = cv2.bitwise_and(resized_image, mask_3ch)

    return resized_image, mask, result

def showImages(images: tuple, labels: tuple):
    plt.close()
    fig, ax = plt.subplots(1, len(images), figsize=(15, 5))

    for i, image in enumerate(images):
        ax[i].axis('off')
        ax[i].imshow(image, cmap="gray" if len(image.shape) == 2 else None)
        ax[i].set_title(labels[i])
    
    plt.show()
    # fig.draw()

def processNShow(e):
    processed_imgs = processImage(image_paths[image_names.index(drop.get_selection())])
    showImages(processed_imgs, ("Original", "Mask", "Result"))

# Process first image
# processed_imgs = processImage(image_paths[0])

# Display results
# showImages(processed_imgs, ("Original", "Mask", "Result"))



image_names = images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg"))]
controls=Tk()
controls.minsize(200, 200)
controls.title('Controls')

drop = MyDropDown(image_names, controls, processNShow, "Choose Sample: ", (0, 0))

controls.mainloop()