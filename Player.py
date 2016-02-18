# -*- coding: utf-8 -*-
import pygame
import sys
import hashlib
import os
import time
from time import sleep
import threading
from threading import Thread
import queue

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

class Player:
  def __init__(self):
    if(sys.platform == 'darwin'):
      pass
    else:
      pygame.init()
      pygame.mixer.init()
      self.channel = pygame.mixer.Channel(0)

  def say(self, text, voice="Thomas"):
    filename = "assets/"+hashlib.md5(text.encode('utf-8')).hexdigest()
    #print(text)
    if(sys.platform == 'darwin'):
      esc_desc = shellquote(text)
      os.system("say -v "+voice+" "+esc_desc)
      #os.system("say -v "+voice+ " -o "+soundfile+" --data-format=LEF32@22050 "+esc_desc+" && ffmpeg -i "+soundfile+"  -acodec libvorbis "+oggfile+"")
    else:
      sound= pygame.mixer.Sound(filename+".ogg")
      self.channel.queue(sound)
      if(self.channel.get_busy() == False):
        self.channel.play()

  def preload(self, text, voice="Thomas"):
    filename = "assets/"+hashlib.md5(text.encode('utf-8')).hexdigest()
    if(sys.platform == 'darwin'):
      esc_desc = shellquote(text)
      os.system("say -v "+voice+ " -o "+filename+".wav --data-format=LEF32@22050 "+esc_desc+" && ffmpeg -i "+filename+".wav  -acodec libvorbis "+filename+".ogg")


    