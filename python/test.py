import cv2
import pyautogui
import numpy as np
import os


# ============================================================
# REFERENCE RESOLUTION
# Coordinates below were originally measured at 1920x1080.
# Do NOT change this when changing your screen resolution.
# ============================================================

REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080


# ============================================================
# PORTAL LOCATIONS
# ============================================================

locations = {

    "Lost Valley": {
        "left": 1192 / REFERENCE_WIDTH,
        "top": 378 / REFERENCE_HEIGHT,
        "width": (1240 - 1192) / REFERENCE_WIDTH,
        "height": (420 - 378) / REFERENCE_HEIGHT
    },

    "Emerald Hill": {
        "left": 1098 / REFERENCE_WIDTH,
        "top": 691 / REFERENCE_HEIGHT,
        "width": (1142 - 1098) / REFERENCE_WIDTH,
        "height": (728 - 691) / REFERENCE_HEIGHT
    },

    "Hill Top": {
        "left": 678 / REFERENCE_WIDTH,
        "top": 385 / REFERENCE_HEIGHT,
        "width": (726 - 678) / REFERENCE_WIDTH,
        "height": (421 - 385) / REFERENCE_HEIGHT
    },

    "Speed Jungle": {
        "left": 934 / REFERENCE_WIDTH,
        "top": 176 / REFERENCE_HEIGHT,
        "width": (990 - 934) / REFERENCE_WIDTH,
        "height": (236 - 176) / REFERENCE_HEIGHT
    }
}


# ============================================================
# TEMPLATE LOCATION
# ============================================================

TEMPLATE_FOLDER = "../screenshots/portal_locked_screenshots"


# ============================================================
# COMPARISON FUNCTION
# ============================================================

def is_image_similar(screenshot, template):

    # Convert both images to grayscale
    screenshot_gray = cv2.cvtColor(
        screenshot,
        cv2.COLOR_BGR2GRAY
    )

    template_gray = cv2.cvtColor(
        template,
        cv2.COLOR_BGR2GRAY
    )

    # Resize screenshot to EXACTLY the template dimensions
    screenshot_gray = cv2.resize(
        screenshot_gray,
        (
            template_gray.shape[1],
            template_gray.shape[0]
        ),
        interpolation=cv2.INTER_CUBIC
    )

    # Template matching
    result = cv2.matchTemplate(
        screenshot_gray,
        template_gray,
        cv2.TM_CCOEFF_NORMED
    )

    _, confidence, _, _ = cv2.minMaxLoc(result)

    return confidence


# ============================================================
# DETECT CURRENT SCREEN RESOLUTION
# ============================================================

screen_width, screen_height = pyautogui.size()

print("=" * 60)
print(f"Detected screen resolution: {screen_width}x{screen_height}")
print("=" * 60)


# ============================================================
# TEST EACH PORTAL
# ============================================================

for name, region in locations.items():

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)

    # --------------------------------------------------------
    # Convert normalized 1920x1080 coordinates
    # to the CURRENT screen resolution.
    # --------------------------------------------------------

    left = int(
        region["left"] * screen_width
    )

    top = int(
        region["top"] * screen_height
    )

    width = int(
        region["width"] * screen_width
    )

    height = int(
        region["height"] * screen_height
    )

    print(
        f"Capture region: "
        f"x={left}, y={top}, "
        f"width={width}, height={height}"
    )


    # --------------------------------------------------------
    # TAKE SCREENSHOT
    # --------------------------------------------------------

    screenshot = pyautogui.screenshot(
        region=(
            left,
            top,
            width,
            height
        )
    )

    # Convert PIL Image → OpenCV image
    screenshot = cv2.cvtColor(
        np.array(screenshot),
        cv2.COLOR_RGB2BGR
    )


    # --------------------------------------------------------
    # LOAD TEMPLATE
    # --------------------------------------------------------

    template_filename = (
        name.lower().replace(" ", "_")
        + "_locked_portal.png"
    )

    template_path = os.path.join(
        TEMPLATE_FOLDER,
        template_filename
    )

    if not os.path.exists(template_path):

        print(
            f"ERROR: Template not found:\n"
            f"{template_path}"
        )

        continue


    template = cv2.imread(
        template_path
    )

    if template is None:

        print("ERROR: Could not load template.")

        continue


    # --------------------------------------------------------
    # PRINT ORIGINAL DIMENSIONS
    # --------------------------------------------------------

    print(
        f"Current screenshot: "
        f"{screenshot.shape[1]}x{screenshot.shape[0]}"
    )

    print(
        f"Template: "
        f"{template.shape[1]}x{template.shape[0]}"
    )


    # --------------------------------------------------------
    # SAVE RAW CURRENT SCREENSHOT
    # --------------------------------------------------------

    raw_filename = (
        name.lower().replace(" ", "_")
        + "_current.png"
    )

    cv2.imwrite(
        raw_filename,
        screenshot
    )

    print(
        f"Saved: {raw_filename}"
    )


    # --------------------------------------------------------
    # CREATE RESIZED VERSION
    # --------------------------------------------------------

    screenshot_resized = cv2.resize(
        screenshot,
        (
            template.shape[1],
            template.shape[0]
        ),
        interpolation=cv2.INTER_CUBIC
    )


    # Save resized version
    resized_filename = (
        name.lower().replace(" ", "_")
        + "_resized.png"
    )

    cv2.imwrite(
        resized_filename,
        screenshot_resized
    )

    print(
        f"Saved: {resized_filename}"
    )


    # --------------------------------------------------------
    # SAVE TEMPLATE COPY
    # --------------------------------------------------------

    template_copy_filename = (
        name.lower().replace(" ", "_")
        + "_template.png"
    )

    cv2.imwrite(
        template_copy_filename,
        template
    )


    # --------------------------------------------------------
    # COMPARE
    # --------------------------------------------------------

    confidence = is_image_similar(
        screenshot,
        template
    )

    print()
    print(
        f"Similarity: {confidence:.6f}"
    )


print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)