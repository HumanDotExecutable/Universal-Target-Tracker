import math
import time


import cv2
import numpy as np
import pyautogui
import pygame
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets
import sys

# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

# Function to update the aiming cursor position based on the aimbot
def update_aim(aimbot_strength, max_distance, target_x, target_y, target_vx, target_vy):
    # Get the current mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Calculate the distance between the aiming cursor and the target
    dist = distance(mouse_x, mouse_y, target_x, target_y)

    # Get the screen width and height
    screen_width, screen_height = pyautogui.size()

    # If the target is within the maximum distance, apply aimbot force
    if dist < max_distance:
        # Calculate the time it will take for the projectile to reach the target
        time_to_impact = dist / np.linalg.norm([target_vx, target_vy])

        # Calculate the future position of the target
        predicted_x = target_x + target_vx * time_to_impact
        predicted_y = target_y + target_vy * time_to_impact

        # Calculate the angle between the aiming cursor and the predicted target position
        angle = math.atan2(predicted_y - mouse_y, predicted_x - mouse_x)

        # Calculate the x and y components of the aimbot force
        force_x = aimbot_strength * math.cos(angle)
        force_y = aimbot_strength * math.sin(angle)

        # Update the aiming cursor position based on the aimbot force
        pyautogui.moveRel(force_x, force_y)

def select_target_pixel(hotkey):
    # Flag to track whether the hotkey has been pressed
    hotkey_pressed = False

    # Flag to track whether a target pixel has been selected
    pixel_selected = False

    # Run a loop to listen for key press and mouse click events
    while not pixel_selected:
        for event in pygame.event.get():
            # Handle the Pygame quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
              # Handle key press events
            if event.type == pygame.KEYDOWN:
                # Check if the hotkey was pressed
                if event.key == hotkey:
                    hotkey_pressed = True

            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the hotkey has been pressed
                if hotkey_pressed:
                    # Get the mouse position when the mouse was clicked
                    x, y = pygame.mouse.get_pos()
                    pixel_selected = True

    # Return the target pixel coordinates
    return x, y

# Function to find the target element in the game using image recognition
def find_target(screenshot, template_path):
    # Convert the screenshot to a grayscale image
    gray_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Load the target image template
    template = cv2.imread(template_path, 0)

    # Use the matchTemplate function to find the target image in the screenshot
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the target image was found in the screenshot, return the target coordinates
    if max_val > 0.8:
        return max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2
    else:
        return None

class AimbotGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a layout for the widgets
        layout = QtWidgets.QVBoxLayout()

        # Create QLineEdit widgets for the hotkeys
        self.flickEdit = QtWidgets.QLineEdit()
        self.triggerEdit = QtWidgets.QLineEdit()
        self.trackEdit = QtWidgets.QLineEdit()

        # Create QSlider widgets for the aimbot strength
        self.flickSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.triggerSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.trackSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        # Set the input mask for the hotkey QLineEdit widgets
        self.flickEdit.setInputMask("X")
        self.triggerEdit.setInputMask("X")
        self.trackEdit.setInputMask("X")

        # Set the range and default value for the aimbot strength QSlider widgets
        self.flickSlider.setRange(0, 100)
        self.flickSlider.setValue(50)
        self.triggerSlider.setRange(0, 100)
        self.triggerSlider.setValue(50)
        self.trackSlider.setRange(0, 100)
        self.trackSlider.setValue(50)

        # Create QLabel widgets for the hotkeys and aimbot strength
        flickLabel = QtWidgets.QLabel("Flick Hotkey:")
        triggerLabel = QtWidgets.QLabel("Trigger Hotkey:")
        trackLabel = QtWidgets.QLabel("Track Hotkey:")
        flickStrengthLabel = QtWidgets.QLabel("Flick Aimbot Strength:")
        triggerStrengthLabel = QtWidgets.QLabel("Trigger Aimbot Strength:")
        trackStrengthLabel = QtWidgets.QLabel("Track Aimbot Strength:")

        # Create QPushButton widgets for starting and stopping the aimbot
        startButton = QtWidgets.QPushButton("Start Aimbot")
        stopButton = QtWidgets.QPushButton("Stop Aimbot")

        # Connect the start button to the startAimbot method
        startButton.clicked.connect(self.startAimbot)

        # Connect the stop button to the stopAimbot method
        stopButton.clicked.connect(self.stopAimbot)

         # Add the widgets to the layout
        layout.addWidget(flickLabel)
        layout.addWidget(self.flickEdit)
        layout.addWidget(flickStrengthLabel)
        layout.addWidget(self.flickSlider)
        layout.addWidget(triggerLabel)
        layout.addWidget(self.triggerEdit)
        layout.addWidget(triggerStrengthLabel)
        layout.addWidget(self.triggerSlider)
        layout.addWidget(trackLabel)
        layout.addWidget(self.trackEdit)
        layout.addWidget(trackStrengthLabel)
        layout.addWidget(self.trackSlider)
        layout.addWidget(startButton)
        layout.addWidget(stopButton)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set the window title
        self.setWindowTitle("Aimbot")

        # Set the window size
        self.resize(250, 300)

    # Method to start the aimbot
    def startAimbot(self):
        # Get the hotkeys and aimbot strength values from the GUI
        flick_hotkey = ord(self.flickEdit.text())
        trigger_hotkey = ord(self.triggerEdit.text())
        track_hotkey = ord(self.trackEdit.text())
        flick_strength = self.flickSlider.value()
        trigger_strength = self.triggerSlider.value()
        track_strength = self.trackSlider.value()

        # Flag to track whether the aimbot is running
        aimbot_running = True

        # Run a loop to keep the aimbot running
        while aimbot_running:
            # Get a screenshot of the game window
            screenshot = pyautogui.screenshot()

            # Select the target pixel using the flick hotkey
            flick_target_x, flick_target_y = select_target_pixel(flick_hotkey)

            # Select the target pixel using the trigger hotkey
            trigger_target_x, trigger_target_y = select_target_pixel(trigger_hotkey)

            # Find the target element using image recognition
            track_target_x, track_target_y = find_target(screenshot, "template.png")

            # Update the aiming cursor position based on the aimbot strength and target coordinates
            update_aim(flick_strength, 100, flick_target_x, flick_target_y)
            update_aim(trigger_strength, 100, trigger_target_x, trigger_target_y)
            update_aim(track_strength, 100, track_target_x, track_target_y)

            # Sleep for a short period of time
            time.sleep(0.01)

    # Method to stop the aimbot
    def stopAimbot(self):
        aimbot_running = False

# Run the GUI
app = QtWidgets.QApplication([])
window = AimbotGUI()
window.show()
app.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AimbotGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
