
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

    template = cv2.imread("../screenshots/portal_button.png")

    with mss.MSS() as sct:

        screen = {
            "left": 0,
            "top": int(constants.POSSIBLE_PORTAL_LOCATION_HEIGHT_RATIO * screen_height),
            "width": screen_width,
            "height": screen_height - int(constants.POSSIBLE_PORTAL_LOCATION_HEIGHT_RATIO * screen_height)
        }

        screenshot = sct.grab(screen) # This returns a screenshot.Screenshot objects containing varios data about the iamge.

        screenshot_pixels = np.array(screenshot) # The way np can conver the screnshot to an array of pixel values it because the screenshot object provides a way to be converted into an array. {__array__ or maybe __buffer__}

        # Remove the alpha channel because mss returns BGRA and also we dont want transparency to affect out search. If we move in game that could affect the pixels with alpha in them.
        screenshot_pixels = cv2.cvtColor(
            screenshot_pixels,
            cv2.COLOR_BGRA2BGR
        )

        result = cv2.matchTemplate( # This returns a grid/matrix of all points that it checked and its similarity value. Out chosen comparison method {TM_CCOEFF_NORMED} returns 1.0 if its a perfect match and 0.0 if its not.
            screenshot_pixels,
            template,
            cv2.TM_CCOEFF_NORMED
        )


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
            save_portal_coordinates(real_x / 1920, real_y / 1080)
            print("Saved button coordinates inside ini file.")

        else:
            print("Travel button not found. Do you have Fast Travel activated in the game settings?")




# ==========================
# Image Comparison
# ==========================

def image_similarity(image1, image2, threshold=2):

    difference = ImageChops.difference(image1, image2)

    difference_np_array = np.array(difference)

    average_pixel_difference = difference_np_array.mean()

    print(average_pixel_difference, image1, image2)

    return average_pixel_difference < threshold


# ==========================
# Screenshot Analysis
# ==========================

def portal_page_check(zone):


    next_counter = 0 # Amount of "Next" buttons we need to press to get to out desired page
    folders = [
        Path("../screenshots/portal_screenshots"),
        Path("../screenshots/portal_locked_screenshots")
    ]

    zone_string = zone.lower().replace(" ", "_") # Make text lower and replace white space with _. So "Green Hill" becomes "green_hill"

    # This code is to check what page we are currently on. So we just cehck the first location of every page. {The top portal}
    for folder in folders:
        for file in folder.iterdir(): # Creates iterable containing all files in that folder

            portal_name = file.name.replace("_portal.png", "").upper() # Removed "_portal" from filename and makes it capitalized so I can access the constants.
            command_name = portal_name.replace("_", " ").title() # This basically converts "green_hill" into "Green Hill"
            zone_portal_coordinates = constants.PORTAL_COORDINATES[portal_name]

            with mss.MSS() as sct:

                screen = {
                    "left": int(zone_portal_coordinates["left"] * screen_width),
                    "top": int(zone_portal_coordinates["top"] * screen_height),
                    "width": int(zone_portal_coordinates["width"] * screen_width),
                    "height": int(zone_portal_coordinates["height"] * screen_height)
                }

                screenshot = sct.grab(screen)

                image = Image.frombytes(
                    "RGB",
                    screenshot.size,
                    screenshot.rgb
                )

                page_distance = constants.ZONES_PAGE_NUMBER[zone] - constants.ZONES_PAGE_NUMBER[command_name] 


                if image_similarity(portal_image, image):

                    if "locked" not in file.name:
                        return page_distance

                    if zone == command_name:
                        print(f"{command_name} is currently locked.")
                        return None

                    return page_distance
                    
   
    




def portal_is_locked(zone):


    file_name = f"{zone.replace(' ', '_').lower()}_locked_portal.png"
    with mss.MSS() as sct:

        screen = {
            "left": int(constants.ZONE_BUTTON_COORDINATES[zone]["left"] * screen_height),
            "top": int(constants.ZONE_BUTTON_COORDINATES[zone]["top"] * screen_height),
            "width": int(constants.ZONE_BUTTON_COORDINATES[zone]["width"] * screen_height),
            "height": int(constants.ZONE_BUTTON_COORDINATES[zone]["height"] * screen_height)
        } 

        screenshot = sct.grab(screen)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        portal_screenshot = Image.open(f"../screenshots/portal_locked_screenshots/{file_name}")
        if image_similarity(image, portal_screenshot):
            print(f"{zone} is currently locked. Please choose another zone.")
            return True
        

        return False












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

        if image_similarity(image, level_screenshot):
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

        if not image_similarity(image, x_screenshot):
            print(f"Auto-run zone has not succesfully been entered. Sending the command {zone} again.")
            send_command(zone)

# ==========================
# AutoHotkey Communication
# ==========================

def send_command(command):
    global rebirthing_in_progress
    page_distance = None


    if command in constants.ZONES:
        send_command("Click_Portal") 
        # This will send a command to click the portal button. The code will be stuck on this until it recieved a done.txt.
        # I will then detect what page we are on and change to the right one if the player is not on it. And then I will check if the player has that place unlocked.

        distance = portal_page_check(command)

        if distance is None:
            send_command("Close_Portal")
            return 
        page_distance = distance

    

    with open("../command.txt", "w") as f:
        print(f"Sending command: {command}")
        f.write(f"{command}")
        
        if page_distance is not None and page_distance != 0: # We check if its non None so in case page_distance is 0 
            f.write(f"\n{page_distance}")



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