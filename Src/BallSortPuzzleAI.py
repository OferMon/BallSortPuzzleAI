import re
from copy import deepcopy
import json
import numpy as np
import time
import pandas as pd

cache = []
states = []

def readConfig():
    with open('Configuration.json', 'r') as configFile:
        configuration = json.load(configFile)
    return configuration

class BallsStack:
    def __init__(self, name, max_size, balls_array):
        self.name = name
        self.maxSize = max_size
        self.size = len(balls_array)
        self.ballsArray = balls_array
        self.isDone = False

    def is_full(self):
        if len(self.ballsArray) == self.maxSize:
            return True
        return False

    def is_empty(self):
        if len(self.ballsArray) == 0:
            return True
        return False

    def top(self):
        if self.is_empty():
            print("Error")
            exit(1)
        return self.ballsArray[self.size-1]

    def puse(self, ball):
        if self.size== self.maxSize:
            print("Error")
            exit(1)
        self.ballsArray.append(ball)
        self.size += 1
        self.update_is_done()

    def pop(self):
        if self.size == 0 or self.isDone:
            print("Error")
            exit(1)
        self.size -= 1
        return self.ballsArray.pop()


    def update_is_done(self):
        if self.is_full() is False:
            return
        if len(set(self.ballsArray)) == 1:
            self.isDone = True

    def to_str(self):
        return str(self.ballsArray)

class BaseState:
    trace = ""
    traceIndex = 0
    score = 0
    def __init__(self):
        self.balls_stacks = []
        configuration = readConfig()
        for s in configuration:
            balls_array = []
            for b in configuration[s][1]:
                balls_array.append(b)
            self.balls_stacks.append(BallsStack(s, configuration[s][0], balls_array))
        for s in self.balls_stacks:
            s.update_is_done()
        self.update_score()
        states.append(self)
        self.cache_add()

    def is_done(self):
        for s in self.balls_stacks:
            if s.isDone is True or len(s.ballsArray) == 0:
                continue
            return False
        return True

    def to_str(self):
        str = ""
        for s in self.balls_stacks:
            str += s.name + ": " + s.to_str() + "\n"
        return str

    def cache_add(self):
        state = self.to_str()
        if cache.count(state) == 0:
            cache.append(state)
            return False
        return True

    def update_score(self):
        counter = 0
        for bs in self.balls_stacks:
            if len(self.balls_stacks) == 0:
                continue
            for i in range(len(bs.ballsArray)-1):
                if bs.ballsArray[i] != bs.ballsArray[i+1]:
                    counter += 1
        self.score = counter

    def build_moves(self):
        for s in range(len(self.balls_stacks)):
            for d in range(len(self.balls_stacks)):
                if s == d:
                    continue
                state = deepcopy(self)
                state = state.move_ball(state.balls_stacks[s], state.balls_stacks[d])
                if state.cache_add():
                    continue
                else:
                    state.traceIndex += 1
                    state.trace += str(state.traceIndex) + "\t" + state.balls_stacks[d].top() + ": " + state.balls_stacks[s].name + " --> " + state.balls_stacks[d].name + "\n"
                    state.update_score()
                    states.append(state)


    def move_ball(self,src,des):
        if src.is_empty() or src.isDone or des.isDone or des.is_full():
            return self
        if des.is_empty() or src.top() == des.top():
            des.puse(src.pop())
            des.update_is_done()
        return self

def score_sort(e):
    return e.score

BaseState()
print(states[0].to_str())
while len(states) != 0:
    if states[0].is_done():
        print("solution found:")
        print(states[0].trace)
        print(states[0].to_str())
        exit(0)
    states[0].build_moves()
    states.pop(0)
    states.sort(key=score_sort)

print("No solution found")













