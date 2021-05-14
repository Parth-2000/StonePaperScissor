import cv2 as cv
import HandTrackingModule as HTM


cap = cv.VideoCapture(0)

detector = HTM.HandTrackingModule()

while True:
    ret, img = cap.read()
    img = detector.find_hands(img)



    cv.imshow("Image", img)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv.destroyAllWindows()
