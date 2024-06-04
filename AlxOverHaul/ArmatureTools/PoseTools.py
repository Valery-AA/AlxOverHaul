import bpy


class Alx_OT_Armature_Pose_ToggleConstraints(bpy.types.Operator):
    """"""

    bl_label = "pose - toggle armature constraints"
    bl_idname = "alx.operator_armature_pose_toggle_constraints"

    bl_options = {"REGISTER", "UNDO"}

    enabled : bpy.props.BoolProperty() #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.object is not None)
    
    def execute(self, context: bpy.types.Context):
        if (context.object is not None) and (context.object.type == "ARMATURE"):
            armature : bpy.types.Object = context.object
        
            bone : bpy.types.PoseBone
            constraint : bpy.types.Constraint
            for bone in armature.pose.bones:
                for constraint in bone.constraints:
                    constraint.enabled = self.enabled
        else:
            self.report({"WARNING"}, message="Type: is not ARMATURE")


        return {"FINISHED"}
    
    def draw(self, context: bpy.types.Context): 
        self.layout.row().prop(self, "enabled", text="global enabled")

    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)