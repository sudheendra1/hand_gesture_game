import time
from pynput.keyboard import Controller, Key

SPECIAL_KEYS = {
    "space": Key.space,
    "enter": Key.enter,
    "esc": Key.esc,
    "tab": Key.tab,
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "cmd": Key.cmd,  # macOS
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "backspace": Key.backspace,
    "delete": Key.delete
}

class KeySender:
    def __init__(self):
        self.kb = Controller()
        self._last_fire = {}

    def _parse_combo(self, combo_str):
        # e.g. "ctrl+w" -> [Key.ctrl, 'w']
        parts = [p.strip().lower() for p in combo_str.split("+")]
        parsed = []
        for p in parts:
            parsed.append(SPECIAL_KEYS.get(p, p))  # fallback to raw char
        return parsed

    def tap_combo(self, combo_str):
        keys = self._parse_combo(combo_str)
        # press modifiers first, then letters; release in reverse
        for k in keys:
            self.kb.press(k)
        for k in reversed(keys):
            self.kb.release(k)

    def throttled_tap(self, gesture, combo_str, cooldown_ms):
        now = time.time() * 1000
        last = self._last_fire.get(gesture, 0)
        if now - last >= cooldown_ms:
            self.tap_combo(combo_str)
            self._last_fire[gesture] = now
            return True
        return False
