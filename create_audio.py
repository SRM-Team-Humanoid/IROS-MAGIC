from gtts import gTTS

tts = gTTS(text="Hello! I am Ghost from SRM HRC. I am here to perform in Humanoid Application Challenge.", lang='en', slow=False)
tts.save('audio_files/Intro.mp3')

