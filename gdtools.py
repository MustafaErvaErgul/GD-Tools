# ---------------- Native Imports ----------------
import threading
import ctypes
import time
import os
import sys

# ---------------- External Imports ----------------
import keyboard
import configparser
from PIL import Image
import pystray

# ---------------- Read Config ----------------
config = configparser.ConfigParser()
config.read('config.ini')

# ---------------- Shortcuts ----------------
SHORTCUT_SELL_MAIN_BAG = config.get('Shortcuts', 'SELL_MAIN_BAG')
SHORTCUT_SELL_SECONDARY_BAG = config.get('Shortcuts', 'SELL_SECONDARY_BAG')
SHORTCUT_DISMANTLE_MAIN_BAG = config.get('Shortcuts', 'DISMANTLE_MAIN_BAG')
SHORTCUT_DISMANTLE_SECONDARY_BAG = config.get('Shortcuts', 'DISMANTLE_SECONDARY_BAG')
SHORTCUT_EXIT_EARLY = config.get('Shortcuts', 'EXIT_EARLY')

# ---------------- Constants ----------------
DEBUG = config.getboolean('Constants', 'DEBUG')

MOUSEEVENTF_RIGHTDOWN = int(config.get('Constants', 'MOUSEEVENTF_RIGHTDOWN'), 16)
MOUSEEVENTF_RIGHTUP = int(config.get('Constants', 'MOUSEEVENTF_RIGHTUP'), 16)
MOUSEEVENTF_LEFTDOWN = int(config.get('Constants', 'MOUSEEVENTF_LEFTDOWN'), 16)
MOUSEEVENTF_LEFTUP = int(config.get('Constants', 'MOUSEEVENTF_LEFTUP'), 16)

SHORT_DELAY = config.getfloat('Constants', 'SHORT_DELAY')
MEDIUM_DELAY = config.getfloat('Constants', 'MEDIUM_DELAY')
LONG_DELAY = config.getfloat('Constants', 'LONG_DELAY')

INVENTORY_CELL_SIDE_LENGTH = config.getint('Constants', 'INVENTORY_CELL_SIDE_LENGTH')
INVENTORY_CELL_BORDER_LENGTH = config.getint('Constants', 'INVENTORY_CELL_BORDER_LENGTH')
MAIN_INVENTORY_ROW_COUNT = config.getint('Constants', 'MAIN_INVENTORY_ROW_COUNT')
MAIN_INVENTORY_COL_COUNT = config.getint('Constants', 'MAIN_INVENTORY_COL_COUNT')
SECONDARY_INVENTORY_ROW_COUNT = config.getint('Constants', 'SECONDARY_INVENTORY_ROW_COUNT')
SECONDARY_INVENTORY_COL_COUNT = config.getint('Constants', 'SECONDARY_INVENTORY_COL_COUNT')

COORDINATES_MAIN_INVENTORY_FIRST_CELL = tuple(map(int, config.get('Constants', 'COORDINATES_MAIN_INVENTORY_FIRST_CELL').split(',')))
COORDINATES_SECONDARY_INVENTORY_FIRST_CELL = tuple(map(int, config.get('Constants', 'COORDINATES_SECONDARY_INVENTORY_FIRST_CELL').split(',')))

COORDINATES_INVENTOR_TRANSMUTE_TAB = tuple(map(int, config.get('Constants', 'COORDINATES_INVENTOR_TRANSMUTE_TAB').split(',')))
COORDINATES_INVENTOR_DISMANTLE_TAB = tuple(map(int, config.get('Constants', 'COORDINATES_INVENTOR_DISMANTLE_TAB').split(',')))
COORDINATES_INVENTOR_ITEM_PLACEMENT_SPOT = tuple(map(int, config.get('Constants', 'COORDINATES_INVENTOR_ITEM_PLACEMENT_SPOT').split(',')))
COORDINATES_INVENTOR_DISMANTLE_BUTTON = tuple(map(int, config.get('Constants', 'COORDINATES_INVENTOR_DISMANTLE_BUTTON').split(',')))
COORDINATES_INVENTOR_DISMANTLE_CONFIRM_BUTTON = tuple(map(int, config.get('Constants', 'COORDINATES_INVENTOR_DISMANTLE_CONFIRM_BUTTON').split(',')))

# ---------------- General ----------------


def is_grim_dawn_focused():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if hwnd == 0:
        return False
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return "Grim Dawn" in buff.value


def sleep(x):
    time.sleep(x)

# ---------------- Mouse Actions ----------------


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def get_cursor_pos():
    point = Point()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return (point.x, point.y)


def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)


def send_right_click():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    sleep(SHORT_DELAY)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def send_left_click():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(SHORT_DELAY)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# ---------------- Helpers ----------------


def generate_coordinates(initial_coordinates, rows, cols):
    initial_x = initial_coordinates[0]
    initial_y = initial_coordinates[1]
    coordinates = []
    CELL_SIZE = INVENTORY_CELL_SIDE_LENGTH + INVENTORY_CELL_BORDER_LENGTH
    for row in range(rows):
        for col in range(cols):
            x = initial_x + col * CELL_SIZE
            y = initial_y + row * CELL_SIZE
            coordinates.append((x, y))
    return coordinates

# ---------------- Main Scripts ----------------


