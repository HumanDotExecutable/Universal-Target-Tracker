# Initialize the Pygame moduleimport pyautogui
import pygame
import math
import cv2
import numpy as np
import time
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore

# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Function to update the aiming cursor position based on the aimbot
def update_aim(aimbot_strength, max_distance, target_x, target_y):
    # Get the current mouse position
    mouse_x, mouse_y = pyautogui.position()

    # Calculate the distance between the aiming cursor and the target
    dist = distance(mouse_x, mouse_y, target_x, target_y)

    # Get the screen width and height
    screen_width, screen_height = pyautogui.size()

    # If the target is within the maximum distance, apply aimbot force
    if dist < max_distance:
        # Calculate the angle between the aiming cursor and the target
        angle = math.atan2(target_y - mouse_y, target_x - mouse_x)

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

        # Create QSpinBox widgets for the aimbot strength and max distance
        self.strengthSpinBox = QtWidgets.QSpinBox()
        self.distanceSpinBox = QtWidgets.QSpinBox()

        # Set the default values for the widgets
        self.flickEdit.setText("f")
        self.triggerEdit.setText("t")
        self.trackEdit.setText("r")
        self.strengthSpinBox.setValue(10)
        self.distanceSpinBox.setValue(100)

        # Create QPushButton widgets for the buttons
        self.startButton = QtWidgets.QPushButton("Start")
        self.stopButton = QtWidgets.QPushButton("Stop")
        self.screenshotButton = QtWidgets.QPushButton("Screenshot")

        # Connect the button clicked signals to the appropriate slots
        self.startButton.clicked.connect(self.startButtonClicked)
        self.stopButton.clicked.connect(self.stopButtonClicked)
        self.screenshotButton.clicked.connect(self.screenshotButtonClicked)

        # Add the widgets to the layout
        layout.addWidget(QtWidgets.QLabel("Flick hotkey:"))
        layout.addWidget(self.flickEdit)
        layout.addWidget(QtWidgets.QLabel("Trigger hotkey:"))
        layout.addWidget(self.triggerEdit)
        layout.addWidget(QtWidgets.QLabel("Track hotkey:"))
        layout.addWidget(self.trackEdit)
        layout.addWidget(QtWidgets.QLabel("Aimbot strength:"))
        layout.addWidget(self.strengthSpinBox)
        layout.addWidget(QtWidgets.QLabel("Max distance:"))
        layout.addWidget(self.distanceSpinBox)

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

        # Create QSpinBox widgets for the aimbot strength and max distance
        self.strengthSpinBox = QtWidgets.QSpinBox()
        self.distanceSpinBox = QtWidgets.QSpinBox()

        # Set the default values for the widgets
        self.flickEdit.setText("f")
        self.triggerEdit.setText("t")
        self.trackEdit.setText("r")
        self.strengthSpinBox.setValue(10)
        self.distanceSpinBox.setValue(100)

        # Create QPushButton widgets for the buttons
        self.startButton = QtWidgets.QPushButton("Start")
        self.stopButton = QtWidgets.QPushButton("Stop")
        self.screenshotButton = QtWidgets.QPushButton("Screenshot")

        # Connect the button clicked signals to the appropriate slots
        self.startButton.clicked.connect(self.startButtonClicked)
        self.stopButton.clicked.connect(self.stopButtonClicked)
        self.screenshotButton.clicked.connect(self.screenshotButtonClicked)

        # Add the widgets to the layout
        layout.addWidget(QtWidgets.QLabel("Flick hotkey:"))
        layout.addWidget(self.flickEdit)
        layout.addWidget(QtWidgets.QLabel("Trigger hotkey:"))
        layout.addWidget(self.triggerEdit)
        layout.addWidget(QtWidgets.QLabel("Track hotkey:"))
        layout.addWidget(self.trackEdit)
        layout.addWidget(QtWidgets.QLabel("Aimbot strength:"))
        layout.addWidget(self.strengthSpinBox)
        layout.addWidget(QtWidgets.QLabel("Max distance:"))
        layout.addWidget(self.distanceSpinBox)
        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.screenshotButton)



