import cv2
import numpy as np
import math

# Cam test splits a image and loop through the 3 dimensional list and set a specific parameter for each individual pixel
# TODO it takes 7-10 second to process one single image (Cube 1) make it faster
# TODO look into Numpy and different ways of processing images

"""
This is a model that works but probably could not be implemented without optimization. Takes too long for one image 
to process (7-10 seconds)
"""

# TODO Find pixel of Camera so that the pixels are aligned


def find_centroid(contour, img):

    try:

        # compute the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    except ZeroDivisionError:
        pass
    # draw the center of the shape on the image
    cv2.circle(img, (cX, cY), 7, (0, 0, 255), -1)

    # Put words on image
    cv2.putText(img, "X: " + str(cX), (cX - 25, cY - 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(img, "Y: " + str(cY), (cX - 25, cY - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    print("X: " + str(cX) + " Y: " + str(cY) + "\n")

    return img


def find_edges(mask):

    # Tying to use edge detection for finding edges, not really necessary
    kernel = np.ones((5, 5), np.float32) / 10
    dst = cv2.filter2D(mask, -1, kernel)
    edges = cv2.Canny(dst, 100, 200)

    return edges


def find_mask(img):

    # find images that are not black and turn them white
    lower = np.array([1, 1, 1], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    # Use a mask to find the contour and plot the rectangle
    mask = cv2.inRange(img, lower, upper)

    return mask


def find_color(name):

    # print(name)

    # img = cv2.imread(name)
    img = cv2.resize(name, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    height, width, channels = img.shape
    # Split image into 3 two dimensional list
    blue_list, green_list, red_list = cv2.split(img)

    # print("height: " + str(height))
    # print("width: " + str(width))

    # loop through all of red_list to access the array inside
    for x in range(width):
        # loop through individual values in the inner most list, and those values are the red values of the pixels
        for i in range(height):

            # Assign values so it's easier to manage
            red = red_list[i][x]
            blue = blue_list[i][x]
            green = green_list[i][x]

            # Setting the green high and low parameter, it's proportional to red
            green_low = red - 30
            green_high = red + 18

            # difference is the difference between red/green and blue, since blue is not usually used in yellow
            # the difference needs to be big
            difference = (int(green) + int(red))/2 - int(blue)

            # Similarity detects the similarities in red blue and green, used for excluding grey, white, black pixel
            similarity = (abs(int(green)-int(red)) + abs(int(red)-int(blue)) + abs(int(green)-int(blue)))

            # green has to be inside parameter
            green_in_param = green_low <= green <= green_high

            # if the difference bigger between red and blue is higher than 80, it is NOT yellow
            isYellow = difference >= 55

            # if the sum of the differences of all 3 rbg values are within 30, that means that it's grey
            isGrey = similarity <= 30

            # if either of those statements are false, it will set te pixel to black
            if not green_in_param or not isYellow or isGrey:
                green_list[i][x] = 0
                blue_list[i][x] = 0
                red_list[i][x] = 0

    # Merge and create the processed image
    final_image = cv2.merge((blue_list, green_list, red_list))

    try:
        im2, contours, hierarchy = cv2.findContours(find_mask(final_image), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cnt)
        find_centroid(cnt, final_image)
        cv2.rectangle(final_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    except ValueError:
        pass
    # Return the final image side by side with the original with np.hstack
    # hm = np.hstack([img, name])
    return final_image


cam = cv2.VideoCapture(0)

# cam.set(cv2.CAP_PROP_EXPOSURE, -4)
while True:
    _, frames = cam.read()
    # Resize Window
    cv2.namedWindow('Processed', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Processed', 2400, 1200)
    # cv2.imshow("Original", frames)
    cv2.imshow("Processed", find_color(frames))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

"""
Cube1 = find_color("Test_Image/Cube1.jpg")
Cube2 = find_color("Test_Image/Cube2.jpg")
Cube3 = find_color("Test_Image/Cube3.jpg")
Cube4 = find_color("Test_Image/Cube4.jpg")
Cube5 = find_color("Test_Image/Cube5.jpg")
Cube6 = find_color("Test_Image/Cube6.jpg")
Cube7 = find_color("Test_Image/Cube7.jpg")
Cube8 = find_color("Test_Image/Cube8.jpg")

cv2.imshow("Cube1", Cube1)
cv2.imshow("Cube2", Cube2)
cv2.imshow("Cube3", Cube3)
cv2.imshow("Cube4", Cube4)
cv2.imshow("Cube5", Cube5)
cv2.imshow("Cube6", Cube6)
cv2.imshow("Cube7", Cube7)
cv2.imshow("Cube8", Cube8)
cv2.waitKey(0)
"""