import bpy
from bpy_extras import node_utils

from .AlxProperties import Alx_Object_Selection_ListItem

# UI Embeded Operators
from .AlxOperators import Alx_OT_Mode_UnlockedModes

from .AlxModifierOperators import Alx_OT_Modifier_ManageOnSelected

from .AlxObjectUtils import AlxRetrieveContextObject, AlxRetrieveContextArmature



class Alx_UL_Armature_ActionSelectorList(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_armature_action_list"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_Object_Selection_ListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        layout.prop(item, "name", icon="ACTION")
        layout.label(text=f"{bpy.data.actions.find(item.name)}")



class Alx_PT_Scene_GeneralPivot(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "ALX_PT_panel_scene_general_pivot"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        AlxLayout = self.layout
                        AlxLayout.ui_units_x = 30.0
                        AlxLayoutRow = AlxLayout.row()
                        PivotMenuSection = AlxLayoutRow.box()
                        #SnapMenuSection = AlxLayoutRow.box()

                        TopRow = PivotMenuSection.row().split(factor=0.5)
                        TopSnapColumn = TopRow.column()
                        TopOrientationColumn = TopRow.column()
                        TopSnapColumn.prop(context.tool_settings, "transform_pivot_point", expand=True)
                        TopOrientationColumn.prop(context.scene.transform_orientation_slots[0], "type", expand=True)
                        
                        TopSnapColumn.prop(context.space_data.overlay, "grid_scale")
                        TopSnapColumn.prop(context.space_data.overlay, "grid_subdivisions")

                        BottomRow = PivotMenuSection.row().split(factor=0.5)
                        BottomSnapColumn = BottomRow.column()
                        BottomOrientationColumn = BottomRow.column()
                        
                        BottomSnapColumn.prop(context.tool_settings, "use_snap", text="Snap")
                        BottomSnapColumn.prop(context.tool_settings, "snap_target", expand=True)
                        BottomSnapColumn.prop(context.tool_settings, "use_snap_align_rotation")
                        BottomSnapColumn.prop(context.tool_settings, "use_snap_grid_absolute")
                        SnapModeRow = BottomSnapColumn.column(align=True)
                        SnapModeRow.prop(context.tool_settings, "use_snap_translate", text="Snap Move", toggle=True)
                        SnapModeRow.prop(context.tool_settings, "use_snap_rotate", text="Snap Rotate", toggle=True)
                        SnapModeRow.prop(context.tool_settings, "use_snap_scale", text="Snap Scale", toggle=True)

                        if (bpy.app.version[0] == 3):
                            BottomOrientationColumn.prop(context.tool_settings, "snap_elements", expand=True)

                        if ((bpy.app.version[0] == 4) and (bpy.app.version[1] in [0, 1])):
                            BottomOrientationColumn.prop(context.tool_settings, "snap_elements_base", expand=True)
                            BottomOrientationColumn.prop(context.tool_settings, "snap_elements_individual", expand=True)

                        # SnapSelAct = SnapMenuSection.row().operator(Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Selected To Active")
                        # SnapSelAct.SourceSnapping = "ACTIVE"
                        # SnapSelAct.TargetSnapping = "SELECTED"

                        # SnapSelCur = SnapMenuSection.row().operator(Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Selected To Cursor")
                        # SnapSelCur.SourceSnapping = "SCENE_CURSOR"
                        # SnapSelCur.TargetSnapping = "SELECTED"
                        # SnapSelCur.SubTargetSnapping = "OBJECT"

                        # SnapCurAct = SnapMenuSection.row().operator(Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Cursor To Active")
                        # SnapCurAct.SourceSnapping = "ACTIVE"
                        # SnapCurAct.TargetSnapping = "SCENE_CURSOR"

                        # SnapOriCur = SnapMenuSection.row().operator(Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Origin To Cursor")
                        # SnapOriCur.SourceSnapping = "SCENE_CURSOR"
                        # SnapOriCur.TargetSnapping = "SELECTED"
                        # SnapOriCur.SubTargetSnapping = "ORIGIN"

                        # SnapCurRes = SnapMenuSection.row().operator(Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Reset Cursor")
                        # SnapCurRes.SourceSnapping = "RESET"
                        # SnapCurRes.TargetSnapping = "SCENE_CURSOR"

# Tool Panels

        

# Sub Panels
class Alx_PT_AlexandriaModifierPanel(bpy.types.Panel):
    """"""

    bl_label = "Alexandria Modifier Panel"
    bl_idname = "ALX_PT_panel_alexandria_modifier_popover"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    bl_options = {"INSTANCED"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context.area.type == "VIEW_3D"
    
    def draw(self, context: bpy.types.Context):
        AlxLayout = self.layout
        AlxLayout.ui_units_x = 35.0
        
        ModifierSpace = AlxLayout.box().grid_flow(columns=5, even_columns=True, row_major=True)

        for Modifier in ["DATA_TRANSFER", "MIRROR", "BEVEL", "BOOLEAN", "ARMATURE",
                         "WEIGHTED_NORMAL", "ARRAY", "SUBSURF", "SOLIDIFY", "SURFACE_DEFORM",
                         "SEPARATOR", "CURVE", "MULTIRES", "SEPARATOR", "DISPLACE"
                         ]:
            
            if (Modifier == "SEPARATOR"):
                ModifierSpace.separator()

            if (Modifier != "SEPARATOR"):
                mod_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items[Modifier].name
                mod_icon = bpy.types.Modifier.bl_rna.properties['type'].enum_items[Modifier].icon
                mod_identifier = bpy.types.Modifier.bl_rna.properties['type'].enum_items[Modifier].identifier

                modifier_button = ModifierSpace.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, text=mod_name, icon=mod_icon)
                modifier_button.modifier_type = mod_identifier
                modifier_button.create_modifier = True
                modifier_button.remove_modifier = False

        #for property in dir(context.active_object.modifiers[0]):
        #   AlxLayout.prop(context.active_object.modifiers[0], property)









# class Alx_PT_ArmatureActionSelector(bpy.types.Panel):
#     """"""

#     bl_label = "" 
#     bl_idname = "ALX_PT_armature_action_panel"

#     bl_space_type = "PROPERTIES"
#     bl_region_type = "WINDOW"

#     @classmethod
#     def poll(self, context: bpy.types.Context):
#         return True

#     def draw(self, context):
#         layout = self.layout

        #layout.template_list(Alx_UL_Armature_ActionSelectorList.bl_idname, "", dataptr=bpy.data, propname="actions", active_dataptr=context.scene, active_propname="alx_armature_action_active_index")

        #row.operator('my_list.new_item', text='NEW')
        #row.operator('my_list.delete_item', text='REMOVE')
        #row.operator('my_list.move_item', text='UP').direction = 'UP'
        #row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'
        #if scene.list_index >= 0 and scene.my_list:
        #item = scene.my_list[scene.list_index] row = layout.row() row.prop(item, "name") row.prop(item, "random_prop")
  























# remove
# class Alx_PT_AlexandriaObjectToolsPanel(bpy.types.Panel):
#     """"""

#     bl_label = "Alexandria Render Panel"
#     bl_idname = "alx_panel_alexandria_object_tools"

#     bl_space_type = "VIEW_3D"
#     bl_region_type = "WINDOW"

#     bl_options = {"INSTANCED"}

#     @classmethod
#     def poll(self, context: bpy.types.Context):
#         return context.area.type == "VIEW_3D"
    
#     def draw(self, context: bpy.types.Context):
#         AlxLayout = self.layout
#         AlxLayout.ui_units_x = 15.0

#         if (context.active_object is not None) and (context.active_object.type == "MESH"):
#             if (AlxCheckBlenderVersion([4], [0]) or AlxCheckBlenderVersion([3])):
#                 AlxPROPS_MESH_Smooth = AlxLayout.row().split(factor=0.25, align=True)
#             if (AlxCheckBlenderVersion([4], [1])):
#                 AlxPROPS_MESH_Smooth = AlxLayout.row().split(factor=0.5, align=True)

#             AlxPROPS_MESH_Smooth.operator("object.shade_smooth", text="Smooth", emboss=True)

#             if (AlxCheckBlenderVersion([4], [0]) or AlxCheckBlenderVersion([3])):
#                 AlxPROPS_MESH_Smooth.operator("object.shade_smooth", text="A-Smooth", emboss=True).use_auto_smooth = True
#                 AlxPROPS_MESH_Smooth.prop(context.active_object.data, "auto_smooth_angle", text="A-SA", toggle=True)
#             AlxPROPS_MESH_Smooth.operator("object.shade_flat", text="Flat", emboss=True)

#         if (context.active_object is not None):
#             if (context.active_object.type == "MESH"):
#                 ObjectBox = AlxLayout.box().split(factor=0.5)

#                 ObjectOptionsBox = ObjectBox.box()
#                 ObjectOptionsBox.label(text="Mesh:")
#                 AlxEditMirror = ObjectOptionsBox.row(align=True)
#                 AlxEditMirror.prop(context.active_object.data, "use_mirror_x", text="X", toggle=True)
#                 AlxEditMirror.prop(context.active_object.data, "use_mirror_y", text="Y", toggle=True)
#                 AlxEditMirror.prop(context.active_object.data, "use_mirror_z", text="Z", toggle=True)
#                 ObjectOptionsBox.row().prop(context.active_object.data, "use_mirror_topology", text="Topology", icon="MESH_GRID", toggle=True)

#                 ObjectWPOptionsBox = ObjectBox.box()
#                 ObjectWPOptionsBox.label(text="Weigth Paint:")
#                 AlxWeightMirror = ObjectWPOptionsBox.row(align=True)
#                 AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_x", text="X", toggle=True)
#                 AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_y", text="Y", toggle=True)
#                 AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_z", text="Z", toggle=True)
#                 ObjectWPOptionsBox.row().prop(bpy.context.active_object.data, "use_mirror_topology", text="Topology", icon="MESH_GRID", expand=True)
#                 ObjectWPOptionsBox.row().prop(bpy.context.active_object.data, "use_mirror_vertex_groups", text="Vx Groups", icon="GROUP_VERTEX")
                
#             if (context.active_object is not None):
#                 if (context.active_object.type == "ARMATURE"):
#                     ArmatureBox = AlxLayout.row().box()
#                     ArmatureBox.label(text="Pose:")
#                     AlxPoseMirror = ArmatureBox.row(align=True)
#                     AlxPoseMirror.prop(context.active_object.pose, "use_mirror_x", text="X Mirror", toggle=True)
#                     AlxPoseMirror.prop(context.active_object.pose, "use_mirror_relative", text="Local Mirror", toggle=True)
#                     ArmatureBox.row().prop(context.active_object.pose, "use_auto_ik", text="Auto IK", icon="CON_KINEMATIC")