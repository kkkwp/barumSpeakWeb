from flask import Flask, render_template, request
from server import predict, remove, output_rem
from module.compare_frame_sali import grade
from module.lip_detect_save import landmark
from module.console.speech import select

import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

app = Flask(__name__)
path = "./inputVideo/"

def vid():
    videofiles = os.listdir(path)
    videofiles.sort()
    if len(videofiles) != 0:
        try:
            content = videofiles[-1]
        except:
            print("Try Except Error")
            pass
    return content

@app.route('/')
@app.route('/home')
def home():
    remove()
    output_rem()
    return render_template("home.html", isActive=True)

# guide
@app.route('/guideline1')
def guideline1():
    return render_template("guideline1.html")
@app.route('/guideline2')
def guideline2():
    return render_template("guideline2.html")
@app.route('/guideline3')
def guideline3():
    return render_template("guideline3.html")
@app.route('/guideline4')
def guideline4():
    return render_template("guideline4.html")

# lecture
@app.route('/lecture1')
def lecture1():
    return render_template("lecture1.html")
@app.route('/lecture2')
def lecture2():
    return render_template("lecture2.html")
@app.route('/lecture3')
def lecture3():
    return render_template("lecture3.html")
@app.route('/lecture4')
def lecture4():
    return render_template("lecture4.html")

# predict
@app.route('/predict1_view')
def predict1():
    predict("../LipNet/training/overlapped_speakers/s1/results/2021:09:08:23:24:27/weights250")
    return render_template("predict1_view.html")
@app.route('/predict2_view')
def predict2():
    predict("../LipNet/training/overlapped_speakers/s1/results/2021:09:08:23:24:27/weights323")
    return render_template("predict2_view.html")
@app.route('/predict3_view')
def predict3():
    predict("../LipNet/training/overlapped_speakers/s1/results/2021:09:08:23:24:27/weights300")
    return render_template("predict3_view.html")
@app.route('/predict4_view')
def predict4():
    predict("../LipNet/evaluation/models/overlapped-weights368")
    return render_template("predict4_view.html")

# score
@app.route('/score1_view')
def score1():
    score = grade('lecture1.mp4', path+vid())
    landmark(path+vid())
    os.system('ffmpeg -i /home/ivpl-d04/Web/static/video/output.mp4 -vcodec libx264 /home/ivpl-d04/Web/static/video/output_new.mp4')
    speech = select(1)
    total = int(score) + int(speech[0]) + int(speech[1]) + int(speech[2]) + int(speech[3])
    mean = total/5
    return render_template("score1_view.html", value = mean, accuracy = speech[0], pronunciation = speech[1], completeness = speech[2], fluency = speech[3])
@app.route('/score2_view')
def score2():
    score = grade('lecture2.mp4', path+vid())
    landmark(path + vid())
    os.system('ffmpeg -i /home/ivpl-d04/Web/static/video/output.mp4 -vcodec libx264 /home/ivpl-d04/Web/static/video/output_new.mp4')
    speech = select(2)
    total = int(score) + int(speech[0]) + int(speech[1]) + int(speech[2]) + int(speech[3])
    mean = total/5
    return render_template("score2_view.html", value = mean, accuracy = speech[0], pronunciation = speech[1], completeness = speech[2], fluency = speech[3])
@app.route('/score3_view')
def score3():
    score = grade('lecture3.mp4', path+vid())
    landmark(path + vid())
    os.system('ffmpeg -i /home/ivpl-d04/Web/static/video/output.mp4 -vcodec libx264 /home/ivpl-d04/Web/static/video/output_new.mp4')
    speech = select(3)
    total = int(score) + int(speech[0]) + int(speech[1]) + int(speech[2]) + int(speech[3])
    mean = total/5
    return render_template("score3_view.html", value = mean, accuracy = speech[0], pronunciation = speech[1], completeness = speech[2], fluency = speech[3])
@app.route('/score4_view')
def score4():
    score = grade('lecture4.mp4', path+vid())
    landmark(path + vid())
    os.system('ffmpeg -i /home/ivpl-d04/Web/static/video/output.mp4 -vcodec libx264 /home/ivpl-d04/Web/static/video/output_new.mp4')
    speech = select(3)
    total = int(score) + int(speech[0]) + int(speech[1]) + int(speech[2]) + int(speech[3])
    mean = total/5
    return render_template("score4_view.html", value = mean, accuracy = speech[0], pronunciation = speech[1], completeness = speech[2], fluency = speech[3])

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
