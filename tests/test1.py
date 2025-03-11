import cv2
import matplotlib.pyplot as plt

img_file = "./DATA_SET/1.jpg"

reducing_factor = 750
frame = cv2.imread(img_file)
resized_frm = cv2.resize(frame, (reducing_factor, reducing_factor))
rgb_img = cv2.cvtColor(resized_frm, cv2.COLOR_BGR2RGB)
grays_img = cv2.cvtColor(resized_frm, cv2.COLOR_RGB2GRAY)


fig, ax = plt.subplots(1, 5, figsize=(10, 10))

ax[0].axis('off')
ax[0].imshow(rgb_img)
ax[0].set_title('Original')

ax[1].axis('off')
ax[1].imshow(rgb_img[:, :, 0], cmap="Reds")
ax[1].set_title('Reds')

ax[2].axis('off')
ax[2].imshow(rgb_img[:, :, 1], cmap="Greens")
ax[2].set_title('Greens')

ax[3].axis('off')
ax[3].imshow(rgb_img[:, :, 2], cmap="Blues")
ax[3].set_title('Blues')

ax[4].axis('off')
ax[4].imshow(grays_img, cmap="Greys")
ax[4].set_title('Greys')


plt.show()

# cv2.imshow("Sample1", resized_frm)
# cv2.waitKey(0)
# cv2.destroyAllWindows()