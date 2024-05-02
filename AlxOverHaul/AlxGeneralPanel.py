import bpy
from bpy_extras import node_utils

from .AlxUtils import AlxRetrieveContextObject, AlxRetrieveContextArmature

from .AlxOperators import Alx_OT_Mode_UnlockedModes, Alx_OT_Armature_MatchIKByMirroredName
from .AlxObjectOperator import Alx_OT_Object_UnlockedQOrigin

from .AlxUVRetopology import Alx_OT_VXGroupBySeams, Alx_OT_UVExtractIsland
from .AlxHairTools import Alx_OT_Armature_BoneChainOnSelection

from .AlxVisibilityOperators import Alx_Tool_SceneIsolator_Properties, Alx_OT_Scene_VisibilityIsolator, Alx_OT_Object_VisibilitySwitch
from .AlxModifierOperators import Alx_OT_Modifier_ManageOnSelected, Alx_OT_Modifier_ApplyReplace, Alx_OT_Modifier_BatchVisibility


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

class Alx_PT_Operator_ModifierChangeSettings(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_modifier_change_settings"
    
    object_name : bpy.props.StringProperty() #type:ignore
    modifier_name : bpy.props.StringProperty() #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True
    
    def execute(self, context: bpy.types.Context):
        Object = context.scene.objects.get(self.object_name)
        Modifier = Object.alx_modifier_collection.get(f"{self.object_name}_{self.modifier_name}")
        Modifier.show_options = not Modifier.show_options
        return {"FINISHED"}

class Alx_UL_UIList_ObjectSelectionModifiers(bpy.types.UIList):
    """"""

    bl_idname = "ALX_UL_ui_list_object_selection_modifiers"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: Alx_PG_PropertyGroup_ObjectSelectionListItem, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        LayoutBox = layout.row().grid_flow(columns=1)

        self.use_filter_show = True

        object_info = LayoutBox.row().box()
        object_info.scale_y = 0.5
        object_info.label(text=item.ObjectPointer.name)



        for raw_object_modifier in item.ObjectPointer.modifiers:
            modifier_slots = LayoutBox.row().box()
            modifier_header = modifier_slots.row(align=True)

            raw_object_modifier : bpy.types.Modifier

            icon_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items.get(raw_object_modifier.type).icon

            modifier_delete_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="PANEL_CLOSE")
            modifier_delete_button.object_pointer_reference = item.ObjectPointer.name
            modifier_delete_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
            modifier_delete_button.create_modifier = False
            modifier_delete_button.remove_modifier = True

            modifier_move_up_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="FILE_TICK")
            modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
            modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
            modifier_move_up_button.create_modifier = False
            modifier_move_up_button.apply_modifier = True
            
            _show_options = item.ObjectPointer.alx_modifier_collection.get(f"{item.ObjectPointer.name}_{raw_object_modifier.name}").show_options

            modifier_operator = modifier_header.row()
            modifier_operator.scale_x = 0.6
            modifier_change_settings : Alx_PT_Operator_ModifierChangeSettings = modifier_operator.operator(Alx_PT_Operator_ModifierChangeSettings.bl_idname, text= "-" if (_show_options) else "+", depress= _show_options)
            modifier_change_settings.object_name = item.ObjectPointer.name
            modifier_change_settings.modifier_name = raw_object_modifier.name



            if (item.ObjectPointer.alx_modifier_collection.get(f"{item.ObjectPointer.name}_{raw_object_modifier.name}").show_options == True):
                ModifierOptionBox = modifier_slots.row().column()

                if (raw_object_modifier.type == "SUBSURF"):
                    ModifierOptionBox.row().prop(raw_object_modifier, "show_only_control_edges", text="optimal")

                if (raw_object_modifier.type == "ARMATURE"):
                    ModifierOptionBox.row().prop(raw_object_modifier, "object", text="")
                    ModifierOptionBox.row().prop(raw_object_modifier, "use_deform_preserve_volume", text="preserve volume")

                if (raw_object_modifier.type == "BEVEL"):
                    row = ModifierOptionBox.row().split(factor=0.33, align=True)

                    row.prop(raw_object_modifier, "offset_type", text="")
                    row.prop(raw_object_modifier, "width", text="width")
                    row.prop(raw_object_modifier, "segments", text="segments")
                    ModifierOptionBox.row().prop(raw_object_modifier, "limit_method", text="")

                    ModifierOptionBox.row().prop(raw_object_modifier, "miter_outer", text="miter outer")
                    ModifierOptionBox.row().prop(raw_object_modifier, "harden_normals", text="harden")



            modifier_header.prop(raw_object_modifier, "name", text="", icon=icon_name, emboss=True)

            modifier_header.prop(raw_object_modifier, "show_in_editmode", text="", emboss=True)
            modifier_header.prop(raw_object_modifier, "show_viewport", text="", emboss=True)
            modifier_header.prop(raw_object_modifier, "show_render", text="", emboss=True)

            modifier_move_up_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_UP")
            modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
            modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
            modifier_move_up_button.move_modifier_up = True

            modifier_move_up_button = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_DOWN")
            modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
            modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
            modifier_move_up_button.move_modifier_down = True

        LayoutBox.row().separator(factor=2.0)


