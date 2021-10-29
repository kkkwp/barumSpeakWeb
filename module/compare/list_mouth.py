import cv2 as cv
import dlib
import numpy as np

def list_video(original):
    # 얼굴 검출을 위해 디폴트 얼굴 검출기 사용
    detector = dlib.get_frontal_face_detector()
    # 검출된 얼굴에서 눈, 코, 입같은 랜드마크를 찾기 위해 사용할 학습모델을 로드합니다.
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # 웹캠으로부터 영상을 가져와 입력으로 사용합니다.
    cap = cv.VideoCapture(original)

    final_ori_point = []

    f_num = cap.get(cv.CAP_PROP_FRAME_COUNT)

    i = 0
    # 웹캠으로부터 입력을 받으려면 무한 반복을 해줘야함
    while i < f_num:

        ret, img_frame = cap.read()

        # 웹캠으로부터 이미지를 가져와서 그레이스케일로 변환한다.
        img_gray = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY)

        # 주어진 이미지에서 얼굴을 검출. 두번째 아규먼트는 업샘플링 횟수.
        dets = detector(img_gray, 1)

        for face in dets:
            # 주어진 이미지 img_frame의 검출된 얼굴 영역 face에서 랜드마크를 검출.
            shape = predictor(img_frame, face)  # 얼굴에서 68개 점 찾기

            list_ori_points = []
            for p in shape.parts():
                list_ori_points.append([p.x, p.y])
            # list_ori_points = np.array(list_ori_points)

            list_ori_mouth_points = []
            # 입 부분 좌표 저장
            for j in range(48, 68):
                list_ori_mouth_points.append(list_ori_points[j])
            # list_ori_mouth_points = np.array(list_ori_mouth_points)

            final_ori_point.append(list_ori_mouth_points)
            # final_ori_point = np.array(final_ori_point)
            i += 1

            # 주어진 이미지 img_frame의 검출된 얼굴 영역 face에서 랜드마크를 검출.
    cap.release()

    return final_ori_point
