
import pygame
import math

pygame.font.init()  # init font

WIN_WIDTH = 800
WIN_HEIGHT = 600

STAT_FONT = pygame.font.SysFont("comicsans", 50)

background_color = (120, 120, 120)
danger_color = (140, 120, 120)

cutting = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.DOUBLEBUF, 64)
pygame.display.set_caption("supposed to be a thingy")


class Node:

    color = (0, 0, 0)
    pos = pygame.Vector2
    prevpos = pygame.Vector2
    locked = False

    def __init__(self, icolor, ipos, ilocked):
        self.color = icolor
        self.pos = ipos
        self.prevpos = ipos
        self.locked = ilocked


class Stick:

    color = (0, 0, 0)
    node1 = Node
    node2 = Node
    leng = 0

    def __init__(self, icolor, nodea, nodeb, length):
        self.color = icolor
        self.node1 = nodea
        self.node2 = nodeb
        self.leng = length


def addNode(locked):
    for p in points:
        if mcords.distance_to(p.pos) < 10:
            if not points.index(p) == selectedNode[0]:
                sticks.append(Stick((51, 51, 51), p, points[selectedNode[0]], p.pos.distance_to(points[selectedNode[0]].pos)))
                selectedNode[0] = points.index(p)
            return
    if locked:
        points.append(Node(pygame.Color(200, 100, 100), mcords, locked))
    else:
        points.append(Node(pygame.Color(100, 100, 100), mcords, locked))
    if len(points) > 1:
        sticks.append(Stick((51, 51, 51), points[len(points) - 1], points[selectedNode[0]], points[len(points) - 1].pos.distance_to(points[selectedNode[0]].pos)))

    selectedNode[0] = len(points) - 1


def invertNode():
    for p in points:
        if mcords.distance_to(p.pos) < 10:
            p.locked = not p.locked
            p.color = (255 - p.color[0], 255 - p.color[1], 255 - p.color[2])


def selectNode():
    for p in points:
        if mcords.distance_to(p.pos) < 10:
            selectedNode[0] = points.index(p)


def drawWindow(win, points, sticks):

    if not cutting:
        pygame.draw.rect(win, background_color, (0, 0, WIN_WIDTH, WIN_HEIGHT))
    else:
        pygame.draw.rect(win, danger_color, (0, 0, WIN_WIDTH, WIN_HEIGHT))

    for point in points:
        if selectedNode[0] == points.index(point):
            pygame.draw.circle(win, point.color, point.pos, 2 * math.cos(drawIterations / 500) + 8)
        else:
            pygame.draw.circle(win, point.color, point.pos, 5)

    for stick in sticks:
        pygame.draw.line(win, stick.color, stick.node1.pos, stick.node2.pos, 2)

    pygame.display.update()


def simulate(points, sticks):

    for point in points:
        if not point.locked:
            positionBeforeMove = pygame.Vector2(point.pos[0], point.pos[1])

            point.pos += (point.pos - point.prevpos) * 0.9999
            point.pos += pygame.Vector2(0, 0.0005)

            point.prevpos = positionBeforeMove

    numIterations = 3
    for x in range(numIterations):
        for stick in sticks:
            stickcentre = pygame.Vector2((stick.node1.pos[0] + stick.node2.pos[0])/2, (stick.node1.pos[1] + stick.node2.pos[1])/2)
            stickdir = pygame.Vector2(stick.node1.pos[0] - stick.node2.pos[0], stick.node1.pos[1] - stick.node2.pos[1]).normalize()

            stick_halfleng = stick.leng / 2

            if not stick.node1.locked:
                stick.node1.pos = stickcentre + stickdir * stick_halfleng
            if not stick.node2.locked:
                stick.node2.pos = stickcentre - stickdir * stick_halfleng


if __name__ == '__main__':

    drawIterations = 0

    selectedNode = [0]

    points = list()
    sticks = list()

    amtx = 10
    amty = 10

    """for x in range(amtx):

        delx = WIN_WIDTH / (amtx + 1)
        dely = WIN_HEIGHT / (amty + 1)

        for y in range(amty):
            position = ((x + 1) * delx, (y + 1) * dely)

            points.append(Node((51, x/amtx*255, y/amty*255), pygame.Vector2(position), False))

            if(x > 0):
                colortemp = points[len(points) - 1 - amty].color
                colorv = points[len(points) - 1].color

                lcolor = ((colorv[0] + colortemp[0]) / 2, (colorv[1] + colortemp[1]) / 2, (colorv[2] + colortemp[2]) / 2)

                sticks.append(Stick(lcolor, points[len(points) - 1], points[len(points) - 1 - amty], delx))
            if(y > 0):
                colortemp = points[len(points) - 2].color
                colorv = points[len(points) - 1].color

                lcolor = (
                (colorv[0] + colortemp[0]) / 2, (colorv[1] + colortemp[1]) / 2, (colorv[2] + colortemp[2]) / 2)

                sticks.append(Stick(lcolor, points[len(points) - 1], points[len(points) - 2], dely))"""

    over = False
    paused = True

    while not over:
        mcords = pygame.Vector2(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_s:
                    cutting = not cutting
                elif event.key == pygame.K_w:
                    addNode(False)
                elif event.key == pygame.K_d:
                    addNode(True)
                elif event.key == pygame.K_a:
                    invertNode()
                elif event.key == pygame.K_LSHIFT:
                    selectNode()

        if cutting:
            for stick in sticks:
                stcenter = pygame.Vector2((stick.node1.pos[0] + stick.node2.pos[0])/2, (stick.node1.pos[1] + stick.node2.pos[1])/2)
                if mcords.distance_to(stcenter) < 10:
                    sticks.pop(sticks.index(stick))

        if not paused:
            simulate(points, sticks)
        drawWindow(WIN, points, sticks)
        drawIterations += 1
