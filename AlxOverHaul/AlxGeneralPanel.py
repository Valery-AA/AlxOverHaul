import bpy

from .AlxKeymapUtils import AlxKeymapRegister
from .AlxObjectUtils import AlxRetrieveContextObject, AlxRetrieveContextArmature

from .AlxOperators import Alx_OT_Mode_UnlockedModes
from .AlxPanels import Alx_PT_AlexandriaModifierPanel
from .AlxVisibilityOperators import Alx_Tool_SceneIsolator_Properties, Alx_OT_Scene_VisibilityIsolator, Alx_OT_Object_VisibilitySwitch
from .AlxModifierOperators import Alx_OT_Modifier_ManageOnSelected, Alx_OT_Modifier_ApplyReplace


class Alx_PG_PropertyGroup_AlexandriaGeneral(bpy.types.PropertyGroup):
    """"""

    panel_tabs : bpy.props.EnumProperty(default="OBJECT", 
        items=[
            ("OBJECT", "Object", "", "OBJECT_DATAMODE", 1),
            ("ARMATURE", "Armature", "", "ARMATURE_DATA", 1<<1),
            ("MODIFIER", "Modifier", "", "MODIFIER", 1<<2),
            ("ALXOPERATORS", "AlxOPS", "", "PLUGIN", 1<<3),
            ("RENDER", "Render", "", "SCENE", 1<<4),
            ("UI_DESIGNER", "UI Designer", "", "WINDOW", 1<<5),
            ("SETTINGS", "Settings", "", "PREFERENCES", 1<<6)
        ]) #type:ignore

    show_object_properties : bpy.props.BoolProperty(name="", default=False) #type:ignore

class Alx_PG_PropertyGroup_ObjectSelectionListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty() #type:ignore
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object) #type:ignore

