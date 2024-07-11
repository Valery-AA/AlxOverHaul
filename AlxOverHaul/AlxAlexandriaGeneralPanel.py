import bpy
from bpy_extras import node_utils

from .AlxUtils import AlxRetrieveContextObject, AlxRetrieveContextArmature

from .AlxOperators import Alx_OT_Armature_MatchIKByMirroredName
from .AlxObjectOperator import Alx_OT_Object_UnlockedQOrigin, Alx_OT_Object_BatchMaterial

from .AlxSculptTools import Alx_OT_Sculpt_ConditionMasking

from .AlxUVRetopology import Alx_OT_VXGroupBySeams, Alx_OT_UVExtractIsland
from .AlxHairTools import Alx_OT_Armature_BoneChainOnSelection


from .AlxVisibilityOperators import Alx_Tool_SceneIsolator_Properties, Alx_OT_Scene_VisibilityIsolator, Alx_OT_Object_VisibilitySwitch
from .AlxModifierOperators import Alx_OT_Modifier_ManageOnSelected, Alx_OT_Modifier_ApplyReplace, Alx_OT_Modifier_BatchVisibility

from .UITools.Alx_OT_UI_SimpleDesigner import Alx_OT_UI_SimpleDesigner

# Mesh Tools
from .MeshTools.AlxMeshCleaners import Alx_OT_Mesh_VertexGroup_Clean
from .MeshTools.AlxShapeKeyToolSet import Alx_OT_Shapekey_TransferShapekeysToTarget


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
        self.use_filter_show = True

        layout.ui_units_x = 10
        item_box = layout.column()


        box_column = item_box.box().column(align=True)

        header = box_column.row(align=True)
        header.prop(item.ObjectPointer, "name", text="", icon="OBJECT_DATA", emboss=True)

        header.prop(item.ObjectPointer, "show_name", text="", icon="SORTALPHA", emboss=True)
        header.prop(item.ObjectPointer, "show_axis", text="", icon="EMPTY_ARROWS", emboss=True)
        if (item.ObjectPointer.type in ["MESH", "META"]):
            header.prop(item.ObjectPointer, "show_wire", text="", icon="MOD_WIREFRAME", emboss=True)
        header.prop(item.ObjectPointer, "show_in_front", text="", icon="OBJECT_HIDDEN", emboss=True)


        body = box_column.row(align=True)

        body.prop(item.ObjectPointer, "display_type", text="")
        if (item.ObjectPointer.type in ["MESH", "META"]):
            body.prop(item.ObjectPointer, "color", text="")


        item_box.separator(factor=2.0)


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
        LayoutBox = layout.row().box().grid_flow(columns=1)

        self.use_filter_show = True

        object_header = LayoutBox.row()
        object_header.prop(item.ObjectPointer, "alx_modifier_expand_settings", text="", icon="TRIA_DOWN" if item.ObjectPointer.alx_modifier_expand_settings == True else "TRIA_RIGHT", emboss=False)

        object_header.label(text=item.ObjectPointer.name)

        
        indented_layout = LayoutBox.row()
        indented_layout.separator()
        modifier_area = indented_layout.column()
        if (item.ObjectPointer.alx_modifier_expand_settings == True):

            for raw_object_modifier in item.ObjectPointer.modifiers:
                modifier_slots = modifier_area.column()
                
                modifier_header = modifier_slots.row(align=True)

                raw_object_modifier : bpy.types.Modifier

                icon_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items.get(raw_object_modifier.type).icon

                show_options = item.ObjectPointer.alx_modifier_collection.get(f"{item.ObjectPointer.name}_{raw_object_modifier.name}").show_options

                modifier_operator = modifier_header.row()
                modifier_change_settings : Alx_PT_Operator_ModifierChangeSettings = modifier_operator.operator(Alx_PT_Operator_ModifierChangeSettings.bl_idname, icon="TRIA_DOWN" if (show_options) else "TRIA_RIGHT", emboss=False, depress=show_options)
                modifier_change_settings.object_name = item.ObjectPointer.name
                modifier_change_settings.modifier_name = raw_object_modifier.name

                modifier_header.separator()
                

                modifier_delete_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="PANEL_CLOSE", emboss=False)
                modifier_delete_button.object_pointer_reference = item.ObjectPointer.name
                modifier_delete_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
                modifier_delete_button.create_modifier = False
                modifier_delete_button.apply_modifier = False
                modifier_delete_button.remove_modifier = True
                modifier_delete_button.move_modifier_up = False
                modifier_delete_button.move_modifier_down = False

                modifier_apply_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="FILE_TICK", emboss=False)
                modifier_apply_button.object_pointer_reference = item.ObjectPointer.name
                modifier_apply_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
                modifier_apply_button.create_modifier = False
                modifier_apply_button.apply_modifier = True
                modifier_apply_button.remove_modifier = False
                modifier_apply_button.move_modifier_up = False
                modifier_apply_button.move_modifier_down = False
                
                


                if (item.ObjectPointer.alx_modifier_collection.get(f"{item.ObjectPointer.name}_{raw_object_modifier.name}").show_options == True):
                    ModifierOptionBox = modifier_slots.row().column()

                    if (raw_object_modifier.type == "DATA_TRANSFER"):
                        row = ModifierOptionBox.row().split(factor=0.65, align=True)
                        row.prop(raw_object_modifier, "object", text="")
                        split = row.row(align=True)
                        split.prop(raw_object_modifier, "use_object_transform", text="", toggle=True, icon="OBJECT_ORIGIN")
                        split.operator("object.datalayout_transfer", text="Transfer Layers")

                        row = ModifierOptionBox.row()
                        row.prop(raw_object_modifier, "use_vert_data", text="")
                        row.prop(raw_object_modifier, "data_types_verts")

                        row = ModifierOptionBox.row()
                        row.prop(raw_object_modifier, "use_edge_data", text="")
                        row.prop(raw_object_modifier, "data_types_edges")

                        row = ModifierOptionBox.row()
                        row.prop(raw_object_modifier, "use_loop_data", text="")
                        row.prop(raw_object_modifier, "data_types_loops")
                        
                        row = ModifierOptionBox.row()
                        row.prop(raw_object_modifier, "use_poly_data", text="")
                        row.prop(raw_object_modifier, "data_types_polys")

                    if (raw_object_modifier.type == "MIRROR"):
                        row = ModifierOptionBox.column()

                        row.prop(raw_object_modifier, "mirror_object", text="object")
                        row.prop(raw_object_modifier, "use_clip", text="clip")
                        row.prop(raw_object_modifier, "use_mirror_merge", text="merge")
                        row.prop(raw_object_modifier, "merge_threshold", text="")
                        

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

                    if (raw_object_modifier.type == "BOOLEAN"):
                        row = ModifierOptionBox.row()
                        row.prop(raw_object_modifier, "object", text="")
                        row.prop(raw_object_modifier, "operation", expand=True)

                    if (raw_object_modifier.type == "TRIANGULATE"):
                        ModifierOptionBox.row().prop(raw_object_modifier, "keep_custom_normals", text="keep normals")

                    if (raw_object_modifier.type == "SOLIDIFY"):
                        row = ModifierOptionBox.row().split(factor=0.5, align=True)
                        row.prop(raw_object_modifier, "thickness")
                        row.prop(raw_object_modifier, "offset")



                    if (raw_object_modifier.type == "SHRINKWRAP"):
                        row = ModifierOptionBox.row().split(factor=0.5, align=True)
                        row.prop(raw_object_modifier, "target", text="")
                        row.prop(raw_object_modifier, "vertex_group", text="")

                        row = ModifierOptionBox.row().split(factor=0.5, align=True)
                        row.prop(raw_object_modifier, "wrap_method", text="")
                        row.prop(raw_object_modifier, "wrap_mode", text="")




                    if (raw_object_modifier.type == "DISPLACE"):
                        row = ModifierOptionBox.row().split(factor=0.034)
                        row.separator()

                        options_layout = row.box()
                        row = options_layout.row()
                        row.prop(raw_object_modifier, "strength")
                        row.prop(raw_object_modifier, "mid_level")



                modifier_header.prop(raw_object_modifier, "name", text="", icon=icon_name, emboss=True)

                modifier_header.prop(raw_object_modifier, "show_in_editmode", text="", emboss=True)
                modifier_header.prop(raw_object_modifier, "show_viewport", text="", emboss=True)
                modifier_header.prop(raw_object_modifier, "show_render", text="", emboss=True)

                modifier_move_up_button : Alx_OT_Modifier_ManageOnSelected = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_UP")
                modifier_move_up_button.object_pointer_reference = item.ObjectPointer.name
                modifier_move_up_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
                modifier_move_up_button.create_modifier = False
                modifier_move_up_button.apply_modifier = False
                modifier_move_up_button.remove_modifier = False
                modifier_move_up_button.move_modifier_up = True
                modifier_move_up_button.move_modifier_down = False

                modifier_move_down_button = modifier_header.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, icon="TRIA_DOWN")
                modifier_move_down_button.object_pointer_reference = item.ObjectPointer.name
                modifier_move_down_button.object_modifier_index = item.ObjectPointer.modifiers.find(raw_object_modifier.name)
                modifier_move_down_button.create_modifier = False
                modifier_move_down_button.apply_modifier = False
                modifier_move_down_button.remove_modifier = False
                modifier_move_down_button.move_modifier_up = False
                modifier_move_down_button.move_modifier_down = True

                    

        LayoutBox.row().separator(factor=2.0)

