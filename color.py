#!/usr/bin/env python

import colorsys
import math
import time

def lerp(a, b, t):
    return a + (b - a) * t

def float2bits(x):
    return int(round(x*255))

class Color():
    def __init__(self, r=0, g=0, b=0):
        self.r = min(255, max(int(r), 0))
        self.g = min(255, max(int(g), 0))
        self.b = min(255, max(int(b), 0))

    def __str__(self):
        r = hex(self.r)[2:]
        g = hex(self.g)[2:]
        b = hex(self.b)[2:]
        return '{0}{1}{2}'.format(r, g, b)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def fromHSV(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color(float2bits(r), float2bits(g), float2bits(b))

    @staticmethod
    def lerp(a, b, t):
        return Color(lerp(a.r, b.r, t), lerp(a.g, b.g, t), lerp(a.b, b.b, t))

class HSVColor():
    def __init__(self, h=0.0, s=1.0, v=0.0):
        self.h = min(1.0, max(h, 0.0))
        self.s = min(1.0, max(s, 0.0))
        self.v = min(1.0, max(v, 0.0))

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.h, self.s, self.v)

    def toRGB(self):
        return Color.fromHSV(self.h, self.s, self.v)

if __name__ == '__main__':
    print "hello"
