
import mss
import pytesseract
from PIL import Image, ImageChops
import time
import os
import pyautogui
import numpy as np
import atexit
import win32gui
import win32con
import configparser
import subprocess

import constants


# ==========================
# Configuration
# ==========================

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

screen_width, screen_height = pyautogui.size()
ahk_process = None


# ==========================
# Player Setup / Portal Detection
# ==========================

def start_player_setup():
    print("Starting setup.")
    find_player_portal_button()
    print("Located portal travel button.")



def start_ahk_script():
    global ahk_process

    ahk_process = subprocess.Popen(
    [
        r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe",
        "../ahk/main.ahk"
    ]
)


def focus_roblox_window():

    window_title = "Roblox"
    hwnd = win32gui.FindWindow(None, window_title) # The none argument specified the classname. We dont care about that. Also hwnd means h=handle, wnd=window. {Handle to a Window}

    if hwnd: # This means that win32gui found a window named Roblox and assigned it a handle
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE) # ShowWindow will show the window if it is minimized, The second paramater defines HOW you want to show it. SW_MAXIMIZE will show the screen in fullscreen
        win32gui.SetForegroundWindow(hwnd) # This will actually focus the window. Same clicking on a window when alt tabbing back into it
    else:
        print("Window not found. Do you have roblox running?")


def save_portal_coordinates(x, y):

    portal_coordinate_file = configparser.ConfigParser() # This creates an INI object


    portal_coordinate_file["Portal"] = {
       "portal_button_x": x,
       "portal_button_y": y
    }

    with open("../ahk/portal_coordinates.ini", "w") as f:
        portal_coordinate_file.write(f) # Here we dont use f.write because configparses has its own built in ".write" function that automatically write the INI file syntax for you,


def find_player_portal_button():
    focus_roblox_window()
    for portal in constants.POSSIBLE_PORTAL_COORDINATES:
        left = int(portal["left_ratio"] * screen_width)
        top = int(portal["top_ratio"] * screen_height)
        width = int(portal["width_ratio"] * screen_width)
        height = int(portal["height_ratio"] * screen_height)

        screen = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }

        with mss.MSS() as sct:

            screenshot = sct.grab(screen)

            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )

            image = image.resize(
                (image.width * 4, image.height * 4),
                Image.Resampling.NEAREST
            )

            text = pytesseract.image_to_string(
                image,
                config="--psm 7" # This means single line. It makes it easier for tesseract to detect the word
            )
            if text.strip().lower() == "travel":
                x, y = (portal["button_coordinates"][0] / 1920), (portal["button_coordinates"][1] / 1080)
                save_portal_coordinates(x, y)
                print(text)
                print("Located portal travel button.")
                break
            else:
                continue


# ==========================
# Image Comparison
# ==========================

def image_similarity(image1, image2, threshold=10):

    difference = ImageChops.difference(image1, image2)

    difference_np_array = np.array(difference)

    average_pixel_difference = difference_np_array.mean()

    print(average_pixel_difference)

    return average_pixel_difference < threshold


# ==========================
# Screenshot Analysis
# ==========================

def take_screenshot_and_analyze_level():

    with mss.MSS() as sct:

        screen = {
            "left": int(constants.LEVEL_LEFT_RATIO * screen_width),
            "top": int(constants.LEVEL_TOP_RATIO * screen_height),
            "width": int(constants.LEVEL_WIDTH_RATIO * screen_width),
            "height": int(constants.LEVEL_HEIGHT_RATIO * screen_height)
        }

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        level_screenshot = Image.open(
            "../Auto_Rebirther_Screenshots/Level_Bar_Permanent/level_bar_section.png"
        )

        if image_similarity(image, level_screenshot):
            return True
        else:
            return False


def take_screenshot_and_analyze_egg():

    with mss.MSS() as sct:

        screen = {
            "left": int(constants.EGG_LEFT_RATIO * screen_width),
            "top": int(constants.EGG_TOP_RATIO * screen_height),
            "width": int(constants.EGG_WIDTH_RATIO * screen_width),
            "height": int(constants.EGG_HEIGHT_RATIO * screen_height)
        }

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        egg_screenshot = Image.open(
            "../Auto_Rebirther_Screenshots/Egg_Notification_Screenshot_Permanent/egg_notification.png"
        )

        if list(image.getdata()) == list(egg_screenshot.getdata()):
            return True
        else:
            return False


def auto_run_entered_check(zone):
    time.sleep(3)
    with mss.MSS() as sct:
        screen = {
            "left": int((1273 / 1920) * screen_width),
            "top": int((778 / 1080) * screen_height),
            "width": int(((1311 - 1273) / 1920) * screen_width),
            "height": int(((816 - 778) / 1080) * screen_height)
        }

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb # This is the actual raw pixel data. Example: (205, 54, 23)
        )

        x_screenshot = Image.open("../Auto_Rebirther_Screenshots/X_Rebirth_Screenshot_Permanent/x_symbol.png")

        if not image_similarity(image, x_screenshot):
            send_command(zone)

# ==========================
# AutoHotkey Communication
# ==========================

def send_command(command):

    with open("../command.txt", "w") as f:
        f.write(f"{command}")

    while not os.path.exists("../done.txt"):
        time.sleep(0.1)

    os.remove("../done.txt")


def clear_command_and_close_ahk():

    with open("../command.txt", "w") as f:
        pass

    if ahk_process and ahk_process.poll() is None:
        ahk_process.terminate()


# ==========================
# Automation State
# ==========================

last_level_change = time.time()
last_xp_claim = time.time()
last_image_analysis = time.time()
last_egg_check = time.time()


# ==========================
# Main Automation Loop
# ==========================

def begin_automation(zone):
    
    global last_level_change, last_xp_claim, last_image_analysis, last_egg_check

    start_player_setup()
    print("Starting ahk script.")
    start_ahk_script()
    print("Started ahk script.")

    print("Starting automation.")

    print(f"Setting up {zone}")
    send_command(zone)
    auto_run_entered_check(zone) # Checks if the walk to autorun worked. If not it sends the command again
    print("Setup done")


    while True:
        current_time = time.time()


        # Egg check

        if current_time - last_egg_check >= 5:
            if take_screenshot_and_analyze_egg():

                print("Claiming Egg")
                send_command("Claim_EGG")
                auto_run_entered_check(zone)
                print("Claimed Egg")

            last_egg_check = current_time



        # Rebirth check

        if current_time - last_image_analysis >= 5:
            result = take_screenshot_and_analyze_level()


            if not result:
                last_level_change = current_time


            else:
                if current_time - last_level_change > 30:

                    print("Rebirthing")
                    send_command("Rebirth")
                    auto_run_entered_check(zone)
                    print("Rebirthed")

                    last_level_change = current_time
                    last_xp_claim = current_time

            last_image_analysis = current_time



        # XP check

        if current_time - last_xp_claim >= 3:

            print("Claiming XP")
            send_command("Claim_XP")
            print("Claimed XP")

            last_xp_claim = current_time



# ==========================
# Cleanup
# ==========================

atexit.register(clear_command_and_close_ahk)