class Alx_PT_Panel_AlexandriaGeneralPanel(bpy.types.Panel):
    """"""

    bl_label = "Alexandria General Panel"
    bl_idname = "ALX_PT_panel_alexandria_general_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    
    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context: bpy.types.Context):
        AlxContextObject = AlxRetrieveContextObject(context)
        AlxContextArmature = AlxRetrieveContextArmature(context)

        GeneralPanelProperties : Alx_PG_PropertyGroup_AlexandriaGeneral = context.scene.alx_panel_alexandria_general_properties
        SceneIsolatorProperties : Alx_Tool_SceneIsolator_Properties = context.scene.alx_tool_scene_isolator_properties

        self.layout.ui_units_x = 25.0



        layout = self.layout.column()
        header_layout = layout.column()
        main_layout = layout.row()
        


        tabs = main_layout.column().prop(GeneralPanelProperties, "panel_tabs", icon_only=True, expand=True, emboss=False)
        tabs_panels = main_layout.column()


        pose_prop = header_layout.column()
        if (AlxContextArmature is not None):
            pose_prop.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)
        else:
            pose_prop.label(text="[Armature] [Missing]")
        pose_prop.separator()


        isolator_box = header_layout.column()
        isolator_row = isolator_box.row()
        isolator_l_column = isolator_row.column()
        isolator_r_column= isolator_row.column()

        isolatior_options = isolator_l_column.row()
        isolatior_options.column().prop(SceneIsolatorProperties, "scene_isolator_type_target", expand=True)
        isolatior_options.column().prop(SceneIsolatorProperties, "scene_isolator_visibility_target", expand=True)
        

        isolator_show_hide = isolator_l_column.row()
        isolator_hide : Alx_OT_Scene_VisibilityIsolator = isolator_show_hide.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="HIDE_ON", emboss=True)
        isolator_hide.PanicReset = False
        isolator_hide.TargetVisibility = False

        isolator_show : Alx_OT_Scene_VisibilityIsolator = isolator_show_hide.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="HIDE_OFF", emboss=True)
        isolator_show.PanicReset = False
        isolator_show.TargetVisibility = True

        isolator_r_column.scale_y = 3.1
        isolator_panik : Alx_OT_Scene_VisibilityIsolator = isolator_r_column.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="", icon="LOOP_BACK", emboss=True)
        isolator_panik.PanicReset = True

        isolator_box.separator()


        overlay_column = header_layout.column(align=True)
        overlay_prop = overlay_column.row(align=True)
        overlay_prop.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
        overlay_prop.prop(context.area.spaces.active.shading, "show_xray", text="Mesh", icon="XRAY")
        overlay_prop.prop(context.space_data.overlay, "show_xray_bone", text="Bone", icon="XRAY")
        overlay_prop.prop(context.area.spaces.active.shading, "type", text="", expand=True)
        poly_prop = header_layout.row(align=True)
        poly_prop.prop(context.space_data.overlay, "show_face_orientation", text="", icon="NORMALS_FACE")
        poly_prop.prop(context.space_data.overlay, "show_wireframes", text="Wireframe", icon="MOD_WIREFRAME")
        poly_prop.prop(context.space_data.overlay, "show_retopology", text="Retopology", icon="MESH_GRID")
        
        header_layout.separator()

        if (GeneralPanelProperties.panel_tabs == "OBJECT"):
            ObjectTabBox = tabs_panels.column()

            ObjectTabBox.template_list(Alx_UL_UIList_ObjectSelectionProperties.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index", type="GRID", columns=2)



        if (GeneralPanelProperties.panel_tabs == "ARMATURE"):
            ArmatureTabBox = tabs_panels.column()

            if (AlxContextArmature is not None):
                armature_display_options = ArmatureTabBox.column()
                armature_display_options.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "display_type", expand=True)
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_names", text="names")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_bone_custom_shapes", text="custom shapes")
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_bone_colors", text="colors")
                
            
                armature_display_options.prop(bpy.data.armatures.get(AlxContextArmature.data.name), "show_axes", text="axis")
                


        if (GeneralPanelProperties.panel_tabs == "MODIFIER"):
            ModifierTabBox = tabs_panels.column()

            modifier_tab_box_header = ModifierTabBox.row().split(factor=0.33)

            modifier_tab_box_header.separator()
            modifier_tab_box_header.popover(Alx_PT_AlexandriaModifierPanel.bl_idname, text="Create Modifier")
            modifier_tab_box_header.separator()

            ModifierTabBox.operator(Alx_OT_Modifier_ApplyReplace.bl_idname, text="Apply-Replace Modifier")
            ModifierTabBox.operator(Alx_OT_Modifier_BatchVisibility.bl_idname, text="Batch Visibility")

            ModifierTabBox.row().template_list(Alx_UL_UIList_ObjectSelectionModifiers.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_modifier", active_dataptr=context.scene, active_propname="alx_object_selection_modifier_index", maxrows=3)
            

        if (GeneralPanelProperties.panel_tabs == "ALXOPERATORS"):
            AlxOperatorsTabBox = tabs_panels.column()

            AlxOperatorsTabBox.operator(Alx_OT_VXGroupBySeams.bl_idname, text="VxGroup - group/mask by seam")

            AlxOperatorsTabBox.operator(Alx_OT_Mesh_VertexGroup_Clean.bl_idname, text="Cleaner - VXGroups")
            

            AlxOperatorsTabBox.operator(Alx_OT_Object_BatchMaterial.bl_idname, text="Batch Material")
            AlxOperatorsTabBox.operator(Alx_OT_Sculpt_ConditionMasking.bl_idname, text="mask by condition")
            
            AlxOperatorsTabBox.operator(Alx_OT_UVExtractIsland.bl_idname, text="UV - Extract islands")
            AlxOperatorsTabBox.row().operator(Alx_OT_Shapekey_TransferShapekeysToTarget.bl_idname, text="Transfer Shapekeys")

            AlxOperatorsTabBox.operator(Alx_OT_Armature_BoneChainOnSelection.bl_idname, text="Hair - Bone chain on edge strip")
            AlxOperatorsTabBox.row().operator(Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="Symmetrize IK")



        if (GeneralPanelProperties.panel_tabs == "RENDER"):
            RenderTabBox = tabs_panels.column()

            render_engine_option = RenderTabBox.row()
            render_engine_option.prop(context.scene.render, "engine", text="")
            render_engine_option.prop(context.area.spaces.active.shading, "type", text="", expand=True)


            if (context.area.spaces.active.shading.type == "SOLID"):
                matcap_preview = RenderTabBox.column()
                matcap_preview.row().prop(context.area.spaces.active.shading, "light", expand=True)

                material_display = matcap_preview.row().split(factor=0.5)

                material_display.template_icon_view(context.area.spaces.active.shading, "studio_light", scale=3.2)
                material_display.grid_flow(columns=2, align=True).prop(context.area.spaces.active.shading, "color_type", expand=True)


            if (context.area.spaces.active.shading.type == "MATERIAL"):
                scene_shading_options = RenderTabBox.column()
                
                if (context.area.spaces.active.shading.use_scene_world == False):
                    material_preview = scene_shading_options.row().split(factor=0.5)
                    material_preview.template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
                    scene_world_shading = material_preview.column()
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="rotation")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_intensity", text="intensity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="opacity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="blur")

                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_lights", text="scene lights")
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_world", text="scene world")

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
                

                if (context.area.spaces.active.shading.use_scene_world_render == False):
                    material_preview = scene_shading_options.row().split(factor=0.5)
                    material_preview.template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
                    scene_world_shading = material_preview.column()
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="rotation")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_intensity", text="intensity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="opacity")
                    scene_world_shading.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="blur")

                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_lights_render", text="scene lights")
                scene_shading_options.prop(context.area.spaces.active.shading, "use_scene_world_render", text="scene world")

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


        if (GeneralPanelProperties.panel_tabs == "UI_DESIGNER"):
            AlxUIDesignerTabBox = tabs_panels.column()

            AlxUIDesignerTabBox.row().operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="UI Designer")
        
            #AreaUITypeSelector.template_header()
            # 

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

        if (GeneralPanelProperties.panel_tabs == "SETTINGS"):
            AlxSettingsTabBox = tabs_panels.column()

            #AlxSettingsTabBox.operator("script.reload", text="reload scripts")
        #     AlxSpace = LayoutSpace.box().row()

            


        # ScenePropertyColumn.row().prop(context.space_data.overlay, "show_stats", text="Statistics", toggle=True)
       

        
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        

        
        #         ScenePropertyColumn.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")


        
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Mesh_EditAttributes.bl_idname, text="Edit Attributes")
        # 