class Alx_UL_UIList_ObjectSelectionProperties(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_object_selection_properties"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_PG_PropertyGroup_ObjectSelectionListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        ItemBox = layout.row().grid_flow(columns=1)
        UISplit = ItemBox.row()

        NameColumn = UISplit.column()
        NameColumn.prop(item.ObjectPointer, "name", text="", icon="OBJECT_DATA", emboss=True)
        NameColumn.prop(item.ObjectPointer.data, "name", text="", icon="OUTLINER_DATA_MESH", emboss=True)
        VisibilityColumn = UISplit.column()
        ToggleRow = VisibilityColumn.row()
        ToggleRow.prop(item.ObjectPointer, "hide_select", text="", emboss=True)
        ToggleRow.operator(Alx_OT_Object_VisibilitySwitch.bl_idname, text="", icon="HIDE_OFF", emboss=True).object_pointer_reference = item.ObjectPointer.name
        ToggleRow.prop(item.ObjectPointer, "hide_render", text="", emboss=True)
        VisibilityColumn.row().prop(item.ObjectPointer, "display_type", text="")

        PropertiesRow = ItemBox.row().split(factor=0.25, align=True)
        PropertiesRow.prop(item.ObjectPointer, "show_name", text="", icon="SORTALPHA", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_axis", text="", icon="EMPTY_ARROWS", emboss=True)
        if (item.ObjectPointer.type in ["MESH", "META"]):
            PropertiesRow.prop(item.ObjectPointer, "show_wire", text="", icon="MOD_WIREFRAME", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_in_front", text="", icon="OBJECT_HIDDEN", emboss=True)
        if (item.ObjectPointer.type in ["MESH"]):
            PropertiesRow.prop(item.ObjectPointer, "color", text="")

        ItemBox.row().separator(factor=2.0)



class Alx_PG_PropertyGroup_ModifierSettings(bpy.types.PropertyGroup):
    """"""
    object_name : bpy.props.StringProperty(name="", default="") #type:ignore
    object_modifier : bpy.props.StringProperty(name="", default="") #type:ignore
    show_options : bpy.props.BoolProperty(name="", default=False) #type:ignore

class Alx_PT_Panel_Modifier_Options(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "ALX_PT_panel_modifier_options"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    object_name : bpy.props.StringProperty(default="") #type:ignore
    modifier_name : bpy.props.StringProperty(default="") #type:ignore
    modifier_type : bpy.props.StringProperty(default="") #type:ignore

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context: bpy.types.Context):
        if (self.modifier_type == "SUBSURF"):
            self.layout.label(text="text")



class Alx_UL_UIList_ObjectSelectionModifiers(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_object_selection_modifiers"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_PG_PropertyGroup_ObjectSelectionListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        LayoutBox = layout.row().grid_flow(columns=1)

        object_info = LayoutBox.row().box()
        object_info.scale_y = 0.5
        object_info.label(text=item.ObjectPointer.name)

        modifier_slots = LayoutBox.row().grid_flow(columns=1)

        for Collection_Modifier in item.ObjectPointer.alx_modifier_collection:
            modifier_header = modifier_slots.row()
            obj_modifier = item.ObjectPointer.modifiers.get(Collection_Modifier.object_modifier)
            icon_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items.get(obj_modifier.type).icon

            modifier_delete_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="PANEL_CLOSE")
            modifier_delete_button.object_pointer_reference = item.ObjectPointer.name
            modifier_delete_button.create_modifier = False
            modifier_delete_button.remove_modifier = True
            modifier_delete_button.object_modifier_index = item.ObjectPointer.modifiers.find(Collection_Modifier.object_modifier)

            modifier_header.prop(obj_modifier, "name", text="", icon=icon_name, emboss=True)
            modifier_header.prop(Collection_Modifier, "show_options")
            options_panel = modifier_slots.row().panel_prop(Collection_Modifier, "show_options")
            options_layout : bpy.types.UILayout = options_panel[1]

            modifier_header.prop(obj_modifier, "show_in_editmode", text="", emboss=True)
            modifier_header.prop(obj_modifier, "show_viewport", text="", emboss=True)
            modifier_header.prop(obj_modifier, "show_render", text="", emboss=True)

        LayoutBox.row().separator(factor=2.0)
        



        # ModifierBox = LayoutBox.row().box()

        # for Modifier in item.ObjectPointer.modifiers:
        #     modifier_ui_row = ModifierBox.row(align=True)

        #     

        #     icon_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items.get(Modifier.type).icon

        #     

        #     modifier_options_panel = modifier_ui_row

        #     

        #     modifier_move_up_button : Alx_OT_Modifier_ManageOnSelected = modifier_ui_row.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_UP")
        #     modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
        #     modifier_move_up_button.create_modifier = False
        #     modifier_move_up_button.remove_modifier = False
        #     modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(Modifier.name)
        #     modifier_move_up_button.move_modifier_up = True
        #     modifier_move_up_button.move_modifier_down = False

        #     modifier_move_up_button = modifier_ui_row.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_DOWN")
        #     modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
        #     modifier_move_up_button.create_modifier = False
        #     modifier_move_up_button.remove_modifier = False
        #     modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(Modifier.name)
        #     modifier_move_up_button.move_modifier_up = False
        #     modifier_move_up_button.move_modifier_down = True
        

class Alx_PT_Panel_AlexandriaGeneral(bpy.types.Panel):
    """"""

    bl_label = "Alexandria General Panel"
    bl_idname = "ALX_PT_panel_alexandria_tool"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context: bpy.types.Context):
        self.layout.ui_units_x = 30.0
        TabsLayout = self.layout.row()

        AlxContextObject = AlxRetrieveContextObject(context)
        AlxContextArmature = AlxRetrieveContextArmature(context)



        GeneralPanelProperties : Alx_PG_PropertyGroup_AlexandriaGeneral = context.scene.alx_panel_alexandria_general_properties
        SceneIsolatorProperties : Alx_Tool_SceneIsolator_Properties = context.scene.alx_tool_scene_isolator_properties



        Tabs = TabsLayout.column().prop(GeneralPanelProperties, "panel_tabs", icon_only=True, expand=True)

        if (GeneralPanelProperties.panel_tabs == "OBJECT") and (context.area.type == "VIEW_3D"):
            self.layout.ui_units_x = 20.0
            ObjectTabBox = TabsLayout.column()

            isolator_box = ObjectTabBox.row().row()

            isolator_options = isolator_box.row()
            isolator_options.column().prop(SceneIsolatorProperties, "scene_isolator_type_target", expand=True)
            isolator_options.column().prop(SceneIsolatorProperties, "scene_isolator_visibility_target", expand=True)
            
            isolator_show_hide = isolator_box.column()
            isolator_hide : Alx_OT_Scene_VisibilityIsolator = isolator_show_hide.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="HIDE_ON", emboss=True)
            isolator_hide.PanicReset = False
            isolator_hide.TargetVisibility = False
            isolator_show : Alx_OT_Scene_VisibilityIsolator = isolator_show_hide.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="HIDE_OFF", emboss=True)
            isolator_show.PanicReset = False
            isolator_show.TargetVisibility = True

            isolator_panik_placement = isolator_box.column()
            isolator_panik_placement.scale_y = 2.0
            isolator_panik : Alx_OT_Scene_VisibilityIsolator = isolator_panik_placement.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="", icon="LOOP_BACK", emboss=True)
            isolator_panik.PanicReset = True



            OverlayBox = ObjectTabBox.row().row()

            overlay_toggle = OverlayBox.column()
            overlay_toggle.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
            overlay_toggle.prop(context.space_data.overlay, "show_face_orientation", text="", icon="NORMALS_FACE")

            xray_toggle = OverlayBox.column()
            xray_toggle.prop(context.area.spaces.active.shading, "show_xray", text="XRay-Mesh", icon="XRAY")
            xray_toggle.prop(context.space_data.overlay, "show_xray_bone", text="XRay-Bone", icon="XRAY")

            topology_toggle = OverlayBox.column()
            topology_toggle.prop(context.space_data.overlay, "show_wireframes", text="Wireframe", icon="MOD_WIREFRAME")
            topology_toggle.prop(context.space_data.overlay, "show_retopology", text="Retopology", icon="MESH_GRID")
            
            ObjectTabBox.row().separator(factor=1.75)

            ObjectTabBox.row().prop(GeneralPanelProperties, "show_object_properties", text="- Object Properties -" if (GeneralPanelProperties.show_object_properties == True) else "+ Object Properties +", toggle=True, emboss=True)

            if (GeneralPanelProperties.show_object_properties == True):
                ObjectTabBox.template_list(Alx_UL_UIList_ObjectSelectionProperties.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")



        if (GeneralPanelProperties.panel_tabs == "ARMATURE") and (context.area.type == "VIEW_3D"):
            self.layout.ui_units_x = 20.0
            ArmatureTabBox = TabsLayout.column()

            if (AlxContextArmature is not None):
                ArmatureTabBox.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)

                armature_display_options = ArmatureTabBox.column()
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_names")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_axes")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "display_type", text="", expand=False)

            #ArmatureTabBox.row().operator(Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="Symmetrize IK")



        if (GeneralPanelProperties.panel_tabs == "MODIFIER") and (context.area.type == "VIEW_3D"):
            self.layout.ui_units_x = 20.0
            ModifierTabBox = TabsLayout.column()

            ModifierTabBox.popover(Alx_PT_AlexandriaModifierPanel.bl_idname, text="Create Modifier")
            ModifierTabBox.operator(Alx_OT_Modifier_ApplyReplace.bl_idname, text="Apply-Replace Modifier")
            
            ModifierTabBox.row().template_list(Alx_UL_UIList_ObjectSelectionModifiers.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")



        # if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "ALXOPERATORS") and (context.area.type == "VIEW_3D"):
        #     AlxLayout.ui_units_x = 20.0
        #     AlxOperatorsTabBox = LayoutBox.box()

        #     AlxOperatorsTabBox.row().operator(Alx_OT_UVRetopology.bl_idname, text="Grid Retopology")
            
            

        # if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "RENDER") and (context.area.type == "VIEW_3D"):
        #     AlxLayout.ui_units_x = 30.0 * PanelProperties.alx_panel_scale_x
        #     AlxRenderSpace = LayoutSpace.column().grid_flow(even_columns=True)



        #     AlxPreviewShadingSpace = AlxRenderSpace.box()

        #     if (context.area.spaces.active.shading.type == "SOLID"):
        #         matcap_shading = AlxPreviewShadingSpace.row().split(factor=0.4)
        #         matcap_preview = matcap_shading.column()
        #         matcap_preview.row().prop(context.area.spaces.active.shading, "light", text="")
        #         matcap_preview.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=3.2, scale_popup=3.0)
        #         matcap_color_shading = matcap_shading.column()
        #         matcap_color_shading.row().grid_flow(columns=2, align=True).prop(context.area.spaces.active.shading, "color_type", expand=True)
        #         matcap_color_shading.row().prop(context.area.spaces.active.shading, "single_color", text="")

        #     if (context.area.spaces.active.shading.type in ["MATERIAL", "RENDERED"]):
        #         scene_shading_options = AlxPreviewShadingSpace.row()
        #         scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_lights", text="Scene Lights")
        #         scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_world", text="Scene World")
        #         if (context.area.spaces.active.shading.use_scene_world == False):
        #             hdri_shading = AlxPreviewShadingSpace.row().split(factor=0.4)
        #             hdri_shading.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
        #             scene_world_shading = hdri_shading.column()
        #             scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="Rotation")
        #             scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_intensity", text="Intensity")
        #             scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="Opacity")
        #             scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="Opacity")

        #         if (context.area.spaces.active.shading.use_scene_world == True):
        #             AlxPreviewShadingSpace.row().prop(context.scene.world, "use_nodes", text="Use Scene World Nodes", toggle=True)

        #             if (context.scene.world.use_nodes == True):
        #                 if (context.scene.world.node_tree is not None):
        #                     WorldMaterial = context.scene.world.node_tree
        #                     MaterialOutput = context.scene.world.node_tree.get_output_node("ALL")
        #                     Surface = node_utils.find_node_input(MaterialOutput, "Surface")
        #                     AlxPreviewShadingSpace.column().template_node_view(WorldMaterial, MaterialOutput, Surface)



        #     AlxRenderShadingSpace = AlxRenderSpace.box()

        #     render_engine_option = AlxRenderShadingSpace.row()
        #     render_engine_option.prop(context.scene.render, "engine", text="")
        #     render_engine_option.prop(context.area.spaces.active.shading, "type", text="", expand=True)

        #     if (context.scene.render.engine in ["BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"]):
        #         eevee_viewport_sample = AlxRenderShadingSpace.row(align=True).split(factor=0.4)
        #         eevee_viewport_sample.prop(context.scene.eevee, "use_taa_reprojection", text="Denoise")
        #         eevee_viewport_sample.prop(context.scene.eevee, "taa_samples", text="Viewport")
        #         eevee_render_sample = AlxRenderShadingSpace.row(align=True).split(factor=0.4)
        #         eevee_render_sample.separator()
        #         eevee_render_sample.prop(context.scene.eevee, "taa_render_samples", text="Render")

        #     if (context.scene.render.engine == "CYCLES"):
        #         cycles_samples = AlxRenderShadingSpace.row(align=True)
        #         cycles_samples.prop(context.scene.cycles, "preview_samples", text="Viewport")
        #         cycles_samples.prop(context.scene.cycles, "samples", text="Render")



        #     AlxPreviewShadingSettingsSpace = AlxRenderSpace.box()

        #     if (context.area.spaces.active.shading.type == "SOLID"):
        #         solid_shading_options = AlxPreviewShadingSettingsSpace.column()
        #         solid_shading_options.row().prop(context.area.spaces.active.shading, "show_backface_culling")
        #         solid_shading_options.row().prop(context.area.spaces.active.shading, "show_cavity")
        #         if (context.area.spaces.active.shading.show_cavity == True):
        #             solid_shading_options.row().prop(context.area.spaces.active.shading, "cavity_type", text="")
        #             cavity_options = solid_shading_options.row()
        #             cavity_options.prop(context.area.spaces.active.shading, "curvature_ridge_factor", text="Ridge")
        #             cavity_options.prop(context.area.spaces.active.shading, "curvature_valley_factor", text="Valley")

        # # if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "UI_DESIGNER"):
        # #     AlxSpace = AlxLayout.box().row().split(factor=0.5, align=True)

        # #     WindowAreaSpace = AlxSpace.box()
        # #     AreaUITypeSelector = WindowAreaSpace.row()
        # #     AreaUITypeSelector.template_header()
        # #     CloseArea = AreaUITypeSelector.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="Close Area")
        # #     CloseArea.UseCloseArea = True

        # #     WindowAreaSpace.row().label(text="Split Vertical:")
        # #     SplitVertical = WindowAreaSpace.row()
        # #     SplitHalf = SplitVertical.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="1/2")
        # #     SplitHalf.UseAreaSplit = True
        # #     # SplitHalf.direction = "VERTICAL"
        # #     # SplitHalf.cursor = context.area.width/2
            
        # #     # # SplitVertical.operator("screen.area_split", text="1/3")
        # #     # # SplitHalf.direction = "VERTICAL"
        # #     # # SplitHalf.factor = 0.33
        # #     # # SplitVertical.operator("screen.area_split", text="1/4")
        # #     # # SplitHalf.direction = "VERTICAL"
        # #     # # SplitHalf.factor = 0.25

        # #     # # bpy.ops.screen.area_split()

            

            
        # #     AlxSpace.label(text=context.area.type)

        # if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "SETTINGS"):
        #     AlxSpace = LayoutSpace.box().row()

        #     AlxSpace.prop(PanelProperties, "alx_panel_scale_x", text="Scale Width")
            




        # # ObjectPropertyColumn = PropertySplit.column()
        # # ObjectPropertyColumn.template_list(Alx_UL_Object_PropertiesList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")

        # ScenePropertyColumn = PropertySplit.column()
        # ScenePropertyColumn.scale_x = 1

        # ScenePropertyColumn.row().prop(context.space_data.overlay, "show_stats", text="Statistics", toggle=True)
       

        
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        

        
        #         ScenePropertyColumn.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")

        # MMenuSectionR = RMenuColumnSpace.row().box()
        
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Mesh_EditAttributes.bl_idname, text="Edit Attributes")
        # 

AlxKeymapRegister(keymap_call_type="PANEL", region_type="WINDOW", item_idname=Alx_PT_Panel_AlexandriaGeneral.bl_idname, key="A", use_ctrl=True, use_alt=True, trigger_type="CLICK")

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