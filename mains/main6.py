import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

global grey_result, thresh255

# Open the camera
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

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
result = cv2.bitwise_and(frame, frame, mask=mask)
grey_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
ret, thresh255 = cv2.threshold(grey_result, 127, 255, cv2.THRESH_BINARY)

# Fix: Convert mask to uint8 to ensure proper display
mask_im = ax[1].imshow(mask.astype(np.uint8), cmap="gray", vmin=0, vmax=255)  
ax[1].axis('off')
ax[1].set_title('Mask')

# Fix: Convert thresholded image to uint8 for proper display
# result_im = ax[2].imshow(thresh255.astype(np.uint8), cmap="gray", vmin=0, vmax=255)  
# ax[2].axis('off')
# ax[2].set_title('Thresholded Result')

def update(_):
    """Update function for Matplotlib animation"""
    global grey_result, thresh255
    ret, frame = cam.read()

    if ret:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Use BGR for consistency
        mask = cv2.inRange(hsv, lower_green, upper_green)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        # grey_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # ret, thresh255 = cv2.threshold(grey_result, 127, 255, cv2.THRESH_BINARY)

        # Debugging prints
        # print(f"Unique values in mask: {np.unique(mask)}")  # Should contain 0 and 255
        # print(f"Unique values in thresholded image: {np.unique(thresh255)}")  # Should contain 0 and 255

        # Show debug mask window
        # cv2.imshow("Mask Debug", mask)
        # cv2.waitKey(1)  

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

ani = animation.FuncAnimation(fig, update, interval=5, blit=False)
plt.show()
