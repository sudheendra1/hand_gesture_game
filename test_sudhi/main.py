import json
import time
from collections import deque

import cv2
import numpy as np
import mediapipe as mp

from gestures import classify_gesture
from keymap import KeySender

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def draw_hud(frame, gesture, mapped, active=True):
    h, w = frame.shape[:2]
    status = "ACTIVE" if active else "PAUSED"
    cv2.rectangle(frame, (0, 0), (w, 50), (0, 0, 0), -1)
    cv2.putText(frame, f"Status: {status}", (10, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0) if active else (0, 200, 200), 2)
    cv2.putText(frame, f"Gesture: {gesture}", (250, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f"Mapped: {mapped}", (520, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 255, 200), 2)

def main():
    cfg = load_config()
    mappings = cfg.get("mappings", {})
    sustain_frames = int(cfg.get("sustain_frames", 4))
    cooldown_ms = int(cfg.get("cooldown_ms", 300))
    show_landmarks = bool(cfg.get("show_landmarks", True))
    camera_index = int(cfg.get("camera_index", 0))
    mirror = bool(cfg.get("mirror_camera", True))
    trigger_mode = cfg.get("trigger_mode", "tap")

    key_sender = KeySender()

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    )
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera index {camera_index}")

    gesture_buffer = deque(maxlen=sustain_frames)
    last_confirmed = "UNKNOWN"
    paused = False

    print("Controls: 'p' to pause/resume, 'q' to quit.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if mirror:
                frame = cv2.flip(frame, 1)

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            current = "UNKNOWN"
            mapped = "-"

            if results.multi_hand_landmarks and results.multi_handedness:
                hand_landmarks = results.multi_hand_landmarks[0]
                hand_label = results.multi_handedness[0].classification[0].label  # "Left"/"Right"

                if show_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                current = classify_gesture(hand_landmarks.landmark, hand_label)

            gesture_buffer.append(current)

            # confirm only if buffer agrees
            if len(gesture_buffer) == gesture_buffer.maxlen and len(set(gesture_buffer)) == 1:
                confirmed = gesture_buffer[0]
            else:
                confirmed = "UNKNOWN"

            # Pause/resume via keyboard key 'p' in window (simpler & safe)
            # You can map a gesture for this toggle later if you want.
            key = cv2.waitKey(1) & 0xFF
            if key == ord('p'):
                paused = not paused
            if key == ord('q') or key == 27:
                break

            # Act only on changes, not continuous spam
            if not paused and confirmed != "UNKNOWN" and confirmed != last_confirmed:
                if confirmed in mappings:
                    mapped = mappings[confirmed]
                    if trigger_mode == "tap":
                        key_sender.throttled_tap(confirmed, mapped, cooldown_ms)
                last_confirmed = confirmed
            elif confirmed == "UNKNOWN":
                last_confirmed = "UNKNOWN"

            if confirmed in mappings:
                mapped = mappings[confirmed]

            draw_hud(frame, confirmed, mapped, active=not paused)
            cv2.imshow("Gesture Controller", frame)

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

if __name__ == "__main__":
    main()
