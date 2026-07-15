import mss
from PIL import Image

SPACE_COLONY_PORTAL = ((934, 176), (990, 236))

with mss.mss() as sct:

    top_left, bottom_right = SPACE_COLONY_PORTAL

    monitor = {
        "left": top_left[0],
        "top": top_left[1],
        "width": bottom_right[0] - top_left[0],
        "height": bottom_right[1] - top_left[1]
    }

    screenshot = sct.grab(monitor)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    image.save("space_colony_portal.png")

    print("Saved space_colony_portal.png")