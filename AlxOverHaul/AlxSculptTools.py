import bpy
import bmesh

class Alx_OT_Sculpt_ConditionMasking(bpy.types.Operator):
    """"""

    bl_label = "Sculpt Mask By Condition"
    bl_idname = "alx.operator_sculpt_mask_by_condition"

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

        selection = set(vert.index for vert in self.ContextBMesh.verts if (vert.select == True))

        sculpt_mask_layer = self.ContextBMesh.verts.layers.float.get(".sculpt_mask")
        if (sculpt_mask_layer is None):
            sculpt_mask_layer = self.ContextBMesh.verts.layers.float.new(".sculpt_mask")

        for vert in selection:
            self.ContextBMesh.verts[vert][sculpt_mask_layer] = 1.0

        bmesh.update_edit_mesh(self.ContextMesh)

        return {"FINISHED"}