import pygame
import math
import copy
import time

pygame.init()
WIDTH, HEIGHT = 1000, 1000
pygame.display.set_caption("3D render")
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


f_near = 0.1
f_far = 1000
fov = 90
aspect_ratio = HEIGHT / WIDTH
fov_rad = 1 / math.tan(math.radians(fov * 0.5))


projection_matrix = [[0.0 for _ in range(4)] for _ in range(4)]
projection_matrix[0][0] = aspect_ratio * fov_rad
projection_matrix[1][1] = fov_rad
projection_matrix[2][2] = f_far / (f_far - f_near)
projection_matrix[3][2] = (-f_far * f_near) / (f_far - f_near)
projection_matrix[2][3] = 1
projection_matrix[3][3] = 0.0


def multiply_matrix(vector, matrix_b):
    output_x = vector.x * matrix_b[0][0] + vector.y * matrix_b[1][0] + vector.z * matrix_b[2][0] + matrix_b[3][0]
    output_y = vector.x * matrix_b[0][1] + vector.y * matrix_b[1][1] + vector.z * matrix_b[2][1] + matrix_b[3][1]
    output_z = vector.x * matrix_b[0][2] + vector.y * matrix_b[1][2] + vector.z * matrix_b[2][2] + matrix_b[3][2]
    w = vector.x * matrix_b[0][3] + vector.y * matrix_b[1][3] + vector.z * matrix_b[2][3] + matrix_b[3][3]

    if w:
        output_x = output_x / w
        output_y = output_y / w
        output_z = output_z / w
    return Vec3d(output_x, output_y, output_z)


class Matrix:
    def __init__(self):
        pass


class Vec3d:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z


class Triangle:
    def __init__(self, v1=None, v2=None, v3=None, color=WHITE):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.color = color


class MeshCube:
    def __init__(self):
        self.triangles = [
            # SOUTH
            Triangle(Vec3d(0, 0, 0), Vec3d(0, 1, 0), Vec3d(1, 1, 0)),
            Triangle(Vec3d(0, 0, 0), Vec3d(1, 1, 0), Vec3d(1, 0, 0)),

            # EAST
            Triangle(Vec3d(1, 0, 0), Vec3d(1, 1, 0), Vec3d(1, 1, 1)),
            Triangle(Vec3d(1, 0, 0), Vec3d(1, 1, 1), Vec3d(1, 0, 1)),

            # NORTH
            Triangle(Vec3d(1, 0, 1), Vec3d(1, 1, 1), Vec3d(0, 1, 1)),
            Triangle(Vec3d(1, 0, 1), Vec3d(0, 1, 1), Vec3d(0, 0, 1)),

            # WEST
            Triangle(Vec3d(0, 0, 1), Vec3d(0, 1, 1), Vec3d(0, 1, 0)),
            Triangle(Vec3d(0, 0, 1), Vec3d(0, 1, 0), Vec3d(0, 0, 0)),

            # TOP
            Triangle(Vec3d(0, 1, 0), Vec3d(0, 1, 1), Vec3d(1, 1, 1)),
            Triangle(Vec3d(0, 1, 0), Vec3d(1, 1, 1), Vec3d(1, 1, 0)),

            # BOTTOM
            Triangle(Vec3d(1, 0, 1), Vec3d(0, 0, 1), Vec3d(0, 0, 0)),
            Triangle(Vec3d(1, 0, 1), Vec3d(0, 0, 0), Vec3d(1, 0, 0))
        ]


def rotate_triangle(triangle):
    matrix_rot_z[0][0] = math.cos(theta)
    matrix_rot_z[0][1] = math.sin(theta)
    matrix_rot_z[1][0] = -(math.sin(theta))
    matrix_rot_z[1][1] = math.cos(theta)
    matrix_rot_z[2][2] = 1
    matrix_rot_z[3][3] = 1

    matrix_rot_x[0][0] = 1
    matrix_rot_x[1][1] = math.cos(theta * 0.5)
    matrix_rot_x[1][2] = math.sin(theta * 0.5)
    matrix_rot_x[2][1] = -(math.sin(theta * 0.5))
    matrix_rot_x[2][2] = math.cos(theta * 0.5)
    matrix_rot_x[3][3] = 1

    tri_rotated_z = Triangle(
        multiply_matrix(triangle.v1, matrix_rot_z),
        multiply_matrix(triangle.v2, matrix_rot_z),
        multiply_matrix(triangle.v3, matrix_rot_z),
        color=triangle.color
    )
    tri_rotated_x = Triangle(
        multiply_matrix(tri_rotated_z.v1, matrix_rot_x),
        multiply_matrix(tri_rotated_z.v2, matrix_rot_x),
        multiply_matrix(tri_rotated_z.v3, matrix_rot_x),
        color=tri_rotated_z.color
    )
    return tri_rotated_x


def draw_triangle(x_1, y_1, x_2, y_2, x_3, y_3, color):
    pygame.draw.line(WINDOW, color, (x_1, y_1), (x_2, y_2))
    pygame.draw.line(WINDOW, color, (x_2, y_2), (x_3, y_3))
    pygame.draw.line(WINDOW, color, (x_3, y_3), (x_1, y_1))


def draw_stuff():
    WINDOW.fill(BLACK)
    for triangle in mesh_cube.triangles:
        copied_tri = copy.deepcopy(triangle)
        tri_rotated = rotate_triangle(copied_tri)

        tri_translated = tri_rotated

        tri_translated.v1.z = triangle.v1.z + 2
        tri_translated.v2.z = triangle.v2.z + 2
        tri_translated.v3.z = triangle.v3.z + 2

        tri_projected = Triangle(
            multiply_matrix(tri_translated.v1, projection_matrix),
            multiply_matrix(tri_translated.v2, projection_matrix),
            multiply_matrix(tri_translated.v3, projection_matrix),
            color=tri_translated.color
        )

        tri_projected.v1.x += 1
        tri_projected.v1.y += 1
        tri_projected.v2.x += 1
        tri_projected.v2.y += 1
        tri_projected.v3.x += 1
        tri_projected.v3.y += 1

        tri_projected.v1.x *= 0.5 * WIDTH
        tri_projected.v1.y *= 0.5 * WIDTH
        tri_projected.v2.x *= 0.5 * WIDTH
        tri_projected.v2.y *= 0.5 * WIDTH
        tri_projected.v3.x *= 0.5 * WIDTH
        tri_projected.v3.y *= 0.5 * WIDTH

        draw_triangle(tri_projected.v1.x, tri_projected.v1.y, tri_projected.v2.x, tri_projected.v2.y, tri_projected.v3.x, tri_projected.v3.y, tri_projected.color)

    pygame.display.flip()


mesh_cube = MeshCube()
elapsed_time = time.time()
theta = 0
matrix_rot_z = [[0. for _ in range(4)] for _ in range(4)]
matrix_rot_x = [[0. for _ in range(4)] for _ in range(4)]

rotate_event = pygame.USEREVENT + 0
pygame.time.set_timer(rotate_event, 1)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                pygame.display.quit()
        if event.type == rotate_event:
            theta = 1 * elapsed_time
    draw_stuff()
    elapsed_time = time.time()