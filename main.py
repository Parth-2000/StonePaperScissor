import cv2 as cv
import HandTrackingModule as HTM
import time
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TEXT_POS = (30, 30)
FONT = cv.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
COLOR = (0, 255, 255)
THICKNESS = 2
LINE_TYPE = cv.LINE_AA
MOVES = ["Stone", "Paper", "Scissor"]
TIMER = 3
WIN_SCORE = 1
COMP_SCORE = 0
USER_SCORE = 0
USER_CHOICE = ""

res = ""
res_img = np.zeros((500, 500, 3), np.uint8)
final_text = ""
final_result = []
tip = [8, 12, 16, 20]

cap = cv.VideoCapture(0)
detector = HTM.HandTrackingModule()


def win(c_choice, u_choice):
    if c_choice == u_choice:
        return "Draw"
    if (c_choice == MOVES[0] and u_choice == MOVES[1]) \
            or (c_choice == MOVES[1] and u_choice == MOVES[2]) \
            or (c_choice == MOVES[2] and u_choice == MOVES[0]):
        return "Win"
    return "Lose"


def render_text(image, text):
    cv.putText(image, text, TEXT_POS, FONT, FONT_SCALE, COLOR, THICKNESS, LINE_TYPE)


start_time = time.time()

while True:
    ret, img = cap.read()
    img = detector.find_hands(img)
    landmarksList = detector.find_position(img, draw=False)

    if landmarksList != 0:
        fingerArr = []
        flag = False
        for i in tip:
            try:
                if landmarksList[i][2] < landmarksList[i - 2][2]:
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
                render_text(img, MOVES[1])
                USER_CHOICE = MOVES[1]
            elif zeros == 4:
                render_text(img, MOVES[0])
                USER_CHOICE = MOVES[0]
            elif fingerArr[0] == 1 and fingerArr[1] == 1:
                render_text(img, "Scissor")
                USER_CHOICE = MOVES[2]
            else:
                render_text(img, "Invalid Symbol")
                USER_CHOICE = "Invalid"
            cv.putText(img, f"Computer:{COMP_SCORE} User:{USER_SCORE}",
                       (250, 30), FONT, FONT_SCALE / 2, COLOR, 1, LINE_TYPE)

    if int(time.time() - start_time) == TIMER:
        comp_choice = random.choice(MOVES)
        print(comp_choice)
        if USER_CHOICE in MOVES:
            res = win(comp_choice, USER_CHOICE)
        if res == "Win":
            USER_SCORE += 1
        elif res == "Lose":
            COMP_SCORE += 1
        final_result.append([USER_CHOICE, comp_choice, res, USER_SCORE, COMP_SCORE])
        start_time = time.time()
    else:
        print(f"Be ready with your choice in {TIMER - (int(time.time() - start_time))} seconds.")

    cv.imshow("Image", img)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

    if COMP_SCORE == WIN_SCORE or USER_SCORE == WIN_SCORE:
        break

cap.release()
cv.destroyAllWindows()

if COMP_SCORE == WIN_SCORE:
    final_text = "You Lost :("
else:
    final_text = "You Won :)"

fig, ax = plt.subplots(1, 1)

column_labels = ["Your Choice", "Comp Choice", "Result", "Your Score", "Comp Score"]
df = pd.DataFrame(final_result, columns=column_labels)
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df.values, colLabels=df.columns, loc="center")
plt.title(final_text)
plt.text(-0.03, 0.04, f"Your Score:{USER_SCORE} Comp Score:{COMP_SCORE}", fontsize=12)
plt.show()

