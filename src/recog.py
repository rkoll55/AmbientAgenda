import cv2          # install with pip install python-opencv
import pytesseract  # install with pip install pytesseract // https://pypi.org/project/pytesseract/


# -------------------- BASIC COMPUTER VISION SCRIPT --------------------------------- 

# could feed the individual boxes into here?

#This is necessary on win10+ installations as tesseract needs to locate the executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('images/recog.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# noise removal and inversion
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# extract text
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
print(data)

#cv2.imshow('thresh', thresh) -- so we can see what tesseract sees
#cv2.imshow('opening', opening)
#cv2.imshow('invert', invert)