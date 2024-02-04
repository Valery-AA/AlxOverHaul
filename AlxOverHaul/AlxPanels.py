import bpy
from bpy_extras import node_utils

from .AlxUtils import AlxCheckBlenderVersion, AlxRetrieveContextObject, AlxRetrieveContextArmature
from .AlxOperators import Alx_OT_Scene_VisibilityIsolator, Alx_OT_Mode_UnlockedModes, Alx_OT_UI_SimpleDesigner

class ObjectSelectionListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

class Alx_UL_Object_PropertiesList(bpy.types.UIList):
    """"""

    bl_idname = "alx_ui_list_object_properties_list"

    def draw_item(self, context: bpy.types.Context, layout: bpy.types.UILayout, data: bpy.types.AnyType, item: bpy.types.AnyType, icon: int, active_data: bpy.types.AnyType, active_property: str, index: int = 0, flt_flag: int = 0):

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

class Alx_PT_AlexandriaNPanel(bpy.types.Panel):
    """"""

    bl_label = "Alx Compound Tools"
    bl_idname = "alx_panel_alexandria_side_menu"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Alx3D"

    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context.area.type == "VIEW_3D"
    
    def draw(self, context: bpy.types.Context):
        AlxLayout = self.layout

class Alx_PT_AlexandriaGeneralPanel(bpy.types.Panel):
    """"""

    bl_label = "Alexandria Tool Panel"
    bl_idname = "alx_panel_alexandria_tool"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context: bpy.types.Context):
        AlxContextObject = None
        AlxContextArmature = AlxRetrieveContextArmature(context)
        AlxVerifiedContextObject = None

        AddonProperties = context.scene.alx_addon_properties
        PanelProperties = context.scene.alx_general_panel_properties

        AlxLayout = self.layout
        AlxLayout.ui_units_x = 30.0 * PanelProperties.alx_panel_scale_x
        AlxLayout.scale_y = PanelProperties.alx_panel_scale_y
        
        
        
        PanelProperties = context.scene.alx_general_panel_properties
        AlxLayout.row().prop(PanelProperties, "alx_panel_tab", expand=True)

        if (context.scene.alx_general_panel_properties.alx_panel_tab == "HOME") and (context.area.type == "VIEW_3D"):
            AlxSpace = AlxLayout.box().row().split(factor=0.5)

            # Alx Visibility
            AlxOPS_VisibilityBox = AlxSpace.box()

            if (AlxContextArmature is not None):
                AlxOPS_VisibilityBox.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)
            else:
                AlxOPS_VisibilityBox.row().label(text="Context Object Missing [Armature]")

            # AlxOPS Isolator
            AlxOPS_IsolatorSpace = AlxOPS_VisibilityBox.box()

            AlxOPS_IsolatorSpace.row().label(text="Isolator:")
            AlxOPS_IsolatorSpace_Options = AlxOPS_IsolatorSpace.row().split(factor=0.5)
            AddonProperties = context.scene.alx_addon_properties
            AlxOPS_IsolatorSpace_Options.prop(AddonProperties, "scene_isolator_visibility_target", expand=True)
            AlxOPS_IsolatorSpace_Options.prop(AddonProperties, "scene_isolator_type_target", expand=True)

            AlxOPS_IsolatorSpace_Visibility = AlxOPS_IsolatorSpace.row().split(factor=0.33, align=True)
            AlxOPS_Isolator_Panik = AlxOPS_IsolatorSpace_Visibility.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Reset", icon="ERROR", emboss=True)
            AlxOPS_Isolator_Panik.Panik = True
            AlxOPS_Isolator_Isolate = AlxOPS_IsolatorSpace_Visibility.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="HIDE_ON", emboss=True)
            AlxOPS_Isolator_Isolate.Panik = False
            AlxOPS_Isolator_Isolate.TargetVisibility = False
            AlxOPS_Isolator_Show = AlxOPS_IsolatorSpace_Visibility.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="HIDE_OFF", emboss=True)
            AlxOPS_Isolator_Show.Panik = False
            AlxOPS_Isolator_Show.TargetVisibility = True

            # AlxProp Overlay
            AlxOPS_OverlaySpace = AlxOPS_VisibilityBox.box()

            AlxOPS_OverlaySpace.row().label(text="Overlay:")
            AlxOPS_Overlay = AlxOPS_OverlaySpace.row().split(factor=0.5, align=False)

            AlxOverlay_XRay = AlxOPS_Overlay.column(align=True)
            AlxOverlay_XRay.prop(context.area.spaces.active.shading, "show_xray", text="Mesh", icon="XRAY")
            AlxOverlay_XRay.prop(context.space_data.overlay, "show_xray_bone", text="Bone", icon="BONE_DATA")

            AlxOverlay_Shading = AlxOPS_Overlay.column(align=True)
            AlxOverlay_Shading.prop(context.space_data.overlay, "show_retopology", text="Retopology", icon="MESH_GRID")
            AlxOverlay_Shading.prop(context.space_data.overlay, "show_wireframes", text="Wireframe", icon="MOD_WIREFRAME")

            AlxOverlay_Options = AlxOPS_OverlaySpace.row().split(factor=0.25, align=True)
            AlxOverlay_Options.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
            AlxOverlay_Options.prop(context.space_data.overlay, "show_annotation", text="Annotations", icon="HIDE_OFF", toggle=True)
            AlxOverlay_Options.prop(context.space_data.overlay, "show_face_orientation", text="Normals", icon="HIDE_OFF", toggle=True)

        if (context.scene.alx_general_panel_properties.alx_panel_tab == "OBJECT") and (context.area.type == "VIEW_3D"):
            AlxSpace = AlxLayout.box().row().split(factor=0.5)

            ObjectPropertyColumn = AlxSpace.column()
            ObjectPropertyColumn.template_list(Alx_UL_Object_PropertiesList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")

        if (context.scene.alx_general_panel_properties.alx_panel_tab == "RENDER") and (context.area.type == "VIEW_3D"):
            AlxSpace = AlxLayout.box().row().split(factor=0.5)

            RenderSpace =  AlxSpace.box()

            RenderEngineBox = RenderSpace.box()
            PreviewSettingsBox = RenderSpace.box()

            RenderEngineSelection = RenderEngineBox.row()
            RenderEngineSelection.prop(context.scene.render, "engine", text="")
            RenderEngineSelection.prop(context.area.spaces.active.shading, "type", text="", expand=True)

            if (context.scene.render.engine in ["BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"]):
                EeveeViewportSampleRow = RenderEngineBox.row(align=True).split(factor=0.30)
                EeveeViewportSampleRow.prop(context.scene.eevee, "use_taa_reprojection", text="Denoise")
                EeveeViewportSampleRow.prop(context.scene.eevee, "taa_samples", text="Viewport")
                EeveeRenderSampleRow = RenderEngineBox.row(align=True).split(factor=0.30)
                EeveeRenderSampleRow.separator()
                EeveeRenderSampleRow.prop(context.scene.eevee, "taa_render_samples", text="Render")

            if (context.area.spaces.active.shading.type == "SOLID"):
                HDRI_Row = PreviewSettingsBox.row().split(factor=0.4)
                MatcapColumn = HDRI_Row.column()
                MatcapColumn.row().prop(context.area.spaces.active.shading, "light", text="")
                MatcapColumn.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=3.2, scale_popup=3.0)
                HDRI_ColorTypeColumn = HDRI_Row.column()
                HDRI_ColorTypeColumn.row().grid_flow(columns=2, align=True).prop(context.area.spaces.active.shading, "color_type", expand=True)
                HDRI_ColorTypeColumn.row().prop(context.area.spaces.active.shading, "single_color", text="")

            if (context.area.spaces.active.shading.type in ["MATERIAL", "RENDERED"]):
                SceneToggleRow = PreviewSettingsBox.row()
                SceneToggleRow.prop(context.area.spaces.active.shading, "use_scene_lights", text="Scene Lights")
                SceneToggleRow.prop(context.area.spaces.active.shading, "use_scene_world", text="Scene World")
                if (context.area.spaces.active.shading.use_scene_world == False):
                    HDRI_Row = PreviewSettingsBox.row().split(factor=0.4)
                    HDRI_Row.row().template_icon_view(context.area.spaces.active.shading, "studio_light", scale=4.3, scale_popup=3.0)
                    MaterialOptions = HDRI_Row.column()
                    MaterialOptions.prop(context.area.spaces.active.shading, "studiolight_rotate_z", text="Rotation")
                    MaterialOptions.prop(context.area.spaces.active.shading, "studiolight_intensity", text="Intensity")
                    MaterialOptions.prop(context.area.spaces.active.shading, "studiolight_background_alpha", text="Opacity")
                    MaterialOptions.prop(context.area.spaces.active.shading, "studiolight_background_blur", text="Opacity")

                if (context.area.spaces.active.shading.use_scene_world == True):
                    
                    PreviewSettingsBox.row().prop(context.scene.world, "use_nodes", text="Use Scene World Nodes", toggle=True)

                    if (context.scene.world.use_nodes == True):
                        if (context.scene.world.node_tree is not None):
                            WorldMaterial = context.scene.world.node_tree
                            MaterialOutput = context.scene.world.node_tree.get_output_node("ALL")
                            Surface = node_utils.find_node_input(MaterialOutput, "Surface")
                            PreviewSettingsBox.column().template_node_view(WorldMaterial, MaterialOutput, Surface)



            #RenderEngineSpace.row().prop(context.area.spaces.active.shading, "show_backface_culling")



            # if (context.scene.render.engine == "CYCLES"):
            #     CyclesSampleRow = RenderEngineSpace.row(align=True)
            #     CyclesSampleRow.prop(context.scene.cycles, "preview_samples", text="Viewport")
            #     CyclesSampleRow.prop(context.scene.cycles, "samples", text="Render")



            TimelineFrameSpace = AlxSpace.box()

            TimelineFrameSpace.prop(bpy.context.scene, "frame_current", text="Frame")

            FrameRow = TimelineFrameSpace.row().split(factor=0.5, align=True)
            FrameRow.prop(bpy.context.scene, "frame_start", text="Start")
            FrameRow.prop(bpy.context.scene, "frame_end", text="End")

        if (context.scene.alx_general_panel_properties.alx_panel_tab == "UI_DESIGNER"):
            AlxSpace = AlxLayout.box().row().split(factor=0.5)

            AlxSpace.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="Viewport").AreaTypeTarget = "VIEW_3D"
            AlxSpace.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="Outliner").AreaTypeTarget = "OUTLINER"
            AlxSpace.operator(Alx_OT_UI_SimpleDesigner.bl_idname, text="Properties").AreaTypeTarget = "PROPERTIES"
            
            



        if (context.scene.alx_general_panel_properties.alx_panel_tab == "SETTINGS"):
            AlxSpace = AlxLayout.box().row().split(factor=0.5)

            PanelSettingSpace = AlxSpace.box()
            PanelSettingSpace.row().prop(PanelProperties, "alx_panel_scale_x", text="Panel Width")
            PanelSettingSpace.row().prop(PanelProperties, "alx_panel_scale_y", text="Panel Height")
            




        # ObjectPropertyColumn = PropertySplit.column()
        # ObjectPropertyColumn.template_list(Alx_UL_Object_PropertiesList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")

        # ScenePropertyColumn = PropertySplit.column()
        # ScenePropertyColumn.scale_x = 1

        # ScenePropertyColumn.row().prop(context.space_data.overlay, "show_stats", text="Statistics", toggle=True)
       

        
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        

        
        #         ScenePropertyColumn.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
        #         ScenePropertyColumn.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")

        # MMenuSectionR = RMenuColumnSpace.row().box()
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Modifier_ManageOnSelected.bl_idname, text="Create Modifier")
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Mesh_EditAttributes.bl_idname, text="Edit Attributes")
        # MMenuSectionR.row().operator(AlxOperators.Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="Symmetrize IK")

