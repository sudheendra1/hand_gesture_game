## Got a Hand? You Don't Need a Controller. 🧙‍♂️



---

### ### Q: So, what is this thing, anyway?

A: This is a Python script that turns your webcam into a controller. It watches your hand, and when it sees you make a specific gesture (like a fist or a peace sign), it presses a key on your keyboard for you. It's designed to let you play simple games, like Subway Surfers, completely hands-free.

---

### ### Q: Sounds neat. What do I need to get it running?

A: Just the usual suspects for a computer vision project. Your shopping list is in the `requirements.txt` file, but the main ingredients are:
* Python
* OpenCV
* MediaPipe
* PyAutoGUI

---

### ### Q: How do I actually set it up?

A: It's a classic three-step dance. First, get the code onto your machine. Next, give the project its own little sandbox to play in (we call this a virtual environment) and tell your terminal to step inside. Finally, run the magic command `pip install -r requirements.txt` to automatically install everything it needs.

---

### ### Q: I'm set up. How do I play?

A: Easy peasy.
1.  Run the `main.py` script from your terminal.
2.  You'll see your webcam feed pop up.
3.  **Click on the game window you want to control.** This part is crucial—it has to be the active window!
4.  Show your hand to the camera and start making gestures.
5.  Press 'q' on the camera window's screen to exit.

---

### ### Q: What are the 'magic spells' or gestures?

A: Glad you asked! Here are the built-in controls:

* 🖐️ **Open Palm:** JUMP (Presses the 'W' key)
* ✊ **Fist:** DUCK (Presses the 'S' key)
* 👉 **Point Right:** GO RIGHT (Presses the 'D' key)
* 👈 **Point Left:** GO LEFT (Presses the 'A' key)
* ✌️ **Peace Sign:** SPECIAL MOVE (Presses the 'Spacebar')

---

### ### Q: What if it's acting weird or not responding?

A: Check these things first:
* Did you remember to click on the game window to make it active?
* Is the lighting in your room decent? The camera needs to see your hand clearly!
* Are you making clear, distinct gestures? Don't be shy.