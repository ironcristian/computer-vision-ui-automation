import cv2
<<<<<<< Updated upstream

image1 = cv2.imread("cool_edge_portalsssssss.png")
image2 = cv2.imread("cool_edge_portals1.png")

if image1 is None or image2 is None:
    raise FileNotFoundError("Could not find one or both images.")

print("Image 1:", image1.shape)
print("Image 2:", image2.shape)

result = cv2.matchTemplate(
    image2,
    image1,
    cv2.TM_CCORR_NORMED
)

_, similarity, _, location = cv2.minMaxLoc(result)

print(f"Similarity: {similarity:.6f}")
print(f"Best location: {location}")

# Save visual difference
diff = cv2.absdiff(image1, image2)
cv2.imwrite("cool_edge_difference.png", diff)

print("Saved cool_edge_difference.png")
=======
import mss
import numpy as np
from PIL import Image

with mss.MSS() as sct:

    # Original 1920x1080 coordinates
    screen = {
        "left": 675,
        "top": 363,
        "width": 732 - 675,   # 57
        "height": 423 - 363   # 60
    }

    screenshot = sct.grab(screen)

    image = Image.frombytes(
        "RGB",
        screenshot.size,
        screenshot.rgb
    )

    image.save("metro_city_1920.png")
    print("Saved metro_city_1920.png")

# Load both images
template = cv2.imread("../screenshots/portal_screenshots/metro_city_portal.png")
current = cv2.imread("metro_city_1920.png")

# Compare
result = cv2.matchTemplate(
    current,
    template,
    cv2.TM_CCORR_NORMED
)

_, confidence, _, location = cv2.minMaxLoc(result)

print(f"Similarity: {confidence:.6f}")
print(f"Best location: {location}")

# Save difference image
diff = cv2.absdiff(template, current)
cv2.imwrite("difference_1920.png", diff)

print("Saved difference_1920.png")
>>>>>>> Stashed changes
