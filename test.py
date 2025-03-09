import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    ax.clear()
    ax.imshow(frame_rgb)
    plt.draw()
    # plt.pause(0.01)  # Short pause to update the plot

    if plt.waitforbuttonpress(0.01):  # Stop if any key is pressed
        break

cap.release()
plt.close()