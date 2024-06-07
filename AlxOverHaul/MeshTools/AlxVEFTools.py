import bpy
from bpy_extras import view3d_utils


class Alx_OT_Mesh_VEF_Utility(bpy.types.Operator):
    """"""

    bl_label = "VEF utility"
    bl_idname = "alx.operator_mesh_vef_utility"

    bl_options = {"REGISTER", "UNDO"}

    at_invoke_mouse_x : tuple() = tuple() #type:ignore
    at_invoke_mouse_y : tuple() = tuple() #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True
    
    def execute(self, context: bpy.types.Context):
        print(view3d_utils.region_2d_to_vector_3d(context.region, context.space_data.region_3d, (self.at_invoke_mouse_x, self.at_invoke_mouse_y)))
        #context.scene.ray_cast(context.evaluated_depsgraph_get())
        
        return {"FINISHED"}
    
    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        self.at_invoke_mouse_x = event.mouse_region_x
        self.at_invoke_mouse_y = event.mouse_region_y

        self.execute(context)
        
        return {"INTERFACE"}

        
    
