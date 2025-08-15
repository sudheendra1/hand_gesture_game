import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

last_command_time = time.time()
command_delay = 0.5  # 500 milliseconds

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    gesture_text = "No Gesture Detected"
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark

            # Landmark assignments 
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
            thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_MCP]
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
            index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            middle_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
            ring_pip = landmarks[mp_hands.HandLandmark.RING_FINGER_PIP]
            pinky_pip = landmarks[mp_hands.HandLandmark.PINKY_PIP]

            if (thumb_tip.y < thumb_mcp.y and index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y):
                gesture_text = "Thumbs Up"
                # print("GRAB!")
                # if time.time() - last_command_time > command_delay:
                #     pyautogui.press('g')
                #     last_command_time = time.time()

            # Check for "Open Palm" (Jump)
            elif (index_tip.y < index_pip.y and middle_tip.y < middle_pip.y and
                ring_tip.y < ring_pip.y and pinky_tip.y < pinky_pip.y):
                gesture_text = "JUMP (Open Palm)"
                print("JUMP!")
                if time.time() - last_command_time > command_delay:
                    pyautogui.press('w')
                    last_command_time = time.time()

            # Check for "Fist" (Roll/Duck)
            elif (index_tip.y > index_pip.y and middle_tip.y > middle_pip.y and
                  ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y and thumb_tip.x < thumb_mcp.x):
                gesture_text = "ROLL (Fist)"
                print("ROLL!")
                if time.time() - last_command_time > command_delay:
                    pyautogui.press('s')
                    last_command_time = time.time()

            # Check for "Peace Sign" (Activate Board)
            elif (index_tip.y < index_pip.y and middle_tip.y < middle_pip.y and
                  ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y):
                gesture_text = "HOVERBOARD (Peace Sign)"
                print("HOVERBOARD!")
                if time.time() - last_command_time > command_delay:
                    pyautogui.press('space')
                    last_command_time = time.time()

            # Check for "Pointing" (Left/Right)
            elif (index_tip.y < index_pip.y and middle_tip.y > middle_pip.y and
                  ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y):
                if index_tip.x < landmarks[mp_hands.HandLandmark.WRIST].x:
                    gesture_text = "LEFT (Pointing)"
                    print("LEFT!")
                    if time.time() - last_command_time > command_delay:
                        pyautogui.press('a')
                        last_command_time = time.time()
                else:
                    gesture_text = "RIGHT (Pointing)"
                    print("RIGHT!")
                    if time.time() - last_command_time > command_delay:
                        pyautogui.press('d')
                        last_command_time = time.time()
            
            # Draw landmarks after all gesture checks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            break # Still only process one hand

    # Draw the text on the frame
    cv2.putText(frame, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Hand Gesture Controller", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Program exited successfully.")