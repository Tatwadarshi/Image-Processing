import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

global grey_result, thresh255

# Open the camera
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Define HSV range for green
lower_green = np.array([35, 40, 40])  
upper_green = np.array([85, 255, 255])

# Create Matplotlib figure
fig, ax = plt.subplots(1, 2, figsize=(10, 10))
ret, frame = cam.read()

if not ret:
    print("Error: Camera not capturing frames!")

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
org_im = ax[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  
ax[0].axis('off')
ax[0].set_title('Original')

mask = cv2.inRange(hsv, lower_green, upper_green)

# Fix: Convert mask to uint8 to ensure proper display
mask_im = ax[1].imshow(mask.astype(np.uint8), cmap="gray", vmin=0, vmax=255)  
ax[1].axis('off')
ax[1].set_title('Mask')


def update(_):
    """Update function for Matplotlib animation"""
    global grey_result, thresh255
    ret, frame = cam.read()

    if ret:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Use BGR for consistency
        mask = cv2.inRange(hsv, lower_green, upper_green)
        # flattened_mask = mask.flatten()
        # num_of_whites = 0
        # for i in flattened_mask:
        #     if i != 0:
        #         num_of_whites += 1
        # print(num_of_whites)

        org_im.set_array(rgb)

        # Fix: Ensure grayscale images are displayed correctly
        mask_im.set_array(mask.astype(np.uint8))  
        # result_im.set_array(thresh255.astype(np.uint8))  

    return org_im, mask_im

def on_close(event):
    """Handles closing event of Matplotlib window"""
    print("Closing camera...")
    cam.release()
    cv2.destroyAllWindows()

fig.canvas.mpl_connect('close_event', on_close)

ani = animation.FuncAnimation(fig, update, interval=100, blit=False)
plt.show()
