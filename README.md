# Introduction

Written in Python, this tool generates an executable that assists with inventory management in Grim Dawn. It uses specific screen coordinates to interact with inventory cells, simulate right-click actions, and more.

![Demo](./assets/demo.gif)

# Features

- **Automated Inventory Management:**  
  Quickly sell or dismantle every item in the inventory with a single key press.

- **System Tray Integration:**  
  A tray icon provides a right-click "Exit" option to easily terminate the app.

- **Configurable Behavior:**  
  Uses a configuration file (`config.ini`) to store constants such as inventory dimensions and keyboard shortcuts.

# Usage

The application utilizes the following hotkeys:

- **F1** – Sell all items in the **Main Inventory** while an NPC window is open.
  - Iterates over each cell in the main inventory and simulates right click
- **F2** – Sell all items in the **Secondary Inventory** while an NPC window is open.
  - Iterates over each cell in the active secondary inventory and simulates right click 
- **F3** – Dismantle all items in the **Main Inventory** while the Inventor window is open.
  - Iterates over each cell in the main inventory and simulates a series of clicks to dismantle. 
- **F4** – Dismantle all items in the **Secondary Inventory** while the Inventor window is open.
  - Iterates over each cell in the main inventory and simulates a series of clicks to dismantle.  

# Installation

> **Note:** The coordinates used in this application are written for a 1920x1080 screen resolution with the default UI scale. Adjustments will be needed for different screen resolutions or UI scaling settings.

[Download latest version from Releases](https://github.com/MustafaErvaErgul/GD-Tools/releases)

# Configuration

As previously mentioned, the config.ini file contains coordinates that are very important for the program to work properly. You will need to adjust the values in the config.ini for your setup if you are not using 1920x1080 resolution with the default UI scale. Here is what the config file looks like 

```
[General]
DEBUG = False
INVENTORY_CELL_SIZE = 30
INVENTORY_CELL_BORDER_SIZE = 1

[Shortcuts]
SELL_ALL = F2
SELL_SECONDARY = F3
DISMANTLE_ALL = F4
DISMANTLE_SECONDARY = F5
GLOBAL_EXIT = F10

[Coordinates]
TRANSMUTE_TAB_LOCATION = 743,266
DISMANTLE_TAB_LOCATION = 639,271
DISMANTLE_ITEM_PLACEMENT_LOCATION = 610,525
DISMANTLE_BUTTON_LOCATION = 635,842
DISMANTLE_CONFIRM_BUTTON_LOCATION = 851,587

[Sleeps]
SLEEP_PANEL_OPEN = 0.01
SLEEP_ACTION = 0.001

[Main_Inventory_Grid]
start_x = 830
start_y = 642
cols = 12
rows = 8

[Secondary_Inventory_Grid]
start_x = 1213
start_y = 640
cols = 8
rows = 8
```

# Packaging the application yourself

Ensure you have Python installed (version 3.6+ recommended). You will also need the following non-native Python packages:

- **PyInstaller** – for packaging the app into a single executable.
- **keyboard** – for capturing and handling key press events.
- **ConfigParser** – for reading configuration files (this is included in Python’s standard library as `configparser`).
- **Pillow (PIL)** – for image processing, required by the tray icon.
- **pystray** – for creating the system tray icon.

```
pip install pyinstaller keyboard pillow pystray
```

To package the application
```
.\package.bat
```
