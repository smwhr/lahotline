#!/usr/bin/env python
# -*- coding: utf-8 -*-

from S63 import S63
from time import sleep
import sys
from Queue import Queue
from Audiotel import Room
from Audiotel import Game


class LaHotline(Game):
  def __init__(self):
    super(LaHotline,self).__init__("La Hot line")

    self.add_room('generic_death', Room("Thomas", [("Tout l'air s'échappe de la pièce. Vous mourez instantanément.",True)]))
    self.add_room('wait_for_help', Room("Amelie", [("Les secours viennent vous chercher mais trop tard. Bravo, vous avez gagnié !",True)]))

    self.add_room('empty_room', Room("Thomas", 
                                    [("Vous êtes dans une pièce vide.",False),
                                     ("Pour ouvrir la porte, tapez 1.",True),
                                     ("Pour attendre, tapez 2.",True),
                                     ("Pour vous équipper, tapez 3.",True),
                                    ]
                                    ))

    self.add_room('empty_room_equipped', Room("Thomas", 
                                        [("Vous êtes dans une pièce vide.",True),
                                         ("Vous portez une combinaison.",True),
                                         ("Pour ouvrir la porte, tapez 1.",True),
                                         ("Pour attendre, tapez 2.",True)
                                        ]
                                        ))
    self.add_room('out_there', Room("Thomas", 
                                    [("""Lorsque vous ouvrez la porte vous constatez que vous êtes dans 
                                      l'espace et que la Terre n'est plus qu'un tout petit point lumineux.
                                        """,True)]))

    self.rooms['empty_room'].add_paths({
        '1': self.rooms['generic_death'],
        '2': self.rooms['wait_for_help'],
        '3': self.rooms['empty_room_equipped']
    })


    self.rooms['empty_room_equipped'].add_paths({
        '1': self.rooms['out_there'],
        '2': self.rooms['wait_for_help']
    })

    self.current_room = 'empty_room';

  def get_current(self):
    return self.rooms[self.current_room]

  def play_current(self):
    self.get_current().play()





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
  laHotline.play_current()

  phone.setCallback(laHotline.get_current().callback_go(phone.setCallback))

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
