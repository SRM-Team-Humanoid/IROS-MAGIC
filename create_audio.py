from gtts import gTTS

tts = gTTS(text='Hi, I am Ghost from SRM Team Humanoid. I am here to perform in Humanoid application Challenge.', lang='en', slow=False)
tts.save('audio_files/Intro.mp3')

tts = gTTS(text='Please, place the die in my hand.', lang='en', slow=False)
tts.save('audio_files/Pass.mp3')

for num in range(1,7):
    tts = gTTS(text = 'This is number '+str(num), lang = 'en', slow = False)
    tts.save('audio_files/Die'+str(num)+'.mp3')
    tts = gTTS(text = 'Please, pick up card number '+str(num), lang = 'en', slow = False)
    tts.save('audio_files/Card' + str(num) + '.mp3')

