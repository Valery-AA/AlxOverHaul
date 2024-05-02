import bpy
from mathutils import Matrix, Vector

import bmesh


class Alx_OT_Object_UnlockedQOrigin(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_object_unlocked_q_origin"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    origin_set_mode : bpy.props.EnumProperty(name="", default="CURSOR_TO_WORLD",
        items={
        ("CURSOR_TO_WORLD", "cursor to world", "", 1),
        ("ORIGIN_TO_SELECTION", "origin to selection", "", 1<<1)
        }) #type:ignore

    ContextMesh : bpy.types.Mesh = None
    ContextBMesh : bmesh.types.BMesh = None


    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area.type == "VIEW_3D") and (context.object is not None)


    def execute(self, context):
        if (self.origin_set_mode == "CURSOR_TO_WORLD"):
            context.scene.cursor.location = (0.0, 0.0, 0.0)
            return {"FINISHED"}

        if (self.origin_set_mode == "ORIGIN_TO_SELECTION"):
            if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
                self.ContextMesh = context.edit_object.data
                if (self.ContextBMesh is None) or (not self.ContextBMesh.is_valid):
                    self.ContextBMesh = bmesh.from_edit_mesh(self.ContextMesh)

                self.ContextBMesh.verts.ensure_lookup_table()
                self.ContextBMesh.edges.ensure_lookup_table()
                self.ContextBMesh.faces.ensure_lookup_table()

                if (self.ContextBMesh is not None):
                    selection = [vert.index for vert in self.ContextBMesh.verts if (vert.select == True)]

                    object_mesh : bpy.types.Mesh = context.object.data
                    object_Wmatrix : Matrix = context.object.matrix_world

                    vertex_co_set = [object_Wmatrix @ self.ContextBMesh.verts[vert_index].co for vert_index in selection]

                    average_co = sum(vertex_co_set, Vector()) / len(vertex_co_set)

                    pre_origin_matrix = object_Wmatrix.copy()
                    object_Wmatrix.translation = average_co

                    _mode = context.mode if (context.mode[0:4] != "EDIT") else "EDIT" if (context.mode[0:4] == "EDIT") else "OBJECT"
                    bpy.ops.object.mode_set(mode="OBJECT")
                    object_mesh.transform(pre_origin_matrix @ Matrix.Translation(-average_co))
                    bpy.ops.object.mode_set(mode=_mode)
            return {"FINISHED"}

        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)