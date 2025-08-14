import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands=mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Start an infinite loop to continuously read frames from the camera
while True:
    # Read a single frame from the camera feed
    # 'success' is a boolean that is True if the frame was read correctly
    # 'frame' is the actual image frame
    success, frame = cap.read()

    # If the frame was not read successfully, break the loop
    if not success:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)

    # OpenCV reads in BGR format, but MediaPipe requires RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if results.multi_hand_landmarks:
        # Loop through each detected hand
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the landmarks (dots) and connections (lines) on the original BGR frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the final frame with landmarks
    cv2.imshow("Hand Gesture Controller", frame)

# After the loop, release the camera resource
cap.release()
# Destroy all the windows created by OpenCV
cv2.destroyAllWindows()

print("Program exited successfully.")