import mss
import pytesseract
from PIL import Image
import pyautogui


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


screen_width, screen_height = pyautogui.size()

screen = {
    "left": int((1327 / 1920) * screen_width),
    "top": int((1050 / 1080) * screen_height),
    "width": int(((1406 - 1327) / 1920) * screen_width),
    "height": int(((1078 - 1050) / 1080) * screen_height)
}


with mss.MSS() as sct:

    screenshot = sct.grab(screen)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    # Save original
    image.save("original.png")

    # Scale
    image = image.resize(
        (image.width * 4, image.height * 4),
        Image.Resampling.NEAREST
    )

    image.save("scaled.png")


    # Test different OCR modes
    for mode in [6, 7, 11, 13]:
        text = pytesseract.image_to_string(
            image,
            config=f"--psm {mode}"
        )

        print(f"PSM {mode}: {repr(text)}")