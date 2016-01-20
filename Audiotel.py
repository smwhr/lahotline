# -*- coding: utf-8 -*-
#OSX Installed : Thomas (fr), Amelie (fr), Karen (en), Alex (en)
import os

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

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

  def __init__(self, voice, description):
    self.voice = voice
    self.description = description
    self.paths = {}

  def play(self):
    for d,c in self.description:
      if c :
        esc_desc = shellquote(d)
        os.system("say -v "+self.voice+" "+esc_desc)

  def go(self, direction):
    return self.paths.get(direction, None)

  def add_paths(self, paths):
    self.paths.update(paths)

  def callback_go(self,phone_callback):
    room = self
    def choices(d):
      print "Vous avez choisi", d
      dest = room.go(d)
      if(dest is not None):
        phone_callback(dest.callback_go(phone_callback))
        dest.play()
      else:
        room.play()
    return choices

class Game(object):
  def __init__(self, name):
    self.name = name
    self.rooms = {}

  def add_rooms(self, rooms):
    self.rooms.update(rooms)

  def add_room(self, key, room):
    self.rooms[key] = room;

class Action:
  def alter_room(self,target, replacement):
    target.voice = replacement.voice
    target.description = replacement.description
    target.add_paths(replacement.paths)