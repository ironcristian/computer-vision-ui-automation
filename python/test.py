import mss
from PIL import Image

ZONE_BUTTON_COORDINATES = {
    "COOL EDGE": {
        "left": 934,
        "top": 176,
        "width": 990 - 934,    # 56
        "height": 236 - 176    # 60
    }
}

with mss.MSS() as sct:
    for zone, coords in ZONE_BUTTON_COORDINATES.items():

        screen = {
            "left": coords["left"],
            "top": coords["top"],
            "width": coords["width"],
            "height": coords["height"]
        }

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        filename = f"{zone.replace(' ', '_').lower()}_locked_portal.png"
        image.save(filename)

        print(f"Saved {filename}")