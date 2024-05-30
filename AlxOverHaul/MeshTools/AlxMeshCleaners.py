import bpy

class Alx_OT_Mesh_VertexGroup_CleanEmpty(bpy.types.Operator):
    """"""

    bl_label = "Cleaner - Mesh Vertex Group Clean Empty"
    bl_idname = "alx.operator_mesh_vertex_group_clean_empty"

    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.object is not None) and (context.object.type == "MESH")
    
    def execute(self, context: bpy.types.Context):
        if (context.object is not None) and (context.object.type == "MESH"):
            cleaning_target : bpy.types.Object = context.object

            VXGroup : bpy.types.VertexGroup
            for VXGroup in cleaning_target.vertex_groups:
                for vert in cleaning_target.data.vertices:
                    try:
                        if (VXGroup.weight(vert.index) != 0.0):
                            break
                    except:
                        pass
                else:
                    cleaning_target.vertex_groups.remove(VXGroup)

        return{"FINISHED"}