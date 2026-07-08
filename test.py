from PIL import Image, ImageOps
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open saved screenshot
image = Image.open("level_test.png")

# Convert to grayscale
image = ImageOps.grayscale(image)

# Enlarge image
image = image.resize(
    (800, 400)
)

# Convert to black and white
image = image.point(lambda p: 255 if p > 150 else 0)

# Save processed image for inspection
image.save("processed_level.png")

# OCR
text = pytesseract.image_to_string(
    image,
    config="--psm 7 -c tessedit_char_whitelist=0123456789"
)

print(repr(text))