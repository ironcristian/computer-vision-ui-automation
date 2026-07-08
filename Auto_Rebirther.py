import mss
import pytesseract
from PIL import Image, ImageOps
import time
import os
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

screen_width, screen_height = pyautogui.size()

IMAGE_NAME = "Screenshot.png"
LEVEL_LEFT_RATIO = 650 / 1920
LEVEL_TOP_RATIO= 20 / 1080
LEVEL_WIDTH_RATIO = (730 - 650) / 1920
LEVEL_HEIGHT_RATIO = (60 - 2) / 1080


# IF you're reading this dont mind this message, it's for me.
# The 2 corners were (650, 20) and (730, 60)


def start_player_setup():
    print("Waiting 8 seconds so you can set yourself up. Go to your CHOSEN area and do not move when you spawn in.")
    for i in range(8):
        time.sleep(1)
        print(f"{8 - i} seconds left")

#start_player_setup()


def take_screenshot_and_analyze_level():
    with mss.MSS() as sct:


        screen = { # Screen area where the level is
            "left": int(LEVEL_LEFT_RATIO * screen_width),
            "top": int(LEVEL_TOP_RATIO * screen_height),
            "width": int(LEVEL_WIDTH_RATIO * screen_width),
            "height": int(LEVEL_HEIGHT_RATIO * screen_height)
        }

        screenshot = sct.grab(screen)  # Returns the array of pixels in that screenshot

        image = Image.frombytes(
            "RGB", # How to interpret the data
            screenshot.size, # Pillow needs the size of the image. Even though screenshot is an array of pixels screenshot.rgb only returns rgb values with no white space so it needs to know the size
            screenshot.rgb
        )

        image = image.resize(
            (800, 400)
        )

        text = pytesseract.image_to_string(
            image,
            config="--psm 7 -c tessedit_char_whitelist=0123456789" # pytesseract will now return any characters in the screenshot and return 
        )

        image.save("upscaled_level_test.png")
        
    return text.strip()

EGG_LEFT_RATIO = 63 / 1920
EGG_TOP_RATIO= 574 / 1080
EGG_WIDTH_RATIO = (314 - 63) / 1920
EGG_HEIGHT_RATIO = (623 - 574) / 1080
def take_screenshot_and_analyze_egg():
    with mss.MSS() as sct:

        screen = { # Screen area where the level is
            "left": int(EGG_LEFT_RATIO * screen_width),
            "top": int(EGG_TOP_RATIO * screen_height),
            "width": int(EGG_WIDTH_RATIO * screen_width),
            "height": int(EGG_HEIGHT_RATIO * screen_height)
        }

        screenshot = sct.grab(screen)  # Returns the array of pixels in that screenshot

        image = Image.frombytes(
            "RGB", # How to interpret the data
            screenshot.size, # Pillow needs the size of the image. Even though screenshot is an array of pixels screenshot.rgb only returns rgb values with no white space so it needs to know the size
            screenshot.rgb
        )

        egg_screenshot = Image.open(f"Auto_Rebirther_Screenshots/Egg_Notification_Screenshot_Permanent/egg_notification.png")
        if (list(image.getdata()) == (list(egg_screenshot.getdata()))):
            return True
        else:
            return False

            

    
def send_command(command):

    with open("command.txt", "w") as f:
        f.write(f"{command}")


    while not os.path.exists("done.txt"):
        time.sleep(0.1)

    os.remove("done.txt")
    

current_level = "" # Variable to store level from the string


last_level_change = time.time()
last_xp_claim = time.time()
last_image_analysis = time.time()
last_egg_check = time.time()

print("Waklking")
send_command("Walk")
print("Walking done")


while True:
    current_time = time.time()


    # Egg check
    if current_time - last_egg_check >= 5:

        if take_screenshot_and_analyze_egg():
            print("Claiming Egg")
            send_command("Claim_EGG")
            print("Claimed Egg")
           
        last_egg_check = current_time


    # Rebirth Check
    if current_time - last_image_analysis >= 5:
        text = take_screenshot_and_analyze_level()
        print(text) 
        print(current_level)

        if text != current_level:
            current_level = text
            last_level_change = current_time
        else:
            if current_time - last_level_change > 30:
                print("Rebirthing")
                send_command("Rebirth")
                print("Rebirthed")
                last_level_change = current_time
                last_xp_claim = current_time

        last_image_analysis = current_time

    # Claim XP every 3 seconds
    if current_time - last_xp_claim >= 3:
        print("Claiming XP")
        send_command("Claim_XP")
        print("Claimed XP")
        last_xp_claim = current_time