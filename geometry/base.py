from core.attribute import Attribute
from typing import Dict, TypeVar

TGeometry = TypeVar('TGeometry', 'Geometry')

class Geometry:
    def __init__(self) -> None:
        self.attributes: Dict[str, Attribute] = {}
        self.vertex_count: int = 0

    def add_attribute(self, data_type, var_name, data):
        self.attributes[var_name] = Attribute(data_type, data)

    def count_vertices(self):
        attrib = list(self.attributes.values())[0]
        self.vertex_count = len(attrib.data)

    def apply_matrix(self, matrix, var_name="vertexPosition"):
        old_pos_data = self.attributes[var_name].data
        new_pos_data = []

        for pos in old_pos_data:
            new_pos = pos.copy()
            # append 1 so we can perform Mat44 operations
            new_pos.append(1)
            new_pos = matrix @ new_pos
            new_pos = list(new_pos[0:3])
            new_pos_data.append(new_pos)
        
        self.attributes[var_name].data = new_pos_data
        self.attributes[var_name].upload_data()

    def merge(self, other: TGeometry):
        for var_name, attrib_obj in self.attributes.items():
            other_geom_attrib = other.attributes.get(var_name)
            if other_geom_attrib is None:
                raise Exception(f"Error when merging geometry: attribute '{var_name}' does not exist in other geometry.")
            attrib_obj.data += other_geom_attrib.data
            attrib_obj.upload_data()

        self.count_vertices()