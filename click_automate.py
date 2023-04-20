import pyautogui
import time
import keyboard
import pygetwindow as gw

def is_mouse_moving():
    prev_x, prev_y = pyautogui.position()
    time.sleep(0.1)
    current_x, current_y = pyautogui.position()
    return prev_x != current_x or prev_y != current_y

def click_automate(x_coord, y_coord, sleep_time=60, inactivity_threshold=5):

    last_activity_time = time.time()

    while True:
        # Update the last_activity_time if the mouse is moving or any key is being pressed
        if is_mouse_moving() or keyboard.is_pressed('*'):
            last_activity_time = time.time()
            print(last_activity_time)

        # If the inactivity period is longer than the threshold, perform the click
        if time.time() - last_activity_time > inactivity_threshold:
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

            # Reset the last_activity_time
            last_activity_time = time.time()

        time.sleep(sleep_time)  # Adjust the sleep time as needed

def get_current_position():
    while True:
        current_x, current_y = pyautogui.position()
        print("Current position:", current_x, current_y)
        time.sleep(1)

click_automate(x_coord=1988, y_coord=365, sleep_time=5, inactivity_threshold=5)
# get_current_position()
