import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

reducing_factor = 750

lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

folder_path = "./DATA_SET/"
image_paths = glob.glob(f"{folder_path}/*.[jJpP][pPnN][gG]")  # Matches .jpg, .png, etc.

def processImage(image_path, reducing_factor=reducing_factor):
    global lower_green, upper_green
    
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (reducing_factor, reducing_factor))

    # Step 2: Convert to HSV color space
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(resized_image, cv2.COLOR_RGB2HSV)

    # Step 4: Create a mask for green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Step 5: Extract the leaf using bitwise AND
    result = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    # Step 6: Apply Morphological Operations (Optional - for noise removal)
    # kernel = np.ones((5, 5), np.uint8)
    # mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return resized_image, mask, result

def showImages(images: tuple, labels: tuple):
    fig, ax = plt.subplots(1, len(images), figsize=(10, 10))

    for image in images:
        # ax[images.index(image)].axis('off')
        # ax[images.index(image)].imshow(image)
        # ax[images.index(image)].set_title(labels[images.index(image)])
        print(images.index(image))

    # plt.show()
    

processed_imgs = processImage(image_paths[0])

showImages(processed_imgs, ("Original", "Mask", "Result"))
