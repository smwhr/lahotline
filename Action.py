# -*- coding: utf-8 -*-


def playable(func):
  def wrapper(*args):
    func(*args)
    if(args[0].description is not None):
      args[1].player.say(args[0].description)
  return wrapper

class Action(object):
  pass

class Goto(Action):
  def __init__(self, room_name):
    self.room_name = room_name

  def execute(self, game):
    old_room = game.s("current_room")
    new_room = game.s("current_room", game.rooms[self.room_name])
    game.on_room_change(old_room, new_room)
    

class ChangeVar(Action):
  def __init__(self, key, value, ns = None, description = None):
    self.key = key
    self.value = value
    self.ns = ns
    self.description = description

  @playable
  def execute(self, game):
    game.s(self.key, self.value, ns = self.ns)

class Lambda(Action):
  def __init__(self, func, description = None):
    self.func = func
    self.description = description

  @playable
  def execute(self, game):
    self.func(game)

class Describe(Action):
  def __init__(self, description = None):
    self.description = description

  @playable
  def execute(self, game):
    pass

class Group(Action):
  def __init__(self, *args):
    self.actions = list(args)

  def execute(self, game):
    for action in self.actions:
      action.execute(game)

    