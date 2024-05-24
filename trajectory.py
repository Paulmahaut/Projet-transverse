from math import *

#https://github.com/pyGuru123/Simulations/blob/main/Projectile%20Motion/functions.py

radius = 160

def to_radian(theta):
    return theta * pi / 180

def to_degrees(theta):
    return theta * 180 / pi

def gradient(p1, p2):
    if p1[0] == p2[0]:
        m = to_radian(90)
    else:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return m

def AngleFromGradient(gradient):
    return atan(gradient)

def get_angle(pos, origin):
    m = gradient(pos, origin)
    thetaRad = AngleFromGradient(m)
    theta = round(to_degrees(thetaRad), 2)
    return theta

def pos_on_circumeference(theta, origin, sign):
    theta = to_radian(theta)
    x = origin[0] + radius * cos(theta) * sign
    y = origin[1] + radius *sin(theta)* sign
    return (x, y)