import cv2
import numpy as np
from matplotlib import pyplot as plt


# TODO make multiple filters for lighting issues

def filter0(frame):

    kernel = np.ones((5, 5), np.float32) / 10
    dst = cv2.filter2D(frame, -1, kernel)
    edges = cv2.Canny(dst, 100, 200)

    cv2.imshow("Edge", edges)


def filter1(frame):

    # create NumPy arrays from the boundaries for color parameters and detections
    lower = np.array([30, 160, 160], dtype="uint8")
    upper = np.array([230, 255, 255], dtype="uint8")

    # mask finds all the colors in range of the boundary and blocks out the rest
    mask = cv2.inRange(frame, lower, upper)

    # transfer frame to hsv for editing purposes
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Split each frame to HSV to decrease or increase brightness
    h, s, v = cv2.split(hsv_frame)
    v += 100
    final_hsv = cv2.merge((h, s, v))

    # background takes final_hsv and is converted to RGB format
    background = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    # Converts mask to HSV so that it could be used to decrease brightness later
    layer1 = cv2.bitwise_and(background, background, mask=mask)

    cv2.imshow("layer1", layer1)

    return layer1


def filter2(layer1):

    # create second layer parameter
    lower = np.array([40, 70, 70], dtype="uint8")
    upper = np.array([100, 100, 100], dtype="uint8")

    mask = cv2.inRange(layer1, lower, upper)

    # transfer frame to hsv for editing purposes
    hsvFrame = cv2.cvtColor(layer1, cv2.COLOR_BGR2HSV)

    # Converts mask to HSV so that it could be used to decrease brightness later
    layer2 = cv2.bitwise_and(layer1, layer1, mask=mask)

    cv2.imshow("mask", mask)
    cv2.imshow("layer2", layer2)

    """"
    try:
        im2, contours, hierarchy = cv2.findContours(wut, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    except ValueError:
        pass
    """


cam = cv2.VideoCapture(1)

# cam.set(cv2.CAP_PROP_EXPOSURE, -4)
while True:
    _, frames = cam.read()
    cv2.imshow("Original", frames)
    filter0(frames)
    filter2(filter1(frames))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()



