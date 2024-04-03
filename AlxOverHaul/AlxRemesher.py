import bpy
import bmesh
import mathutils



class Alx_OT_RemeshObject(bpy.types.Operator):
    """"""

    bl_label = "Tool - Remesh Object"
    bl_idname = "alx.operator_remesh_object"
    bl_options = {"REGISTER", "UNDO"}

    ContextBmesh : bmesh.types.BMesh = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")
    
    def execute(self, context: bpy.types.Context):
        if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
            self.ContextMesh = context.edit_object.data
            if (self.ContextBmesh is None) or (not self.ContextBmesh.is_valid):
                self.ContextBmesh = bmesh.from_edit_mesh(self.ContextMesh)

        if (self.ContextBmesh is not None):
            vert : bmesh.types.BMVert
            edge : bmesh.types.BMEdge
            face : bmesh.types.BMFace



            for edge in self.ContextBmesh.edges:
                vert_co_1 = edge.verts[0].co
                vert_co_2 = edge.verts[1].co

                delta_x = (vert_co_1[0] - vert_co_2[0])
                delta_y = (vert_co_1[1] - vert_co_2[1])
                delta_z = (vert_co_1[2] - vert_co_2[2])

                delta_vector = mathutils.Vector((delta_x, delta_y, delta_z))

                print(delta_vector)
            # edge_length = [math.sqrt(((edge.verts[0].co[0] - edge.verts[1].co[0])*(edge.verts[0].co[0] - edge.verts[1].co[0])) + ((edge.verts[0].co[1] - edge.verts[1].co[1])*(edge.verts[0].co[1] - edge.verts[1].co[1])) + ((edge.verts[0].co[2] - edge.verts[1].co[2])*(edge.verts[0].co[2] - edge.verts[1].co[2]))) for edge in self.ContextBmesh.edges]
            # print("edge l min", min(edge_length), "edge l max", max(edge_length))



        return {"FINISHED"}