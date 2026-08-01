import mss
import pyautogui
from PIL import Image

screen_width, screen_height = pyautogui.size()

ZONE_BUTTON_COORDINATES = {
    "Cool Edge": {
        "left": 934 / 1920,
        "top": 176 / 1080,
        "width": (990 - 934) / 1920,
        "height": (236 - 176) / 1080
    }
}

with mss.MSS() as sct:
    for zone, coords in ZONE_BUTTON_COORDINATES.items():

        screen = {
            "left": int(coords["left"] * screen_width),
            "top": int(coords["top"] * screen_height),
            "width": int(coords["width"] * screen_width),
            "height": int(coords["height"] * screen_height)
        }

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        filename = f"{zone.lower().replace(' ', '_')}_portal.png"
        image.save(filename)

        print(f"Saved {filename}")