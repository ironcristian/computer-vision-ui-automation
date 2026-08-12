import pyautogui


REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080


locations = {
    "Space Colony": {
        "left": 940 / 1920,
        "top": 182 / 1080,
        "width": (984 - 940) / 1920,
        "height": (238 - 182) / 1080
    },

    "Radical Highway": {
        "left": 1195 / 1920,
        "top": 369 / 1080,
        "width": (1241 - 1195) / 1920,
        "height": (424 - 369) / 1080
    },

    "Pumpkin Hill": {
        "left": 1091 / 1920,
        "top": 666 / 1080,
        "width": (1151 - 1091) / 1920,
        "height": (732 - 666) / 1080
    },

    "Autumn Forest": {
        "left": 776 / 1920,
        "top": 661 / 1080,
        "width": (830 - 776) / 1920,
        "height": (728 - 661) / 1080
    },
    "Metro City": {
            "left": 675 / 1920,
            "top": 363 / 1080,
            "width": (732 - 675) / 1920,
            "height": (423 - 363) / 1080
    },
    
}


# Detect current screen resolution
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