import cv2 as cv
from module.compare.list_mouth_open import open_frame


def cut_vid(original, name):

    print("cut_vid")

    start_frame = open_frame(original)

    endframe = 75

    icurrentframe = 0

    cap = cv.VideoCapture(original)

    fps = cap.get(cv.CAP_PROP_FPS)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(name, fourcc, fps, (width, height))

    cap.set(cv.CAP_PROP_POS_FRAMES, start_frame)

    while True:
        if icurrentframe > (endframe - start_frame):
            break

        icurrentframe += 1

        ret, frame = cap.read()

        if frame is None:
            break

        out.write(frame)

        #cv.imshow('frame', frame)
        #cv.waitKey(1)
    print('cut_vid_end')
    cap.release()