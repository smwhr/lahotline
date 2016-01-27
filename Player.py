import pygame
import sys
import hashlib
import os

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

class Player:
  def __init__(self):
    if(sys.platform == 'darwin'):
      pass
    else:
      pygame.init()
      pygame.mixer.init()


  def say(self, text, voice="Thomas"):
    soundfile = "assets/"+hashlib.md5(text.encode('utf-8')).hexdigest()+".wav"
    print(text)
    if(sys.platform == 'darwin'):
      esc_desc = shellquote(text)
      os.system("say -v "+voice+" "+esc_desc)
      return
    else:
      sound= pygame.mixer.Sound(soundfile)
      sound.play()

  def preload(self, text, voice="Thomas"):
    soundfile = "assets/"+hashlib.md5(text.encode('utf-8')).hexdigest()+".wav"
    if(sys.platform == 'darwin'):
      esc_desc = shellquote(text)
      os.system("say -v "+voice+ " -o "+soundfile+" --data-format=LEF32@8000 "+esc_desc)


    