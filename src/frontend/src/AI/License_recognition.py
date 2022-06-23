from tkinter.tix import MAX
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract #ocr 글씨를 읽음

plt.style.use('dark_background')

img_path = '/Users/jjk/Desktop/git/TeamProject_AI_AUTO/src/frontend/data/num2.jpeg'
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


MIN_AREA = 80 #번호판 숫자의 최소, 최대 넓이
MIN_WIDTH, MIN_HEIGHT = 2, 8
MIN_RATIO, MAX_RATIO = 0.25, 1.0 #가로대비 세로 비율

possible_contours = []  #번호판만 넣어줌

cnt = 0
for d in contours_dict:
    area = d['w'] * d['h'] #넓이
    ratio = d['w'] / d['h'] #가로대비 세로 비율

    if area > MIN_AREA \
    and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
    and  MIN_RATIO <ratio < MAX_RATIO:
        d['idx'] = cnt #갯수
        cnt += 1
        possible_contours.append(d) #번호판의 확률이 높은애만 따로 저장
        
#conturs 그림
temp_result = np.zeros((height, width, channel), dtype=np.uint8)      

for d in possible_contours:
    cv2.rectangle(temp_result, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255,255,255), thickness=2)

#번호판 배열의 모양들을 보고 정렬확인
MAX_DIAG_MULTIPLAYER = 5 # 각 rectangle 마다의 길이 가 5배 
MAX_ANGEL_DIFF =12.0    # 각 컨투어의 세타의 최댓값 너무 벌어지면 안됨
MAX_AREA_DIFF=0.5 #각 컨투어의 면적차이
MAX_WIDTH_DIFF=0.8  #각 컨투어의 너비 차이
MAX_HEIGHT_DIFF=0.2 #각 컨투어의 높이차이
MIN_N_MATCHED=3 #위의 조건들을 모두 만족하는 애들이 최대 3개 (번호판은 최소 3개 이상)

def find_chars(contour_list):
    matched_result_idx = [] #최종적으로 남는 값들의 Idx
    
    #d1의 컨투어 상자와 d2으 컨투어 상자를 비교
    for d1 in contour_list:
        matched_contours_idx = []
        for d2 in contour_list:
            if d1['idx'] == d2['idx']:  #같은 컨투어
                continue
                
            #센터 점끼리의 가로, 세로
            dx = abs(d1['cx'] - d2['cx'])
            dy = abs(d1['cy'] - d2['cy'])

            diagonal_length1 = np.sqrt(d1['w'] **2 + d1['h'] **2)
            #dx, dy 삼각형의 대각선 길이, 두 컨투어의 거리 구함
            distance = np.linalg.norm(np.array([d1['cx'], d1['cy']]) - np.array([d2['cx'], d2['cy']]))  #np.linalg.norm(a-b): 벡터 a와 벡터 b 사이의 거리
            
            #두 컨투어의 각도 차이, 세타 = arctan(dy/dx)
            if dx == 0: #가로차이 = 0이면 위나 아래에 위치해 번호판일 확률이 적음, dx 분모가 0
                angle_diff = 90
            else:
                angle_diff = np.degrees(np.arctan(dy/dx)) #np.degree: 라디안 값 -> 몇도 인지(세타값)

            area_diff 
            #11:21




plt.figure(figsize=(12, 10))
plt.imshow(temp_result, cmap='gray')
plt.show()