# Set the layout for the widget
self.setLayout(layout)

# Set the window title
self.setWindowTitle("Aimbot")

# Set the size and position of the window
self.setGeometry(300, 300, 300, 150)

# Initialize the Pygame module
pygame.init()

# Set the Pygame window caption
pygame.display.set_caption("Aimbot")

# Set the Pygame window size
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Flag to track whether the aimbot is running
self.running = False

# Flag to track whether the flick hotkey is being held down
self.flick_down = False

# Flag to track whether the trigger hotkey is being held down
self.trigger_down = False

# Flag to track whether the track hotkey is being held down
self.track_down = False

# Target coordinates
self.target_x = 0
self.target_y = 0

# Target color
self.target_color = (0, 0, 0)

# Timer to update the aimbot
self.aimbot_timer = QtCore.QTimer()
self.aimbot_timer.timeout.connect(self.update_aimbot)

# Timer to update the hotkey states
self.hotkey_timer = QtCore.QTimer()
self.hotkey_timer.timeout.connect(self.update_hotkeys)


def startButtonClicked(self):
    # Get the hotkeys from the QLineEdit widgets
    flick_hotkey = self.flickEdit.text()
    trigger_hotkey = self.triggerEdit.text()
    track_hotkey = self.trackEdit.text()

    # Get the aimbot strength and max distance from the QSpinBox widgets
    aimbot_strength = self.strengthSpinBox.value()
    max_distance = self.distanceSpinBox.value()

    # Select the target color using the flick hotkey
    self.target_color = select_target_color(flick_hotkey)

    # Start the aimbot
    self.running = True
    self.aimbot_timer.start(10)
    self.hotkey_timer.start(10)

    # Set the button states
    self.startButton.setEnabled(False)
    self.stopButton.setEnabled(True)
    self.screenshotButton.setEnabled(False)


def stopButtonClicked(self):
    # Stop the aimbot
    self.running = False
    self.aimbot_timer.stop()
    self.hotkey_timer.stop()

    # Set the button states
    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
    self.screenshotButton.setEnabled(True)

    def screenshotButtonClicked(self):
        # Take a screenshot using Pyautogui
        screenshot = pyautogui.screenshot()

    # Find the target using the selected target color
    target_coords = find_target(screenshot, self.target_color)

    # If a target was found, update the target coordinates
    if target_coords is not None:
        self.target_x, self.target_y = target_coords

def update_aimbot(self):
    # Check if the aimbot is running
    if self.running:
        # Update the aiming cursor position based on the aimbot settings
        update_aim(
            self.strengthSpinBox.value(),
            self.distanceSpinBox.value(),
            self.target_x,
            self.target_y,
        )

        # Check if the trigger hotkey is being held down
        if self.trigger_down:
            # Left click the mouse
            pyautogui.click()


