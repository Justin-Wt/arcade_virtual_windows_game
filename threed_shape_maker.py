from pyglet.math import Mat4, Vec3, Vec4


class ThreeD_Cube:
    def __init__(self, x, y, z, color):
        x = x * 4
        y = y
        z = z * 4
        self.vertices = [
            (x - 2, y - 2, z - 2),
            (x + 2, y - 2, z - 2),
            (x + 2, y + 2, z - 2),
            (x - 2, y + 2, z - 2),
            (x - 2, y - 2, z + 2),
            (x + 2, y - 2, z + 2),
            (x + 2, y + 2, z + 2),
            (x - 2, y + 2, z + 2),
        ]
        self.faces = [
            (0, 1, 2, 3),  # back
            (4, 5, 6, 7),  # front
            (0, 1, 5, 4),  # bottom
            (2, 3, 7, 6),  # top
            (1, 2, 6, 5),  # right
            (0, 3, 7, 4),  # left
        ]
        self.colors = [
            color,
            color,
            color,
            color,
            color,
            color,
        ]

        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

    def draw_cube(
        self, width, height, up_rotation, side_rotation, walk, up_moves, left_moves
    ):
        cube_color = []
        cube_outline = []
        rotation = Mat4.from_rotation(up_rotation, Vec3(1, 0, 0)) @ Mat4.from_rotation(
            side_rotation * 0.7, Vec3(0, 1, 0)
        )

        transform = rotation

        projected = []

        for vertex in self.vertices:
            v = Vec4(vertex[0], vertex[1], vertex[2], 1)

            transformed = transform @ v

            # Basic perspective
            z = transformed.z + walk
            if z < 0.1:
                z = 0.1

            factor = 300 / z if z != 0 else 1

            x = transformed.x * factor + width / 2 + left_moves
            y = transformed.y * factor + height / 2 + up_moves

            projected.append((x, y))
        face_depth = []

        for i, face in enumerate(self.faces):

            avg_z = 0
            points = []

            for vertex_index in face:

                x, y, z = self.vertices[vertex_index]

                v = Vec4(x, y, z, 1)

                transformed = transform @ v

                avg_z += transformed.z

                points.append(projected[vertex_index])

            avg_z /= 4

            face_depth.append((avg_z, points, self.colors[i]))

        # Draw farthest faces first
        face_depth.sort(reverse=True)

        for depth, points, color in face_depth:

            cube_color.append((depth, points, color))

        # Draw cube wireframe
        for edge in self.edges:
            p1 = projected[edge[0]]
            p2 = projected[edge[1]]

            cube_outline.append((p1[0], p1[1], p2[0], p2[1], (255, 255, 255), 2))
        return cube_color, cube_outline
