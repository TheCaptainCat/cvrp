import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from cvrp import Builder
from cvrp.graphics import Graph


def main():
    pygame.init()
    display = (1200, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(-50.0, -50.0, -150)
    vertices = Builder('../data/data03.csv').build()
    graph = Graph(vertices)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        graph.draw()
        pygame.display.flip()


main()
