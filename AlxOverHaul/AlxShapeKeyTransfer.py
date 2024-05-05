import math

import bpy
import bmesh
from mathutils import kdtree

class Alx_OT_Shapekey_TransferShapekeysToTarget(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_shapekey_transfer_shapekeys_to_target"
    bl_options = {"REGISTER", "UNDO"}


    source_mesh : bpy.types.Mesh = None
    source_bmesh : bmesh.types.BMesh = None

    target_mesh : bpy.types.Mesh = None
    target_bmesh : bmesh.types.BMesh = None

    shapekey_source_kdtree : kdtree.KDTree
    shapekey_target_kdtree : kdtree.KDTree

    def auto_retrieve_shapekeys(self, context: bpy.types.Context):
        unique_shapekey_set = set()
        unique_shapekey_set.add(("NONE", "none", ""))

        if (len(context.selectable_objects) != 0):
            [unique_shapekey_set.add((shapekey.name, shapekey.name, "")) for shapekey in context.window_manager.alx_session_properties.shapekey_transfer_source_object.data.shape_keys.key_blocks]

        return unique_shapekey_set

    shapekey_source_name : bpy.props.EnumProperty(name="source shapekeys", items=auto_retrieve_shapekeys) #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True


    def execute(self, context: bpy.types.Context):
        properties = context.window_manager.alx_session_properties

        if (properties.shapekey_transfer_source_object is not None) and (properties.shapekey_transfer_source_object.type == "MESH"):
            source_object : bpy.types.Object = properties.shapekey_transfer_source_object
            self.source_mesh : bpy.types.Mesh = source_object.data

            if (self.source_bmesh is None) or (not self.source_bmesh.is_valid):
                if (self.source_bmesh is None):
                    self.source_bmesh = bmesh.new()
                self.source_bmesh.from_mesh(self.source_mesh)

            self.source_bmesh.verts.ensure_lookup_table()
            self.source_bmesh.edges.ensure_lookup_table()
            self.source_bmesh.faces.ensure_lookup_table()


            source_tree_size = len(self.source_bmesh.verts)
            self.shapekey_source_kdtree = kdtree.KDTree(source_tree_size)

            for index, vert in enumerate(self.source_bmesh.verts):
                self.shapekey_source_kdtree.insert(vert.co, index)

            self.shapekey_source_kdtree.balance()

        if (properties.shapekey_transfer_target_object is not None) and (properties.shapekey_transfer_target_object.type == "MESH"):
            target_object : bpy.types.Object = properties.shapekey_transfer_target_object
            self.target_mesh : bpy.types.Mesh = target_object.data

            if (self.target_bmesh is None) or (not self.target_bmesh.is_valid):
                if (self.target_bmesh is None):
                    self.target_bmesh = bmesh.new()
                self.target_bmesh.from_mesh(self.target_mesh)

            self.target_bmesh.verts.ensure_lookup_table()
            self.target_bmesh.edges.ensure_lookup_table()
            self.target_bmesh.faces.ensure_lookup_table()


            target_tree_size = len(self.target_bmesh.verts)
            self.shapekey_target_kdtree = kdtree.KDTree(target_tree_size)

            for index, vert in enumerate(self.target_bmesh.verts):
                self.shapekey_target_kdtree.insert(vert.co, index)

            self.shapekey_target_kdtree.balance()

        if (self.shapekey_source_kdtree is not None) and (self.shapekey_target_kdtree is not None):

            if (self.shapekey_source_name not in ["Basis", ""]):
                shapekey_layer = self.source_bmesh.verts.layers.shape.get(self.shapekey_source_name)

                shape_key_co_set = dict()

                for source_vert in self.source_bmesh.verts:
                    original_co = source_vert.co
                    co, target_index, distance = self.shapekey_target_kdtree.find(original_co)
                    
                    vert_co = source_vert[shapekey_layer]
                    shape_key_co_set.update({target_index : vert_co})

                

                if (self.target_bmesh.verts.layers.shape.get(self.shapekey_source_name) is None):
                    properties.shapekey_transfer_target_object.shape_key_add(name=self.shapekey_source_name)

                self.target_bmesh.free()

                target_object : bpy.types.Object = properties.shapekey_transfer_target_object
                self.target_mesh : bpy.types.Mesh = target_object.data

                if (self.target_bmesh is None) or (not self.target_bmesh.is_valid):
                    self.target_bmesh = bmesh.new()
                    self.target_bmesh.from_mesh(self.target_mesh)

                self.target_bmesh.verts.ensure_lookup_table()
                self.target_bmesh.edges.ensure_lookup_table()
                self.target_bmesh.faces.ensure_lookup_table()

                self.target_shapekey_layer = self.target_bmesh.verts.layers.shape.get(self.shapekey_source_name)

                if (self.target_shapekey_layer is not None):
                    for target_index_key in shape_key_co_set:
                        self.target_bmesh.verts[target_index_key][self.target_shapekey_layer] = shape_key_co_set[target_index_key]
                else:
                    self.report({"WARNING"}, "Layer is not present")

            self.target_bmesh.to_mesh(self.target_mesh)

        return {"FINISHED"}
    

    def draw(self, context: bpy.types.Context):
        properties = context.window_manager.alx_session_properties 

        self.layout.prop(properties, "shapekey_transfer_source_object", text="source")
        self.layout.prop(properties, "shapekey_transfer_target_object", text="target")
        self.layout.prop(self, "shapekey_source_name", text="source")
        

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)