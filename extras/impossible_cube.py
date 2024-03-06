from core.Object3D import Object3D
from core.mesh import Mesh
from geometry import SphereGeometry, RectangleGeometry, BoxGeometry, PyramidGeometry, CylinderGeometry, EllipsoidGeometry, PrismGeometry
from material.surface import SurfaceMaterial
from core.texture import Texture
from OpenGL.GL import *
from math import pi


class ImpossibleCube(Object3D):
    def __init__(self, object_material=SurfaceMaterial) -> None:
        super().__init__()

        face_geom = RectangleGeometry(width=2, height=2)
        face_properties = {"stencilWrite": True, "baseColor": [1, 1, 1],
                           "stencilFunc": GL_ALWAYS, "stencilZPass": GL_REPLACE, "depthWrite": False, "colorWrite": False}
        object_properties = {"stencilWrite": True,
                             "stencilFunc": GL_EQUAL}

        wall_texture = Texture("wall.webp")

        def generate_walls(face: Mesh, stencil_ref: int):
            material = object_material(wall_texture, properties={
                                       **object_properties, "stencilRef": stencil_ref, "doubleSide": False})
            wall1 = Mesh(RectangleGeometry(width=2, height=2), material)
            wall2 = Mesh(RectangleGeometry(width=2, height=2), material)
            wall3 = Mesh(RectangleGeometry(width=2, height=2), material)
            wall4 = Mesh(RectangleGeometry(width=2, height=2), material)
            wall5 = Mesh(RectangleGeometry(width=2, height=2), material)
            face.add(wall1)
            face.add(wall2)
            face.add(wall3)
            face.add(wall4)
            face.add(wall5)

            if "shininess" in material.uniforms.keys():
                material.uniforms["specularStrength"].data = .01
                material.uniforms["shininess"].data = 0.01

            wall1.translate(1, 0, -1)
            wall1.rotate_y(-pi/2)
            wall2.translate(0, 0, -2)
            wall3.translate(-1, 0, -1)
            wall3.rotate_y(pi/2)
            wall4.translate(0, 1, -1)
            wall4.rotate_x(pi/2)
            wall5.translate(0, -1, -1)
            wall5.rotate_x(-pi/2)

            border_material = SurfaceMaterial(
                {**object_properties, "stencilRef": stencil_ref, "baseColor": [0, 0, 0]})
            border1 = Mesh(RectangleGeometry(
                width=2, height=0.05), border_material)
            border2 = Mesh(RectangleGeometry(
                width=2, height=0.05), border_material)
            border3 = Mesh(RectangleGeometry(
                width=2, height=0.05), border_material)
            border4 = Mesh(RectangleGeometry(
                width=2, height=0.05), border_material)

            face.add(border1)
            face.add(border2)
            face.add(border3)
            face.add(border4)

            border1.translate(0, -1, 0)
            border2.translate(1, 0, 0)
            border2.rotate_z(-pi/2)
            border3.translate(0, 1, 0)
            border4.translate(-1, 0, 0)
            border4.rotate_z(pi/2)

        face1 = Mesh(face_geom, SurfaceMaterial(
            {"stencilRef": 1, **face_properties}))
        object1 = Mesh(SphereGeometry(radius=0.5), object_material(
            properties={"baseColor": [1.0, 0.0, 0.0], "stencilRef": 1, **object_properties}))
        face1.translate(0, 0, 1)
        object1.translate(0, 0, -1)
        face1.add(object1)
        self.add(face1)
        generate_walls(face1, 1)

        face2 = Mesh(face_geom, SurfaceMaterial(
            {"stencilRef": 2, **face_properties}))
        object2 = Mesh(BoxGeometry(), object_material(
            properties={"baseColor": [0, 0, 1], "stencilRef": 2, **object_properties}))
        face2.translate(1, 0, 0)
        face2.rotate_y(pi/2)
        object2.translate(0, 0, -1)
        face2.add(object2)
        self.add(face2)
        generate_walls(face2, 2)

        face3 = Mesh(face_geom, SurfaceMaterial(
            {"stencilRef": 3, **face_properties}))
        object3 = Mesh(PyramidGeometry(width_bottom=0.75), object_material(
            properties={"baseColor": [1, 0, 1], "stencilRef": 3, **object_properties}))
        face3.translate(0, 0, -1)
        face3.rotate_y(pi)
        object3.translate(0, 0, -1)
        face3.add(object3)
        self.add(face3)
        generate_walls(face3, 3)

        face4 = Mesh(face_geom, SurfaceMaterial(
            {"stencilRef": 4, **face_properties}))
        object4 = Mesh(CylinderGeometry(radius=0.5), object_material(
            properties={"baseColor": [1, 1, 0], "stencilRef": 4, **object_properties}))
        face4.translate(-1, 0, 0)
        face4.rotate_y(-pi/2)
        object4.translate(0, 0, -1)
        face4.add(object4)
        self.add(face4)
        generate_walls(face4, 4)

        face5 = Mesh(face_geom, SurfaceMaterial(
            {"stencilRef": 5, **face_properties}))
        object5 = Mesh(EllipsoidGeometry(width=1.25), object_material(
            properties={"baseColor": [0.5, 0.2, 1], "stencilRef": 5, **object_properties}))
        face5.translate(0, 1, 0)
        face5.rotate_x(-pi/2)
        object5.translate(0, 0, -1)
        face5.add(object5)
        self.add(face5)
        generate_walls(face5, 5)

        face6 = Mesh(face_geom, SurfaceMaterial(
            {"stencilRef": 6, **face_properties}))
        object6 = Mesh(PrismGeometry(radius=0.5), object_material(
            properties={"baseColor": [0.2, 1, 0.5], "stencilRef": 6, **object_properties}))
        face6.translate(0, -1, 0)
        face6.rotate_x(pi/2)
        object6.translate(0, 0, -1)
        object6.rotate_x(pi/2)
        face6.add(object6)
        self.add(face6)
        generate_walls(face6, 6)
