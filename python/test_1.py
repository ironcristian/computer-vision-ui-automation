import pyautogui


REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080


locations = {
    "Speed Jungle": {
        "left": 934 / 1920,
        "top": 176 / 1080,
        "width": (990 - 934) / 1920,
        "height": (236 - 176) / 1080
    },

    "No Place": {
        "left": 1190 / 1920,
        "top": 360 / 1080,
        "width": (1247 - 1190) / 1920,
        "height": (422 - 360) / 1080
    },

    "Cyber Station": {
        "left": 1091 / 1920,
        "top": 665 / 1080,
        "width": (1148 - 1091) / 1920,
        "height": (724 - 665) / 1080
    },

    "Metal City": {
        "left": 781 / 1920,
        "top": 669 / 1080,
        "width": (828 - 781) / 1920,
        "height": (727 - 669) / 1080
    },

    "New Yoke": {
        "left": 673 / 1920,
        "top": 361 / 1080,
        "width": (731 - 673) / 1920,
        "height": (425 - 361) / 1080
    }
}


# Detect current screen resolution
screen_width, screen_height = pyautogui.size()

print(f"Current resolution: {screen_width}x{screen_height}")
print()


for name, region in locations.items():

    # Scale coordinates to current resolution
    left = int(region["left"] * screen_width)
    top = int(region["top"] * screen_height)
    width = int(region["width"] * screen_width)
    height = int(region["height"] * screen_height)

    print(
        f"{name}: "
        f"x={left}, y={top}, "
        f"width={width}, height={height}"
    )

    # Take screenshot
    screenshot = pyautogui.screenshot(
        region=(left, top, width, height)
    )

    # Filename
    filename = (
        name.lower().replace(" ", "_")
        + "_portal.png"
    )

    screenshot.save(filename)

    print(f"Saved: {filename}")
    print()


print("Done.")