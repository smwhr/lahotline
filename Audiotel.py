# -*- coding: utf-8 -*-
#OSX Installed : Thomas (fr), Amelie (fr), Karen (en), Alex (en)
import os
from queue import Queue

class Game(object):
  def __init__(self, name,initial = {}):
    self.name = name
    self.rooms = {}
    self.actions = {}
    self.state = GameState(initial)
    self.current_room = None
    self.player = None
    self.actions

  def add_room(self, key, room):
    self.rooms[key] = room;

  def add_action(self, key, action):
    self.actions[key] = action;

  def get_current(self):
    return self.rooms[self.current_room]

  def play_current(self):
    self.get_current().play()

  def input(self, in):


  def loop():
    while True:

class GameState:
  def __init__(self, initial = {}):
    self.states = {}
    self.states.update(initial)

  def get(self, name, ns="global"):
    ns_states = self.states.get(ns, None)
    if ns_states is None:
      return None
    else:
      state = ns_states.get(name,None)
      return state

  def set(self, name, value, ns="global"):
    ns_states = self.states.get(ns, None)
    if ns_states is None:
      self.states[ns] = {}
    
    self.states[ns]
    return state

class Room:
  def __init__(self, lines, options):
    self.voice = voice
    self.lines = lines
    self.options = options
    self.paths = {}

  def play(self):
    to_play = []
    for d,cond in self.lines:
      say_d = True
      if callable(cond):
        say_d = cond()
      else :
        say_d = cond
      if say_d :
        to_play.append(d)

  def go(self, direction):
    return self.paths.get(direction, None)

  def add_paths(self, paths):
    self.paths.update(paths)

  def get_paths(self):
    available = []
    for d,cond in self.lines:
      can_d = True
      if callable(cond):
        can_d = cond()
      else :
        can_d = cond
      if can_d :
        available.append(d)


class Action:
  def __init__(self, voice, description, *args, **kwargs):
    arglist = list(args)
    self.action = arglist.pop(0)
    self.voice = voice
    self.description = description
    self.args = tuple(arglist)
    self.kwargs = kwargs

  def do(self):
    return self.action(*self.args, **self.kwargs)

  def play(self):
    
