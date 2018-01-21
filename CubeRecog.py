import cv2
import numpy as np
import glob


"""
# for i in range(1, 3):
"""

"""
# Convert  image to HSV
hsv = cv2.cvtColor(imgs, cv2.COLOR_BGR2HSV)

# Set color boundary
lower_yellow = np.array([180, 0, 180], dtype=np.uint8) # 180,0,180
upper_yellow = np.array([255, 75, 255], dtype=np.uint8) # 255,275,255

# Make black and white image with only yellow stuff
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
res = cv2.bitwise_and(imgs, imgs, mask=mask)

while True:
    cv2.imshow("images", np.hstack([imgs, res]))


# takes threshold??

cv2.imshow("Show", imgs)
print("Done?")
"""
"""

while (1):
"""
cam = cv2.VideoCapture(1)
# cam.set(cv2.CAP_PROP_EXPOSURE, -4)

while True:

    _, frame = cam.read()

    # create NumPy arrays from the boundaries
    lower = np.array([0, 180, 180], dtype="uint8")
    upper = np.array([155, 255, 255], dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(frame, lower, upper)
    # fil = cv2.bitwise_and(image, image, mask=mask)

    # show the images
    _, thresh = cv2.threshold(mask, 255, 255, 255)

    try:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # cv2.cvtColor(fil, cv2.COLOR_BGR2GRAY)
    except ValueError:
        pass

    cv2.namedWindow('images', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('images', 2400, 1200)
    cv2.imshow("thresh", thresh)
    cv2.imshow("images", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
