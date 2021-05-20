import cv2 as cv
import HandTrackingModule as HTM

TEXT_POS = (30, 30)
FONT = cv.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
COLOR = (0, 255, 255)
THICKNESS = 2
LINE_TYPE = cv.LINE_AA

cap = cv.VideoCapture(0)

detector = HTM.HandTrackingModule()

tip = [8, 12, 16, 20]


def render_text(image, text):
    cv.putText(image, text, TEXT_POS, FONT, FONT_SCALE, COLOR, THICKNESS, LINE_TYPE)


while True:
    ret, img = cap.read()
    img = detector.find_hands(img)
    landmarksList = detector.find_position(img, draw=False)

    if landmarksList != 0:
        fingerArr = []
        flag = False
        for i in tip:
            try:
                if landmarksList[i][2] < landmarksList[i-2][2]:
                    fingerArr.append(1)
                else:
                    fingerArr.append(0)
            except IndexError:
                flag = True
                break
        if not flag:
            ones = fingerArr.count(1)
            zeros = fingerArr.count(0)
            if ones == 4:
                render_text(img, "Paper")
            elif zeros == 4:
                render_text(img, "Stone")
            elif ones == 3 or ones == 1:
                render_text(img, "Invalid Symbol")
            elif ones == 2:
                if fingerArr[0] == 1 and fingerArr[1] == 1:
                    render_text(img, "Scissor")
                else:
                    render_text(img, "Invalid Symbol")

    cv.imshow("Image", img)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv.destroyAllWindows()
