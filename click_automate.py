import pyautogui
import time
import keyboard
import pygetwindow as gw

def is_mouse_moving():
    prev_x, prev_y = pyautogui.position()
    time.sleep(0.1)
    current_x, current_y = pyautogui.position()
    return prev_x != current_x or prev_y != current_y

def click_automate(x_coord, y_coord, click_interval=60, inactivity_threshold=5):

    last_click_time = time.time()

    while True:
        current_time = time.time()
        # print('continuous current_time:', current_time)

        # If the time since the last click is greater than the click interval
        if current_time - last_click_time > click_interval:

            print('I would like to click now:', current_time)

            # we can have in different stages I am active or inactive
            # inactive means that there was no activity for a certain period of time

            # Wait for inactivity in the personal window
            while is_mouse_moving() or keyboard.is_pressed('*'):
                print('you are active:', current_time)
                time.sleep(0.1)

            # I think we have to set last active here

            # Perform the click after a period of inactivity
            if current_time - last_click_time > click_interval + inactivity_threshold:
                print('you were inactive, so clicking:', current_time)

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
        print("Current position:", current_x, current_y)
        time.sleep(1)

click_automate(x_coord=1988, y_coord=365, click_interval=5, inactivity_threshold=5)
# get_current_position()
