from operator import le
import re
from tkinter.tix import MAX
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract #ocr 글씨를 읽음

plt.style.use('dark_background')

img_path = '/Users/jjk/Desktop/git/TeamProject_AI_AUTO/src/frontend/data/num3.jpeg'
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

            #면적, 너비, 높이의비율
            area_diff = abs(d1['w']*d1['h'] - d2['w']*d2['h']) / (d1['w'] * d1['h'])
            width_diff = abs(d1['w'] -d2['w']) / d1['w']
            height_diff = abs(d1['h'] - d2['h']) / d1['h']
            
            #MAX_DIAG_MULTIPLAYER: 각 rectangle 마다의 길이
            #해당 조건에 성립하면 새로운 리스트에 ind 값 입력
            if distance < diagonal_length1 * MAX_DIAG_MULTIPLAYER \
                and angle_diff < MAX_ANGEL_DIFF and area_diff < MAX_AREA_DIFF \
                and width_diff < MAX_WIDTH_DIFF and height_diff < MAX_HEIGHT_DIFF:
                    matched_contours_idx.append(d2['idx'])

        #d1도 넣어줌
        matched_contours_idx.append(d1['idx'])

        #번호판이라고 인식된 컨투어의 갯수가 < MIN_N_MATCHED 제외
        if len(matched_contours_idx) < MIN_N_MATCHED:
            continue
        
        #최종 후보 리스트에 남은걸 넣음
        matched_result_idx.append(matched_contours_idx)
        
        unmatched_contour_idx = []  #최종 후보군에 들지 않은것들
        for d4 in contour_list:
            if d4['idx'] not in matched_contours_idx:
                unmatched_contour_idx.append(d4['idx'])
        
        #np.take :  possible_contours에서 unmatched_contour_idx와 같은 값의 idx만 추출
        unmatched_contour = np.take(possible_contours, unmatched_contour_idx)   
        
        #재귀
        recursive_contour_list = find_chars(unmatched_contour)

        for idx in recursive_contour_list:
            matched_result_idx.append(idx)  #최종 결과물
            
        break
    return matched_result_idx

result_idx = find_chars(possible_contours)

matched_result = []
for idx_list in result_idx:
    matched_result.append(np.take(possible_contours, idx_list))
    
#그리기
temp_result = np.zeros((height, width, channel), dtype=np.uint8)

for r in matched_result:
    for d in r:
        #이미지에 사각형 박스를 그림
        cv2.rectangle((temp_result), pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), color=(255,255,255), thickness=2)     



PLATE_WIDTH_PADDING = 1.3 # 1.3
PLATE_HEIGHT_PADDING = 1.5 # 1.5

MIN_PLATE_RATIO = 3
MAX_PLATE_RATIO = 10

