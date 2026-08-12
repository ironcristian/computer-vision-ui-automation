import pyautogui


REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080


locations = {
    "Cool Edge": {
        "left": 934 / 1920,
        "top": 176 / 1080,
        "width": (990 - 934) / 1920,
        "height": (236 - 176) / 1080
    },

    "Kronos Island": {
        "left": 1165 / 1920,
        "top": 579 / 1080,
        "width": (1225 - 1165) / 1920,
        "height": (644 - 579) / 1080
    },

    "Pixel Green Hill": {
        "left": 700 / 1920,
        "top": 581 / 1080,
        "width": (754 - 700) / 1920,
        "height": (642 - 581) / 1080
    }
}


screen_width, screen_height = pyautogui.size()

print(f"Current resolution: {screen_width}x{screen_height}")
print()


for name, region in locations.items():

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