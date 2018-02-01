import cv2
import numpy as np
import math


# TODO Find a way to find the line dead on and not twisted
# TODO Find width of the line and find the midpoint and then plot line between midpoint

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
    for z in range(width):
        for i in range(height):

            red = red_list[i][z]
            blue = blue_list[i][z]
            green = green_list[i][z]

            if not is_red(red, blue, green):
                green_list[i][z] = 0
                blue_list[i][z] = 0
                red_list[i][z] = 0

    pImage = cv2.merge((blue_list, green_list, red_list))

    # find mask of the black stuff
    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    mask = cv2.inRange(pImage, lower, upper)

    gray = cv2.cvtColor(pImage, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.01)
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    pImage[dst > 0.1 * dst.max()] = [0, 255, 0]

    cv2.imshow("dst", pImage)
    cv2.waitKey(0)

    # get contour and craps
    try:
        im2, contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        """
        x1 = [5000, 5000]
        x2 = [0, 0]

        y1 = [5000, 0]
        y2 = [0, 5000]
        """
        contours = max(contour, key=cv2.contourArea)

        """
        for i in range(len(contours)):

            # going right
            if x2[0] < contours[i][0][0]:
                x2 = contours[i][0]

            if x1[1] > contours[i][0][1]:
                x1[1] = contours[i][0][1]

        for z in range(len(contours)-1, 0, -1):

            # going left
            if x1[0] > contours[z][0][0]:
                x1 = contours[z][0]

            if x2[0] < contours[z][0][0]:
                x2[0] = contours[z][0][0]
        """

        # print(x1)
        # print(x2)

        # print(y1)
        # print(y2)

        # cv2.circle(pImage, (x1[0], x1[1]), 7, (255, 0, 0), -1)
        # cv2.circle(pImage, (x2[0], x2[1]), 7, (0, 255, 0), -1)

        """


        cv2.circle(pImage, (y2[0], y2[1]), 7, (255, 0, 0), -1)
        cv2.circle(pImage, (y1[0], y1[1]), 7, (0, 255, 0), -1)

        cv2.line(pImage, (y2[0], y2[1]), (y1[0], y1[1]), (0, 255, 0), thickness=2, lineType=8)
        cv2.line(pImage, (x1[0], x1[1]), (x2[0], x2[1]), (0, 255, 0), thickness=2, lineType=8)

        """

        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        if is_red(red_list[cY][cX], blue_list[cY][cX], green_list[cY][cX]):

            # draw the center of the shape on the image
            cv2.circle(pImage, (cX, cY), 7, (0, 255, 0), -1)

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


# cv2.imshow("IMAGE1", find_line("../Test_Image/Line1.jpg"))
cv2.imshow("IMAGE2", find_line("../Test_Image/Line2.jpg"))
cv2.imshow("IMAGE3", find_line("../Test_Image/Line3.jpg"))
cv2.imshow("IMAGE4", find_line("../Test_Image/Line4.jpg"))
cv2.imshow("IMAGE5", find_line("../Test_Image/Line4.jpg"))
# cv2.imshow("IMAGE7", find_line("../Test_Image/Line7.jpg"))
# cv2.imshow("IMAGE8", find_line("../Test_Image/Line8.jpg"))
cv2.waitKey(0)