def sell_main_bag(keyboard_event):
    if not is_grim_dawn_focused():
        return
    original_cursor_pos = get_cursor_pos()
    inventory_cell_coordinates = generate_coordinates(COORDINATES_MAIN_INVENTORY_FIRST_CELL, MAIN_INVENTORY_ROW_COUNT, MAIN_INVENTORY_COL_COUNT)
    for coordinate in inventory_cell_coordinates:
        set_cursor_pos(coordinate[0], coordinate[1])
        if DEBUG:
            return
        send_right_click()
        if keyboard.is_pressed(SHORTCUT_EXIT_EARLY):
            print("Exiting sell_main_bag early.")
            set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])
            return
    set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])


def sell_secondary_bag(keyboard_event):
    if not is_grim_dawn_focused():
        return
    original_cursor_pos = get_cursor_pos()
    inventory_cell_coordinates = generate_coordinates(COORDINATES_SECONDARY_INVENTORY_FIRST_CELL, SECONDARY_INVENTORY_ROW_COUNT, SECONDARY_INVENTORY_COL_COUNT)
    for coordinate in inventory_cell_coordinates:
        set_cursor_pos(coordinate[0], coordinate[1])
        if DEBUG:
            return
        send_right_click()
        if keyboard.is_pressed(SHORTCUT_EXIT_EARLY):
            print("Exiting sell_secondary_bag early.")
            set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])
            return
    set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])


def dismantle_main_bag(keyboard_event):
    if not is_grim_dawn_focused():
        return
    original_cursor_pos = get_cursor_pos()
    inventory_cell_coordinates = generate_coordinates(COORDINATES_MAIN_INVENTORY_FIRST_CELL, MAIN_INVENTORY_ROW_COUNT, MAIN_INVENTORY_COL_COUNT)
    for coordinate in inventory_cell_coordinates:
        set_cursor_pos(COORDINATES_INVENTOR_TRANSMUTE_TAB[0], COORDINATES_INVENTOR_TRANSMUTE_TAB[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_DISMANTLE_TAB[0], COORDINATES_INVENTOR_DISMANTLE_TAB[1])
        send_left_click()
        set_cursor_pos(coordinate[0], coordinate[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_ITEM_PLACEMENT_SPOT[0], COORDINATES_INVENTOR_ITEM_PLACEMENT_SPOT[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_DISMANTLE_BUTTON[0], COORDINATES_INVENTOR_DISMANTLE_BUTTON[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_DISMANTLE_CONFIRM_BUTTON[0], COORDINATES_INVENTOR_DISMANTLE_CONFIRM_BUTTON[1])
        if DEBUG:
            return
        send_left_click()
        if keyboard.is_pressed(SHORTCUT_EXIT_EARLY):
            print("Exiting dismantle_main_bag early.")
            set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])
            return
    set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])


def dismantle_secondary_bag(keyboard_event):
    if not is_grim_dawn_focused():
        return
    original_cursor_pos = get_cursor_pos()
    inventory_cell_coordinates = generate_coordinates(COORDINATES_SECONDARY_INVENTORY_FIRST_CELL, SECONDARY_INVENTORY_ROW_COUNT, SECONDARY_INVENTORY_COL_COUNT)
    for coordinate in inventory_cell_coordinates:
        set_cursor_pos(COORDINATES_INVENTOR_TRANSMUTE_TAB[0], COORDINATES_INVENTOR_TRANSMUTE_TAB[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_DISMANTLE_TAB[0], COORDINATES_INVENTOR_DISMANTLE_TAB[1])
        send_left_click()
        set_cursor_pos(coordinate[0], coordinate[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_ITEM_PLACEMENT_SPOT[0], COORDINATES_INVENTOR_ITEM_PLACEMENT_SPOT[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_DISMANTLE_BUTTON[0], COORDINATES_INVENTOR_DISMANTLE_BUTTON[1])
        send_left_click()
        set_cursor_pos(COORDINATES_INVENTOR_DISMANTLE_CONFIRM_BUTTON[0], COORDINATES_INVENTOR_DISMANTLE_CONFIRM_BUTTON[1])
        if DEBUG:
            return
        send_left_click()
        if keyboard.is_pressed(SHORTCUT_EXIT_EARLY):
            print("Exiting dismantle_secondary_bag early.")
            set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])
            return
    set_cursor_pos(original_cursor_pos[0], original_cursor_pos[1])

# ---------------- Tray Icon ----------------


def exit_program(icon, item):
    print("Exiting via tray icon.")
    icon.stop()
    os._exit(0)


def create_image():
    icon_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "assets", "icon.ico")
    return Image.open(icon_path)


def setup_tray_icon():
    menu = pystray.Menu(pystray.MenuItem("Exit", exit_program))
    icon = pystray.Icon("GD Utils", create_image(), "GD Utils", menu)
    icon.run()


# ---------------- Key Listeners ----------------
keyboard.on_press_key(SHORTCUT_SELL_MAIN_BAG, sell_main_bag)
keyboard.on_press_key(SHORTCUT_SELL_SECONDARY_BAG, sell_secondary_bag)
keyboard.on_press_key(SHORTCUT_DISMANTLE_MAIN_BAG, dismantle_main_bag)
keyboard.on_press_key(SHORTCUT_DISMANTLE_SECONDARY_BAG, dismantle_secondary_bag)

# ---------------- Start Tray Icon and Main Loop ----------------
tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
tray_thread.start()

print("Listening for F1-F4 keys.")
print("F1 to SELL all items in MAIN inventory.")
print("F2 to SELL all items in SECONDARY inventory.")
print("F3 to DISMANTLE all items in MAIN inventory.")
print("F4 to DISMANTLE all items in SECONDARY inventory.")

# Instead of keyboard.wait(), run an infinite loop that sleeps
while True:
    sleep(0.1)
