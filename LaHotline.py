#!/usr/bin/env python
# -*- coding: utf-8 -*-

from S63 import S63
from time import sleep
import sys
from Queue import Queue
from Audiotel import Room
from Audiotel import Action
from Audiotel import Game
from Player import Player


class LaHotline(Game):
  def __init__(self):

    initial = {'equipped':False}

    super(LaHotline,self).__init__("La Hot line", initial)
    self.player = Player()

    self.add_room('generic_death', Room([("Tout l'air s'échappe de la pièce. Vous mourez instantanément.",True)]))
    self.add_room('wait_for_help', Room("Amelie", [("Les secours viennent vous chercher mais trop tard. Bravo, vous avez gagnié !",True)]))

    self.add_room('empty_room', Room([("Vous êtes dans une pièce vide.",False),
                                     ("Vous portez une combinaison.",lambda: self.state.get("equipped")),
                                     ("Pour ouvrir la porte, tapez 1.",True),
                                     ("Pour attendre, tapez 2.",True),
                                     ("Pour vous équipper, tapez 3.",lambda: not self.state.get("equipped")),
                                    ]
                                    ))

    self.add_action('equip', Action("Vous enfilez une combinaison",lambda:self.state.set('equipped',True)))

    self.add_room('out_there', Room([("""Lorsque vous ouvrez la porte vous constatez que vous êtes dans 
                                      l'espace et que la Terre n'est plus qu'un tout petit point lumineux.
                                        """,True)]))

    self.rooms['empty_room'].add_paths({
        '1': self.rooms['generic_death'],
        '2': self.rooms['wait_for_help'],
        '3': self.actions['equip']
    })  

    self.current_room = 'empty_room';





def error(msg):
  print msg
  sys.exit(1)

def callback(d):
    print "Court :", d

q = Queue()

try:
  phone = S63(queue=q)
  phone.start()
  phone.setErrorCallback(error)

  laHotline = LaHotline()
  phone.setCallback(laHotline.input)
  laHotline.run() #game loop (will yield regularly)


  while True:
    line = raw_input('hotline> ')
    if line == 'quit':
      break
    q.put(line.split(","))
    sleep(.1)

except:
  raise
finally:
  phone.clean()
  e = sys.exc_info()
  if(e[0] is not None):
    raise
  sys.exit()
