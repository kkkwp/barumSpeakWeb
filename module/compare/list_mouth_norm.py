import cv2 as cv
import dlib
import numpy as np

def get_frames_mouth(original):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    MOUTH_WIDTH = 100
    MOUTH_HEIGHT = 50
    HORIZONTAL_PAD = 0.19
    normalize_ratio = None
    mouth_frames = []

    cap = cv.VideoCapture(original)
    j = 0
    while j < 75:
        ret, frames = cap.read()


        for frame in frames:
            dets = detector(frame, 1)
            shape = None

            global i
            for k, d in enumerate(dets):
                shape = predictor(frame, d)
                i = -1
            if shape is None:  # Detector doesn't detect face, just return as is
                return frames

            mouth_points = []
            for part in shape.parts():
                i += 1
                if i < 48:  # Only take mouth region
                    continue

                # 여기서 part.x가 x좌표를, part.y가 y좌표를 추출 mouth_poins array에 추가
                mouth_points.append((part.x, part.y))
            np_mouth_points = np.array(mouth_points)

            # 입의 중앙 점 찾기
            mouth_centroid = np.mean(np_mouth_points[:, -2:], axis=0)

            if normalize_ratio is None:
                # 입의 가장 왼쪽 부분 찾기
                mouth_left = np.min(np_mouth_points[:, :-1]) * (1.0 - HORIZONTAL_PAD)
                # x좌표만 필요하니까 x좌표만 사용 np_mouth_points[:, :-1]
                # 입의 가장 오른쪽 부분 찾기
                mouth_right = np.max(np_mouth_points[:, :-1]) * (1.0 + HORIZONTAL_PAD)

                # 정규화(normalization)를 위해 / MOUTH_WIDTH = 100
                normalize_ratio = MOUTH_WIDTH / float(mouth_right - mouth_left)

            # 새로운 이미지가 들어왔을 때 위에서 구한 정규화 시키기는 비율(?)로 원하는 크기로 만들어 줌
            new_img_shape = (int(frame.shape[0] * normalize_ratio),
                             int(frame.shape[1] * normalize_ratio))  # frame.shape[0]: 프레임 구조 첫번째 요소(Width)
            # frame.shape[1]: 프레임 구조 첫번째 요소(Height)
            resized_img = cv.resize(frame, dsize=new_img_shape)

            # 정규화된 입의 포인트
            mouth_centroid_norm = mouth_centroid * normalize_ratio

            # mouth_centroid_norm[0]이 입의 중앙점의 x좌표
            # mouth_centroid_norm[1]이 입의 중앙점의 y좌표
            mouth_l = int(mouth_centroid_norm[0] - MOUTH_WIDTH / 2)
            mouth_r = int(mouth_centroid_norm[0] + MOUTH_WIDTH / 2)
            mouth_t = int(mouth_centroid_norm[1] - MOUTH_HEIGHT / 2)
            mouth_b = int(mouth_centroid_norm[1] + MOUTH_HEIGHT / 2)

            # mouth좌표를 바탕으로 정규화 된 이미지 사이즈를 저장
            mouth_crop_image = resized_img[mouth_t:mouth_b, mouth_l:mouth_r]

            # mouth_frames(WxH)에 이미지 사이즈 정보 추가
            mouth_frames.append(mouth_crop_image)
            j += 1

    return mouth_frames


'''def list_video(original):
    # 얼굴 검출을 위해 디폴트 얼굴 검출기 사용
    detector = dlib.get_frontal_face_detector()
    # 검출된 얼굴에서 눈, 코, 입같은 랜드마크를 찾기 위해 사용할 학습모델을 로드합니다.
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    # 웹캠으로부터 영상을 가져와 입력으로 사용합니다.
    cap = cv.VideoCapture(original)

    final_ori_point = []

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

    return final_ori_point'''

