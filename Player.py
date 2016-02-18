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

    self.running = threading.Event()
    self.queue = queue.Queue()
    self.loop = PlayerLoop(self.running, queue=self.queue)
    self.start()

  def start(self):
    self.running.set()
    self.loop.start()

  def clean(self):
    self.running.clear()
    self.loop.join()


  def say(self, text, voice="Thomas"):
    filename = "assets/"+hashlib.md5(text.encode('utf-8')).hexdigest()
    #print(text)
    if(sys.platform == 'darwin'):
      esc_desc = shellquote(text)
      os.system("say -v "+voice+" "+esc_desc)
      #os.system("say -v "+voice+ " -o "+soundfile+" --data-format=LEF32@22050 "+esc_desc+" && ffmpeg -i "+soundfile+"  -acodec libvorbis "+oggfile+"")
    else:
      sound= pygame.mixer.Sound(filename+".ogg")
      self.queue.add(sound)

  def preload(self, text, voice="Thomas"):
    filename = "assets/"+hashlib.md5(text.encode('utf-8')).hexdigest()
    if(sys.platform == 'darwin'):
      esc_desc = shellquote(text)
      os.system("say -v "+voice+ " -o "+filename+".wav --data-format=LEF32@22050 "+esc_desc+" && ffmpeg -i "+filename+".wav  -acodec libvorbis "+filename+".ogg")

class PlayerLoop(Thread):
  def __init__(self,event, queue = None):
    Thread.__init__(self)
    self.daemon = True
    self.runningEvent = event
    self.queue = queue

  def run(self):
    initial = time.time()
    while self.runningEvent.is_set():
      try:
        if self.queue is not None:
          sound = self.queue.get(False)
          sound.play()
          while sound.get_busy()
            continue
          continue
      except queue.Empty:
        continue
      except Exception as e:
        continue
      sleep(.1)
    print("Player Subroutine ended by clearing runningEvent")
    self.clean()

    