import subprocess
from gtts import gTTS
import os
import pygame
def play_sound(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
def say(speak):
        tts = gTTS(speak)
        tts.save(".outputQwerthjgfr5ty4ui3j4b5fr4t6e7wuisdjhfgrty4u.mp3")
        play_sound('.outputQwerthjgfr5ty4ui3j4b5fr4t6e7wuisdjhfgrty4u.mp3')
        os.remove(".outputQwerthjgfr5ty4ui3j4b5fr4t6e7wuisdjhfgrty4u.mp3")
