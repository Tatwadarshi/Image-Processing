import cv2
import numpy as np
import matplotlib.pyplot as plt

reducing_factor = 750

# Read the image
folder_path = "./DATA_SET/"
image = cv2.imread(f"{folder_path}1.jpg")
image = cv2.resize(image, (reducing_factor, reducing_factor))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define lower and upper bounds for green color
lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

# Create a binary mask where green pixels are 255 (white), others are 0 (black)
mask = cv2.inRange(hsv, lower_green, upper_green)

# Apply the mask on the original image using bitwise_and
result = cv2.bitwise_and(image, image, mask=mask)

# Display the results
# cv2.imshow("Original Image", image)
# cv2.imshow("Mask", mask)  # Binary mask (Black & White)
# cv2.imshow("Extracted Leaf", result)  # Only the green part remains

fig, ax = plt.subplots(1, 3, figsize=(10, 10))

ax[0].axis('off')
ax[0].imshow(image)
ax[0].set_title('Original')

# ax[1].axis('off')
ax[1].imshow(mask, cmap='Greys')
ax[1].set_title('Mask')

# ax[2].axis('off')
ax[2].imshow(result)
ax[2].set_title('Extracted Result')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
