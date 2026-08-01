import mss
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
import cv2
import sys
from pathlib import Path

import constants


# ==========================
# Configuration
# ==========================

screen_width, screen_height = pyautogui.size()
scale_x, scale_y = (screen_width / 1920), (screen_height / 1080)
ahk_process = None
current_page = None

# ==========================
# Player Setup / Portal Detection
# ==========================

def start_player_setup():
    print("Starting setup.")
    find_player_portal_button()
    print("Located portal travel button.")



def start_ahk_script():
    global ahk_process
    
    print("Starting ahk script")
    ahk_process = subprocess.Popen(
        [
            r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe",
            "../ahk/main.ahk"
        ]
    )

    print("Started ahk script.")


def focus_roblox_window():

    print("Putting Roblox window into focus.")
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

    # This turns the file into a numpy array
    template = cv2.imread("../screenshots/portal_button.png")

    # Scale the based of the individual users resolution
    template = cv2.resize(
        template,
        None,
        fx=scale_x,
        fy=scale_y,
        interpolation=cv2.INTER_LINEAR
    )

    with mss.MSS() as sct:

        screen = {
            "left": 0,
            "top": int(constants.POSSIBLE_PORTAL_LOCATION_HEIGHT_RATIO * screen_height),
            "width": screen_width,
            "height": screen_height - int(constants.POSSIBLE_PORTAL_LOCATION_HEIGHT_RATIO * screen_height)
        }
        print(f"[DEBUG] Screen capture region: {screen}")
        screenshot = sct.grab(screen) # This returns a screenshot.Screenshot objects containing varios data about the iamge.
        print(f"[DEBUG] Screenshot captured. Size: {screenshot.size}")
        screenshot_pixels = np.array(screenshot) # The way np can conver the screnshot to an array of pixel values it because the screenshot object provides a way to be converted into an array. {__array__ or maybe __buffer__}
        print(f"[DEBUG] Screenshot array shape: {screenshot_pixels.shape}")        

        # Remove the alpha channel because mss returns BGRA and also we dont want transparency to affect out search. If we move in game that could affect the pixels with alpha in them.
        screenshot_pixels = cv2.cvtColor(
            screenshot_pixels,
            cv2.COLOR_BGRA2BGR
        )
        print(f"[DEBUG] Converted screenshot shape: {screenshot_pixels.shape}")
        result = cv2.matchTemplate( # This returns a grid/matrix of all points that it checked and its similarity value. Out chosen comparison method {TM_CCOEFF_NORMED} returns 1.0 if its a perfect match and 0.0 if its not.
            screenshot_pixels,
            template,
            cv2.TM_CCOEFF_NORMED
        )

        print(f"[DEBUG] Template matching complete. Result shape: {result.shape}")

        # minMaxLoc returns the min_value, max_value, where the minimum happened, and where the maximum happened.
        # Since we only care the best score we only take the 2n and 4th value that the method returns and we name the 2nd {confidence} because that is how confident cv2 is that its the same picture
        _, confidence, _, location = cv2.minMaxLoc(result) 
        # Also. Location returns the top left corner of the match it found from the {screen} area we checked. So if we checked 1920, 90 it could return 1300, 34 But those obviouslt arent the screen coordinates.
        # We need to turn them into the real screen coordinates.

        if confidence > 0.90:
            real_x = location[0] # location[0] is the x value of the tuple location
            real_y = location[1] + screen["top"] # Here we add the y coord of the small area we checked with the y value of all the screen size up to the heigth of the image. to make easier to understand.
            # Imagine this. Forget about the coords of the pic. Say we find the portal at  1050. And the portal spans from 1050 down to 1060. Now lets say to make cv2 do less work we first crop the area where,
            # We know the image will be. We know it will be at the bottom somewhere anywhere along the x axis but always after y = 1040. Now cropped region will be 1920, 40. When we run cv2 on this image,
            # It will return something like 1500, 10. Because top of image starts at y = 0. Now to get the real coordinates back we need to add 10 + 1040. So now we get the real screen coordinates
            print(f"Located portal travel button at: {real_x}, {real_y}")
            save_portal_coordinates(real_x / screen_width, real_y / screen_height)
            print("Saved button coordinates inside ini file.")

        else:
            print("[WARNING] Portal button not found.")
            print(f"[DEBUG] Highest confidence was only {confidence:.4f}")
            print("Travel button not found. Do you have Fast Travel activated in the game settings?")




