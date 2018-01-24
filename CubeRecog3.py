import cv2
import numpy as np
import math

# Cam test splits a image and loop through the 3 dimensional list and set a specific parameter for each individual pixel
# TODO it takes 7-10 second to process one single image (Cube 1) make it faster
# TODO look into Numpy and different ways of processing images


img = cv2.imread("Cube2.jpg")

# Split image into 3 two dimensional list
blue_list, green_list, red_list = cv2.split(img)

# TODO find out why it's only detecting a square 960 x 960 pixel image
print(len(blue_list))
print(len(green_list))
print(len(red_list))


# loop through all of red_list to access the array inside
for x in range(len(red_list)):
    # loop through individual values in the inner most list, and those values are the red values of the pixels
    for i in range(len(red_list)):

        # Assign values so it's easier to manage
        red = red_list[i][x]
        blue = blue_list[i][x]
        green = green_list[i][x]

        # Setting the green high and low parameter, it's proportional to red
        green_low = red - 18
        green_high = red + 18

        # difference is the difference between red/green and blue, since blue is not usually used in yellow
        # the difference needs to be big
        difference = (int(green) + int(red))/2 - int(blue)

        # Similarity detects the similarities in red blue and green, used for excluding grey, white, black pixels
        similarity = (abs(int(green)-int(red)) + abs(int(red)-int(blue)) + abs(int(green)-int(blue)))

        # green has to be inside parameter
        green_in_param = green_low <= green <= green_high

        # if the difference bigger between red and blue is higher than 80, it is NOT yellow
        isYellow = difference >= 80

        # if the sum of the differences of all 3 rbg values are within 30, that means that it's grey
        isGrey = similarity <= 30

        # if either of those statements are false, it will set te pixel to black
        if not green_in_param or not isYellow or isGrey:
            green_list[i][x] = 0
            blue_list[i][x] = 0
            red_list[i][x] = 0

final_image = cv2.merge((blue_list, green_list, red_list))
cv2.imshow("processing", np.hstack([img, final_image]))
cv2.waitKey(0)

"""

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask finds all the colors in range of the boundary and blocks out the rest
    mask = cv2.inRange(frame, lower, upper)

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

"""