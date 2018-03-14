import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

from cvrp import Builder
from cvrp.graphics import Graphics
from cvrp.logic import Graph
from cvrp.logic.algorithm import Tabu


def draw_text(position, v_color, text_string):
    font = pygame.font.Font(None, 25)
    text_surface = font.render(text_string, True, v_color, (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def main():
    pygame.init()
    display = (1200, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 150.0)
    glTranslatef(-50.0, -50.0, -150)
    vertices = Builder('../data/data03.csv').build()
    graph = Graph(vertices, 100)
    graph.random_routes()
    graphics = Graphics(graph)
    tabu = Tabu(graph, 5, 200)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        graphics.draw()

        v1, v2 = tabu.find_best_permutation()
        graph.swap_vertices(v1, v2)

        i = 0
        for path in graphics.paths:
            draw_text((-30, (100 - i * 3), 0), (path.color[0] * 255, path.color[1] * 255, path.color[2] * 255, 255),
                      ("Route %d: %.2f" % (i, path.route.distance)))
            i += 1
        draw_text((-30, (100 - i * 3), 0), (255, 255, 255, 255), ("Total distance: %d" % graph.distance))

        pygame.display.flip()


main()
