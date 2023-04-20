import pyautogui
import time
import keyboard
import pygetwindow as gw
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')

def is_mouse_moving():
    prev_x, prev_y = pyautogui.position()
    time.sleep(0.1)
    current_x, current_y = pyautogui.position()
    return prev_x != current_x or prev_y != current_y

def click_automate(x_coord, y_coord, click_interval=60, inactivity_threshold=5):
    last_click_time = time.time()
    last_activity_time = time.time()

    while True:
        current_time = time.time()

        # Continuously check for user activity and update the last_activity_time
        while is_mouse_moving() or keyboard.is_pressed('*'):
            last_activity_time = time.time()
            time.sleep(0.1)
        logging.info("Inactivity detected")

        # If the time since the last click is greater than the click interval
        if current_time - last_click_time > click_interval:
            logging.info("It is time to click")
            # If the time since the last activity is greater than the inactivity threshold
            if current_time - last_activity_time > inactivity_threshold:
                logging.info("Clicking")

                # Get the title of the active window
                original_window = gw.getActiveWindow()

                # Save the current mouse position
                original_x, original_y = pyautogui.position()

                # Move the mouse cursor to the specified coordinates, click, and return to the original position
                pyautogui.moveTo(x_coord, y_coord)
                pyautogui.mouseDown(button='right')  # Use 'right' for a right-click
                pyautogui.mouseUp(button='right')    # Use 'right' for a right-click
                pyautogui.moveTo(original_x, original_y)

                # Activate the original window
                original_window.activate()

                # Reset the last_click_time
                last_click_time = time.time()

        time.sleep(0.1)  # Use a short sleep time to continuously check for activity

def get_current_position():
    while True:
        current_x, current_y = pyautogui.position()
        logging.info("Current position: %s, %s", current_x, current_y)
        time.sleep(1)

click_automate(x_coord=1988, y_coord=365, click_interval=5, inactivity_threshold=5)
# get_current_position()
