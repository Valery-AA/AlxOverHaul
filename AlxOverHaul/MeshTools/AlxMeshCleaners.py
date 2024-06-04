import bpy

class Alx_OT_Mesh_VertexGroup_Clean(bpy.types.Operator):
    """"""

    bl_label = "cleaner - mesh vertex group "
    bl_idname = "alx.operator_mesh_vertex_group_clean"

    bl_options = {"REGISTER", "UNDO"}


    condition_empty : bpy.props.BoolProperty() #type:ignore
    condition_non_bone : bpy.props.BoolProperty() #type:ignore


    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.object is not None) and (context.object.type == "MESH")


    def execute(self, context: bpy.types.Context):
        if (context.object is not None) and (context.object.type == "MESH"):
            cleaning_target : bpy.types.Object = context.object
            pending_delete = set()


            VXGroup : bpy.types.VertexGroup
            if (self.condition_empty == True):
                for VXGroup in cleaning_target.vertex_groups:
                    for vert in cleaning_target.data.vertices:
                        try:
                            if (VXGroup.weight(vert.index) != 0.0):
                                break
                        except:
                            pass
                    else:
                        pending_delete.add(VXGroup)


            if (self.condition_non_bone == True):
                armature_object = cleaning_target.find_armature()
                if (armature_object is not None):
                    bone_name_set = set(bone.name for bone in armature_object.data.bones)

                    for VXGroup in cleaning_target.vertex_groups:
                        if (VXGroup.name not in bone_name_set):
                            pending_delete.add(VXGroup)


            for VXGroup in pending_delete:
                cleaning_target.vertex_groups.remove(VXGroup)

        return{"FINISHED"}
    
    def draw(self, context: bpy.types.Context): 
        self.layout.row().label(text="remove:")
        self.layout.row().prop(self, "condition_empty", text="empty")
        self.layout.row().prop(self, "condition_non_bone", text="armature missmatch")

    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)