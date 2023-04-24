import pyautogui
import time
import keyboard
import pygetwindow as gw
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

class User:
    def __init__(self, inactivity_threshold):
        self.inactivity_threshold = inactivity_threshold
        self.last_activity_time = time.time()
        self.last_activity_logged_time = None
        self.active = True
        self.inactivity_logged = False
        self.activity_logged = False

    def update_activity(self):
        current_active = is_mouse_moving() or keyboard.is_pressed('*')
        if current_active != self.active:
            self.active = current_active
            if current_active:
                # Check if a certain amount of time has passed since the last "user became active" message
                if (not self.activity_logged or
                    (
                            self.last_activity_logged_time and time.time() - self.last_activity_logged_time > self.inactivity_threshold)) and self.inactivity_logged:
                    logging.info("User became active")
                    self.activity_logged = True
                    self.inactivity_logged = False
                    self.last_activity_logged_time = time.time()
            else:
                self.activity_logged = False
            self.last_activity_time = time.time()

        if not self.active and not self.inactivity_logged:
            if time.time() - self.last_activity_time > self.inactivity_threshold:
                logging.info("User became inactive")
                self.inactivity_logged = True
                self.activity_logged = False

    def is_inactive(self):
        current_time = time.time()
        return current_time - self.last_activity_time > self.inactivity_threshold

def is_mouse_moving():
    prev_x, prev_y = pyautogui.position()
    time.sleep(0.1)
    current_x, current_y = pyautogui.position()
    return prev_x != current_x or prev_y != current_y

def click_automate(x_coord, y_coord, click_interval=60, inactivity_threshold=5):
    user = User(inactivity_threshold)
    last_click_time = time.time()
    time_to_click = last_click_time + click_interval
    time_to_click_logged = False

    while True:
        user.update_activity()

        current_time = time.time()

        if current_time > time_to_click:
            if not time_to_click_logged:
                logging.info("It's time to click")
                time_to_click_logged = True

            if user.is_inactive():
                logging.info("Clicking")

                # Get the title of the active window
                original_window = gw.getActiveWindow()

                # Save the current mouse position
                original_x, original_y = pyautogui.position()

                # Block keyboard input
                keyboard.block_key('*')

                # Move the mouse cursor to the specified coordinates, click, and return to the original position
                pyautogui.moveTo(x_coord, y_coord)
                pyautogui.mouseDown(button='right')  # Use 'right' for a right-click
                pyautogui.mouseUp(button='right')    # Use 'right' for a right-click
                pyautogui.moveTo(original_x, original_y)

                # Unblock keyboard input
                keyboard.unblock_key('*')

                # Activate the original window
                original_window.activate()

                # Reset the last_click_time, time_to_click, and time_to_click_logged
                last_click_time = time.time()
                time_to_click = last_click_time + click_interval
                time_to_click_logged = False

        time.sleep(0.1)  # Use a short sleep time to continuously check for activity


def get_current_position():
    while True:
        current_x, current_y = pyautogui.position()
        logging.info("Current position: %s, %s", current_x, current_y)
        time.sleep(1)

click_automate(x_coord=2343, y_coord=370, click_interval=60, inactivity_threshold=7)
# get_current_position()
