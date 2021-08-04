import cv2 as cv
import HandTrackingModule as HTM
import time
import random
# import numpy as np
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
WIN_SCORE = 3
COMP_SCORE = 0
USER_SCORE = 0
USER_CHOICE = ""

res = ""
# res_img = np.zeros((500, 500, 3), np.uint8)
final_text = ""
final_result = []
tip = [8, 12, 16, 20]

cap = cv.VideoCapture(0)
detector = HTM.HandTrackingModule()


# Calculate Result
def win(c_choice, u_choice):
    if c_choice == u_choice:
        return "Draw"
    if (c_choice == MOVES[0] and u_choice == MOVES[1]) \
            or (c_choice == MOVES[1] and u_choice == MOVES[2]) \
            or (c_choice == MOVES[2] and u_choice == MOVES[0]):
        return "Win"
    return "Lose"


# Show Gesture Detected
def render_text(image, text):
    cv.putText(image, text, TEXT_POS, FONT, FONT_SCALE, COLOR, THICKNESS, LINE_TYPE)


# Show Counter
def show_counter(image, text, ct):
    cv.rectangle(image, (390, 10), (620, 100), (0, 0, 0), -1, cv.LINE_AA)
    cv.putText(image, text,
               (400, 40), FONT, FONT_SCALE / 1.5, COLOR, 1, LINE_TYPE)
    cv.putText(image, f"{TIMER - ct} seconds",
               (400, 80), FONT, FONT_SCALE * 1.25, COLOR, 1, LINE_TYPE)


# Show Score
def show_score(img, COMP_SCORE, USER_SCORE):
    cv.rectangle(img, (180, 10), (360, 40), (0, 0, 0), -1, cv.LINE_AA)
    cv.putText(img, f"Computer:{COMP_SCORE} User:{USER_SCORE}",
               (200, 30), FONT, FONT_SCALE / 2, COLOR, 1, LINE_TYPE)


# Show Counter
def computer_previous_choice(image, text, choice):
    cv.rectangle(image, (390, 105), (620, 195), (0, 0, 0), -1, cv.LINE_AA)
    cv.putText(image, text,
               (400, 135), FONT, FONT_SCALE / 2, COLOR, 1, LINE_TYPE)
    cv.putText(image, f"{choice}",
               (400, 175), FONT, FONT_SCALE * 1.25, COLOR, 1, LINE_TYPE)


start_time = time.time()

previous_computer_choice = "( * _ * )"

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
            elif fingerArr[0] == 1 and fingerArr[1] == 1 and fingerArr[2] == 0 and fingerArr[3] == 0:
                render_text(img, "Scissor")
                USER_CHOICE = MOVES[2]
            else:
                render_text(img, "Invalid Symbol")
                USER_CHOICE = "Invalid"

            show_score(img, COMP_SCORE, USER_SCORE)

    if int(time.time() - start_time) == TIMER:
        comp_choice = random.choice(MOVES)
        if USER_CHOICE in MOVES:
            res = win(comp_choice, USER_CHOICE)
            if res == "Win":
                USER_SCORE += 1
            elif res == "Lose":
                COMP_SCORE += 1
            previous_computer_choice = comp_choice
            final_result.append([USER_CHOICE, comp_choice, res, USER_SCORE, COMP_SCORE])
        start_time = time.time()
    else:
        ct1 = int(time.time() - start_time)
        computer_previous_choice(img, "Computer Previous Choice", previous_computer_choice)
        show_counter(img, "Select Choice in", ct1)

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

user_draw_count = 0
computer_draw_count = 0

user_win_count = 0
computer_win_count = 0

user_loose_count = 0
computer_loose_count = 0

for i in final_result:
    if i[2] == "Draw":
        user_draw_count += 1
        computer_draw_count += 1
    elif i[2] == "Win":
        user_win_count += 1
        computer_loose_count += 1
    else:
        computer_win_count += 1
        user_loose_count += 1

user_stats = {
    'Win': user_win_count,
    'Lose': user_loose_count,
    'Draw': user_draw_count
}

computer_stats = {
    'Win': computer_win_count,
    'Lose': computer_loose_count,
    'Draw': computer_draw_count
}

status = ["Win", "Lose", "Draw"]


figure, axis = plt.subplots(2)

axis[0].bar(status, list(user_stats.values()), width=0.5)
axis[0].set_title("User Stats")

axis[1].bar(status, list(computer_stats.values()), width=0.5)
axis[1].set_title("Computer Stats")

plt.tight_layout()

plt.show()