LABEL = "LABEL_"
SEPARATOR = "SEPARATOR"

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
        AlxLayout.ui_units_x = 40.0
        
        ModifierLayout = AlxLayout.row()
        
        modifier_columns = [
            [
            LABEL + "data:",
            "DATA_TRANSFER",
            "MESH_CACHE",
            "MESH_SEQUENCE_CACHE",
            SEPARATOR + "3.4",
            SEPARATOR + "3.4",
        
            LABEL + "normals:",
            "NORMAL_EDIT",
            "WEIGHTED_NORMAL",

            LABEL + "UVs:",
            "UV_PROJECT",
            "UV_WARP",
            SEPARATOR + "1",
            ],
            
            [
            LABEL + "instances:",
            "MIRROR",
            "ARRAY",
            "BUILD",
            "SKIN",
            SEPARATOR + "3.4",

            LABEL + "edit:",
            "BEVEL",
            "BOOLEAN",
            "EDGE_SPLIT",
            "WELD",
            "MASK",
            "SOLIDIFY",
            "WIREFRAME",
            "SCREW",
            ],

            [
            LABEL + "resolution:",
            "SUBSURF",
            "MULTIRES",
            "TRIANGULATE",
            "DECIMATE",
            "REMESH",
            
            LABEL + "deform:",
            "ARMATURE",
            "SURFACE_DEFORM",
            "MESH_DEFORM",
            "LAPLACIANDEFORM",
            "LATTICE",
            "CURVE",
            

            LABEL + "displace:",
            "SHRINKWRAP",
            "DISPLACE",
            "SMOOTH",
            "CORRECTIVE_SMOOTH",
            "LAPLACIANSMOOTH"
            ]
        ]


        for modifier_column in modifier_columns:
            modifier_space = ModifierLayout.column()

            for Modifier in modifier_column:

                if (Modifier[0:6] == "LABEL_"):
                    modifier_space.label(text=Modifier[6:])

                if (Modifier[0:9] == "SEPARATOR"):
                    modifier_space.separator(factor= float(Modifier[9:]) )

                if (Modifier[0:6] != "LABEL_") and (Modifier[0:9] != "SEPARATOR"):
                    mod_name = bpy.types.Modifier.bl_rna.properties['type'].enum_items[Modifier].name
                    mod_icon = bpy.types.Modifier.bl_rna.properties['type'].enum_items[Modifier].icon
                    mod_identifier = bpy.types.Modifier.bl_rna.properties['type'].enum_items[Modifier].identifier

                    modifier_button = modifier_space.operator(Alx_OT_Modifier_ManageOnSelected.bl_idname, text=mod_name, icon=mod_icon)
                    modifier_button.modifier_type = mod_identifier
                    modifier_button.create_modifier = True
                    modifier_button.remove_modifier = False


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
        pivot_column.prop(context.scene.transform_orientation_slots[0], "type", expand=True)
        pivot_column.prop(context.tool_settings, "transform_pivot_point", expand=True)
        pivot_column.prop(context.space_data.overlay, "grid_scale")
        pivot_column.prop(context.space_data.overlay, "grid_subdivisions")

        pivot_column.operator(Alx_OT_Object_UnlockedQOrigin.bl_idname, text="Q-Origin")

        snapping_column = PivotLayout.column()

        if (bpy.app.version[0] == 3):
            snapping_column.prop(context.tool_settings, "snap_elements", expand=True)

        if ((bpy.app.version[0] == 4) and (bpy.app.version[1] in [0, 1, 2])):
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