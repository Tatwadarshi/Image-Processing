import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import glob
from tkinter import *
import sys
sys.path.append("./")
from dropdown import MyDropDown


import os

reducing_factor = 750

# lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
# upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

folder_path = os.path.join(".", "DATA_SET")
image_paths = glob.glob(f"{folder_path}/*.[jJpP][pPnN][gG]")  # Matches .jpg, .png, etc.
image__names = images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".png"))]

def processImage(image_path, reducing_factor=reducing_factor):
    
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (reducing_factor, reducing_factor))

    # Convert to HSV color space
    rgb_img = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    reds = rgb_img[:, :, 0]
    greens = rgb_img[:, :, 1]
    blues = rgb_img[:, :, 2]

    return (rgb_img, reds, greens, blues)

def showImages(canvas, images: tuple, labels: tuple):
    for i, image in enumerate(images):
        ax[i].clear()
        # ax[i].axis('off')
        ax[i].imshow(image, cmap=labels[i] if len(image.shape) == 2 else None)
        ax[i].set_title(labels[i])
    canvas.draw()

def processNShow(e):
    selected_image = drop.get_selection()
    if selected_image in image__names:
        processed_imgs = processImage(image_paths[image__names.index(selected_image)])
    else:
        print(f"Error: Image '{selected_image}' not found.")
        return
    
    showImages(canvas, processed_imgs, ("Original", "Reds", "Greens", "Blues"))

plt.figure(num="My Window")
fig, ax = plt.subplots(1, 4, figsize=(10, 10))
fig.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.1, wspace=0.3)

root = Tk()
root.title("Leaf Image Extraction")

drop = MyDropDown(image__names, root, bind_fun=processNShow, label_str="Choose Sample: ", grid_loc=(0, 0))

canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().grid(row=0, column=3, rowspan=10, sticky="nsew", pady=0)  # Add to Tkinter window
canvas.get_tk_widget().grid(row=5, column=0, columnspan=4, sticky="nsew", pady=5)

root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)

processed_imgs = processImage(image_paths[image__names.index("1.jpg")])
showImages(canvas, processed_imgs, ("Original", "Reds", "Greens", "Blues"))
canvas.draw()  # Render the plot


root.protocol("WM_DELETE_WINDOW", lambda: (plt.close("all"), root.quit()))
root.mainloop()