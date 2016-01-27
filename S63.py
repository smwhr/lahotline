import time
from time import sleep
import threading
from threading import Thread
import random
import sys
import queue

class S63:
  def __init__(self,callback = None, error_callback = None, queue = None):
    self.running = threading.Event()
    self.queue = queue
    
    if(callback is None):
      def callback(d):
        print(d)
    if(error_callback is None):
      def error_callback(msg):
        print(msg)
    
    self.io = S63IO(self.running, callback=callback, error_callback=error_callback, queue=self.queue)

  def start(self):
    self.running.set()
    self.io.start()

  def clean(self):
    self.running.clear()
    self.io.join()

  def setCallback(self,callback):
    if(callable(callback)):
      self.io.setCallback(callback)
    else:
      raise Exception("Cannot set a non callable objet as callback")

  def setErrorCallback(self,callback):
    if(callable(callback)):
      self.io.setErrorCallback(callback)
    else:
      raise Exception("Cannot set a non callable objet as error_callback")


class S63Config:
  pins = {"lines": {7:0,8:1,25:2,24:3}, "columns" : {11:0, 9:1, 10:2}}
  touches = [['1','2','3'],['4','5','6'],['7','8','9'],['*','0','#']]


class S63IO(Thread):
  """ PINS : 
  23 : hanger
  7 : line 0
  8 : line 1
  25 : line 2
  24 : line 3
  11 : col 0
  9 : col 1
  10 : col 2 """

  def __init__(self,event, callback = None, error_callback = None, queue = None):
    try:
      import RPi.GPIO as GPIO
      self.isRaspi = True
    except ImportError:
      self.isRaspi = False

    Thread.__init__(self)
    self.daemon = True
    self.runningEvent = event
    self.last_collect = 0
    self.last_compose = 0
    self.collector = [None,None]
    self.event_callback = callback
    self.error_callback = error_callback
    self.queue = queue

    self.hook_state = 0

    if self.isRaspi:
      GPIO.setmode(GPIO.BCM)

    try:
      if self.isRaspi:
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(23, GPIO.BOTH, callback=self.phone_hook, bouncetime=10)

        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(7, GPIO.FALLING, callback=self.compose_line, bouncetime=200)
        GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(8, GPIO.FALLING, callback=self.compose_line, bouncetime=100)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(25, GPIO.FALLING, callback=self.compose_line, bouncetime=100)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=self.compose_line, bouncetime=100)

        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(11, GPIO.FALLING, callback=self.compose_column, bouncetime=200)
        GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(9, GPIO.FALLING, callback=self.compose_column, bouncetime=100)
        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(10, GPIO.FALLING, callback=self.compose_column, bouncetime=100)
      else:
        print("Dummy GPIOs")
    except Exception:
      self.error_callback("Could not setup GPIO")
      self.clean()
      sys.exit(1)


  def clean(self):
    print("GPIO.cleanup()")
    if self.isRaspi:
      GPIO.cleanup()

  def setCallback(self,callback):
      self.event_callback = callback

  def setErrorCallback(self,callback):
      self.error_callback = callback

  def phone_hook(self,channel):
    if self.isRaspi:
      state = GPIO.input(channel)
    else:
      state = self.hook_state
    event = "U" if state == 0 else "D"
    self.event_callback(event)

  def compose_line(self,channel):
    self.collect(line = S63Config.pins["lines"][channel])

  def compose_column(self,channel):
    self.collect(column = S63Config.pins["columns"][channel])

  def collect(self,line = None, column = None):
    now = time.time()
    #print(now - last_collect)
    if now - self.last_collect > 0.005:
      self.collector = [None, None]
      if(line is not None):
        self.collector[0] = line
    if(column is not None):
      self.collector[1] = column
    if(self.collector[0] != None and self.collector[1] != None):
      #print(collector)
      self.composed(self.collector)
      self.collector = [None, None]
    self.last_collect = now

  def composed(self,tap):
    now = time.time()
    if now - self.last_compose < 0.100: #debounce at 100ms
      return
    digit = S63Config.touches[tap[0]][tap[1]]
    print(digit)
    self.event_callback(digit)
    self.last_compose = now

  def run(self):
    initial = time.time()
    while self.runningEvent.is_set():
      try:
        if self.queue is not None:
          l,c = self.queue.get(False)
          self.compose_line(int(l))
          self.compose_column(int(c))
          sleep(0.006) #so that there's no conflict with regular input
          continue
      except queue.Empty:
        continue
      except Exception as e:
        self.error_callback(e)
      sleep(.1)
    print("S63 Subroutine ended by clearing runningEvent")
    self.clean()
