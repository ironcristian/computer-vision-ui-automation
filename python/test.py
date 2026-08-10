import cv2

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