class Alx_PT_AlexandriaRenderPanel(bpy.types.Panel):
    """"""

    bl_label = "Alexandria Render Panel"
    bl_idname = "alx_panel_alexandria_render"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    bl_options = {"INSTANCED"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context.area.type == "VIEW_3D"
    
    def draw(self, context: bpy.types.Context):
        AlxLayout = self.layout
        AlxLayout.ui_units_x = 20
        
        

class Alx_PT_AlexandriaObjectToolsPanel(bpy.types.Panel):
    """"""

    bl_label = "Alexandria Render Panel"
    bl_idname = "alx_panel_alexandria_object_tools"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    bl_options = {"INSTANCED"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context.area.type == "VIEW_3D"
    
    def draw(self, context: bpy.types.Context):
        AlxLayout = self.layout
        AlxLayout.ui_units_x = 15.0

        if (context.active_object is not None) and (context.active_object.type == "MESH"):
            if (AlxCheckBlenderVersion([4], [0]) or AlxCheckBlenderVersion([3])):
                AlxPROPS_MESH_Smooth = AlxLayout.row().split(factor=0.25, align=True)
            if (AlxCheckBlenderVersion([4], [1])):
                AlxPROPS_MESH_Smooth = AlxLayout.row().split(factor=0.5, align=True)

            AlxPROPS_MESH_Smooth.operator("object.shade_smooth", text="Smooth", emboss=True)

            if (AlxCheckBlenderVersion([4], [0]) or AlxCheckBlenderVersion([3])):
                AlxPROPS_MESH_Smooth.operator("object.shade_smooth", text="A-Smooth", emboss=True).use_auto_smooth = True
                AlxPROPS_MESH_Smooth.prop(context.active_object.data, "auto_smooth_angle", text="A-SA", toggle=True)
            AlxPROPS_MESH_Smooth.operator("object.shade_flat", text="Flat", emboss=True)

        if (context.active_object is not None):
            if (context.active_object.type == "MESH"):
                ObjectBox = AlxLayout.box().split(factor=0.5)

                ObjectOptionsBox = ObjectBox.box()
                ObjectOptionsBox.label(text="Mesh:")
                AlxEditMirror = ObjectOptionsBox.row(align=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_x", text="X", toggle=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_y", text="Y", toggle=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_z", text="Z", toggle=True)
                ObjectOptionsBox.row().prop(context.active_object.data, "use_mirror_topology", text="Topology", icon="MESH_GRID", toggle=True)

                ObjectWPOptionsBox = ObjectBox.box()
                ObjectWPOptionsBox.label(text="Weigth Paint:")
                AlxWeightMirror = ObjectWPOptionsBox.row(align=True)
                AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_x", text="X", toggle=True)
                AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_y", text="Y", toggle=True)
                AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_z", text="Z", toggle=True)
                ObjectWPOptionsBox.row().prop(bpy.context.active_object.data, "use_mirror_topology", text="Topology", icon="MESH_GRID", expand=True)
                ObjectWPOptionsBox.row().prop(bpy.context.active_object.data, "use_mirror_vertex_groups", text="Vx Groups", icon="GROUP_VERTEX")
                
            if (context.active_object is not None):
                if (context.active_object.type == "ARMATURE"):
                    ArmatureBox = AlxLayout.row().box()
                    ArmatureBox.label(text="Pose:")
                    AlxPoseMirror = ArmatureBox.row(align=True)
                    AlxPoseMirror.prop(context.active_object.pose, "use_mirror_x", text="X Mirror", toggle=True)
                    AlxPoseMirror.prop(context.active_object.pose, "use_mirror_relative", text="Local Mirror", toggle=True)
                    ArmatureBox.row().prop(context.active_object.pose, "use_auto_ik", text="Auto IK", icon="CON_KINEMATIC")


class Alx_PT_Scene_GeneralPivot(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "alx_panel_scene_general_pivot"

    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "AlxInternal"

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
                        SnapMenuSection = AlxLayoutRow.box()

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



class Alx_MT_UnlockedModesPie(bpy.types.Menu):
    """"""

    bl_label = ""
    bl_idname = "alx_menu_unlocked_modes"

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
            PoseMBox = PieUI.box()
            if (context.mode == "POSE"):
                PoseMBox.label(text="[Mode] | [Pose]")
            else:
                if (AlxContextArmature is None):
                    PoseMBox.label(text="[Active Mesh] [Missing] [Armature]")

        if (context.mode != "PAINT_WEIGHT") and (AlxContextObject is not None) and (AlxContextArmature is not None):
            AlxOPS_AutoMode_WEIGHT = PieUI.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="A-WPAINT", icon="WPAINT_HLT")
            AlxOPS_AutoMode_WEIGHT.DefaultBehaviour = False
            AlxOPS_AutoMode_WEIGHT.TargetMode = "PAINT_WEIGHT"
            AlxOPS_AutoMode_WEIGHT.TargetObject = AlxRetrieveContextObject(context=context).name
            AlxOPS_AutoMode_WEIGHT.TargetArmature = AlxContextArmature.name
        else:
            WeightPaintMBox = PieUI.box()
            if (context.mode == "PAINT_WEIGHT"):
                WeightPaintMBox.label(text="[Mode] | [Weight Paint]")
            else:
                if (AlxContextObject is None): 
                    WeightPaintMBox.row().label(text="[Active Object] [Incorrect] | [Mesh] [Only]")
                if (AlxContextArmature is None):
                    WeightPaintMBox.row().label(text="[Active Mesh] [Missing] [Armature]")
        
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



class Alx_PT_Modifier_CreationList(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = ""

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        AlxLayout = self.layout

        #AlxLayout.row().operator(Alx_OT_Modifier_ManageOnSelected, text="Create Modifier")