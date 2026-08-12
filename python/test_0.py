import pyautogui


locations = {
    "Green Hill": {
        "left": 933 / 1920,
        "top": 180 / 1080,
        "width": (985 - 933) / 1920,
        "height": (244 - 180) / 1080
    },
    "Lost Valley": {
        "left": 1190 / 1920,
        "top": 353 / 1080,
        "width": (1246 - 1190) / 1920,
        "height": (428 - 353) / 1080
    },

    "Emerald Hill": {
        "left": 1095 / 1920,
        "top": 662 / 1080,
        "width": (1149 - 1095) / 1920,
        "height": (732 - 662) / 1080
    },

    "Hill Top": {
        "left": 680 / 1920,
        "top": 357 / 1080,
        "width": (733 - 680) / 1920,
        "height": (428 - 357) / 1080
    },

    "City Escape": {
        "left": 777 / 1920,
        "top": 668 / 1080,
        "width": (828 - 777) / 1920,
        "height": (729 - 668) / 1080
    }
}


# Get current screen resolution
screen_width, screen_height = pyautogui.size()

print(f"Current resolution: {screen_width}x{screen_height}")
print()


for name, region in locations.items():

    # Scale the 1920x1080 coordinates to the current resolution
    left = int(region["left"] * screen_width)
    top = int(region["top"] * screen_height)
    width = int(region["width"] * screen_width)
    height = int(region["height"] * screen_height)

    print(
        f"{name}: "
        f"x={left}, y={top}, "
        f"width={width}, height={height}"
    )

    screenshot = pyautogui.screenshot(
        region=(left, top, width, height)
    )

    filename = (
        name.lower().replace(" ", "_")
        + "_portal.png"
    )

    screenshot.save(filename)

    print(f"Saved: {filename}")
    print()


print("Done.")