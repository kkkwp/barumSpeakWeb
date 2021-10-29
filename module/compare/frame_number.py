import cv2 as cv
import dlib
import numpy as np

def f_num(original):
    # 얼굴 검출을 위해 디폴트 얼굴 검출기 사용
    detector = dlib.get_frontal_face_detector()
    # 검출된 얼굴에서 눈, 코, 입같은 랜드마크를 찾기 위해 사용할 학습모델을 로드합니다.
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # 웹캠으로부터 영상을 가져와 입력으로 사용합니다.
    cap = cv.VideoCapture(original)

    final_ori_point = []

    f_num = cap.get(cv.CAP_PROP_FRAME_COUNT)

    return f_num
