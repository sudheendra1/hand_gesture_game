import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands

hands=mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Start an infinite loop to continuously read frames from the camera
while True:
    success, frame = cap.read()

    if not success:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gesture Controller", frame)

cap.release()
cv2.destroyAllWindows()

print("Program exited successfully.")