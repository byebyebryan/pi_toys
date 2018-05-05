#!/usr/bin/env python

import time
import random

import colorsys
import math

import unicornhat as unicorn

from snmp import SNMP

targetFPS = 12
updateInterval = 3.0

unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)
unicorn.brightness(0.5)

snmp = SNMP()
snmp.init()

timeSinceFrameStart = time.time()
targetFrameTime = 1.0 / targetFPS

timeTillNextUpdate = updateInterval

def lerp(a, b, t):
    return a + (b - a) * t

def clip(x, a, b):
    return max(a, min(x, b))

def float2bits(x):
    x = clip(x, 0.0, 1.0)
    return int(round(x*255))

def setPixel(x, y, cell):
    r, g, b = colorsys.hsv_to_rgb(cell.h, 1.0, cell.v)
    unicorn.set_pixel(x, y, float2bits(r), float2bits(g), float2bits(b))

inRate = 0.0
inRate_ = 0.0
targetInRate = 0.0
outRate = 0.0
outRate_ = 0.0
targetOutRate = 0.0

class Cell():
    def __init__(self, h=0.0, v=0.0):
        self.h = h
        self.v = v

grid = [[Cell() for i in range(9)] for i in range(8)]

def tick(dt):
    global timeTillNextUpdate, inRate, targetInRate, outRate, targetOutRate, inRate_, outRate_
    if timeTillNextUpdate <= 0.0:
        snmp.update()
        targetInRate = snmp.inRate
        targetOutRate = snmp.outRate
        timeTillNextUpdate = updateInterval
    else:
        timeTillNextUpdate -= dt

    inRate = lerp(inRate, targetInRate, dt * 0.4)
    outRate = lerp(outRate, targetOutRate, dt * 0.4)
    inRate_ = lerp(inRate_, targetInRate, dt * 0.2)
    outRate_ = lerp(outRate_, targetOutRate, dt * 0.2)
    #print "{0} : {1}".format(inRate, outRate)
    render(dt)

intervalCounter = 0

def render(dt):
    global inRate, targetInRate, outRate, targetOutRate, grid, intervalCounter, inRate_, outRate_

    rate = clip(inRate / 32000, 0, 1)
    rate_ = clip(inRate_ / 32000, 0, 1)

    if intervalCounter <= 0:
        intervalCounter = 8

        if rate_ > 0.05:
            grid[3][8].h = lerp(0.5, 0.0, rate)
            grid[3][8].v = 1.0
        if rate_ > 0.1:
            grid[4][8].h = lerp(0.5, 0.0, rate)
            grid[4][8].v = 1.0
        if rate_ > 0.15:
            grid[2][8].h = lerp(0.5, 0.0, rate)
            grid[2][8].v = 1.0
        if rate_ > 0.2:
            grid[5][8].h = lerp(0.5, 0.0, rate)
            grid[5][8].v = 1.0
        if rate_ > 0.25:
            grid[1][8].h = lerp(0.5, 0.0, rate)
            grid[1][8].v = 1.0
        if rate_ > 0.3:
            grid[6][8].h = lerp(0.5, 0.0, rate)
            grid[6][8].v = 1.0
        if rate_ > 0.35:
            grid[0][8].h = lerp(0.5, 0.0, rate)
            grid[0][8].v = 1.0
        if rate_ > 0.4:
            grid[7][8].h = lerp(0.5, 0.0, rate)
            grid[7][8].v = 1.0
    else:
        intervalCounter -= 1
        for y in range(8):
            v = clip(grid[y][8].v - 0.1, 0, 0.5)
            h = 0.5 + grid[y][8].h
            grid[y][8].v -= v * v * h * h

    for x in range(8):
        for y in range(8):
            #d.pixel(x, y, Color.fromHSV(lerp(0.0, 0.25, x/7.0), 1, y/7.0))
            grid[y][x].v = grid[y][x+1].v
            grid[y][x].h = grid[y][x+1].h
            #hsv.v *= 0.9
            setPixel(x, y, grid[y][x])

    unicorn.show()

while True:
    dt = time.time() - timeSinceFrameStart
    restTime = targetFrameTime - dt
    if restTime > 0:
        time.sleep(restTime)

    dt = time.time() - timeSinceFrameStart
    timeSinceFrameStart = time.time()
    tick(dt)
