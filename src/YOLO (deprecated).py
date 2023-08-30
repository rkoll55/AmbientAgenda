import cv2
import numpy as np

# Load YOLO model
net = cv2.dnn.readNetFromDarknet("C:/Users/a458622/OneDrive - Volvo Group/IBM/Byte-Me/src/yolo/yolov3.cfg","C:/Users/a458622/OneDrive - Volvo Group/IBM/Byte-Me/src/yolo/yolov3.weights")

# Load COCO class labels (for reference)
classes = []
with open("C:/Users/a458622/OneDrive - Volvo Group/IBM/Byte-Me/src/coco.names", "r") as f:
    classes = f.read().strip().split("\n")

# Load image
image = cv2.imread("images/dog.jpg")

# Get image dimensions
height, width, _ = image.shape

# Preprocess the image for YOLO
blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

# Set the input to the model
net.setInput(blob)

# Get output layer names
output_layer_names = net.getUnconnectedOutLayersNames()

# Forward pass and get predictions
outs = net.forward(output_layer_names)

# Process the detections
boxes = []
confidences = []
class_ids = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.5:  # Adjust this threshold as needed
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Perform Non-maximum Suppression to get the final boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Draw the boxes on the image
for i in indices:
    box = boxes[i]
    x, y, w, h = box
    label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

# Display or save the output image
cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()