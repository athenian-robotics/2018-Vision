import cv2
import numpy as np
import math


def plot_line(img, contour, green_list, blue_list, red_list):

    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    x, y, w, h = cv2.boundingRect(contour)

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    red = red_list[cX, cY]
    blue = blue_list[cX, cY]
    green = green_list[cX, cY]

    green_high =
    green_in_param = 0 <= green <= green_high
    blue_in_param = 0 <= blue <= blue_high

    if not green_in_param or not blue_in_param:

        # draw the center of the shape on the image
        cv2.circle(img, (cX, cY), 7, (0, 0, 255), -1)

        # Put words on image
        cv2.putText(img, "X: " + str(cX), (cX - 25, cY - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2)

        cv2.putText(img, "Y: " + str(cY), (cX - 25, cY - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 2)


def find_mask(img):

    # find images that are not black and turn them white
    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    # Use a mask to find the contour and plot the rectangle
    mask = cv2.inRange(img, lower, upper)

    return mask


def find_color(name):

    # print(name)

    img = cv2.imread(name)
    # img = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
    height, width, channels = img.shape
    # Split image into 3 two dimensional list
    blue_list, green_list, red_list = cv2.split(img)

    print("height: " + str(height))
    print("width: " + str(width) + "\n")

    # loop through all of red_list to access the array inside
    for x in range(width):
        # loop through individual values in the inner most list, and those values are the red values of the pixels
        for i in range(height):

            # Assign values so it's easier to manage
            red = red_list[i][x]
            blue = blue_list[i][x]
            green = green_list[i][x]

            # Setting the green high and low parameter, it's proportional to red
            green_high = red - 100
            blue_high = red - 100

            # green has to be inside parameter
            green_in_param = 0 <= green <= green_high
            blue_in_param = 0 <= blue <= blue_high

            # if either of those statements are false, it will set te pixel to black
            if not green_in_param or not blue_in_param:
                green_list[i][x] = 0
                blue_list[i][x] = 0
                red_list[i][x] = 0

    # Merge and create the processed image
    final_image = cv2.merge((blue_list, green_list, red_list))

    try:
        im2, contours, hierarchy = cv2.findContours(find_mask(final_image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        plot_line(final_image, cnt, green_list, green_list, red_list)

    except ValueError:
        pass
    # Return the final image side by side with the original with np.hstack
    # hm = np.hstack([img, name])

    return final_image


cv2.imshow("Line1", find_color("Test_Image/Line1.jpg"))
cv2.imshow("Line2", find_color("Test_Image/Line2.jpg"))
cv2.imshow("Line3", find_color("Test_Image/Line3.jpg"))
cv2.imshow("Line4", find_color("Test_Image/Line4.jpg"))

cv2.waitKey(0)