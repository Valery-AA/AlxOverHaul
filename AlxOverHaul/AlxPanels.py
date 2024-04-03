import bpy
from bpy_extras import node_utils

from .AlxProperties import Alx_Object_Selection_ListItem

from .AlxUtils import AlxRetrieveContextObject, AlxRetrieveContextArmature

# UI Embeded Operators
from .AlxOperators import Alx_OT_Scene_VisibilityIsolator, Alx_OT_Mode_UnlockedModes

from .AlxOperators import Alx_OT_Armature_MatchIKByMirroredName
from .AlxModifierOperators import Alx_OT_Modifier_ApplyReplace, Alx_OT_Modifier_ManageOnSelected
from .AlxUVRetopology import Alx_OT_UVRetopology


class Alx_UL_Object_PropertiesList(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_object_properties_list"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_Object_Selection_ListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        ItemBox = layout.box().grid_flow(columns=1)
        UISplit = ItemBox.row().split(factor=0.5, align=False)

        UISplit.prop(item.ObjectPointer, "name", text="", emboss=True)
        UISplit.prop(item.ObjectPointer, "display_type", text="")

        PropertiesRow = ItemBox.row().split(factor=0.25, align=True)
        PropertiesRow.prop(item.ObjectPointer, "show_name", text="", icon="SORTALPHA", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_axis", text="", icon="EMPTY_ARROWS", emboss=True)
        if (item.ObjectPointer.type in ["MESH", "META"]):
            PropertiesRow.prop(item.ObjectPointer, "show_wire", text="", icon="MOD_WIREFRAME", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_in_front", text="", icon="OBJECT_HIDDEN", emboss=True)
        if (item.ObjectPointer.type in ["MESH"]):
            PropertiesRow.prop(item.ObjectPointer, "color", text="")

class Alx_UL_Object_ModifierList(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_object_modifier_list"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_Object_Selection_ListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        layout.scale_y = 1.0
        LayoutBox = layout.box().grid_flow(columns=1)
        LayoutBox.box().label(text=item.ObjectPointer.name)

        try:
            bpy.data.objects.get(item.ObjectPointer.name).modifiers[0]

            ModifierBox = LayoutBox.row().box()
            for Modifier in item.ObjectPointer.modifiers:
                modifier_ui_row = ModifierBox.row(align=True)

                modifier_delete_button = modifier_ui_row.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="PANEL_CLOSE")
                modifier_delete_button.object_pointer_reference = item.ObjectPointer.name
                modifier_delete_button.create_modifier = False
                modifier_delete_button.remove_modifier = True
                modifier_delete_button.object_modifier_index = item.ObjectPointer.modifiers.find(Modifier.name)

                icon_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items.get(Modifier.type).icon

                modifier_ui_row.prop(Modifier, "name", text="", icon=icon_name, emboss=True)

                modifier_ui_row.prop(Modifier, "show_in_editmode", text="", emboss=True)
                modifier_ui_row.prop(Modifier, "show_viewport", text="", emboss=True)
                modifier_ui_row.prop(Modifier, "show_render", text="", emboss=True)

                modifier_move_up_button = modifier_ui_row.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_UP")
                modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
                modifier_move_up_button.create_modifier = False
                modifier_move_up_button.remove_modifier = False
                modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(Modifier.name)
                modifier_move_up_button.move_modifier_up = True
                modifier_move_up_button.move_modifier_down = False

                modifier_move_up_button = modifier_ui_row.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_DOWN")
                modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
                modifier_move_up_button.create_modifier = False
                modifier_move_up_button.remove_modifier = False
                modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(Modifier.name)
                modifier_move_up_button.move_modifier_up = False
                modifier_move_up_button.move_modifier_down = True
        except Exception as error:
            pass
            #print("Exception: %s | %s" % (type(error).__name__, error))

class Alx_UL_Armature_ActionSelectorList(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_armature_action_list"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_Object_Selection_ListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        layout.prop(item, "name", icon="ACTION")
        layout.label(text=f"{bpy.data.actions.find(item.name)}")

# Panels
class Alx_PT_AlexandriaGeneralPanel(bpy.types.Panel):
    """"""

    bl_label = "Alexandria Tool Panel"
    bl_idname = "ALX_PT_panel_alexandria_tool"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    bl_order = 0
    bl_ui_units_x = 30

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context: bpy.types.Context):
        AlxContextObject = AlxRetrieveContextObject(context)
        AlxContextArmature = AlxRetrieveContextArmature(context)

        AddonProperties = context.scene.alx_tool_scene_isolator_properties
        PanelProperties = context.scene.alx_panel_alexandria_general_properties

        AlxLayout = self.layout
        AlxLayout.ui_units_x = 30.0

        LayoutBox = AlxLayout.row()

        Tabs = LayoutBox.box().prop(PanelProperties, "alx_panel_tab", icon_only=True, expand=True)

        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "VISIBILITY") and (context.area.type == "VIEW_3D"):
            AlxLayout.ui_units_x = 20.0
            VisibilityTabBox = LayoutBox.box()



            isolator_box = VisibilityTabBox.box().row()

            isolator_options = isolator_box.row()
            isolator_options.column().prop(AddonProperties, "scene_isolator_type_target", expand=True)
            isolator_options.column().prop(AddonProperties, "scene_isolator_visibility_target", expand=True)
            
            isolator_show_hide = isolator_box.column()
            isolator_hide = isolator_show_hide.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="HIDE_ON", emboss=True)
            isolator_hide.Panik = False
            isolator_hide.TargetVisibility = False
            isolator_show = isolator_show_hide.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="HIDE_OFF", emboss=True)
            isolator_show.Panik = False
            isolator_show.TargetVisibility = True

            isolator_panik_placement = isolator_box.column()
            isolator_panik_placement.scale_y = 2.0
            isolator_panik = isolator_panik_placement.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="", icon="LOOP_BACK", emboss=True)
            isolator_panik.Panik = True



            OverlayBox = VisibilityTabBox.box().row()

            overlay_toggle = OverlayBox.column()
            overlay_toggle.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
            overlay_toggle.prop(context.space_data.overlay, "show_face_orientation", text="", icon="NORMALS_FACE")

            xray_toggle = OverlayBox.column()
            xray_toggle.prop(context.area.spaces.active.shading, "show_xray", text="XRay-Mesh", icon="XRAY")
            xray_toggle.prop(context.space_data.overlay, "show_xray_bone", text="XRay-Bone", icon="XRAY")

            topology_toggle = OverlayBox.column()
            topology_toggle.prop(context.space_data.overlay, "show_wireframes", text="Wireframe", icon="MOD_WIREFRAME")
            topology_toggle.prop(context.space_data.overlay, "show_retopology", text="Retopology", icon="MESH_GRID")



        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "OBJECT") and (context.area.type == "VIEW_3D"):
            AlxLayout.ui_units_x = 20.0
            ObjectTabBox = LayoutBox.box()

            ObjectTabBox.template_list(Alx_UL_Object_PropertiesList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")



        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "ARMATURE") and (context.area.type == "VIEW_3D"):
            AlxLayout.ui_units_x = 20.0
            ArmatureTabBox = LayoutBox.box()

            if (AlxContextArmature is not None):
                ArmatureTabBox.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)

                armature_display_options = ArmatureTabBox.column()
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_names")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_axes")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "display_type", text="", expand=False)
            else:
                ArmatureTabBox.row().label(text="[Active Armature] [Missing]")

            ArmatureTabBox.row().operator(Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="Symmetrize IK")



        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "MODIFIER") and (context.area.type == "VIEW_3D"):
            AlxLayout.ui_units_x = 20.0
            ModifierTabBox = LayoutBox.box()

            ModifierTabBox.popover(Alx_PT_AlexandriaModifierPanel.bl_idname, text="Create Modifier")
            ModifierTabBox.operator(Alx_OT_Modifier_ApplyReplace.bl_idname, text="Apply-Replace Modifier")
            
            ModifierTabBox.row().template_list(Alx_UL_Object_ModifierList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")



        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "ALXOPERATORS") and (context.area.type == "VIEW_3D"):
            AlxLayout.ui_units_x = 20.0
            AlxOperatorsTabBox = LayoutBox.box()

            AlxOperatorsTabBox.row().operator(Alx_OT_UVRetopology.bl_idname, text="Grid Retopology")
            
            

        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "RENDER") and (context.area.type == "VIEW_3D"):
            AlxLayout.ui_units_x = 30.0 * PanelProperties.alx_panel_scale_x
            AlxRenderSpace = LayoutSpace.column().grid_flow(even_columns=True)



            AlxPreviewShadingSpace = AlxRenderSpace.box()

            if (context.area.spaces.active.shading.type == "SOLID"):
                matcap_shading = AlxPreviewShadingSpace.row().split(factor=0.4)
                matcap_preview = matcap_shading.column()
                matcap_preview.row().prop(context.area.spaces.active.shading, "light", text="")
                matcap_preview.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=3.2, scale_popup=3.0)
                matcap_color_shading = matcap_shading.column()
                matcap_color_shading.row().grid_flow(columns=2, align=True).prop(context.area.spaces.active.shading, "color_type", expand=True)
                matcap_color_shading.row().prop(context.area.spaces.active.shading, "single_color", text="")

            if (context.area.spaces.active.shading.type in ["MATERIAL", "RENDERED"]):
                scene_shading_options = AlxPreviewShadingSpace.row()
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_lights", text="Scene Lights")
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_world", text="Scene World")
                if (context.area.spaces.active.shading.use_scene_world == False):
                    hdri_shading = AlxPreviewShadingSpace.row().split(factor=0.4)
                    hdri_shading.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
                    scene_world_shading = hdri_shading.column()
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="Rotation")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_intensity", text="Intensity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="Opacity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="Opacity")

                if (context.area.spaces.active.shading.use_scene_world == True):
                    AlxPreviewShadingSpace.row().prop(context.scene.world, "use_nodes", text="Use Scene World Nodes", toggle=True)

                    if (context.scene.world.use_nodes == True):
                        if (context.scene.world.node_tree is not None):
                            WorldMaterial = context.scene.world.node_tree
                            MaterialOutput = context.scene.world.node_tree.get_output_node("ALL")
                            Surface = node_utils.find_node_input(MaterialOutput, "Surface")
                            AlxPreviewShadingSpace.column().template_node_view(WorldMaterial, MaterialOutput, Surface)



            AlxRenderShadingSpace = AlxRenderSpace.box()

            render_engine_option = AlxRenderShadingSpace.row()
            render_engine_option.prop(context.scene.render, "engine", text="")
            render_engine_option.prop(context.area.spaces.active.shading, "type", text="", expand=True)

            if (context.scene.render.engine in ["BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"]):
                eevee_viewport_sample = AlxRenderShadingSpace.row(align=True).split(factor=0.4)
                eevee_viewport_sample.prop(context.scene.eevee, "use_taa_reprojection", text="Denoise")
                eevee_viewport_sample.prop(context.scene.eevee, "taa_samples", text="Viewport")
                eevee_render_sample = AlxRenderShadingSpace.row(align=True).split(factor=0.4)
                eevee_render_sample.separator()
                eevee_render_sample.prop(context.scene.eevee, "taa_render_samples", text="Render")

            if (context.scene.render.engine == "CYCLES"):
                cycles_samples = AlxRenderShadingSpace.row(align=True)
                cycles_samples.prop(context.scene.cycles, "preview_samples", text="Viewport")
                cycles_samples.prop(context.scene.cycles, "samples", text="Render")



            AlxPreviewShadingSettingsSpace = AlxRenderSpace.box()

            if (context.area.spaces.active.shading.type == "SOLID"):
                solid_shading_options = AlxPreviewShadingSettingsSpace.column()
                solid_shading_options.row().prop(context.area.spaces.active.shading, "show_backface_culling")
                solid_shading_options.row().prop(context.area.spaces.active.shading, "show_cavity")
                if (context.area.spaces.active.shading.show_cavity == True):
                    solid_shading_options.row().prop(context.area.spaces.active.shading, "cavity_type", text="")
                    cavity_options = solid_shading_options.row()
                    cavity_options.prop(context.area.spaces.active.shading, "curvature_ridge_factor", text="Ridge")
                    cavity_options.prop(context.area.spaces.active.shading, "curvature_valley_factor", text="Valley")

        # if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "UI_DESIGNER"):
        #     AlxSpace = AlxLayout.box().row().split(factor=0.5, align=True)

        #     WindowAreaSpace = AlxSpace.box()
        #     AreaUITypeSelector = WindowAreaSpace.row()
        #     AreaUITypeSelector.template_header()
        #     CloseArea = AreaUITypeSelector.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="Close Area")
        #     CloseArea.UseCloseArea = True

        #     WindowAreaSpace.row().label(text="Split Vertical:")
        #     SplitVertical = WindowAreaSpace.row()
        #     SplitHalf = SplitVertical.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="1/2")
        #     SplitHalf.UseAreaSplit = True
        #     # SplitHalf.direction = "VERTICAL"
        #     # SplitHalf.cursor = context.area.width/2
            
        #     # # SplitVertical.operator("screen.area_split", text="1/3")
        #     # # SplitHalf.direction = "VERTICAL"
        #     # # SplitHalf.factor = 0.33
        #     # # SplitVertical.operator("screen.area_split", text="1/4")
        #     # # SplitHalf.direction = "VERTICAL"
        #     # # SplitHalf.factor = 0.25

        #     # # bpy.ops.screen.area_split()

            

            
        #     AlxSpace.label(text=context.area.type)

        if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "SETTINGS"):
            AlxSpace = LayoutSpace.box().row()

            AlxSpace.prop(PanelProperties, "alx_panel_scale_x", text="Scale Width")
            




        # ObjectPropertyColumn = PropertySplit.column()
        # ObjectPropertyColumn.template_list(Alx_UL_Object_PropertiesList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")

        # ScenePropertyColumn = PropertySplit.column()
        # ScenePropertyColumn.scale_x = 1

        # ScenePropertyColumn.row().prop(context.space_data.overlay, "show_stats", text="Statistics", toggle=True)
       

        
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        

        
        #         ScenePropertyColumn.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")

        # MMenuSectionR = RMenuColumnSpace.row().box()
        
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Mesh_EditAttributes.bl_idname, text="Edit Attributes")
        # 