# ==========================
# Image Comparison
# ==========================


def ensure_numpy(image):
    if isinstance(image, Image.Image):
        result = np.array(image)

    return result


def is_image_similar(screenshot, template, threshold=0.9):

    screenshot = ensure_numpy(screenshot)
    template = ensure_numpy(template)

    result = cv2.matchTemplate( # This returns a grid/matrix of all points that it checked and its similarity value. Our chosen comparison method {TM_CCOERR_NORMED} returns 1.0 if its a perfect match and 0.0 if its not.
        screenshot,
        template,
        cv2.TM_CCORR_NORMED
    )

    _, confidence, _, _  = cv2.minMaxLoc(result)

    print(confidence)
    return confidence > threshold



# ==========================
# Screenshot Analysis
# ==========================

def portal_page_distance_check_and_command_send(zone):
    global current_page

    # If we are already on the page we want to get to just send the {zone} straight away and skin the page check and distance
    if current_page is not None and current_page == constants.ZONES_PAGE_NUMBER[zone]:
        return 0

    
    folders = [
        Path("../screenshots/portal_screenshots"),
        Path("../screenshots/portal_locked_screenshots")
    ]

    # This code is to check what page we are currently on. So we just cehck the first location of every page. {The top portal}
    for folder in folders:
        for file in folder.iterdir(): # Creates iterable containing all files in that folder

            print(f"Checking file {file.name}")
            if folder.name == "portal_locked_screenshots":
                portal_name = file.name.replace("_portal_locked.png", "").upper() # Removed "_portal.png" from filename and makes it capitalized so I can access the constants.
            else:
                portal_name = file.name.replace("_portal.png", "").upper() # Removed "_portal.png" from filename and makes it capitalized so I can access the constants.


            command_name = portal_name.replace("_", " ").title() # This basically converts "green_hill" into "Green Hill"
            zone_portal_coordinates = constants.ZONE_BUTTON_COORDINATES[command_name]

            with mss.MSS() as sct:

                screen = {
                    "left": int(zone_portal_coordinates["left"] * screen_width),
                    "top": int(zone_portal_coordinates["top"] * screen_height),
                    "width": int(zone_portal_coordinates["width"] * screen_width),
                    "height": int(zone_portal_coordinates["height"] * screen_height)
                }

                print(screen)

                screenshot = sct.grab(screen)

                image = Image.frombytes( # Screenshot of the portal we are comparing from in game.
                    "RGB",
                    screenshot.size,
                    screenshot.rgb
                )

            portal_image = Image.open(file) # Image of portal we are currently on to compare.
            portal_image = resize_PIL_image(portal_image)

            portal_image.save("debug_template.png")
            image.save("debug_screenshot.png")


            # If the current portal we are checking is the same as the screenshot we took
            if is_image_similar(portal_image, image):
                page_distance = constants.ZONES_PAGE_NUMBER[zone] - constants.ZONES_PAGE_NUMBER[command_name]
                current_page = constants.ZONES_PAGE_NUMBER[zone]
                return page_distance
            else:
                continue


            # if is_portal_locked(zone):
            #     print(f"{zone} portal is currently locked. Choose a different zone")
            # else:
            #     return True


def resize_PIL_image(image):
    new_width = int(image.width * scale_x)
    new_height = int(image.height * scale_y)
    
    portal_image = image.resize(
        (new_width, new_height),
        Image.Resampling.BILINEAR
    )

    return portal_image


