# barumSpeakWeb

### - 추진 배경 및 목적

### - 작품 소개

### - 시나리오
* Barum Speak LipNet code
 <a href="https://github.com/barumSpeak/barumLipNet">barumSpeakWeb</a>

### - 시스템 구조
![KakaoTalk_20211029_135507103](https://user-images.githubusercontent.com/67499154/139378113-8ba4fa71-e1e4-4444-9f44-5d2b456625ea.jpg)

### - 기대효과
* 영어 발음을 조금 더 원어민에 가깝게 발음할 수 있도록 도움을 줄 수 있을 것을 기대
* 더 많은 데이터를 이용하여 학습할 수 있는 문장을 늘림에 따라 서비스의 확대 기대
* 음성인식 모델

### - 사용 환경
- **Library** : OpenCV, DLib
- **Tool** : PyCharm, Microsoft Azure Congnitive Services speech SDK
- **Language** : Python
- **Web Framework** : Flask

---
# 개발환경 설정
- python 3.6.13
- Anaconda 4.10.1
- dlib 19.22.0
- ffmpeg 4.2.4-1

---
# 실행 방법
Web 파일에 들어있는 코드를 다음 위치로 옮겨줍니다.
/var/www/html/Web

### - 동영상 설정
Web/ 과 /static/inputVideo/ 에 (가이드라인 영상)lecture{i}.mp4를 추가하여 준다.<br>
/static/video/ 에 (입모양 점수 비교 기준 영상)lecture{i}.mp4와 (입모양 표시 된 영상) lecture{i}\_lip.mp4를 추가해 준다.<br>

현 코드에서는 초상권 보호로 영상을 올려 놓지 않았습니다.

### - 실행

flask코드가 들어있는 파일로 이동 후 터미널에서 실행을 시켜줍니다.

```
flask run
```

실행된 채로 Chrome에 접속해 http://0.0.0.0:5000/ 주소로 이동한 후 첫번째 페이지가 나옵니다.
