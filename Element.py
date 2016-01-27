# -*- coding: utf-8 -*-

class Room(object):
  def __init__(self):
    self.actions = {}
    self.descriptions = []

  def a(self, actions):
    self.add_actions(actions)

  def add_actions(self, actions):
    self.actions.update(actions)

  def d(self, descriptions):
    return self.add_descriptions(descriptions)

  def add_descriptions(self, descriptions):
    if(type(descriptions) == list):
      self.descriptions += descriptions
    else:
      self.descriptions.append(descriptions)

  def describe(self, game):
    for description in self.descriptions:
      if type(description) == tuple:
        description, cond = description
      else:
        cond = lambda g:True
      if cond(game):
        game.player.say(description)