class Alx_PT_Panel_AlexandriaGeneralModeling(bpy.types.Panel):
    """"""

    bl_label = "Alexandria General Modeling Panel"
    bl_idname = "ALX_PT_panel_alexandria_general_modeling"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context: bpy.types.Context):
        self.layout.ui_units_x = 20.0
        TabsLayout = self.layout.row()

        AlxContextObject = AlxRetrieveContextObject(context)
        AlxContextArmature = AlxRetrieveContextArmature(context)


        GeneralPanelProperties : Alx_PG_PropertyGroup_AlexandriaGeneral = context.scene.alx_panel_alexandria_general_properties
        SceneIsolatorProperties : Alx_Tool_SceneIsolator_Properties = context.scene.alx_tool_scene_isolator_properties


        Tabs = TabsLayout.column().prop(GeneralPanelProperties, "panel_tabs", icon_only=True, expand=True)

        if (GeneralPanelProperties.panel_tabs == "OBJECT") and (context.area.type == "VIEW_3D"):
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
            ArmatureTabBox = TabsLayout.column()

            if (AlxContextArmature is not None):
                ArmatureTabBox.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)

                armature_display_options = ArmatureTabBox.column()
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_names")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_axes")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "display_type", text="", expand=False)



        if (GeneralPanelProperties.panel_tabs == "MODIFIER") and (context.area.type == "VIEW_3D"):
            ModifierTabBox = TabsLayout.column()

            ModifierTabBox.popover(Alx_PT_AlexandriaModifierPanel.bl_idname, text="Create Modifier")
            ModifierTabBox.operator(Alx_OT_Modifier_ApplyReplace.bl_idname, text="Apply-Replace Modifier")
            ModifierTabBox.operator(Alx_OT_Modifier_BatchVisibility.bl_idname, text="Batch Visibility")

            ModifierTabBox.row().template_list(Alx_UL_UIList_ObjectSelectionModifiers.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index", maxrows=3)
            

        if (GeneralPanelProperties.panel_tabs == "ALXOPERATORS") and (context.area.type == "VIEW_3D"):
            AlxOperatorsTabBox = TabsLayout.column()

            AlxOperatorsTabBox.operator(Alx_OT_VXGroupBySeams.bl_idname, text="VxGroup - group/mask by seam")

            AlxOperatorsTabBox.operator(Alx_OT_UVExtractIsland.bl_idname, text="UV - Extract islands")
            # AlxOperatorsTabBox.row().operator(Alx_OT_UVRetopology.bl_idname, text="Grid Retopology")

            AlxOperatorsTabBox.operator(Alx_OT_Armature_BoneChainOnSelection.bl_idname, text="Hair - Bone chain on edge strip")
            ArmatureTabBox.row().operator(Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="Symmetrize IK")



        if (GeneralPanelProperties.panel_tabs == "RENDER") and (context.area.type == "VIEW_3D"):
            RenderTabBox = TabsLayout.column()

            render_engine_option = RenderTabBox.row()
            render_engine_option.prop(context.scene.render, "engine", text="")
            render_engine_option.prop(context.area.spaces.active.shading, "type", text="", expand=True)

            if (context.scene.render.engine in ["BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"]):
                eevee_viewport_sample = RenderTabBox.row(align=True).split(factor=0.4)
                eevee_viewport_sample.prop(context.scene.eevee, "use_taa_reprojection", text="Denoise")
                eevee_viewport_sample.prop(context.scene.eevee, "taa_samples", text="Viewport")
                eevee_render_sample = RenderTabBox.row(align=True).split(factor=0.4)
                eevee_render_sample.separator()
                eevee_render_sample.prop(context.scene.eevee, "taa_render_samples", text="Render")

            if (context.scene.render.engine == "CYCLES"):
                cycles_samples = RenderTabBox.row(align=True)
                cycles_samples.prop(context.scene.cycles, "preview_samples", text="Viewport")
                cycles_samples.prop(context.scene.cycles, "samples", text="Render")

            if (context.area.spaces.active.shading.type == "SOLID"):
                matcap_preview = RenderTabBox.column()
                matcap_preview.row().prop(context.area.spaces.active.shading, "light", expand=True)
                matcap_preview.row().template_icon_view(context.area.spaces.active.shading, "studio_light")

                matcap_preview.row().grid_flow(columns=2, align=True).prop(context.area.spaces.active.shading, "color_type", expand=True)
                matcap_preview.row().prop(context.area.spaces.active.shading, "single_color", text="")

            if (context.area.spaces.active.shading.type == "MATERIAL"):
                scene_shading_options = RenderTabBox.column()
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_lights", text="scene Lights")
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_world", text="Scene world")

                if (context.area.spaces.active.shading.use_scene_world == False):
                    scene_shading_options.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
                    scene_world_shading = scene_shading_options.column()
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="rotation")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_intensity", text="intensity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="opacity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="blur")

                if (context.area.spaces.active.shading.use_scene_world == True):
                    scene_shading_options.row().prop(context.scene.world, "use_nodes", text="Use Scene World Nodes", toggle=True)

                    if (context.scene.world.use_nodes == True):
                        if (context.scene.world.node_tree is not None):
                            WorldMaterial = context.scene.world.node_tree
                            MaterialOutput = context.scene.world.node_tree.get_output_node("ALL")
                            Surface = node_utils.find_node_input(MaterialOutput, "Surface")
                            scene_shading_options.column().template_node_view(WorldMaterial, MaterialOutput, Surface)

            if (context.area.spaces.active.shading.type == "RENDERED"):
                scene_shading_options = RenderTabBox.column()
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_lights_render", text="scene lights")
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_world_render", text="scene world")

                if (context.area.spaces.active.shading.use_scene_world_render == False):
                    hdri_shading = scene_shading_options
                    hdri_shading.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
                    scene_world_shading = hdri_shading.column()
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="rotation")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_intensity", text="intensity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="opacity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="blur")

                if (context.area.spaces.active.shading.use_scene_world_render == True):
                    scene_shading_options.row().prop(context.scene.world, "use_nodes", text="Use Scene world Nodes", toggle=True)

                    if (context.scene.world.use_nodes == True):
                        if (context.scene.world.node_tree is not None):
                            WorldMaterial = context.scene.world.node_tree
                            MaterialOutput = context.scene.world.node_tree.get_output_node("ALL")
                            Surface = node_utils.find_node_input(MaterialOutput, "Surface")
                            scene_shading_options.column().template_node_view(WorldMaterial, MaterialOutput, Surface)

            if (context.area.spaces.active.shading.type == "SOLID"):
                solid_shading_options = RenderTabBox.column()
                solid_shading_options.row().prop(context.area.spaces.active.shading, "show_backface_culling")
                solid_shading_options.row().prop(context.area.spaces.active.shading, "show_cavity")
                if (context.area.spaces.active.shading.show_cavity == True):
                    solid_shading_options.row().prop(context.area.spaces.active.shading, "cavity_type", text="")
                    cavity_options = solid_shading_options.row()
                    cavity_options.prop(context.area.spaces.active.shading, "curvature_ridge_factor", text="ridge")
                    cavity_options.prop(context.area.spaces.active.shading, "curvature_valley_factor", text="valley")



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

        # if (context.scene.alx_panel_alexandria_general_properties.alx_panel_tab == "SETTINGS"):
        #     AlxSpace = LayoutSpace.box().row()

            


        # ScenePropertyColumn.row().prop(context.space_data.overlay, "show_stats", text="Statistics", toggle=True)
       

        
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        

        
        #         ScenePropertyColumn.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")


        
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Mesh_EditAttributes.bl_idname, text="Edit Attributes")
        # 


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
                         "SEPARATOR", "CURVE", "MULTIRES", "WELD", "DISPLACE"
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


