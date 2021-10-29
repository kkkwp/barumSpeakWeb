const recordButton =document.querySelector(".record-button");
const stopButton =document.querySelector(".stop-button");
const playButton =document.querySelector(".play-button");
const predictButton =document.querySelector(".predict-button");
const previewPlayer = document.querySelector("#preview");
const recordingPlayer = document.querySelector("#recording");

let recorder;
let recordedChunks;

//functions
function videoStart() {
  navigator.mediaDevices.getUserMedia({ video:true,audio:true })
  .then(stream => {
    previewPlayer.srcObject = stream;
    startRecording(previewPlayer.captureStream())
  })
}
function startRecording(stream) {
  recordedChunks=[];
  recorder = new MediaRecorder(stream);
  recorder.ondataavailable = (e)=>{ recordedChunks.push(e.data) }
  recorder.start();
}
function stopRecording() {
   previewPlayer.srcObject.getTracks().forEach(track => track.stop());
   recorder.stop();
}
function playRecording() {
   const recordedBlob = new Blob(recordedChunks, {type:"video/webm"});
   var url = URL.createObjectURL(recordedBlob);
   var date = new Date();

   // 녹화 보기
   recordingPlayer.src=url;
   recordingPlayer.play();

   // 결과 보기 (predict)
   result = date.toISOString();
   console.log(result);
   predictButton.href=url;
   predictButton.download =`recording_${result}.webm`;
   console.log(url);
}
//event
recordButton.addEventListener("click",videoStart);
stopButton.addEventListener("click",stopRecording);
playButton.addEventListener("click",playRecording);
