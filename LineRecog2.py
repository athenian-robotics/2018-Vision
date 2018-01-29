import cv2
import numpy as np
import math

# TODO Change the way it plots the lines, make it go from centroid to side not corner to corner (Step 1)
# TODO Find the angle (Step 2)

def is_red(red, blue, green):

    green_high = red - 100
    blue_high = red - 100

    green_in_param = 0 <= green <= green_high
    blue_in_param = 0 <= blue <= blue_high

    return green_in_param and blue_in_param


def find_line(name):

    print(name)

    img = cv2.imread(name)

    height, width, channels = img.shape
    blue_list, green_list, red_list = cv2.split(img)

    print("height: " + str(height))
    print("width: " + str(width) + "\n")

    # loop through craps and return a merged image with black stuff
    for x in range(width):
        for i in range(height):

            red = red_list[i][x]
            blue = blue_list[i][x]
            green = green_list[i][x]

            if not is_red(red, blue, green):
                green_list[i][x] = 0
                blue_list[i][x] = 0
                red_list[i][x] = 0

    pImage = cv2.merge((blue_list, green_list, red_list))

    # find mask of the black stuff
    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    mask = cv2.inRange(pImage, lower, upper)

    # get contour and craps
    try:

        lines = cv2.HoughLines(mask, 1, np.pi / 180, 200)
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
            cv2.line(pImage, p1, p2, (0, 255, 0), 2)

            print(np.sqrt(np.square(p1[0] - p1[0]) + np.square(p2[1] - p1[1])))

        print("CHECK-1")
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)

        # get centroid
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        print("CHECK1")

        if is_red(red_list[cY][cX], blue_list[cY][cX], green_list[cY][cX]):

            print("CHECK2")
            # draw the center of the shape on the image
            cv2.circle(pImage, (cX, cY), 7, (0, 255, 0), -1)

            print("CHECK3")
            # Put words on image
            cv2.putText(pImage, "X: " + str(cX), (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.putText(pImage, "Y: " + str(cY), (cX - 25, cY - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            # Put words on image
            cv2.putText(pImage, "NOT A LINE YOU ****", (cX - 25, cY - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    except:
        print("WTF")
        pass
    
    return pImage


cv2.imshow("IMAGE1", find_line("Test_Image/Line1.jpg"))
cv2.imshow("IMAGE2", find_line("Test_Image/Line2.jpg"))
cv2.imshow("IMAGE3", find_line("Test_Image/Line3.jpg"))
cv2.imshow("IMAGE4", find_line("Test_Image/Line4.jpg"))

cv2.waitKey(0)