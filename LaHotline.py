#!/usr/bin/env python
# -*- coding: utf-8 -*-

from S63 import S63
from time import sleep
import sys
from Queue import Queue
from Audiotel import Room


generic_death = Room("Thomas", "Tout l'air s'échappe de la pièce. Vous mourez instantanément.")
wait_for_help = Room("Amelie", "Les secours viennent vous chercher mais trop tard. Bravo, vous avez gagné !")

start = Room("Thomas", 
  """Vous êtes dans une pièce vide. 
  Pour ouvrir la porte, tapez 1. 
  Pour attendre, tapez 2.
  Pour vous équipper, tapez 3.
  """)

start_equipped = Room("Thomas", 
  """Vous êtes dans une pièce vide. Vous portez une combinaison.
  Pour ouvrir la porte, tapez 1. 
  Pour attendre, tapez 2.
  """)

out_there = Room("Thomas", 
  """Lorsque vous ouvrez la porte vous constatez que vous êtes dans 
l'espace et que la Terre n'est plus qu'un tout petit point lumineux.
  """)

start.add_paths({
    '1': generic_death,
    '2': wait_for_help,
    '3': start_equipped
})

start_equipped.add_paths({
    '1': out_there,
    '2': wait_for_help
})





def error(msg):
  print msg,"FROM HERE"
  sys.exit(12)

def callback(d):
    print "Court :", d

q = Queue()

try:
  phone = S63(queue=q)
  phone.start()
  phone.setErrorCallback(error)
  start.play()
  phone.setCallback(start.callback_go(phone.setCallback))

  while True:
    line = raw_input('hotline> ')
    if line == 'quit':
      break
    q.put(line.split(","))
    sleep(.1)

finally:
  phone.clean()
  e = sys.exc_info()
  if(e[0] is not None):
    raise
  sys.exit()