class Alx_MT_UnlockedModesPie(bpy.types.Menu):
    """"""

    bl_label = "This is a a way to show how it works"
    bl_idname = "ALX_MT_menu_unlocked_modes"

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"
    
    def draw(self, context):
        AlxLayout = self.layout

        AlxContextObject = AlxRetrieveContextObject(context=context)
        AlxContextArmature = AlxRetrieveContextArmature(context=context)

        PieUI = AlxLayout.menu_pie()

        AlxOPS_AutoMode_OBJECT = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="OBJECT", icon="OBJECT_DATAMODE")
        AlxOPS_AutoMode_OBJECT.DefaultBehaviour = True
        AlxOPS_AutoMode_OBJECT.TargetMode = "OBJECT"

        if (context.mode != "POSE") and (AlxContextArmature is not None):
            AlxOPS_AutoMode_POSE = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="A-POSE", icon="ARMATURE_DATA")
            AlxOPS_AutoMode_POSE.DefaultBehaviour = False
            AlxOPS_AutoMode_POSE.TargetMode = "POSE"
            AlxOPS_AutoMode_POSE.TargetArmature = AlxContextArmature.name
        else:
            if (context.mode == "POSE"):
                PoseMBox = PieUI.box()
                PoseMBox.label(text="[Mode] | [Pose]")
            else:
                AlxOPS_AutoMode_POSE = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="POSE", icon="ARMATURE_DATA")
                AlxOPS_AutoMode_POSE.DefaultBehaviour = True
                AlxOPS_AutoMode_POSE.TargetMode = "POSE"

                # if (AlxContextArmature is None):
                #     PoseMBox.label(text="[Active Mesh] [Missing] [Armature]")

        if (context.mode != "PAINT_WEIGHT") and (AlxContextObject is not None) and (AlxContextArmature is not None):
            AlxOPS_AutoMode_WEIGHT = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="A-WPAINT", icon="WPAINT_HLT")
            AlxOPS_AutoMode_WEIGHT.DefaultBehaviour = False
            AlxOPS_AutoMode_WEIGHT.TargetMode = "PAINT_WEIGHT"
            AlxOPS_AutoMode_WEIGHT.TargetObject = AlxRetrieveContextObject(context=context).name
            AlxOPS_AutoMode_WEIGHT.TargetArmature = AlxContextArmature.name
        else:
            if (context.mode == "PAINT_WEIGHT"):
                WeightPaintMBox = PieUI.box()
                WeightPaintMBox.label(text="[Mode] | [Weight Paint]")
            else:
                AlxOPS_AutoMode_WEIGHT = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="WPAINT", icon="WPAINT_HLT")
                AlxOPS_AutoMode_WEIGHT.DefaultBehaviour = True
                AlxOPS_AutoMode_WEIGHT.TargetMode = "PAINT_WEIGHT"

                # if (AlxContextObject is None): 
                #     WeightPaintMBox.row().label(text="[Active Object] [Incorrect] | [Mesh] [Only]")
                # if (AlxContextArmature is None):
                #     WeightPaintMBox.row().label(text="[Active Mesh] [Missing] [Armature]")
        
        if (AlxContextObject is not None) and (AlxContextObject.type == "MESH"):
            VertexMode = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Edge", icon="EDGESEL")
            VertexMode.DefaultBehaviour = True
            VertexMode.TargetObject = AlxContextObject.name
            VertexMode.TargetMode = "EDIT"
            VertexMode.TargetType = "MESH"
            VertexMode.TargetSubMode = "EDGE"

            VertexMode = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Vertex", icon="VERTEXSEL")
            VertexMode.DefaultBehaviour = True
            VertexMode.TargetObject = AlxContextObject.name
            VertexMode.TargetMode = "EDIT"
            VertexMode.TargetType = "MESH"
            VertexMode.TargetSubMode = "VERT"
            
            VertexMode = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Face", icon="FACESEL")
            VertexMode.DefaultBehaviour = True
            VertexMode.TargetObject = AlxContextObject.name
            VertexMode.TargetMode = "EDIT"
            VertexMode.TargetType = "MESH"
            VertexMode.TargetSubMode = "FACE"
        else:
            if (AlxContextObject is not None):
                if (AlxContextObject.type != "MESH"):
                    PieUI.box().row().label(text="[Selection] [Incorrect] | [Mesh] [Only]")
                    PieUI.box().row().label(text="[Selection] [Incorrect] | [Mesh] [Only]")
                    PieUI.box().row().label(text="[Selection] [Incorrect] | [Mesh] [Only]")
            else: 
                PieUI.box().row().label(text="[Selection] [Incorrect] | [Mesh] [Only]")
                PieUI.box().row().label(text="[Selection] [Incorrect] | [Mesh] [Only]")
                PieUI.box().row().label(text="[Selection] [Incorrect] | [Mesh] [Only]")
        
        if (len(context.selected_objects) != 0):
        
            GeneralEditTab = PieUI.box().row().split(factor=0.33)
            GeneralEditSectionL = GeneralEditTab.column()
            GeneralEditSectionM = GeneralEditTab.column()
            GeneralEditSectionR = GeneralEditTab.column()

            GeneralEditFont = GeneralEditSectionL.row().operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Armature", icon="ARMATURE_DATA")
            GeneralEditFont.DefaultBehaviour = True
            GeneralEditFont.TargetMode = "EDIT"
            GeneralEditFont.TargetType = "ARMATURE"
            GeneralEditFont.TargetSubMode = ""

            GeneralEditFont = GeneralEditSectionL.row().operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Curve", icon="CURVE_DATA")
            GeneralEditFont.DefaultBehaviour = True
            GeneralEditFont.TargetMode = "EDIT"
            GeneralEditFont.TargetType = "CURVE"
            GeneralEditFont.TargetSubMode = ""

            GeneralEditFont = GeneralEditSectionL.row().operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Surface", icon="SURFACE_DATA")
            GeneralEditFont.DefaultBehaviour = True
            GeneralEditFont.TargetMode = "EDIT"
            GeneralEditFont.TargetType = "SURFACE"
            GeneralEditFont.TargetSubMode = ""

            GeneralEditFont = GeneralEditSectionM.row().operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="MetaShape", icon="META_DATA")
            GeneralEditFont.DefaultBehaviour = True
            GeneralEditFont.TargetMode = "EDIT"
            GeneralEditFont.TargetType = "META"
            GeneralEditFont.TargetSubMode = ""

            GeneralEditFont = GeneralEditSectionM.row().operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Text", icon="FILE_FONT")
            GeneralEditFont.DefaultBehaviour = True
            GeneralEditFont.TargetMode = "EDIT"
            GeneralEditFont.TargetType = "FONT"
            GeneralEditFont.TargetSubMode = ""

            GPencilRow = GeneralEditSectionR.row()
            GeneralEditGPencilPoint = GPencilRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="GPencil", icon="GP_SELECT_POINTS")
            GeneralEditGPencilPoint.DefaultBehaviour = True
            GeneralEditGPencilPoint.TargetMode = "EDIT"
            GeneralEditGPencilPoint.TargetType = "GPENCIL"
            GeneralEditGPencilPoint.TargetSubMode = "POINT"
            

            GeneralEditGPencilStroke = GPencilRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="", icon="GP_SELECT_STROKES")
            GeneralEditGPencilStroke.DefaultBehaviour = True
            GeneralEditGPencilStroke.TargetMode = "EDIT"
            GeneralEditGPencilStroke.TargetType = "GPENCIL"
            GeneralEditGPencilStroke.TargetSubMode = "STROKE"

            GeneralEditGPencilSegment = GPencilRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="", icon="GP_SELECT_BETWEEN_STROKES")
            GeneralEditGPencilSegment.DefaultBehaviour = True
            GeneralEditGPencilSegment.TargetMode = "EDIT"
            GeneralEditGPencilSegment.TargetType = "GPENCIL"
            GeneralEditGPencilSegment.TargetSubMode = "SEGMENT"

            GeneralEditLattice = GeneralEditSectionR.row().operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Lattice", icon="LATTICE_DATA")
            GeneralEditLattice.DefaultBehaviour = True
            GeneralEditLattice.TargetMode = "EDIT"
            GeneralEditLattice.TargetType = "LATTICE"
            GeneralEditLattice.TargetSubMode = ""
        else:
            PieUI.box().label(text="[Selection] [Missing]")
            
        if (context.mode != "SCULPT") and (AlxContextObject is not None):
            SculptMode = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="Sculpt", icon="SCULPTMODE_HLT")
            SculptMode.DefaultBehaviour = True
            SculptMode.TargetMode = "SCULPT"
        else:
            SculptMBox = PieUI.box()
            if (context.mode == "SCULPT"):
                SculptMBox.label(text="[Mode] | [Sculpt]")
            else:
                if (AlxContextObject is None):
                    SculptMBox.label(text="[Active Object] [Incorrect] | [Mesh] [Only]")

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









class Alx_PT_ArmatureActionSelector(bpy.types.Panel):
    """"""

    bl_label = "" 
    bl_idname = "ALX_PT_armature_action_panel"

    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True

    def draw(self, context):
        layout = self.layout

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