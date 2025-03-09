import matplotlib.pyplot as plt
import numpy as np
import time

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create first named window
plt.figure(num="Sine Wave Window")
plt.plot(x, y1, label="sin(x)", color="blue")
plt.legend()
plt.title("Sine Wave")
plt.grid(True)

# Create second named window
plt.figure(num="Cosine Wave Window")
plt.plot(x, y2, label="cos(x)", color="red")
plt.legend()
plt.title("Cosine Wave")
plt.grid(True)

# Show all windows without blocking execution
plt.show(block=False)
plt.waitforbuttonpress(0)



# Select the "Sine Wave Window" and update its plot
plt.figure("Sine Wave Window")
for i in range(5):
    plt.plot(x, np.sin(x + i * 0.5), label=f"sin(x+{i*0.5})")
    plt.legend()
    plt.draw()  # Redraw the updated plot
    plt.pause(1)  # Pause to see the changes
