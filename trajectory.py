import math

radius = 160

def toradian(theta):
    return theta * math.pi / 180

def todegrees(theta):
    return theta * 180 / math.pi

def gradient(p1, p2):
    if p1[0] == p2[0]:
        m = toradian(90)
    else:
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    return m

def AngleFromGradient(gradient):
    return math.atan(gradient)

def getangle(pos, origin):
    m = gradient(pos, origin)
    thetaRad = AngleFromGradient(m)
    theta = round(todegrees(thetaRad), 2)
    return theta

def posoncircumeference(theta, origin):
    theta = toradian(theta)
    x = origin[0] + radius * math.cos(theta)
    y = origin[1] + radius * math.sin(theta)
    return (x, y)