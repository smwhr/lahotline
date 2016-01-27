# -*- coding: utf-8 -*-
from queue import Queue
import threading
from Player import Player

class Game(object):

  def __init__(self, initial_state={},global_actions={}, player=Player()):
    #needed arguments
    self.player = player
    self.collector = []
    self.initial_state = initial_state.copy()
    self.game_state = GameState(initial_state)
    self.global_actions = global_actions
    self.rooms = {}

    self.setup()

    # self.inputs = Queue()
    # self.loopEvent = threading.Event()
    #self.loop  = GameLoop(loopEvent = self.loopEvent, queue = self.inputs, actioner = self.update)

  def setup(self):
    pass

  def start(self):
    self.look()

  def stop(self):
    pass

  def save(self):
    pass

  def preload(self):
    for room_name in self.rooms:
      room = self.rooms[room_name]
      for description in room.descriptions:
        if type(description) == tuple:
          description, cond = description
        self.player.preload(description)

  def r(self, rooms):
    self.add_rooms(rooms)

  def add_rooms(self, rooms):
    self.rooms.update(rooms)

  def set_current_room(self, room):
    self.game_state.set("current_room",room)

  def get_current_room(self):
    return self.game_state.get("current_room")

  def on_room_change(self, old_room, new_room):
    new_room.describe(self)

  def look(self):
    self.get_current_room().describe(self)


  def ga(self, actions):
    self.add_global_actions(actions)

  def add_global_actions(self, actions):
    self.global_actions.update(actions)

  def get_available_actions(self):
    all_actions = {}
    all_actions.update(self.global_actions)
    room_actions = self.get_current_room().actions
    all_actions.update(room_actions)

    actions = {}
    for action_code in all_actions:
      action = all_actions[action_code]
      if type(action_code) == tuple:
        action_code, cond = action_code
      else:
        cond = lambda g:True
      if cond(self):
        actions.update({action_code:action})
    return actions
    

  def pyramid_inputs(self):
    p = ""
    while self.collector:
      b = self.collector.pop()
      p += str(b)
      yield p

  def update(self, d):
    self.collector.append(d)
    actions = self.get_available_actions()
    didSomething = False
    for code in self.pyramid_inputs():
      if(code in actions):
        actions[code].execute(self)
        self.collector = []
        didSomething = True
        break

  def s(self, *args, **kwargs):
    if(len(args) == 1):
      return self.game_state.get(*args, **kwargs)
    else:
      return self.game_state.set(*args, **kwargs)

  def inc(self,key, **kwargs):
    return self.game_state.inc( key, **kwargs)


    

class GameLoop(threading.Thread):
  def __init__(self, *args, **kwargs):
    #needed arguments
    self.loopEvent = kwargs['loopEvent']
    self.queue = kwargs['queue']
    self.actioner = kwargs['actioner']

    threading.Thread.__init__(self)
    self.daemon = True
    

  def run(self):
    while self.loopEvent.is_set():
      try:
        d = self.queue.get(False)
        self.actionner(d)
      except:
        continue
      sleep(0.1)
    print("Game stopped via loopEvent")

class GameState:
  def __init__(self, initial = {}):
    self.states = {}
    self.states.update(initial)

  def get(self, key, ns=None):
    ns_states = self.states.get(ns, None)
    if ns_states is None:
      return None
    else:
      state = ns_states.get(key,None)
      return state

  def set(self, key, value, ns=None):
    print("setting",key,"to",value)
    ns_states = self.states.get(ns, None)
    if ns_states is None:
      self.states[ns] = {}
    
    self.states[ns][key] = value
    return value

  def inc(self, key, ns=None):
    ns_states = self.states.get(ns, None)
    if ns_states is None:
      self.states[ns] = {}
    curr_val = self.states[ns].get(key,None)
    if(curr_val is None):
      self.states[ns][key] = 0;
    self.states[ns][key]+=1

    