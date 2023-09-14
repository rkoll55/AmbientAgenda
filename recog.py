import cv2          # install with pip install opencv-python
import pytesseract  # install with pip install pytesseract // https://pypi.org/project/pytesseract/
from PIL import Image
import numpy as np
import torch
import ESRGAN2.RRDBNet_arch as arch
import platform
import json
# -------------------- BASIC COMPUTER VISION SCRIPT --------------------------------- 

username = "ser bron"
# could feed the individual boxes into here?

#This is necessary on win10+ installations as tesseract needs to locate the executable
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 


def main():

    # init recog
    #recognize_text(upscale('images/bigwords.png'))
    #recognize_text(cv2.imread('images/bigwords.png'))
    
    days = box_recog('images/marked_template.png') # recognise the day boxes 
    for day in days.keys():
        print(f"{day}: {days[day]}")
    write_to_temp(days)
    return

def write_to_temp(days, infile="template.json", outfile="output.json"): 

    # load template    
    with open(infile, "r") as json_template:
        json_template = json.load(json_template)
    
    for day in json_template.keys():
        if days[day] != "":
            if username in json_template[day].keys():
                # recognize what text is ours and what isnt -- MAYBE WE CAN FILTER COLOUR IN THE RECOG???
                
                json_template[day][username] += days[day]
            else:
                json_template[day][username] = days[day]
        

    with open(outfile, 'w') as outfile:
        outfile.write(json.dumps(json_template, indent=4))
    return json.dumps(json_template, indent=4)

def upscale(path):
    #model setup
    model_path = 'ESRGAN/models/RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
    device = torch.device('cpu') # pi has no cuda sadge
    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device) # model bound to CPU since pi has no CUDA cores 

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)

    with torch.no_grad():

        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round() 
    
    cv2.imshow('output', output)
    cv2.waitKey(0)
 
    cv2.imwrite('images/{:s}'.format((((path.split('/'))[-1].split('.'))[0]) + "_up." + ((path.split('/'))[-1].split('.'))[1]), output)
    return 'images/{:s}'.format((((path.split('/'))[-1].split('.'))[0]) + "_up." + ((path.split('/'))[-1].split('.'))[1])

# ----

def recognize_text(image, debug=False):
    # Grayscale, Gaussian blur, Otsu's threshold - fun little preprocessing techniques ( ͡° ͜ʖ ͡°)
    if (type(image) == str):
        image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (3,3), 0) this completely fucks it on small images
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # noise removal and inversion
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1) # Too harsh on small text
    invert = 255 - opening

    # extract text
    data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    
    if debug:
        print(pytesseract.image_to_data(thresh))
        cv2.imshow('thresh', thresh) # so we can see what tesseract sees
        cv2.imshow('opening', opening)
        cv2.imshow('invert', invert)

    return data




def box_recog(path, debug=False):
    # Read the input image
    
    image = cv2.imread(path)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection using Canny
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    colors = [(0,255,0),(255,0,0),(0,0,255)]
    # Loop through the contours and identify squares
    i = 0
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Check if the polygon has 4 corners (a square) - not done 
        # if len(approx) == 10:
            
        #     # Calculate the aspect ratio to distinguish squares from rectangles
        #     x, y, w, h = cv2.boundingRect(approx)
        #     aspect_ratio = float(w) / h
        #     if (0.5 <= aspect_ratio <= 1 or 1.5 <= aspect_ratio) <= 4 and w > 50 and h > 100:
        #         # Draw bounding box around the square
        #         cv2.drawContours(image, [approx], 0, colors[i%3], 10)
        #         print(f"Found a  box with\nx: {x}\ny: {y}\nw: {w}\nh: {h}\n")
        #         i += 1
        #         #cropped_image = image[y:y+h, x:x+w]

        # CONVEX HULL FOR HIGHER DIMENSIONAL SHAPES    
        if 3 < len(approx):    
            # Calculate the aspect ratio to distinguish squares from rectangles
            hull = cv2.convexHull(approx, returnPoints=False)
            hull_draw = cv2.convexHull(approx)
            hull_points = [approx[x] for x in hull]
            hull_points = [points[0] for points in hull_points]
            hull_points = [points[0] for points in hull_points]
            x, y, w, h = cv2.boundingRect(np.array(hull_points))
            # Draw bounding box around the square
            if w > 50 and h > 50:
                print(f"Found a convex box with\nx: {x}\ny: {y}\nw: {w}\nh: {h}\n")
                cropped_image = image[y+10:y+h-10, x+10:x+w-10]
                #cv2.imshow(str(i), cropped_image)
                cv2.drawContours(image, [hull_draw], 0, colors[i%3], 5)
                i += 1
                boxes.append((cropped_image, (x, y, w, h)))
    # Display the image with detected squares
    print(f"BOXLEN {len(boxes)}")

    # Sorting our boxes 
    
    def sort_boxes(box):
        if box[1][2] > box[1][3]: # Sat or Sun
            return 10000 + box[1][0] # skew sort by pushing them back
        else: 
            return box[1][0]

    boxes = sorted(boxes, key=sort_boxes)
    
    days = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '', 'Friday':'', 'Saturday':'', 'Sunday':''}
    text = [recognize_text(img[0]) for img in boxes] 
    for i in range(len(text)):
        days[list(days.keys())[i]] = text[i]
    

    if debug:
        cv2.imshow('Detected Squares', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return days

if __name__ == "__main__":
    main()