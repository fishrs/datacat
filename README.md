# Fishing Data Viewer GUI

This Python application provides a graphical user interface (GUI) for viewing and managing fishing data stored in `.fson` files.

Using cutting edge technology we have developed the brand new `.fson` file format.. that's literally just json but with an f for fish :)

## Features

- Load `.fson` files containing fishing data.
- Display loaded data in a scrollable list with options to label each entry as fish or no fish.
- Calculate and display the average pull of selected entries.
- Save labeled data back to the original `.fson` file.

## Requirements

- Python 3.x
- tkinter library (usually included with Python installations)

# Running

To run this GUI, simply cd into the root directory and run 

```
python3 main.py
```

It's that easy, now get out there and start labeling fish data 🦾

## Usage

1. **Load Data**: Click on "Load .fson File" to select and load a `.fson` file.
2. **View Data**: Loaded data is displayed in a list with details including longitude, latitude, pull, and current label status.
3. **Label Entries**: Select one or more entries and click either "FISH" or "NO FISH" to label them accordingly.
4. **Save Data**: Click "Save" to save the labeled data back to the original `.fson` file.
