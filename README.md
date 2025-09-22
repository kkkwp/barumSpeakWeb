# barumSpeakWeb

영어 발음 교정을 위한 웹 기반 서비스로, LipNet 기반 입모양 분석 모델을 활용하여 사용자의 발음을 시각적으로 피드백합니다. 

Flask 프레임워크로 구현되었습니다.

---

## 추진 배경 및 목적

- 한국어 화자가 영어 발음 학습에서 겪는 어려움 해결 필요
- 기존 청각 중심 학습의 한계를 넘어 시각적 학습 도구 제공

---

## 작품 소개
- **바름스픽(BarumSpeak)** 은 LipNet 기반 입모양 분석 모델을 적용했습니다.
- 사용자가 업로드한 발음을 기준 영상과 비교해 점수화합니다.
- 결과를 웹 환경에서 시각적으로 표시해 학습자가 즉시 피드백 확인이 가능합니다.
- 관련 코드: [barumLipNet](https://github.com/barumSpeak/barumLipNet)

---

## 시스템 구조

![System Architecture](https://user-images.githubusercontent.com/67499154/139378113-8ba4fa71-e1e4-4444-9f44-5d2b456625ea.jpg)

---

## 기대 효과
* 영어 발음을 조금 더 원어민에 가깝게 발음할 수 있도록 도움을 줄 수 있을 것을 기대
* 더 많은 데이터를 이용하여 학습할 수 있는 문장을 늘림에 따라 서비스의 확대 기대

---

## 개발 환경
- **Language** : Python 3.6.13
- **Web Framework** : Flask
- **Library** : OpenCV, DLib 19.22.0
- **Tool** : PyCharm, Microsoft Azure Cognitive Services Speech SDK
- **Package Manager** : Anaconda 4.10.1
- **Etc** : ffmpeg 4.2.4-1

---

## 실행 방법
1. Web 파일에 들어있는 코드를 `/var/www/html/Web` 경로로 이동

2. 영상 파일 추가
   - `Web/` 과 `/static/inputVideo/`에 가이드라인 영상 `lecture{i}.mp4` 추가
   - `/static/video/`에 기준 영상 `lecture{i}.mp4`와 입모양 표시 영상 `lecture{i}\_lip.mp4` 추가
   - 현 코드에서는 초상권 보호로 영상을 올려 놓지 않았습니다.

3. Flask 실행
```bash
flask run
```

4. [http://0.0.0.0:5000/](http://0.0.0.0:5000/) 접속
