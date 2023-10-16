import cv2          # install with pip install opencv-python
import pytesseract  # install with pip install pytesseract // https://pypi.org/project/pytesseract/
from PIL import Image
import numpy as np
import torch

import sys
sys.path.append('../ESRGAN2')
from ESRGAN2 import RRDBNet_arch as arch

import platform
import json
# -------------------- BASIC COMPUTER VISION SCRIPT --------------------------------- 

username = "user1"

# could feed the individual boxes into here?

#This is necessary on win10+ installations as tesseract needs to locate the executable
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 


def main():

    # init recog
    #recognize_text(upscale('images/bigwords.png'))
    #recognize_text(cv2.imread('images/bigwords.png'))
    
    days = box_recog('images/poll.jpg', debug=True, real = True) # recognise the day boxes 
    for day in days.keys():
        print(f"{day}: {days[day]}")
    write_to_temp(days, username, infile="json/template.json", outfile="json/time_test.json")
    return

def write_to_temp(days, username, infile="json/template.json", outfile="json/output.json"): 

    # load template    
    with open(infile, "r") as json_template:
        json_template = json.load(json_template)
    
    for day in json_template.keys():
        if days[day] != "":
            for time in json_template[day].keys():
                if days[day][time] != "":
                    if username in json_template[day][time].keys():
                        # recognize what text is ours and what isnt -- MAYBE WE CAN FILTER COLOUR IN THE RECOG???
                        json_template[day][time][username] += days[day][time]
                    else:
                        json_template[day][time][username] = days[day][time]
        

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




def box_recog(path, debug=False, real=False):
    # Read the input image
    
    image = cv2.imread(path)
    # Convert the image to grayscale

    

    def box_seeker(image, whole = False):
    
        boxes = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply edge detection using Canny
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
            if len(approx) == 4:    
                # Calculate the aspect ratio to distinguish squares from rectangles
                hull = cv2.convexHull(approx, returnPoints=False)
                hull_draw = cv2.convexHull(approx)
                hull_points = [approx[x] for x in hull]
                hull_points = [points[0] for points in hull_points]
                hull_points = [points[0] for points in hull_points]
                x, y, w, h = cv2.boundingRect(np.array(hull_points))
                # Draw bounding box around the square

                #find relevant distances to take out the 
                def dist(hull_points):
                    return True 
                if w > 50 and h > 50 and len(hull_points) > 3 and dist(hull_points):
                    cropped_image = image[y+10:y+h-10, x+10:x+w-10]
                    if debug:
                        #Image.fromarray(cropped_image).show()
                        print(f"Found a convex box with\nx: {x}\ny: {y}\nw: {w}\nh: {h}\n")
                        #cv2.imshow(str(i), cropped_image)
                        if whole:
                            cv2.drawContours(image, [hull_draw], 0, colors[i%3], 5)
                    i += 1
                    boxes.append((cropped_image, (x, y, w, h)))
        # Display the image with detected squares
        #print(f"BOXLEN {len(boxes)}")
        return boxes
    boxes = box_seeker(image)
    # Sorting our boxes 

    def sort_largest(box):
        return -(box[1][2] + box[1][3])
    
    if real:
        boxes = sorted(boxes, key=sort_largest)
        image = boxes[0][0]
        boxes = box_seeker(image, whole=True)
    

    def sort_boxes(box):
        if box[1][2] > box[1][3]: # Sat or Sun
            return 10000 + box[1][0] # skew sort by pushing them back
        else: 
           return box[1][0]

    boxes = sorted(boxes, key=sort_boxes)
    boxes = boxes[:7]
    days = {'Monday': '', 'Tuesday': '', 'Wednesday': '', 'Thursday': '', 'Friday':'', 'Saturday':'', 'Sunday':''}
    text = [recognize_text(img[0]) for img in boxes]
     
    if debug:
        Image.fromarray(image).show()
        #cv2.imshow('Detected Squares', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    
    for i in range(len(text)):
        days[list(days.keys())[i]] = text[i]
    
    for day in days.keys():
        times = {"00": '',"01": '',"02": '',
        "03": '', 
        "04": '', 
        "05": '', 
        "06": '', 
        "07": '', 
        "08": '', 
        "09": '', 
        "10": '', 
        "11": '', 
        "12": '', 
        "13": '', 
        "14": '', 
        "15": '', 
        "16": '', 
        "17": '', 
        "18": '', 
        "19": '', 
        "20": '', 
        "21": '', 
        "22": '', 
        "23": '', 
        "24": '', 
        }
        temp = [x for x in days[day].split('\n') if x != ''] 
        # go backwards to link up newline sep'd events
        buff = ''
        # first pass: join continuated events 
        for line in reversed(temp):
            #check buffer - anything from the line below that isn't a separate time
            if buff != '':
                temp[temp.index(line)] += ' ' + buff
                buff = ''
            if not line[0].isnumeric():
                buff += line
                temp.pop(temp.index(line))        

        #second pass: check for time
        for line in temp:
            print(day, temp)
            splat = line.split(' ')
            if len(splat) == 1:
                continue
            if line.split(' ')[0].isnumeric() and line.split(' ')[1] in ('AM','PM', 'am','pm','Am','aM','pM','Pm'):
               #incorrectly formatted 
                splat[0] = splat[0] + splat[1].upper()
                splat.pop(1)
                temp[temp.index(line)] = ' '.join(splat)
            elif len(splat[0]) in [3, 4]:
                time, period = splat[0][:-2], splat[0][-2:]
                splat[0] = time + period.upper()
                temp[temp.index(line)] = ' '.join(splat)
        # Begin sorting
        for line in temp:
            # Split the string into the numerical part and the AM/PM part
            time, period = line.split(' ')[0][:-2], line.split(' ')[0][-2:]
            # Convert to 24-hour format
            if period == 'PM' and time != '12':
                time = str(int(time) + 12)
            elif period == 'AM' and time == '12':
                time = '00'
            elif period == 'AM' and int(time) < 10:
                time = '0' + time
            if time not in times.keys():
                continue
            times[time] += line + '\n'
        days[day] = times
        print(day)

        #last pass: create dict key in 24hr time
        print(temp)
    

    return days

if __name__ == "__main__":
    main()
