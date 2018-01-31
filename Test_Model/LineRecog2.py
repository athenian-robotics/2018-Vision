import cv2
import numpy as np
import math

# TODO Find a way to find the line dead on and not twisted


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

    # get contour and craps
    try:
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        right_low_x = 0
        right_low_y = 0

        p1_high = []
        right_high_y = 0

        p2_low = []
        left_low_y = 5000
        cnt = max(contours, key=cv2.contourArea)

        for i in range(len(contours[0])):

            right_low_y = contours[0][i][0][1] if right_low_y <= contours[0][i][0][1] else right_low_y
            right_low_x = contours[0][i][0][0] if right_low_x <= contours[0][i][0][0] else right_low_x

            if right_high_y <= contours[0][i][0][1]:
                right_high_y = contours[0][i][0][1]
                p1_high = contours[0][i][0]

            if left_low_y >= contours[0][i][0][1]:
                left_low_y = contours[0][i][0][1]
                p2_low = contours[0][i][0]

        left_high_x = 5000
        left_high_y = 5000

        for z in range(len(contours[0])-1, 0, -1):
            left_high_x = contours[0][z][0][0] if left_high_x >= contours[0][z][0][0] else left_high_x
            left_high_y = contours[0][z][0][1] if left_high_y >= contours[0][z][0][1] else left_high_y

        p1_low = [right_low_x, right_low_y]
        p2_high = [left_high_x, left_high_y]

        print(p1_low)
        print(p1_high)

        print(p2_low)
        print(p2_high)

        cv2.circle(pImage, (p1_low[0], p1_low[1]), 7, (0, 255, 0), -1)
        cv2.circle(pImage, (p1_high[0], p1_high[1]), 7, (0, 255, 0), -1)
        cv2.circle(pImage, (p2_high[0], p2_high[1]), 7, (0, 255, 0), -1)
        cv2.circle(pImage, (p2_low[0], p2_low[1]), 7, (0, 255, 0), -1)

        cv2.line(pImage, (p2_high[0], p2_high[1]), (p1_low[0], p1_low[1]), (0, 255, 0), thickness=2, lineType=8)
        cv2.line(pImage, (p2_low[0], p2_low[1]), (p1_high[0], p1_high[1]), (0, 255, 0), thickness=2, lineType=8)

        M = cv2.moments(cnt)
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


#cv2.imshow("IMAGE1", find_line("../Test_Image/Line1.jpg"))
# cv2.imshow("IMAGE2", find_line("../Test_Image/Line2.jpg"))
# cv2.imshow("IMAGE3", find_line("../Test_Image/Line3.jpg"))
cv2.imshow("IMAGE4", find_line("../Test_Image/Line4.jpg"))

cv2.waitKey(0)