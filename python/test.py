import cv2
import mss
import numpy as np
import pyautogui
import constants


screen_width, screen_height = pyautogui.size()


def test_portal_detection():

    template = cv2.imread(
        "../Auto_Rebirther_Screenshots/Portal_Button_Screenshot_Permanent/portal_button.png"
    )

    if template is None:
        print("Template image not found")
        return


    with mss.MSS() as sct:

        # Same search area you will use in the real script
        screen = {
            "left": 0,
            "top": int(constants.POSSIBLE_PORTAL_LOCATION_HEIGHT_RATIO * screen_height),
            "width": screen_width,
            "height": screen_height - int(constants.POSSIBLE_PORTAL_LOCATION_HEIGHT_RATIO * screen_height)
        }


        screenshot = sct.grab(screen)

        screenshot_pixels = np.array(screenshot)

        screenshot_pixels = cv2.cvtColor(
            screenshot_pixels,
            cv2.COLOR_BGRA2BGR
        )


        result = cv2.matchTemplate(
            screenshot_pixels,
            template,
            cv2.TM_CCOEFF_NORMED
        )


        _, confidence, _, location = cv2.minMaxLoc(result)


        print("Confidence:", confidence)
        print("Location inside cropped image:", location)


        if confidence > 0.90:

            real_x = location[0] + screen["left"]
            real_y = location[1] + screen["top"]

            print("REAL SCREEN POSITION:")
            print(real_x, real_y)


            # Show the found location
            debug = cv2.cvtColor(
                screenshot_pixels,
                cv2.COLOR_BGR2RGB
            )

            cv2.rectangle(
                debug,
                location,
                (
                    location[0] + template.shape[1],
                    location[1] + template.shape[0]
                ),
                (255,0,0),
                2
            )

            cv2.imshow(
                "Detected Portal",
                debug
            )

            cv2.waitKey(0)

        else:
            print("Portal not found")


test_portal_detection()