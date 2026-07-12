import mss
import pytesseract
from PIL import Image
import pyautogui


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


screen_width, screen_height = pyautogui.size()

screen = {
    "left": int((1273 / 1920) * screen_width),
    "top": int((778 / 1080) * screen_height),
    "width": int(((1311 - 1273) / 1920) * screen_width),
    "height": int(((816 - 778) / 1080) * screen_height)
}


with mss.MSS() as sct:

    screenshot = sct.grab(screen)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    # Save original
    image.save("../Auto_Rebirther_Screenshots/X_Rebirth_Screenshot_Permanent/x_symbol.png")


  