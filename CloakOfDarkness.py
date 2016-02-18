#!/usr/bin/env python
# -*- coding: utf-8 -*-

from S63 import S63
from time import sleep
import sys
from queue import Queue
from Audiotel2 import Game
from Player import Player
from Action import Goto, ChangeVar, Lambda, Describe, Group
from Element import Room


class CloakOfDarkness(Game):
  def setup(g):

    g.s('wear_coat', True)
    g.s('disturbed_room', 0)
    g.ga({'#' : Lambda(lambda g: g.look())})

    foyer = Room()
    
    foyer.d("Vous êtes dans le foyer de l'Opéra.")
    foyer.d("Une porte donne vers l'extérieur mais vous n'avez aucunement l'intention de sortir sous la pluie battante.")
    foyer.d(("Votre manteau est ruisselant de pluie.", lambda g:g.s('wear_coat')))
    foyer.d("Il n'y a personne autour de vous.")
    foyer.d("Pour aller au bar, tapez 1.")
    foyer.d("Pour aller au vestiaire, tapez 2.")
    foyer.d(("Pour examiner votre manteau, tapez 3.", lambda g:g.s('wear_coat')))

    foyer.a({
      ('1', lambda g:not g.s('wear_coat')) : Goto('bar'),
      ('1', lambda g:g.s('wear_coat')) : Lambda(lambda g:g.inc('disturbed_room'), description="Vous essayez d'entrer mais il fait trop sombre, vous ressortez de peur de déranger quelquechose dans l'obscurité."),
      '2':Goto('vestiaire'),
      '3':Describe(description = "Il s'agit de votre manteau absorbeur de lumière qui rend tout si ténébreux.")
      })
    
    g.r({'foyer':foyer})

    bar = Room()
    bar.d(("Vous pénétrez dans le bar désormais éclairé.", lambda g: True))
    bar.d(("Sur le sol, le sable déplacé par vos tentatives précédentes révèle un message : vous avez perdu", lambda g:g.s('disturbed_room') >= 2))
    bar.d(("Sur le sol, du sable savament arrangé révèle un message : vous avez ganié.", lambda g:g.s('disturbed_room') < 2))
    
    g.r({'bar':bar})

    vestiaire = Room()
    vestiaire.d("Le vestiaire est également désert.")
    vestiaire.d("Au mur, se trouve un crochet.")
    vestiaire.d("Pour retourner dans le foyer, tapez 1")
    vestiaire.d(("Pour accrocher votre manteau, tapez 2.", lambda g:g.s('wear_coat')))
    vestiaire.d(("Pour enfiler votre manteau, tapez 2.", lambda g:not g.s('wear_coat')))

    vestiaire.a({
      '1':Goto('foyer'),
      ('2', lambda g:not g.s('wear_coat')) : ChangeVar('wear_coat', True, description="Vous enfilez à nouveau votre manteau."),
      ('2', lambda g:g.s('wear_coat')) : ChangeVar('wear_coat', False, description="Vous posez votre manteau sur le petit crochet."),
      })

    g.r({'vestiaire':vestiaire})

    g.set_current_room(foyer)

def error(msg):
  print(msg)
  sys.exit(1)

if __name__ == "__main__":
  try:
    import RPi.GPIO as GPIO
    q = None
  except ImportError:
    q = Queue()
  

  try:
    phone = S63(queue=q)
    phone.start()
    phone.setErrorCallback(error)

    p = Player()

    game = CloakOfDarkness(player = p)
    phone.setCallback(game.update)
    if(sys.platform == 'darwin'):
      game.preload()
      #pass
    game.start()

    while True:
      if q is not None:
        line = input('mygame> ')
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