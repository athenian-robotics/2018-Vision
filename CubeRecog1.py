import cv2
import numpy as np
import glob

cam = cv2.VideoCapture(1)
# cam.set(cv2.CAP_PROP_EXPOSURE, -4)

"""
This is a temporary model that works...
(Doesn't work that well)
"""

while True:

    _, frame = cam.read()

    # create NumPy arrays from the boundaries
    lower = np.array([0, 180, 180], dtype="uint8")
    upper = np.array([155, 255, 255], dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(frame, lower, upper)
    # fil = cv2.bitwise_and(image, image, mask=mask)

    _, thresh = cv2.threshold(mask, 255, 255, 255)

    try:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    except ValueError:
        pass

    # Resize Window
    cv2.namedWindow('images', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('images', 2400, 1200)
    cv2.imshow("thresh", thresh)
    cv2.imshow("images", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
