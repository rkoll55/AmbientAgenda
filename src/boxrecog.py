import cv2
import numpy as np

# Read the input image
image = cv2.imread('images/blackbox.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection using Canny
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

squares = []
colors = [(0,255,0),(255,0,0),(0,0,255)]
# Loop through the contours and identify squares
i = 0
for contour in contours:
    # Approximate the contour to a polygon
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # Check if the polygon has 4 corners (a square)
    if len(approx) == 4:
        
        # Calculate the aspect ratio to distinguish squares from rectangles
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        
        # Draw bounding box around the square
        cv2.drawContours(image, [approx], 0, colors[i], 10)
        print(f"Found a  box with\nx: {x}\ny: {y}\nw: {w}\nh: {h}\n")
        i += 1
        #cropped_image = image[y:y+h, x:x+w]
# Display the image with detected squares
cv2.imshow('Detected Squares', image)
cv2.waitKey(0)
cv2.destroyAllWindows()