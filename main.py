import pygame
from math import sin, cos, tan, radians
import copy
import time

WIDTH, HEIGHT = 1000, 1000
OFFSET = (WIDTH // 2, HEIGHT // 2)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D rendering")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
scalar = 50
rotation_theta = time.time()

near = 0.1
far = 1000
aspect_ratio = WIDTH / HEIGHT
fov = 1 / tan(radians(100 / 2))

rot_x_speed = .3
rot_y_speed = .1
rot_z_speed = .2

camera_cords = (0, 0, 0)


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vector_list = [[self.x], [self.y], [self.z]]


class Triangle:
    def __init__(self, points_1, points_2, points_3, color):
        self.color = color
        self.v1 = Vector(points_1[0], points_1[1], points_1[2])
        self.v2 = Vector(points_2[0], points_2[1], points_2[2])
        self.v3 = Vector(points_3[0], points_3[1], points_3[2])
        self.vectors = (self.v1, self.v2, self.v3)


class Cube:
    def __init__(self):
        self.mesh = [
            # NORTH
            Triangle((-1.0, 1.0,  -1.0), (1.0, -1.0, -1.0), (-1.0,  -1.0,  -1.0), WHITE),
            Triangle((-1.0, 1.0,  -1.0), (1.0, 1.0,  -1.0), (1.0,   -1.0,  -1.0), WHITE),

            # EAST
            Triangle((1.0,  1.0,  -1.0), (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), WHITE),
            Triangle((1.0,  1.0,  -1.0), (1.0, 1.0,  1.0), (1.0, -1.0,  1.0), WHITE),

            # SOUTH
            Triangle((1.0,  1.0,  1.0), (-1.0, -1.0, 1.0), (1.0,  -1.0,  1.0), WHITE),
            Triangle((1.0,  1.0,  1.0), (-1.0, 1.0,  1.0), (-1.0, -1.0, 1.0), WHITE),

            # WEST
            Triangle((-1.0, 1.0,  1.0), (-1.0, -1.0, -1.0), (-1.0, -1.0,  1.0), WHITE),
            Triangle((-1.0, 1.0,  1.0), (-1.0, 1.0,  -1.0), (-1.0, -1.0, -1.0), WHITE),

            # TOP
            Triangle((-1.0, 1.0,  1.0), (1.0,  1.0, -1.0), (-1.0, 1.0, -1.0), WHITE),
            Triangle((-1.0, 1.0,  1.0), (1.0,  1.0,  1.0), (1.0,  1.0, -1.0), WHITE),

            # BOTTOM
            Triangle((-1.0, -1.0,  -1.0), (1.0,  -1.0, 1.0), (1.0, -1.0, 1.0), WHITE),
            Triangle((-1.0, -1.0,  -1.0), (-1.0, -1.0, 1.0), (1.0,  -1.0,  1.0), WHITE)
        ]


def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix

    else:
        print("Columns of the first matrix must be equal to the rows of the second matrix")
        return None


def multiply_vector(vector, matrix_b):
    out_x = vector.x * matrix_b[0][0] + vector.y * matrix_b[1][0] + vector.z * matrix_b[2][0]
    out_y = vector.x * matrix_b[0][1] + vector.y * matrix_b[1][1] + vector.z * matrix_b[2][1]
    out_z = vector.x * matrix_b[0][2] + vector.y * matrix_b[1][2] + vector.z * matrix_b[2][2]
    return out_x, out_y, out_z


def scale(triangle):
    scaled_axis = [[], [], []]
    for index, vector in enumerate([triangle.v1, triangle.v2, triangle.v3]):
        scaled_axis[index].append(vector.x * scalar + OFFSET[0])
        scaled_axis[index].append(vector.y * -scalar + OFFSET[1])
        scaled_axis[index].append(vector.z)
    return Triangle((scaled_axis[0][0], scaled_axis[0][1], scaled_axis[0][2]), (scaled_axis[1][0], scaled_axis[1][1], scaled_axis[1][2]), (scaled_axis[2][0], scaled_axis[2][1], scaled_axis[2][1]))


def draw_triangle(x_1, y_1, x_2, y_2, x_3, y_3, color):
    pygame.draw.line(WINDOW, color, (x_1, y_1), (x_2, y_2))
    pygame.draw.line(WINDOW, color, (x_2, y_2), (x_3, y_3))
    pygame.draw.line(WINDOW, color, (x_3, y_3), (x_1, y_1))


def blit():
    rot_z_matrix = [[cos(rotation_theta * rot_z_speed), -sin(rotation_theta * rot_z_speed), 0],
                    [sin(rotation_theta * rot_z_speed), cos(rotation_theta * rot_z_speed), 0],
                    [0, 0, 1]]

    rot_x_matrix = [[1, 0, 0],
                    [0, cos(rotation_theta * rot_x_speed), -sin(rotation_theta * rot_x_speed)],
                    [0, sin(rotation_theta * rot_x_speed), cos(rotation_theta * rot_x_speed)]]

    rot_y_matrix = [[cos(rotation_theta * rot_y_speed), 0, -sin(rotation_theta * rot_y_speed)],
                    [0, 1, 0],
                    [sin(rotation_theta * rot_y_speed), 0, cos(rotation_theta * rot_y_speed)]]
    WINDOW.fill(BLACK)
    for triangle in square.mesh:
        triangle_copy = copy.deepcopy(triangle)
        for vector in triangle_copy.vectors:
            rotated_2d = matrix_multiplication(rot_z_matrix, vector.vector_list)
            rotated_2d = matrix_multiplication(rot_x_matrix, rotated_2d)
            rotated_2d = matrix_multiplication(rot_y_matrix, rotated_2d)
            rotated_2d.append([1])

            distance = 3
            z = 1 / (distance - rotated_2d[2][0])
            projection_matrix = [[aspect_ratio * fov, 0, 0, 0],
                                 [0, fov, 0, 0],
                                 [0, 0, distance / (distance - rotated_2d[2][0]), 1],
                                 [0, 0, 0, -(distance * rotated_2d[2][0]) / (distance - rotated_2d[2][0])]]

            vector.vector_list[2][0] += 3
            rotated_2d[0][0] /= z
            rotated_2d[1][0] /= z
            projected_2d = matrix_multiplication(projection_matrix, rotated_2d)
            vector.vector_list[0][0] = int(projected_2d[0][0] * scalar) + OFFSET[0]
            vector.vector_list[1][0] = int(projected_2d[1][0] * scalar) + OFFSET[1]

            pygame.draw.circle(WINDOW, WHITE, (vector.vector_list[0][0], vector.vector_list[1][0]), 10)
        draw_triangle(triangle_copy.v1.vector_list[0][0], triangle_copy.v1.vector_list[1][0],
                      triangle_copy.v2.vector_list[0][0], triangle_copy.v2.vector_list[1][0],
                      triangle_copy.v3.vector_list[0][0], triangle_copy.v3.vector_list[1][0], WHITE)
    pygame.display.update()


square = Cube()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
    blit()
    rotation_theta = time.time()
