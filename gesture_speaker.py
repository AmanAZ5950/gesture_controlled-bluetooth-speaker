import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_action = 0
cooldown = 1

print("Gesture Speaker Control Started")

# ---------- finger detection ----------
def fingers_up(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tips = [8, 12, 16, 20]

    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

# ---------- main ----------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            f = fingers_up(handLms)
            now = time.time()

            # 👍 THUMB → VOLUME UP
            if f == [1,0,0,0,0]:
                cv2.putText(img,"VOLUME UP",(50,80),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

                if now-last_action>cooldown:
                    pyautogui.press("volumeup")
                    last_action = now

            # ☝ INDEX → VOLUME DOWN
            elif f == [0,1,0,0,0]:
                cv2.putText(img,"VOLUME DOWN",(50,80),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)

                if now-last_action>cooldown:
                    pyautogui.press("volumedown")
                    last_action = now

            # ✌ TWO FINGERS → PLAY
            elif f == [0,1,1,0,0]:
                cv2.putText(img,"PLAY",(50,80),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

                if now-last_action>cooldown:
                    pyautogui.press("playpause")
                    last_action = now

            # ✊ FIST → PAUSE
            elif f == [0,0,0,0,0]:
                cv2.putText(img,"PAUSE",(50,80),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),3)

                if now-last_action>cooldown:
                    pyautogui.press("playpause")
                    last_action = now

    cv2.imshow("Gesture Speaker Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
