# import bpy
# import bmesh
# import mathutils

# class Alx_PG_PropertyGroup_GizmoControlPointData(bpy.types.PropertyGroup):
#     position_vector : bpy.props.FloatVectorProperty() #type:ignore


# class Alx_OT_Remesh_Gizmo_ControlPoint(bpy.types.GizmoGroup):
#     bl_label = ""
#     bl_idname = "ALX_GGT_remesh_gizmo_control_point"
    
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'WINDOW'
#     bl_options = {'3D', 'PERSISTENT'}



#     @classmethod
#     def poll(self, context: bpy.types.Context):
#         return (context.object is not None) and (context.object.type == "MESH") and (context.object.mode == "EDIT")

#     def setup(self, context):
#         ContextObject = context.object

#         control_arrow = self.gizmos.new("GIZMO_GT_box_3d")
#         control_arrow.target_set_prop("offset", self, "")


#         gz.matrix_basis = ob.matrix_world.normalized()
#         gz.draw_style = 'BOX'

#         gz.color = 1.0, 0.5, 0.0
#         gz.alpha = 0.5

#         gz.color_highlight = 1.0, 0.5, 1.0
#         gz.alpha_highlight = 0.5

#         self.energy_gizmo = gz

#     def refresh(self, context):
#         ob = context.object
#         gz = self.energy_gizmo
#         gz.matrix_basis = ob.matrix_world.normalized()