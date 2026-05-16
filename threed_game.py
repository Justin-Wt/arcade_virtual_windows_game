# 6 hrs
import math
import arcade
from threed_shape_maker import ThreeD_Cube
import random
import trimesh
import open3d as o3d
import numpy as np
import moderngl

WIDTH = 1280
HEIGHT = 720


def trimesh_to_o3d(mesh):
    o3d_mesh = o3d.geometry.TriangleMesh()

    o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
    o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)

    o3d_mesh.compute_vertex_normals()
    return o3d_mesh


def simplify_mesh(mesh, target_triangles=3000):
    o3d_mesh = trimesh_to_o3d(mesh)

    simplified = o3d_mesh.simplify_quadric_decimation(target_triangles)

    simplified.compute_vertex_normals()

    return simplified


def o3d_to_trimesh(o3d_mesh):
    vertices = np.asarray(o3d_mesh.vertices)
    faces = np.asarray(o3d_mesh.triangles)

    import trimesh

    return trimesh.Trimesh(vertices=vertices, faces=faces)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade 3D")
        arcade.set_background_color(arcade.color.BLACK)
        self.cube = []
        for i in range(1, 9):
            for j in range(1, 9):
                cube = ThreeD_Cube(
                    i,
                    1,
                    j,
                    (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    ),
                )
                self.cube.append(cube)
        self.up_rotation = 0
        self.side_rotation = 0
        self.up_moves = 0
        self.left_moves = 0
        self.walk = 10
        # 3D model loading
        self.model = trimesh.load("assets/3D Models/Arlecchino.glb")
        if isinstance(self.model, trimesh.Scene):
            self.model = trimesh.util.concatenate(tuple(self.model.geometry.values()))

        # simplify with Open3D
        o3d_mesh = trimesh_to_o3d(self.model)
        o3d_mesh = o3d_mesh.simplify_quadric_decimation(5000)
        o3d_mesh.compute_vertex_normals()

        self.model = o3d_to_trimesh(o3d_mesh)
        self.model.apply_scale(1.0 / self.model.scale)
        self.model.apply_translation(-self.model.centroid)
        self.vertices = self.model.vertices
        self.faces = self.model.faces
        self.base_vertices = self.model.vertices.copy()

        # OpenGL context for future use (e.g., shaders)
        self.gl = moderngl.get_context()
        self.gl.enable(moderngl.DEPTH_TEST)
        self.program = self.gl.program(
            vertex_shader="""
                #version 330
                in vec3 in_position;
                in vec3 in_color;
                out vec3 v_color;
                uniform float rot_y;
                uniform float rot_x;
                uniform float zoom;
                void main() {
                    vec3 pos = in_position;
                    float cy = cos(rot_y);
                    float sy = sin(rot_y);
                    pos = vec3(
                        pos.x * cy - pos.z * sy,
                        pos.y,
                        pos.x * sy + pos.z * cy
                    );
                    float cx = cos(rot_x);
                    float sx = sin(rot_x);
                    pos = vec3(
                        pos.x,
                        pos.y * cx - pos.z * sx,
                        pos.y * sx + pos.z * cx
                    );
                    float z = pos.z + 5.0;
                    gl_Position = vec4(
                        pos.x / z,
                        pos.y / z,
                        pos.z * 0.1,
                        1.0+zoom
                    );
                    v_color = in_color;
                }
            """,
            fragment_shader="""
                #version 330
                in vec3 v_color;
                out vec4 fragColor;
                void main() {
                    fragColor = vec4(v_color, 1.0);
                }
            """,
        )
        gpu_data = []

        for face in self.faces:
            for idx in face:
                v = self.vertices[idx]

                c = self.model.visual.vertex_colors[idx]

                gpu_data.extend(
                    [
                        v[0],
                        v[1],
                        v[2],
                        c[0] / 255.0,
                        c[1] / 255.0,
                        c[2] / 255.0,
                    ]
                )

        gpu_data = np.array(gpu_data, dtype="f4")
        self.vbo = self.gl.buffer(gpu_data.tobytes())
        self.vao = self.gl.vertex_array(
            self.program, [(self.vbo, "3f 3f", "in_position", "in_color")]
        )

    def transform_vertex(v, rotation_matrix, camera_matrix):
        v = rotation_matrix @ v
        v = camera_matrix @ v
        return v

    def project(self, v):
        x, y, z = v
        distance = 5
        scale = 400

        z += distance
        if z == 0:
            z = 0.001

        factor = scale / z
        screen_x = x * factor + WIDTH // 2
        screen_y = y * factor + HEIGHT // 2

        return screen_x, screen_y

    def rotate_y(self, v, angle):
        x, y, z = v
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        return (x * cos_a - z * sin_a, y, x * sin_a + z * cos_a)

    def rotate_x(self, v, angle):
        x, y, z = v
        c = math.cos(angle)
        s = math.sin(angle)

        return (x, y * c - z * s, y * s + z * c)

    def on_draw(self):
        self.clear()
        self.program["rot_y"] = self.side_rotation
        self.program["rot_x"] = self.up_rotation
        self.program["zoom"] = self.walk

        self.vao.render(moderngl.TRIANGLES)
        self.gl.disable(moderngl.DEPTH_TEST)
        all_faces = []
        all_lines = []
        for cube in self.cube:
            cube_color, cube_outline = cube.draw_cube(
                WIDTH,
                HEIGHT,
                self.up_rotation,
                self.side_rotation,
                self.walk,
                self.up_moves,
                self.left_moves,
            )
            all_faces.extend(cube_color)
            all_lines.extend(cube_outline)
        all_faces.sort(key=lambda item: item[0], reverse=True)
        for x1, y1, x2, y2, color, width in all_lines:
            arcade.draw_line(x1, y1, x2, y2, color, width)
        for _, points, color in all_faces:
            arcade.draw_polygon_filled(points, color)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & arcade.MOUSE_BUTTON_LEFT:
            self.up_rotation += dy * 0.01
            self.side_rotation -= dx * 0.01
        elif buttons & arcade.MOUSE_BUTTON_RIGHT:
            self.up_moves += dy * 1
            self.left_moves += dx * 1

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.walk -= scroll_y * 0.5

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.walk -= 0.5
        elif key == arcade.key.S:
            self.walk += 0.5
        if key == arcade.key.A:
            self.side_rotation += 0.1
        elif key == arcade.key.D:
            self.side_rotation -= 0.1


window = Game()
arcade.run()