class Alx_MT_UnlockedModesPie(bpy.types.Menu):
    """"""

    bl_label = "Unlocked Modes"
    bl_idname = "ALX_MT_menu_unlocked_modes"


    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area.type == "VIEW_3D")
    
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
        

        if (AlxContextObject is not None) and (AlxContextObject.type == "MESH") and (len(context.selected_objects) != 0):
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
            for i in range(0, 3):
                if (AlxContextObject is None) and (AlxContextArmature is None) or (len(context.selected_objects) == 0):
                    PieUI.box().row().label(text="[Selection] [Missing]")

                if (AlxContextObject is None) and (AlxContextArmature is not None) and ((len(context.selected_objects) != 0)):
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
        self.layout.ui_units_x = 20.0

        PivotLayout = self.layout.row().split(factor=0.5)

        pivot_column = PivotLayout.column()
        pivot_column.prop(context.tool_settings, "transform_pivot_point", expand=True)
        pivot_column.prop(context.space_data.overlay, "grid_scale")
        pivot_column.prop(context.space_data.overlay, "grid_subdivisions")
        pivot_column.prop(context.scene.transform_orientation_slots[0], "type", expand=True)

        pivot_column.operator(Alx_OT_Object_UnlockedQOrigin.bl_idname, text="Q-Origin")

        snapping_column = PivotLayout.column()

        if (bpy.app.version[0] == 3):
            snapping_column.prop(context.tool_settings, "snap_elements", expand=True)

        if ((bpy.app.version[0] == 4) and (bpy.app.version[1] in [0, 1])):
            snapping_column.prop(context.tool_settings, "snap_elements_base", expand=True)
            snapping_column.prop(context.tool_settings, "snap_elements_individual", expand=True)

        snapping_column.prop(context.tool_settings, "use_snap", text="Snap")
        snapping_column.prop(context.tool_settings, "snap_target", expand=True)

        snapping_column.row().label(text="Snap to:")
        snap_affect_type = snapping_column.row(align=True)
        snap_affect_type.prop(context.tool_settings, "use_snap_translate", text="Move", toggle=True)
        snap_affect_type.prop(context.tool_settings, "use_snap_rotate", text="Rotate", toggle=True)
        snap_affect_type.prop(context.tool_settings, "use_snap_scale", text="Scale", toggle=True)

        snapping_column.prop(context.tool_settings, "use_snap_align_rotation")
        snapping_column.prop(context.tool_settings, "use_snap_grid_absolute")