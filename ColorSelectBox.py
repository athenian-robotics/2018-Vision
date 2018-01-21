import cv2
import numpy as np
from typing import Tuple

cam = cv2.VideoCapture(1)
firstRun = True
shape = center = P1 = P2 = 0
OFFSET = 5


# TODO rewrite in c/c++
def avg_colors(colorBox: np.ndarray) -> Tuple[int, int, int]:
    r_sum = g_sum = b_sum = 0
    for row in colorBox:
        for col in row:
            b_sum += col[0]
            g_sum += col[1]
            r_sum += col[2]
    b_sum //= (colorBox.shape[0] * colorBox.shape[1])
    g_sum //= (colorBox.shape[0] * colorBox.shape[1])
    r_sum //= (colorBox.shape[0] * colorBox.shape[1])
    return int(b_sum), int(g_sum), int(r_sum)


while 1:
    ret, frame = cam.read()
    if firstRun:
        shape = frame.shape
        center = (int(shape[0] / 2), int(shape[1] / 2))
        P1 = (center[1] - OFFSET, center[0] - OFFSET)
        P2 = (center[1] + OFFSET, center[0] + OFFSET)
        firstRun = False
    colorBox = frame[P1[1]:P2[1], P1[0]:P2[0]]
    cv2.imshow('colorBox', colorBox)
    color = avg_colors(colorBox)
    print(color)
    cv2.rectangle(frame, P1, P2, (0, 0, 255))
    cv2.rectangle(frame, (0, 0), (20, 20), color, thickness=-1)
    cv2.imshow(str(shape), frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
