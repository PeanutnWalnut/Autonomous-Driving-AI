import cv2
import numpy as np
from dynamikontrol import Module

CONFIDENCE = 0.9
THRESHOLD = 0.3
LABELS = ['Car', 'Plate']
CAR_WIDTH_TRESHOLD = 500
img_path = '/Users/jjk/Desktop/git/TeamProject/src/frontend/data/num3.jpeg'
cap = cv2.VideoCapture(img_path)

net = cv2.dnn.readNetFromDarknet('/Users/jjk/Desktop/git/TeamProject/src/frontend/src/AI/License plate recognition _parking lot/cfg/yolov4-ANPR.cfg', '/Users/jjk/Desktop/git/TeamProject/src/frontend/src/AI/License plate recognition _parking lot/yolov4-ANPR.weights')

#module = Module()

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    H, W, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255., size=(416, 416), swapRB=True)
    net.setInput(blob)
    output = net.forward()

    boxes, confidences, class_ids = [], [], []

    for det in output:
        box = det[:4]
        scores = det[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > CONFIDENCE:
            cx, cy, w, h = box * np.array([W, H, W, H])
            x = cx - (w / 2)
            y = cy - (h / 2)

            boxes.append([int(x), int(y), int(w), int(h)])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE, THRESHOLD)  # 신뢰도 측정 DNN

    if len(idxs) > 0:
        for i in idxs.flatten():
            x, y, w, h = boxes[i]

            cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
            cv2.putText(img, text='%s %.2f %d' % (LABELS[class_ids[i]], confidences[i], w), org=(x, y - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 255), thickness=2)

            if class_ids[i] == 0:
                if w > CAR_WIDTH_TRESHOLD:
                    #module.motor.angle(80)
                    print('차단기 열림')
                else:
                    #module.motor.angle(0)
                    print('차단기 닫침')
    else:
        #module.motor.angle(0)
        print('차단기 닫침')
        
    cv2.imshow('result', img)
    if cv2.waitKey(1) == ord('q'):
        break
