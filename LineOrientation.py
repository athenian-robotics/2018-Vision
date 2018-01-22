import cv2
import numpy as np

cap = cv2.VideoCapture(1)
# TODO actually find lines, this is just boiler plate

while 1:
    ret, frame = cap.read()

    cv2.imshow('Frame', cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
