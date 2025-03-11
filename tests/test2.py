import cv2
import numpy as np
import matplotlib.pyplot as plt

reducing_factor = 750

# Step 1: Load the image
image = cv2.imread("./DATA_SET/4.jpg")  # Replace with your image path

resized_img = cv2.resize(image, (reducing_factor, reducing_factor))



# Step 2: Convert to HSV color space
resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(resized_img, cv2.COLOR_RGB2HSV)

# Step 3: Define Green Color Range in HSV
lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

# Step 4: Create a mask for green color
mask = cv2.inRange(hsv, lower_green, upper_green)

# Step 5: Extract the leaf using bitwise AND
result = cv2.bitwise_and(resized_img, resized_img, mask=mask)

# Step 6: Apply Morphological Operations (Optional - for noise removal)
kernel = np.ones((5, 5), np.uint8)
mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Step 7: Show the images:

# cv2.imshow("Original Image", resized_img)
# cv2.imshow("Green Mask", mask)
# cv2.imshow("Extracted Leaf", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

fig, ax = plt.subplots(1, 4, figsize=(10, 10))

ax[0].axis('off')
ax[0].imshow(resized_img)
ax[0].set_title('Original')

ax[1].axis('off')
ax[1].imshow(mask)
ax[1].set_title('Mask')

ax[2].axis('off')
ax[2].imshow(result)
ax[2].set_title('Result')

ax[3].axis('off')
ax[3].imshow(mask_cleaned)
ax[3].set_title('Mask cleaned')

plt.show()