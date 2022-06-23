import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract #ocr 글씨를 읽음

plt.style.use('dark_background')

img_path = '/Users/jjk/Desktop/git/TeamProject_AI_AUTO/src/frontend/data/num1.jpeg'
img_ori = cv2.imread(img_path)

height, width, channel = img_ori.shape

#이미지 컬러 체계를 변경한다 = grayScale
gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
#hsv -> v채널만 사용도 가능

#Adaptive Thresholding : 
img_blurred = cv2.GaussianBlur(gray, ksize=(5,5), sigmaX=0) #노이즈를 줄이기 위해 GaussianBlur 활용
#이미지를 구분하기 쉽게 값을 정함
img_thresh = cv2.adaptiveThreshold(
    img_blurred,
    maxValue=255.0,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=19,
    C=9
)

#컨투어 윤곽선을 찾음
contours, _ = cv2.findContours(
    img_thresh,
    mode=cv2.RETR_LIST,
    method=cv2.CHAIN_APPROX_SIMPLE
)

temp_result = np.zeros((height, width, channel), dtype=np.uint8)

#-1로 컨투어를 전체그럼
cv2.drawContours(temp_result, contours=contours, contourIdx=-1, color=(255, 255, 255))

temp_result = np.zeros((height, width, channel), dtype=np.uint8)
                       
contours_dict = []  #컨투어의 정보들을 모두 저장
#컨투어의 사각형 범위를 찾아냄, 컨투어를 감싸는 사각형
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(temp_result, pt1=(x,y), pt2=(x+w, y+h), color=(255,255,255), thickness=2)  #이지미에 사각형을 그림

    #dict에 넣어줌
    contours_dict.append({
        'contour:': contour,
        'x':x,
        'y':y,
        'w':w,
        'h':h,
        'cx': x+(w/2),  #중심좌표
        'cy': y+(h/2)   #중심좌표
    })







plt.figure(figsize=(12, 10))
plt.imshow(temp_result, cmap='gray')
plt.show()