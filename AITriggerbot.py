import ctypes
import random
import time
import threading
import win32con
import win32gui
import numpy as np
import win32ui
import cv2
from concurrent.futures import ThreadPoolExecutor
from ctypes import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog
import pyautogui

# Get the handle of the current window
game_window_handle = win32gui.GetForegroundWindow()

# Get the dimensions of the current window
game_window_rect = win32gui.GetWindowRect(game_window_handle)

# Set the trigger bot to off
running = False

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_longlong),
                ("y", ctypes.c_longlong)]
    
class MSG(ctypes.Structure):
    _fields_ = [("hwnd", ctypes.c_int),
                ("message", ctypes.c_uint),
                ("wParam", ctypes.c_int),
                ("lParam", ctypes.c_longlong),
                ("time", ctypes.c_int),
                ("pt", POINT)]

HOOKPROC = CFUNCTYPE(c_int, c_int, c_void_p, POINTER(MSG))
user32 = ctypes.windll.user32

# Function to start the triggerbot loop
def triggerbot_loop():
     while True:
        # Take a screenshot of the game window
        screenshot = take_screenshot(game_window_handle, game_window_rect)
        # Check if the crosshair is over an enemy player
        if check_if_enemy_in_sight(screenshot):   
            # Simulate a left mouse button click
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            # Simulate a left mouse button release
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            # Sleep for a random amount of time to avoid detection
            time.sleep(random.uniform(0.1, 0.5))
        if not running:
            break

# Function to stop the triggerbot loop
def triggerbot_stop():
    global running
    running = False
    
# Function to create the low-level keyboard hook
def create_keyboard_hook(hotkey, callback):
    # Set the low-level keyboard hook callback
    hook_callback = HOOKPROC(callback)
    # Set the hook
    hook_id = user32.SetWindowsHookExA(win32con.WH_KEYBOARD_LL, hook_callback, None, 0)
    return hook_id

# Function to remove the low-level keyboard hook
def remove_keyboard_hook(hook_id):
    user32.UnhookWindowsHookEx(hook_id)

def low_level_keyboard_callback(nCode, wParam, lParam, hook_id, hotkey):
    global running
    if wParam == win32con.WM_KEYDOWN:
        # Check if the hotkey has been pressed
        if lParam[0] == ord(hotkey):
            # Start the triggerbot loop
            running = True
    elif wParam == win32con.WM_KEYUP:
        # Check if the hotkey has been released
        if lParam[0] == ord(hotkey):
            # Stop the triggerbot loop
            running = False
    # Pass the hook information to the next hook in the chain
    return user32.CallNextHookEx(0, nCode, wParam, lParam)

def take_screenshot(game_window_handle, game_window_rect):
    save_dc = win32ui.CreateDCFromHandle(win32gui.GetDC(game_window_handle))
    try:
        # code using save_dc goes here
        with win32ui.CreateDCFromHandle(win32gui.GetDC(game_window_handle)) as save_dc:
            with save_dc.CreateCompatibleDC() as compatible_dc:
                with win32ui.CreateBitmap() as save_bit_map:
                    save_bit_map = win32ui.CreateBitmap()
                    save_bit_map.CreateCompatibleBitmap(save_dc, game_window_rect[2], game_window_rect[3])
                    compatible_dc.SelectObject(save_bit_map)
                    compatible_dc.BitBlt((0, 0), (game_window_rect[2], game_window_rect[3]), save_dc, (0, 0), win32con.SRCCOPY)
                    bmp_info = save_bit_map.GetInfo()
                    bmp_str = ctypes.create_string_buffer(bmp_info['bmHeight'] * bmp_info['bmWidth'] * 4)
                    save_bit_map.GetDIBits(compatible_dc, save_bit_map, 0, bmp_info['bmHeight'], byref(bmp_str), byref(bmp_info), win32con.DIB_RGB_COLORS)
                    img = np.frombuffer(bmp_str, dtype='uint8')
                    img.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
                    win32gui.DeleteObject(save_bit_map.GetHandle())
                    return img
    finally:
        save_dc.DeleteDC()
        compatible_dc.DeleteDC()

# Start triggerbot loop on hotkey press
hotkey = 'F1'
hook_id = create_keyboard_hook(hotkey, low_level_keyboard_callback)
running = True
thread = threading.Thread(target=triggerbot_loop, args=(running,))
thread.start()

class GUIThread(QtCore.QObject):
    color_selected = QtCore.pyqtSignal(int, int, int)
    window_selected = QtCore.pyqtSignal(str)
    key_selected = QtCore.pyqtSignal(str)
    triggerbot_paused = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.color_button = QtWidgets.QPushButton('Select Target Color', None)
        self.color_label = QtWidgets.QLabel(None)
        self.window_button = QtWidgets.QPushButton('Select Target Window', None)
        self.window_label = QtWidgets.QLabel(None)
        self.key_button = QtWidgets.QPushButton('Select Key', None)
        self.key_label = QtWidgets.QLabel(None)
        self.start_button = QtWidgets.QPushButton('Start', None)
        self.pause_button = QtWidgets.QPushButton('Pause', None)
        self.stop_button = QtWidgets.QPushButton('Stop', None)
        
        self.color_button.clicked.connect(self.select_color)
        self.window_button.clicked.connect(self.select_window)
        self.key_button.clicked.connect(self.select_key)
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.color_button)
        layout.addWidget(self.color_label)
        layout.addWidget(self.window_button)
        layout.addWidget(self.window_label)
        layout.addWidget(self.key_button)
        layout.addWidget(self.key_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        
        self.color_selected.connect(self.update_color_label)
        self.window_selected.connect(self.update_window_label)
        self.key_selected.connect(self.update_key_label)
        self.triggerbot_paused.connect(self.update_buttons)
        
        widget.show()

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_selected.emit(color.red(), color.green(), color.blue())
            self.target_color = (color.red(), color.green(), color.blue())

    def update_color_label(self, r, g, b):
        self.color_label.setText(f'Red: {r}, Green: {g}, Blue: {b}')

    def select_window(self):
        window = win32gui.GetForegroundWindow()
        self.window_selected.emit(win32gui.GetWindowText(window))
        self.target_window = window
        
    def update_window_label(self, window_name):
        self.window_label.setText(window_name)
        
    def select_key(self):
        self.key, ok = QtWidgets.QInputDialog.getText(None, 'Select Key', 'Enter a single character:')
        if ok:
            self.key_selected.emit(self.key)
            self.hotkey = self.key
            
    def update_key_label(self, key):
        self.key_label.setText(key)

        
    # Function to start the triggerbot
    def start(self):
        global running
        running = True
        # Create the low-level keyboard hook
        self.hook_id = create_keyboard_hook

        # Set the triggerbot loop as a daemon thread
        self.thread = threading.Thread(target=triggerbot_loop, daemon=True)
        self.thread.start()
        # Update the buttons
        self.triggerbot_paused.emit(False)
        
    # Function to pause the triggerbot
    def pause(self):
        global running
        running = False
        # Update the buttons
        self.triggerbot_paused.emit(True)
        
    # Function to stop the triggerbot
    def stop(self):
        global running
        running = False
        # Remove the low-level keyboard hook
        remove_keyboard_hook(self.hook_id)
        # Update the buttons
        self.triggerbot_paused.emit(False)
        
    def update_buttons(self, paused):
        if paused:
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    GUIThread()
    app.exec_()
    
    