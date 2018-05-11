#!/usr/bin/env python

import colorsys
import math
import time
import random

from color import Color, HSVColor
import unicornhat as unicorn

unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)
unicorn.brightness(1)

def lerp(a, b, t):
    return a + (b - a) * t

def float2bits(x):
    x = min(1.0, max(x, 0.0))
    return int(round(x*255))

class UnicornDisplay():
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.bufferA = [[Color() for i in range(width)] for i in range(height)]
        self.bufferB = [[Color() for i in range(width)] for i in range(height)]
        self.flipped = False

    def getPixel(self, x, y):
        return self.frontBuffer()[y][x]

    def setPixel(self, x, y, color):
        self.frontBuffer()[y][x] = color

    def frontBuffer(self):
        return self.bufferA if self.flipped else self.bufferB

    def backBuffer(self):
        return self.bufferB if self.flipped else self.bufferA

    def swapBuffer(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.frontBuffer()[y][x]
                if color != self.backBuffer()[y][x]:
                    unicorn.set_pixel(x, y, color.r, color.g, color.b)
                    self.backBuffer()[y][x] = color
        self.flipped = not self.flipped
        unicorn.show()

if __name__ == '__main__':

    #line = [HSVColor() for i in range(8)]
    matrix = [[HSVColor() for i in range(9)] for i in range(8)]

    d = UnicornDisplay()

    while True:
        for y in range(8):
            if random.random() < 0.05:
                matrix[y][8].h = random.random()
                matrix[y][8].v = 1.0
            else:
                matrix[y][8].v -= 0.1

        for x in range(8):
            for y in range(8):
                #d.pixel(x, y, Color.fromHSV(lerp(0.0, 0.25, x/7.0), 1, y/7.0))
                matrix[y][x].v = matrix[y][x+1].v
                matrix[y][x].h = matrix[y][x+1].h
                #hsv.v *= 0.9
                r, g, b = colorsys.hsv_to_rgb(matrix[y][x].h, matrix[y][x].s, matrix[y][x].v)
                unicorn.set_pixel(x, y, float2bits(r), float2bits(g), float2bits(b))

        unicorn.show()
        time.sleep(0.1)
