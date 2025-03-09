import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Open the USB camera with DirectShow (for Windows)
cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

lower_green = np.array([35, 40, 40])  # Lower bound (H: 35, S: 40, V: 40)
upper_green = np.array([85, 255, 255])  # Upper bound (H: 85, S: 255, V: 255)

# Get the frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create a VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# Create a figure and axis for Matplotlib
fig, ax = plt.subplots(1, 3, figsize=(10, 10))
frame = cam.read()[1]
hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
org_im = ax[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Initialize with first frame
ax[0].axis('off')  # Hide axes
ax[0].set_title('Original')

mask = cv2.inRange(hsv, lower_green, upper_green)
result = cv2.bitwise_and(frame, frame, mask=mask)

mask_im = ax[1].imshow(mask)
ax[1].axis('off')
ax[1].set_title('Mask')

result_im = ax[2].imshow(result)
ax[2].axis('off')
ax[2].set_title('Result')



def update(frame):
    """Update function for Matplotlib animation"""
    ret, frame = cam.read()
    if ret:
        # out.write(frame)  # Save frame to video
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        org_im.set_array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert and update image
        mask_im.set_array(mask)
        result_im.set_array(result)
    return org_im, mask_im, result_im

def on_close(event):
    """Handles closing event of Matplotlib window"""
    print("Closing camera...")
    cam.release()
    # out.release()
    cv2.destroyAllWindows()

# Connect the close event to the function
fig.canvas.mpl_connect('close_event', on_close)

# Create an animation loop
ani = animation.FuncAnimation(fig, update, interval=50, blit=False)

plt.show()