def update_hotkeys(self):
    # Reset the hotkey states
    self.flick_down = False
    self.trigger_down = False
    self.track_down = False

    # Get the hotkeys from the QLineEdit widgets
    flick_hotkey = self.flickEdit.text()
    trigger_hotkey = self.triggerEdit.text()
    track_hotkey = self.trackEdit.text()

    # Get the current pressed keys
    keys = pygame.key.get_pressed()

    # Check if the flick hotkey is being held down
    if keys[getattr(pygame, "K_" + flick_hotkey)]:
        self.flick_down = True

    # Check if the trigger hotkey is being held down
    if keys[getattr(pygame, "K_" + trigger_hotkey)]:
        self.trigger_down = True

    # Check if the track hotkey is being held down
    if keys[getattr(pygame, "K_" + track_hotkey)]:
        self.track_down = True

        # Take a screenshot using Pyautogui
        screenshot = pyautogui.screenshot()

        # Find the target using the selected target color
        target_coords = find_target(screenshot, self.target_color)

        # If a target was found, update the target coordinates
        if target_coords is not None:
            self.target_x, self.target_y = target_coords

            def aimbot(
                window_title,
                aimbot_strength=0.1,
                max_distance=50,
                flick_key=pygame.K_1,
                trigger_key=pygame.K_2,
                track_key=pygame.K_3,
                trigger_delay=0.1,
            ):
                # Find the window with the specified title
                windows = pyautogui.getWindowsWithTitle(window_title)

    if windows:
        pyautogui.getWindow(windows[0]).activate()
    else:
        print(f"Window with title '{window_title}' not found")
        return

    # Create a Pygame window to listen for key press and mouse click events
    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    # Create a variable to track whether the aimbot is active
    aimbot_active = False

    # Create a variable to track whether the trigger is being held down
    trigger_held = False

    # Run a loop to listen for key press and mouse click events
    while True:
        for event in pygame.event.get():
            # Handle the Pygame quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key press events
            if event.type == pygame.KEYDOWN:
                # Check if the flick key was pressed
                if event.key == flick_key:
                    # Toggle the aimbot on or off
                    aimbot_active = not aimbot_active

                # Check if the trigger key was pressed
                if event.key == trigger_key:
                    # Set the trigger_held flag to True
                    trigger_held = True

                # Check if the track key was pressed
                if event.key == track_key:
                    # Select a target pixel using the track key as the hotkey
                    target_x, target_y = select_target_pixel(track_key)

            # Handle key release events
            if event.type == pygame.KEYUP:
                # Check if the trigger key was released
                if event.key == trigger_key:
                    # Set the trigger_held flag to False
                    trigger_held = False

        # Get a screenshot of the game window
        screenshot = pyautogui.screenshot()

        # Find the target element in the screenshot
        target_coords = find_target(screenshot, "target.png")

        # If the target element was found, aim at it
        if target_coords is not None:
            target_x, target_y = target_coords

            # If the aimbot is active and the trigger is being held down, apply aimbot force
            if aimbot_active and trigger_held:
                update_aim(aimbot_strength, max_distance, target_x, target_y)

                # Delay the trigger release to simulate human-like shooting
                time.sleep(trigger_delay)

                # Release the trigger
                pyautogui.keyUp(trigger)

        # Update the Pygame window
        pygame.display.update()


pygame.init()

# Set the Pygame window caption
pygame.display.set_caption("Aimbot")

# Set the Pygame window size
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Flag to track whether the aimbot is running
self.running = False

# Flag to track whether the flick hotkey is being held down
self.flick_down = False

# Flag to track whether the trigger hotkey is being held down
self.trigger_down = False

# Flag to track whether the track hotkey is being held down
self.track_down = False

# Target coordinates
self.target_x = 0
self.target_y = 0

# Target color
self.target_color = (0, 0, 0)

# Timer to update the aimbot
self.aimbot_timer = QtCore.QTimer()
self.aimbot_timer.timeout.connect(self.update_aimbot)

# Timer to update the hotkey states
self.hotkey_timer = QtCore.QTimer()
self.hotkey_timer.timeout.connect(self.update_hotkeys)


def startButtonClicked(self):
    # Get the hotkeys from the QLineEdit widgets
    flick_hotkey = self.flickEdit.text()
    trigger_hotkey = self.triggerEdit.text()
    track_hotkey = self.trackEdit.text()

    # Get the aimbot strength and max distance from the QSpinBox widgets
    aimbot_strength = self.strengthSpinBox.value()
    max_distance = self.distanceSpinBox.value()

    # Select the target color using the flick hotkey
    self.target_color = select_target_color(flick_hotkey)

    # Start the aimbot
    self.running = True
    self.aimbot_timer.start(10)
    self.hotkey_timer.start(10)

    # Set the button states
    self.startButton.setEnabled(False)
    self.stopButton.setEnabled(True)
    self.screenshotButton.setEnabled(False)


def stopButtonClicked(self):
    # Stop the aimbot
    self.running = False
    self.aimbot_timer.stop()
    self.hotkey_timer.stop()

    # Set the button states
    self.startButton.setEnabled(True)
    self.stopButton.setEnabled(False)
    self.screenshotButton.setEnabled(True)

    def screenshotButtonClicked(self):
        # Take a screenshot using Pyautogui
        screenshot = pyautogui.screenshot()

    # Find the target using the selected target color
    target_coords = find_target(screenshot, self.target_color)

    # If a target was found, update the target coordinates
    if target_coords is not None:
        self.target_x, self.target_y = target_coords


