import bpy
import bmesh


class Alx_OT_Armature_StripHairRigify(bpy.types.Operator):
    """"""

    bl_label = "VX - Group By Seams"
    bl_idname = "alx.operator_vx_group_by_seam"
    bl_options = {"REGISTER", "UNDO"}

    ContextMesh : bpy.types.Mesh = None
    ContextBMesh : bmesh.types.BMesh = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")
    
    def execute(self, context: bpy.types.Context):
        if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
            self.ContextMesh = context.edit_object.data
            if (self.ContextBMesh is None) or (not self.ContextBMesh.is_valid):
                self.ContextBMesh = bmesh.from_edit_mesh(self.ContextMesh)

            self.ContextBMesh.verts.ensure_lookup_table()
            self.ContextBMesh.edges.ensure_lookup_table()
            self.ContextBMesh.faces.ensure_lookup_table()

            vert : bmesh.types.BMVert
            edge : bmesh.types.BMEdge
            face : bmesh.types.BMFace
            loop : bmesh.types.BMLoop

