import cv2
import numpy as np
import math

img = cv2.imread("Cube2.jpg")
blue_list, green_list, red_list = cv2.split(img)

print(len(blue_list))
print(len(green_list))
print(len(red_list))

for x in range(len(red_list)):
    for i in range(len(red_list)):
        red = red_list[i][x]
        blue = blue_list[i][x]
        green = green_list[i][x]

        green_low = red - 18
        green_high = red + 18
        difference = (int(green) + int(red))/2 - int(blue)
        similarity = (abs(int(green)-int(red)) + abs(int(red)-int(blue)) + abs(int(green)-int(blue)))

        lower = np.array([20, green_high, red], dtype="uint8")
        upper = np.array([170, green_low, red], dtype="uint8")

        # print("red is: " + str(red))
        # print("blue is: " + str(blue))
        # print("green is: " + str(green))

        if not (green_low <= green <= green_high) or difference <= 80 or similarity <= 30:
            green_list[i][x] = 0
            blue_list[i][x] = 0
            red_list[i][x] = 0
            wtf = True
            # print(str(wtf))


final_image = cv2.merge((blue_list, green_list, red_list))
cv2.imshow("FUCK YOU", np.hstack([img, final_image]))
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