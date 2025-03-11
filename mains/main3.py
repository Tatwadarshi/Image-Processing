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

folder_path = os.path.join(".", "DATA_SET")
image_paths = glob.glob(f"{folder_path}/*.[jJpP][pPnN][gG]")  # Matches .jpg, .png, etc.
image__names = images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".png"))]

def processImage(image_path, lower_green=lower_green, upper_green=upper_green, reducing_factor=reducing_factor):
    
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

def showImages(canvas, images: tuple, labels: tuple):
    for i, image in enumerate(images):
        ax[i].clear()
        ax[i].axis('off')
        ax[i].imshow(image, cmap="gray" if len(image.shape) == 2 else None)
        ax[i].set_title(labels[i])
    canvas.draw()

def processNShow(e):
    selected_image = drop.get_selection()
    if selected_image in image__names:
        processed_imgs = processImage(image_paths[image__names.index(selected_image)], lower_green, upper_green)
    else:
        print(f"Error: Image '{selected_image}' not found.")
        return
    
    showImages(canvas, processed_imgs, ("Original", "Mask", "Result"))
    # print(drop.get_selection())

def val_test(val):
    print(val)

plt.figure(num="My Window")
fig, ax = plt.subplots(1, 3, figsize=(10, 10))


root = Tk()
root.title("Leaf Image Extraction")
drop = MyDropDown(image__names, root, bind_fun=processNShow, label_str="Choose Sample: ", grid_loc=(0, 0))

labelUH = Label(root, text="Upper H:", font=("Arial", 10))
labelUH.grid(row=1, column=0, pady=10)

labelUS = Label(root, text="Upper S:", font=("Arial", 10))
labelUS.grid(row=1, column=1, pady=10)

labelUV = Label(root, text="Upper V:", font=("Arial", 10))
labelUV.grid(row=1, column=2, pady=10)


sliderUH = Scale(root, from_=0, to=360, orient="horizontal", length=300, command=val_test)
sliderUH.grid(row=2, column=0)
sliderUH.set(upper_green[0])

sliderUS = Scale(root, from_=0, to=100, orient="horizontal", length=300, command=val_test)
sliderUS.grid(row=2, column=1)
sliderUS.set(upper_green[1])

sliderUV = Scale(root, from_=0, to=100, orient="horizontal", length=300, command=val_test)
sliderUV.grid(row=2, column=2)
sliderUV.set(upper_green[2])


labelLH = Label(root, text="Lower H:", font=("Arial", 10))
labelLH.grid(row=3, column=0, pady=10)

labelLS = Label(root, text="Lower S:", font=("Arial", 10))
labelLS.grid(row=3, column=1, pady=10)

labelLV = Label(root, text="Lower V:", font=("Arial", 10))
labelLV.grid(row=3, column=2, pady=10)


sliderLH = Scale(root, from_=0, to=360, orient="horizontal", length=300, command=val_test)
sliderLH.grid(row=4, column=0)
sliderLH.set(lower_green[0])

sliderLS = Scale(root, from_=0, to=100, orient="horizontal", length=300, command=val_test)
sliderLS.grid(row=4, column=1)
sliderLS.set(lower_green[1])

sliderLV = Scale(root, from_=0, to=100, orient="horizontal", length=300, command=val_test)
sliderLV.grid(row=4, column=2)
sliderLV.set(lower_green[2])


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=5, column=0, columnspan=3, sticky="nsew")  # Add to Tkinter window

processed_imgs = processImage(image_paths[image__names.index("1.jpg")])
showImages(canvas, processed_imgs, ("Original", "Mask", "Result"))
canvas.draw()  # Render the plot


root.protocol("WM_DELETE_WINDOW", lambda: (plt.close("all"), root.quit()))
root.mainloop()