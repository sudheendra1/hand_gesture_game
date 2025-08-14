import math

# MediaPipe hand landmark indices
# https://google.github.io/mediapipe/solutions/hands#hand-landmark-model
TIP_IDS = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20
}
PIP_IDS = {
    "index": 6,
    "middle": 10,
    "ring": 14,
    "pinky": 18
}
THUMB_IP_ID = 3  # thumb interphalangeal joint for side test


def _is_finger_open(landmarks, tip_id, pip_id):
    # y axis goes downwards in image coords; "open" finger tip sits higher (smaller y) than PIP
    tip_y = landmarks[tip_id].y
    pip_y = landmarks[pip_id].y
    return tip_y < pip_y


def _is_thumb_open(landmarks, hand_label):
    # Rough rule: for right hand, open thumb extends to the right (tip.x > ip.x); left is opposite
    tip_x = landmarks[TIP_IDS["thumb"]].x
    ip_x  = landmarks[THUMB_IP_ID].x
    if hand_label == "Right":
        return tip_x > ip_x
    else:  # "Left"
        return tip_x < ip_x


def get_finger_states(landmarks, hand_label):
    """
    Returns dict of finger states: True=open/extended, False=closed
    """
    states = {}
    states["thumb"]  = _is_thumb_open(landmarks, hand_label)
    states["index"]  = _is_finger_open(landmarks, TIP_IDS["index"], PIP_IDS["index"])
    states["middle"] = _is_finger_open(landmarks, TIP_IDS["middle"], PIP_IDS["middle"])
    states["ring"]   = _is_finger_open(landmarks, TIP_IDS["ring"], PIP_IDS["ring"])
    states["pinky"]  = _is_finger_open(landmarks, TIP_IDS["pinky"], PIP_IDS["pinky"])
    return states


def classify_gesture(landmarks, hand_label):
    """
    Map finger states to a small set of robust starter gestures.
    Returns one of: "FIST", "OPEN_PALM", "THUMBS_UP", "VICTORY", "POINT", or "UNKNOWN"
    """
    s = get_finger_states(landmarks, hand_label)

    all_open  = all(s.values())
    none_open = not any(s.values())

    if none_open:
        return "FIST"
    if all_open:
        return "OPEN_PALM"

    # Thumbs up: thumb open, others closed
    if s["thumb"] and not (s["index"] or s["middle"] or s["ring"] or s["pinky"]):
        return "THUMBS_UP"

    # Victory: index + middle open, ring + pinky closed (thumb don't-care)
    if s["index"] and s["middle"] and not s["ring"] and not s["pinky"]:
        return "VICTORY"

    # Point: index open, others closed (thumb don't-care)
    if s["index"] and not s["middle"] and not s["ring"] and not s["pinky"]:
        return "POINT"

    return "UNKNOWN"