# Checks if the chosen {zone} portal is locked
def is_portal_locked(zone):


    portal_locked = f"../screenshots/portal_locked_screenshots/{zone.replace(' ', '_').lower()}_portal_locked.png"
    portal_unlocked = f"../screenshots/portal_screenshots/{zone.replace(' ', '_').lower()}_portal.png"


    portal_locked = resize_PIL_image(Image.open(portal_locked))
    portal_unlocked = resize_PIL_image(Image.open(portal_unlocked))

    with mss.MSS() as sct:

        screen = {
            "left": int(constants.ZONE_BUTTON_COORDINATES[zone]["left"] * screen_width),
            "top": int(constants.ZONE_BUTTON_COORDINATES[zone]["top"] * screen_height),
            "width": int(constants.ZONE_BUTTON_COORDINATES[zone]["width"] * screen_width),
            "height": int(constants.ZONE_BUTTON_COORDINATES[zone]["height"] * screen_height)
        } 

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        # portal_screenshot = Image.open(f"../screenshots/portal_locked_screenshots/{file_name}")
        if is_image_similar(image, portal_locked) == True:
            return True

        
        if is_image_similar(image, portal_unlocked) == True:
            return False

        print(f"Wrong zone. {zone}")

        return
        



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
            "../screenshots/level_bar_section.png"
        )

        level_screenshot = resize_PIL_image(level_screenshot)



        if is_image_similar(image, level_screenshot):
            print("Detected max level. Rebirth available")
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
            "../screenshots/egg_notification.png"
        )

        egg_screenshot = resize_PIL_image(egg_screenshot)

        if list(image.getdata()) == list(egg_screenshot.getdata()):
            print("Detected egg notification")
            return True
        else:
            return False


def auto_run_entered_check(zone):
    time.sleep(2) # This is to wait for the black screen animation to pass when you enter auto-run
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

        x_screenshot = Image.open("../screenshots/x_symbol.png")
        x_screenshot = resize_PIL_image(x_screenshot)

        if not is_image_similar(image, x_screenshot):
            print(f"Auto-run zone has not succesfully been entered. Sending the command {zone} again.")
            send_command(zone)

# ==========================
# AutoHotkey Communication
# ==========================

def send_command(command):
    global rebirthing_in_progress
    page_distance = None

    print(command)
    if command in constants.ZONE_BUTTON_COORDINATES:
        send_command("Click_Portal") 
        print("CLICKED PORTAL BUTTON")
        # This will send a command to click the portal button. The code will be stuck on this until it recieved a done.txt.
        # I will then detect what page we are on and change to the right one if the player is not on it. And then I will check if the player has that place unlocked.

        page_distance = portal_page_distance_check_and_command_send(command)

        send_command(page_distance)

        if is_portal_locked(command):
            print(f"Current {command} is locked. Please choose a diffrent zone")
            send_command("Close_Portal")
            return
            


    with open("../command.txt", "w") as f:
        print(f"Sending command: {command}")
        f.write(f"{command}")


    print(f"Checking if ahk has finished performing command: {command}")
    while not os.path.exists("../done.txt"):
        time.sleep(0.1)

    print(f"ahk has finished performing: {command}")

    os.remove("../done.txt")
    print("Done file deleted:", not os.path.exists("../done.txt"))

    if command == "Rebirth":
        print("Rebirth no longer in progress")
        rebirthing_in_progress = False


def clear_command_and_close_ahk():
    
    print("Clearing command.txt file.")
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

rebirthing_in_progress = False


# ==========================
# Main Automation Loop
# ==========================

def begin_automation(zone):
    
    global last_level_change, last_xp_claim, last_image_analysis, last_egg_check, rebirthing_in_progress

    if rebirthing_in_progress:
        rebirthing_in_progress = False

    start_player_setup()
    start_ahk_script()

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
                print("Checking if auto-run zone has been succesfully entered.")
                auto_run_entered_check(zone)
                print("Claimed Egg")

            last_egg_check = current_time



        # Rebirth check

        if current_time - last_image_analysis >= 5:
            result = take_screenshot_and_analyze_level()


            if not result:
                last_level_change = current_time


            else:
                if current_time - last_level_change > 30 and not rebirthing_in_progress:

                    print("Starting Rebirth")
                    send_command("Rebirth") # We check if we entered the auto-run area becuase at the end of Rebirth we walk back to auto-run area.
                    rebirthing_in_progress = True
                    print("Rebirth in progress")
                    print("Checking if auto-run zone has been succesfully entered.")
                    auto_run_entered_check(zone)
                    print("Rebirthed")

                    last_level_change = current_time
                    last_xp_claim = current_time

            last_image_analysis = current_time



        # XP check

        if current_time - last_xp_claim >= 3:

            print("Claiming XP")
            send_command("Claim_XP")
            print("Checking if auto-run zone has been succesfully entered.")
            auto_run_entered_check(zone)
            print("Claimed XP")

            last_xp_claim = current_time



# ==========================
# Cleanup
# ==========================

atexit.register(clear_command_and_close_ahk)