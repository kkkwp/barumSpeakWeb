import os
import subprocess
import datetime
import threading
import numpy as np

upload_dir= "/home/ivpl-d04/다운로드/"
input_dir= "inputVideo/"
output_dir= "/var/www/html/barum/static/outputVideo/"
video_dir = "/var/www/html/barum/static/video/"


def remove():
    resultfile = os.listdir(output_dir)
    resultfile_mp4 = [file for file in resultfile if file.endswith(".mp4")]
    resultfile_png = [file for file in resultfile if file.endswith(".png")]
    if len(resultfile_mp4) != 0:
        try:
            result = str(resultfile_mp4[0])
            print(result)
            os.system('rm ' + output_dir + result)
            for i in range(len(resultfile_png)):
                os.system('rm ' + output_dir + resultfile_png[i])

        except:
            print("No result file")
            pass

def output_rem():
    outputfile = os.listdir(video_dir)
    outputfile_mp4= [file for file in outputfile if file.startswith("out")]
    if len(outputfile_mp4) != 0:
        try:
            for i in range(len(outputfile_mp4)):
                os.system('rm ' + video_dir + outputfile_mp4[i])
        except:
            print("No result file")
            pass

def predict(weight):
    videofiles = os.listdir(upload_dir)
    videofiles_mp4 = [file for file in videofiles if file.endswith(".webm")]
    videofiles_mp4.sort()
    if len(videofiles_mp4) != 0:
        try:
            content = str(videofiles_mp4[-1])
            print(content)
            content_new = ""
            for i in range(len(content)-4):
                content_new = content_new + content[i]
            content_video = content_new + "mp4"
            content_audio = content_new + "wav"

            os.system("ffmpeg -i " + upload_dir + content + " " + input_dir + content_video)
            os.system("ffmpeg -i " + upload_dir + content + " " + input_dir + content_audio)
            os.system("mv " + input_dir + content_audio + " /home/ivpl-d04/Web/module/console/")
            os.system('rm ' + upload_dir + content)
            os.system('python ../LipNet/evaluation/predict.py ' + str(weight) + '.h5 ./inputVideo/' + content_video)
        except:
            print("Try Except Error")
            pass

    threading.Timer(5, predict).start()