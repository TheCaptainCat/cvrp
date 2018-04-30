import copy
import pygame
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

from cvrp import Builder
from cvrp.console import Console
from cvrp.graphics import Graphics
from cvrp.logic import Graph


def draw_text(position, v_color, text_string):
    font = pygame.font.Font(None, 25)
    text_surface = font.render(text_string, True, v_color, (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def main():
    vertices = Builder(Console.file()).build()
    graph = Graph(vertices, 100)
    graph.set_random_routes()
    graphics = Graphics(graph)
    graph.algorithm = Console.algorithm(graph)

    pygame.init()
    display = (1200, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(-50.0, -50.0, -150)

    min_distance = graph.distance
    min_graph = copy.deepcopy(graph)
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        if not loop:
            break
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        graphics.draw()

        i = 0
        for i in range(0, len(graph.routes)):
            route = graph.routes[i]
            v_color = graphics.colors[i]
            draw_text((-30, (100 - i * 3), 0), (v_color[0] * 255, v_color[1] * 255, v_color[2] * 255, 255),
                      ("Route %d: %.2f (%d %d)" % (i,
                                                   graph.route_length(i),
                                                   len(route),
                                                   graph.route_quantity(i))))
            i += 1
        draw_text((-30, (100 - i * 3), 0), (255, 255, 255, 255), ("Total distance: %d" % graph.distance))
        i += 1
        if min_distance > graph.distance:
            min_distance = graph.distance
            min_graph = copy.deepcopy(graph)
        draw_text((-30, (100 - i * 3), 0), (255, 255, 255, 255), ("Minimum distance: %d" % min_distance))

        graph.compute_algorithm()

        pygame.display.flip()

    graphics.graph = min_graph
    graph = min_graph

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        graphics.draw()

        i = 0
        for i in range(0, len(graph.routes)):
            route = graph.routes[i]
            v_color = graphics.colors[i]
            draw_text((-30, (100 - i * 3), 0), (v_color[0] * 255, v_color[1] * 255, v_color[2] * 255, 255),
                      ("Route %d: %.2f (%d %d)" % (i,
                                                   graph.route_length(i),
                                                   len(route),
                                                   graph.route_quantity(i))))
            i += 1

        draw_text((-30, (100 - i * 3), 0), (255, 255, 255, 255), ("Final distance: %d" % min_distance))

        pygame.display.flip()


main()