def update_aimbot(self):
    # Check if the aimbot is running
    if self.running:
        # Update the aiming cursor position based on the aimbot settings
        update_aim(
            self.strengthSpinBox.value(),
            self.distanceSpinBox.value(),
            self.target_x,
            self.target_y,
        )

        # Check if the trigger hotkey is being held down
        if self.trigger_down:
            # Left click the mouse
            pyautogui.click()


def update_hotkeys(self):
    # Reset the hotkey states
    self.flick_down = False
    self.trigger_down = False
    self.track_down = False

    # Get the hotkeys from the QLineEdit widgets
    flick_hotkey = self.flickEdit.text()
    trigger_hotkey = self.triggerEdit.text()
    track_hotkey = self.trackEdit.text()

    # Get the current pressed keys
    keys = pygame.key.get_pressed()

    # Check if the flick hotkey is being held down
    if keys[getattr(pygame, "K_" + flick_hotkey)]:
        self.flick_down = True

    # Check if the trigger hotkey is being held down
    if keys[getattr(pygame, "K_" + trigger_hotkey)]:
        self.trigger_down = True

    # Check if the track hotkey is being held down
    if keys[getattr(pygame, "K_" + track_hotkey)]:
        self.track_down = True

        # Take a screenshot using Pyautogui
        screenshot = pyautogui.screenshot()

        # Find the target using the selected target color
        target_coords = find_target(screenshot, self.target_color)

        # If a target was found, update the target coordinates
        if target_coords is not None:
            self.target_x, self.target_y = target_coords

            def aimbot(
                window_title,
                aimbot_strength=0.1,
                max_distance=50,
                flick_key=pygame.K_1,
                trigger_key=pygame.K_2,
                track_key=pygame.K_3,
                trigger_delay=0.1,
            ):
                # Find the window with the specified title
                windows = pyautogui.getWindowsWithTitle(window_title)

    if windows:
        pyautogui.getWindow(windows[0]).activate()
    else:
        print(f"Window with title '{window_title}' not found")
        return

    # Create a Pygame window to listen for key press and mouse click events
    pygame.init()
    screen = pygame.display.set_mode((1, 1))

    # Create a variable to track whether the aimbot is active
    aimbot_active = False

    # Create a variable to track whether the trigger is being held down
    trigger_held = False

    # Run a loop to listen for key press and mouse click events
    while True:
        for event in pygame.event.get():
            # Handle the Pygame quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key press events
            if event.type == pygame.KEYDOWN:
                # Check if the flick key was pressed
                if event.key == flick_key:
                    # Toggle the aimbot on or off
                    aimbot_active = not aimbot_active

                # Check if the trigger key was pressed
                if event.key == trigger_key:
                    # Set the trigger_held flag to True
                    trigger_held = True

                # Check if the track key was pressed
                if event.key == track_key:
                    # Select a target pixel using the track key as the hotkey
                    target_x, target_y = select_target_pixel(track_key)

            # Handle key release events
            if event.type == pygame.KEYUP:
                # Check if the trigger key was released
                if event.key == trigger_key:
                    # Set the trigger_held flag to False
                    trigger_held = False

        # Get a screenshot of the game window
        screenshot = pyautogui.screenshot()

        # Find the target element in the screenshot
        target_coords = find_target(screenshot, "target.png")

        # If the target element was found, aim at it
        if target_coords is not None:
            target_x, target_y = target_coords

            # If the aimbot is active and the trigger is being held down, apply aimbot force
            if aimbot_active and trigger_held:
                update_aim(aimbot_strength, max_distance, target_x, target_y)

                # Delay the trigger release to simulate human-like shooting
                time.sleep(trigger_delay)

                # Release the trigger
                pyautogui.keyUp(trigger)

        # Update the Pygame window
        pygame.display.update()
