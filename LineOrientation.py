import cv2
import numpy as np


def dist(point1, point2):
    return np.sqrt(np.square(point2[0] - point1[0]) + np.square(point2[1] - point1[1]))


cap = cv2.VideoCapture(1)
# TODO actually find lines, this is just boiler plate
# upper_white = np.uint8([255, 255, 255])
# lower_white = np.uint8([230, 230, 230])
# upper_black = np.uint8([110, 110, 110])
# lower_black = np.uint8([0, 0, 0])
upper_red = np.uint8([190, 190, 255])
lower_red = np.uint8([110, 110, 215])
# upper_blue = np.uint8([255, 245, 220])
# lower_blue = np.uint8([210, 165, 135])
# TODO Make sure that the RGB values are within acceptable range for the black and white detection
# TODO Maybe write the above in a lower level language
p1 = p2 = 0
while 1:
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    # white_m = cv2.inRange(frame, lower_white, upper_white)
    # black_m = cv2.inRange(frame, lower_black, upper_black)
    # blue_m = cv2.inRange(frame, lower_blue, upper_blue)
    red_m = cv2.inRange(frame, lower_red, upper_red)

    img_cpy = np.copy(frame)
    lines = cv2.HoughLines(red_m, 1, np.pi / 180, 200)
    try:
        for r, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * r
            y0 = b * r
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * a)
            p1 = (x1, y1)
            p2 = (x2, y2)
            cv2.line(img_cpy, p1, p2, (0, 0, 255), 2)
    except:
        print('No Line found')
    print(dist(p1, p2))
    cv2.imshow('Canny', red_m)
    cv2.imshow('Original', img_cpy)
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('\x1b'):
        break
cap.release()
cv2.destroyAllWindows()