plate_imgs = []
plate_infos = []
#기울어진 번호판을 정렬
#x 방향으로 순차적 정렬
for i, matched_chars in enumerate(matched_result):
    sorted_chars = sorted(matched_chars, key=lambda x: x['cx'])

    #센터 x, 센터 y 좌표
    plate_cx = (sorted_chars[0]['cx'] + sorted_chars[-1]['cx'])/2
    plate_cy = (sorted_chars[0]['cy'] + sorted_chars[-1]['cy'])/2
    
    plate_width = (sorted_chars[-1]['x']  + sorted_chars[-1]['w'] - sorted_chars[0]['x']) * PLATE_WIDTH_PADDING

    sum_height = 0
    for d in sorted_chars:
        sum_height += d['h']

    plate_height = int(sum_height/len(sorted_chars) * PLATE_HEIGHT_PADDING)
    
    #   삐뚤어진 정렬의 각도각도
    #높이 길이
    triangle_height = sorted_chars[-1]['cy'] - sorted_chars[0]['cy']
    #빗변의 길이: 첫번째와 마지막 번호판의 거리
    triangle_hypotenus = np.linalg.norm(
        np.array([sorted_chars[0]['cx'], sorted_chars[0]['cy']])-
        np.array([sorted_chars[-1]['cx'], sorted_chars[-1]['cy']])
    )
    
    #arcsin : 높이 / 빗변 => 라디안값을 도(세터)로 변경
    angle = np.degrees(np.arcsin(triangle_height/triangle_hypotenus))


    
    #삐뚤어진 이미지를 똑바로 돌려줌
    rotation_matrix = cv2.getRotationMatrix2D(center=(plate_cx, plate_cy), angle=angle, scale=1.0)
    img_rotated = cv2.warpAffine(img_thresh, M=rotation_matrix, dsize=(width, height))

    #cv2.getRectSubPix(): 회전된 이미지에서 원하는 부분만 자름
    #번호판 부분만 crop
    img_cropped = cv2.getRectSubPix(
        img_rotated,
        patchSize=(int(plate_width), int(plate_height)),
        center = (int(plate_cx), int(plate_cy))
    )
    if img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO or img_cropped.shape[1] / img_cropped.shape[0] < MIN_PLATE_RATIO > MAX_PLATE_RATIO:
        continue
    
    plate_imgs.append(img_cropped)
    plate_infos.append({
        'x': int(plate_cx - plate_width / 2),
        'y': int(plate_cy - plate_height / 2),
        'w': int(plate_width),
        'h': int(plate_height)
    })
    
    plt.subplot(len(matched_result), 1, i+1)
    plt.imshow(img_cropped, cmap='gray')
    
    
    
    longest_idx, longest_text = -1, 0
    plate_chars = []
    #한번 더 쓰레시홀딩
    for i, plate_img in enumerate(plate_imgs):
        plate_img = cv2.resize(plate_img, dsize=(0,0), fx = 1.6, fy=1.6)
        _, plate_img = cv2.threshold(plate_img, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)


    #컨투어를 한번 더 찾아 확실하게 만들어줌
    contours, _ = cv2.findContours(plate_img, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    
    plate_min_x, plate_min_y = plate_img.shape[1], plate_img.shape[0]
    plate_max_x, plate_max_y = 0, 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)


        area = w * h
        ratio = w/h
        
        if area >MIN_AREA \
            and w > MIN_WIDTH and h > MIN_HEIGHT \
            and MIN_RATIO < ratio < MAX_RATIO:
                if x < plate_min_x:
                    plate_min_x = x
                if y < plate_min_y:
                    plate_min_y = y
                if x+w > plate_max_x:
                    plate_max_x = x+w
                if y+h > plate_max_y:
                    plate_max_y = y+h
                    
    #번호판 부분만 이미지를 crop                
    img_result = plate_img[plate_min_y:plate_max_y, plate_min_x:plate_max_x]

    #글씨를 읽기전 전처리
    #GaussianBlur로 노이즈를 없앰
    img_result = cv2.GaussianBlur(img_result, ksize=(3,3), sigmaX=0)        
        
    _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU )

    #약간의 여백 padding 추가 (0,0,0)-> 검정색여백
    img_result = cv2.copyMakeBorder(img_result, top=10,bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT, value=(0,0,0))

    #pytesseract.image_to_string: 이미지에서 글자를 읽어옴
    #--psm 7: 이미지 안 글자 한줄,  --oem 0 : 가장 오래된 엔진 선택(문맥 X)
    chars = pytesseract.image_to_string(img_result, lang='kor', config='--psm 7 --oem 0')

    result_chars = ''
    has_digit = False
    
    # 잘못된 특수문자들을 모두 삭제
    for c in chars:
        if ord('가') <= ord(c) <= ord('힣') or c.isdigit(): #숫자나 한글이 포함됨
            if c.isdigit(): #숫자가 하나라도 있는지 확인
                has_digit=True
        result_chars += c
    
    print(result_chars)
    
    plate_chars.append(result_chars)
    
    #가장 긴 번호판이 찾는 번호판임을 설정
    if has_digit and len(result_chars) > longest_text:
        longest_idx = i
    
#최종 결과
info = plate_infos[longest_idx]
chars = plate_chars[longest_idx]

print(chars)

img_out = img_ori.copy()

cv2.rectangle(img_out, pt1=(info['x'], info['y']), pt2=(info['x']+info['w'], info['y']+info['h']), color=(255,0,0), thickness=2)


cv2.imwrite(chars + '.jpg', img_out)

plt.figure(figsize=(12, 10))
plt.imshow(img_out, cmap='gray')
plt.show()