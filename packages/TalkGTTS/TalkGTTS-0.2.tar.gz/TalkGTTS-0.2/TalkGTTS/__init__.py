import subprocess
from gtts import gTTS
import os
from playsound import playsound
def say(speak):
        tts = gTTS(speak)
        tts.save(".outputQwerthjgfr5ty4ui3j4b5fr4t6e7wuisdjhfgrty4u.mp3")
        playsound('.outputQwerthjgfr5ty4ui3j4b5fr4t6e7wuisdjhfgrty4u.mp3')
        os.remove(".outputQwerthjgfr5ty4ui3j4b5fr4t6e7wuisdjhfgrty4u.mp3")
