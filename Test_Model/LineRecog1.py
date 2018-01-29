import cv2
import numpy as np
import math


def plot_line(img, contour, red_list, blue_list, green_list):

    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])


    if is_red(red_list[cY][cX], blue_list[cY][cX], green_list[cY][cX]):
        # draw the center of the shape on the image
        cv2.circle(img, (cX, cY), 7, (0, 255, 0), -1)

        # Put words on image
        cv2.putText(img, "X: " + str(cX), (cX - 25, cY - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(img, "Y: " + str(cY), (cX - 25, cY - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        # Put words on image
        cv2.putText(img, "NOT A LINE YOU ****", (cX - 25, cY - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)


def is_red(red, blue, green):

    green_high = red - 100
    blue_high = red - 100

    green_in_param = 0 <= green <= green_high
    blue_in_param = 0 <= blue <= blue_high

    return green_in_param and blue_in_param


def find_mask(img):

    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    mask = cv2.inRange(img, lower, upper)

    return mask


def dist(point1, point2):
    return np.sqrt(np.square(point2[0] - point1[0]) + np.square(point2[1] - point1[1]))


def find_color(name):

    print(name)

    img = cv2.imread(name)

    height, width, channels = img.shape

    blue_list, green_list, red_list = cv2.split(img)

    print("height: " + str(height))
    print("width: " + str(width) + "\n")
    for x in range(width):
        for i in range(height):

            # check if a specific pixel is red
            red = red_list[i][x]
            blue = blue_list[i][x]
            green = green_list[i][x]

            if not is_red(red, blue, green):
                green_list[i][x] = 0
                blue_list[i][x] = 0
                red_list[i][x] = 0

    chicken = cv2.merge((blue_list, green_list, red_list))

#######################################################################################################################
#######################################################################################################################

    red_m = find_mask(chicken)

    chicken = np.copy(chicken)
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
            cv2.line(chicken, p1, p2, (0, 255, 0), 2)
            print(dist(p1, p2))
    except:
        pass

#######################################################################################################################
#######################################################################################################################

    try:
        im2, contours, hierarchy = cv2.findContours(red_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        plot_line(chicken, cnt, red_list, blue_list, green_list)

    except ValueError:
        pass

    return chicken


cv2.imshow("Line1", find_color("Test_Image/Line1.jpg"))
cv2.imshow("Line2", find_color("Test_Image/Line2.jpg"))
cv2.imshow("Line3", find_color("Test_Image/Line3.jpg"))
cv2.imshow("Line4", find_color("Test_Image/Line4.jpg"))

cv2.waitKey(0)