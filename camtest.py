import cv2
cam = cv2.VideoCapture(1)
# Basically just to make sure that the camera actually works
while True:
    _,frame = cam.read()
    cv2.imshow('HI', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()