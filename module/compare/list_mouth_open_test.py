import cv2 as cv
import dlib
import numpy as np

original = 'comp1_1.mpg'

# 얼굴 검출을 위해 디폴트 얼굴 검출기 사용
detector = dlib.get_frontal_face_detector()
# 검출된 얼굴에서 눈, 코, 입같은 랜드마크를 찾기 위해 사용할 학습모델을 로드합니다.
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# 웹캠으로부터 영상을 가져와 입력으로 사용합니다.
cap = cv.VideoCapture(original)

open_lip_frame = []

i = 0
# 웹캠으로부터 입력을 받으려면 무한 반복을 해줘야함

while i < 75:
    ret, img_frame = cap.read()

    # 웹캠으로부터 이미지를 가져와서 그레이스케일로 변환한다.
    img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)

    # 주어진 이미지에서 얼굴을 검출. 두번째 아규먼트는 업샘플링 횟수.
    dets = detector(img_gray, 1)

    for face in dets:
        # 주어진 이미지 img_frame의 검출된 얼굴 영역 face에서 랜드마크를 검출.
        shape = predictor(img_frame, face)  # 얼굴에서 68개 점 찾기

        list_points = []

        for p in shape.parts():
            list_points.append([p.x, p.y])

        list_points = np.array(list_points)

        mid = list_points[66][1] - list_points[62][1]

        if mid > 2:
            frame_num = cap.get(cv.CAP_PROP_POS_FRAMES)
            open_lip_frame.append(frame_num)

    i += 1

cap.release()

print(open_lip_frame[0])