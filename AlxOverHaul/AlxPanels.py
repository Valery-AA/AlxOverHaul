import bpy
from bpy.types import AnyType, Context, UILayout

from AlxOverHaul import AlxOperators, AlxUtils

class ObjectPropertiesListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

class ObjectModifiersListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

class Alx_UL_Object_PropertiesList(bpy.types.UIList):
    """"""

    bl_idname = "alx_ui_list_object_properties_list"

    def draw_item(self, context: Context, layout: UILayout, data: AnyType, item: AnyType, icon: int, active_data: AnyType, active_property: str, index: int = 0, flt_flag: int = 0):
        ItemBox = layout.box()
        UISplit = ItemBox.row().split(factor=0.5, align=False)

        NameRow = UISplit.row()
        PropertiesRow = UISplit.row().split(factor=0.25, align=True)

        NameRow.prop(item.ObjectPointer, "name", text="", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_name", text="", icon="SORTALPHA", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_axis", text="", icon="EMPTY_ARROWS", emboss=True)
        if (item.ObjectPointer.type == "MESH"):
            PropertiesRow.prop(item.ObjectPointer, "show_wire", text="", icon="MOD_WIREFRAME", emboss=True)
        PropertiesRow.prop(item.ObjectPointer, "show_in_front", text="", icon="OBJECT_HIDDEN", emboss=True)

class Alx_PT_AlexandriaToolPanel(bpy.types.Panel):
    bl_label = "Alexandria Tool Panel"
    bl_idname = "alx_panel_alexandria_tool"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def draw(self, context):
        AlxLayout = self.layout
        AlxLayout.ui_units_x = 50.0
        AlexandriaToolPanel = AlxLayout.grid_flow(columns=2, align=False)

        AlxContextObject = None
        AlxContextArmature = AlxUtils.AlxRetrieveContextArmature(context)
        AlxVerifiedContextObject = None



        LMenuColumnSpace = AlexandriaToolPanel.box()
        RMenuColumnSpace = AlexandriaToolPanel.box()

        TMenuSectionL = LMenuColumnSpace.row().box()
        TMenuSectionL.scale_x = 2.0

        if (AlxContextArmature is not None):
            TMenuSectionL.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)
        else:
            TMenuSectionL.row().label(text="Context Object Missing [Armature]")

        AddonProperties = context.scene.alx_addon_properties
        TMenuSectionL.row().prop(AddonProperties, "SceneIsolatorVisibilityTarget", expand=True)
        AlxOPS_OBJECT_Isolator = TMenuSectionL.row().split(factor=0.25, align=True)
        AlxOPS_OBJECT_Isolator_Isolate = AlxOPS_OBJECT_Isolator.operator(AlxOperators.Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="OBJECT_DATA", emboss=True)
        AlxOPS_OBJECT_Isolator_Isolate.TargetVisibility = False
        AlxOPS_OBJECT_Isolator_Isolate.UseObject = True
        AlxOPS_OBJECT_Isolator_Isolate.UseCollection = False

        AlxOPS_OBJECT_Isolator_ShowAll = AlxOPS_OBJECT_Isolator.operator(AlxOperators.Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="OBJECT_DATA", emboss=True)
        AlxOPS_OBJECT_Isolator_ShowAll.TargetVisibility = True
        AlxOPS_OBJECT_Isolator_ShowAll.UseObject = True
        AlxOPS_OBJECT_Isolator_ShowAll.UseCollection = False

        AlxOPS_COLLECTION_Isolator_Isolate = AlxOPS_OBJECT_Isolator.operator(AlxOperators.Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="OUTLINER_COLLECTION", emboss=True)
        AlxOPS_COLLECTION_Isolator_Isolate.TargetVisibility = False
        AlxOPS_COLLECTION_Isolator_Isolate.UseObject = False
        AlxOPS_COLLECTION_Isolator_Isolate.UseCollection = True

        AlxOPS_COLLECTION_Isolator_ShowAll = AlxOPS_OBJECT_Isolator.operator(AlxOperators.Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="OUTLINER_COLLECTION", emboss=True)
        AlxOPS_COLLECTION_Isolator_ShowAll.TargetVisibility = True
        AlxOPS_COLLECTION_Isolator_ShowAll.UseObject = False
        AlxOPS_COLLECTION_Isolator_ShowAll.UseCollection = True

        AlxOverlayShading = TMenuSectionL.row().split(factor=0.20, align=True)
        AlxOverlayShading.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
        AlxOverlayShading.prop(context.area.spaces.active.shading, "show_xray", text="Mesh", icon="XRAY")
        AlxOverlayShading.prop(context.space_data.overlay, "show_xray_bone", text="Bone", icon="XRAY")
        AlxOverlayShading.prop(context.space_data.overlay, "show_retopology", text="", icon="MESH_GRID")
        AlxOverlayShading.prop(context.space_data.overlay, "show_wireframes", text="", icon="MOD_WIREFRAME")
        
        if (context.active_object is not None) and (context.active_object.type == "MESH"):
            AlxPROPS_MESH_Smooth = TMenuSectionL.row().split(factor=0.25, align=True)
            AlxPROPS_MESH_Smooth.operator("object.shade_smooth", text="Smooth", emboss=True)
            AlxPROPS_MESH_Smooth.operator("object.shade_smooth", text="A-Smooth", emboss=True).use_auto_smooth = True
            AlxPROPS_MESH_Smooth.prop(context.active_object.data, "auto_smooth_angle", text="A-SA", toggle=True)
            AlxPROPS_MESH_Smooth.operator("object.shade_flat", text="Flat", emboss=True)

        TMenuSectionR = RMenuColumnSpace.row().box()

        EngineRow = TMenuSectionR.row()
        EngineRow.prop(context.scene.render, "engine", text="")
        EngineRow.prop(context.area.spaces.active.shading, "type", text="", expand=True)

        if (context.scene.render.engine == "BLENDER_EEVEE"):
            EeveeSampleRow = TMenuSectionR.row(align=True)
            EeveeSampleRow.prop(context.scene.eevee, "use_taa_reprojection", text="Denoise")
            EeveeSampleRow.prop(context.scene.eevee, "taa_samples", text="Viewport")
            EeveeSampleRow.prop(context.scene.eevee, "taa_render_samples", text="Render")
        
        if (context.scene.render.engine == "CYCLES"):
            CyclesSampleRow = TMenuSectionR.row(align=True)
            CyclesSampleRow.prop(context.scene.cycles, "preview_samples", text="Viewport")
            CyclesSampleRow.prop(context.scene.cycles, "samples", text="Render")

        FrameRow = TMenuSectionR.row(align=True)
        FrameRow.prop(bpy.context.scene, "frame_current", text="Frame")
        FrameRow.prop(bpy.context.scene, "frame_start", text="Start")
        FrameRow.prop(bpy.context.scene, "frame_end", text="End")

        if (context.scene.render.engine == "BLENDER_EEVEE") or (context.scene.render.engine == "CYCLES"):
            HDRIRow = TMenuSectionR.row()
            if (context.area.spaces.active.shading.type == "SOLID"):
                HDRIRow.prop(context.area.spaces.active.shading, "light")
            if (context.area.spaces.active.shading.light != "FLAT") and (context.area.spaces.active.shading.type != "WIREFRAME"):
                HDRIRow.prop(context.area.spaces.active.shading, "studio_light")
            if (context.area.spaces.active.shading.type == "SOLID"):
                TMenuSectionR.row().prop(context.area.spaces.active.shading, "color_type", expand=True)
 


        MMenuSectionL = LMenuColumnSpace.row().box()

        PropertySplit = MMenuSectionL.row()

        ObjectPropertyColumn = PropertySplit.column()
        ObjectPropertyColumn.template_list(Alx_UL_Object_PropertiesList.bl_idname, list_id="", dataptr=context.scene, propname="alx_object_selection_properties", active_dataptr=context.scene, active_propname="alx_object_selection_properties_index")

        ScenePropertyColumn = PropertySplit.column()
        ScenePropertyColumn.scale_x = 1

        ScenePropertyColumn.row().prop(context.space_data.overlay, "show_stats", text="Statistics", toggle=True)
        ScenePropertyColumn.row().prop(context.space_data.overlay, "show_face_orientation", text="Face Orientation", toggle=True)

        if (context.active_object is not None):
            if (context.active_object.type == "MESH"):
                ScenePropertyColumn.label(text="Mesh:")
                AlxEditMirror = ScenePropertyColumn.row(align=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_x", text="X", toggle=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_y", text="Y", toggle=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_z", text="Z", toggle=True)
                AlxEditMirror.prop(context.active_object.data, "use_mirror_topology", text="", icon="MESH_GRID", toggle=True)
                ScenePropertyColumn.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        if (context.active_object is not None):
            if (context.active_object.type == "ARMATURE"):
                ScenePropertyColumn.label(text="Pose:")
                AlxPoseMirror = ScenePropertyColumn.row(align=True)
                AlxPoseMirror.prop(context.active_object.pose, "use_mirror_x", text="X Mirror", toggle=True)
                AlxPoseMirror.prop(context.active_object.pose, "use_mirror_relative", text="Local Mirror", toggle=True)
                ScenePropertyColumn.row().prop(context.active_object.pose, "use_auto_ik", text="Auto IK", icon="CON_KINEMATIC")

        if (context.active_object is not None):
            if (context.active_object.type == "MESH"):
                ScenePropertyColumn.label(text="Weigth Paint:")
                AlxWeightMirror = ScenePropertyColumn.row(align=True)
                AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_x", text="X", toggle=True)
                AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_y", text="Y", toggle=True)
                AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_z", text="Z", toggle=True)
                AlxWeightMirror.prop(bpy.context.active_object.data, "use_mirror_vertex_groups",text="", icon="GROUP_VERTEX")
                AlxWeightMirror.prop(bpy.context.active_object.data, "use_mirror_topology",text="", icon="MESH_GRID", expand=True)
                ScenePropertyColumn.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
                ScenePropertyColumn.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")

        MMenuSectionR = RMenuColumnSpace.row().box()
        MMenuSectionR.row().operator(AlxOperators.Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="Symmetrize IK")

class Alx_PT_Scene_SubPanel(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "alx_panel_scene_sub_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        AlxLayout = self.layout



class Alx_PT_Object_SubPanel(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "alx_panel_Object_sub_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        AlxLayout = self.layout
        AlxLayout.ui_units_x = 20.0



class Alx_PT_Modifier_SubPanel(bpy.types.Menu):
    """"""

    bl_label = ""
    bl_idname = "alx_panel_modifier_sub_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        AlxLayout = self.layout

        AlxLayout.label(text="Test")

class Alx_MT_UnlockedModesPie(bpy.types.Menu):
    """"""

    bl_label = ""
    bl_idname = "alx_menu_unlocked_modes"

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        AlxLayout = self.layout

        AlxContextObject = AlxUtils.AlxRetrieveContextObject(context=context)
        AlxContextArmature = AlxUtils.AlxRetrieveContextArmature(context=context)

        PieUI = AlxLayout.menu_pie()

        AlxOPS_AutoMode_OBJECT = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="OBJECT", icon="OBJECT_DATAMODE")
        AlxOPS_AutoMode_OBJECT.DefaultBehaviour = True
        AlxOPS_AutoMode_OBJECT.TargetMode = "OBJECT"

        if (context.mode != "POSE") and (AlxContextArmature is not None):
            AlxOPS_AutoMode_POSE = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="A-POSE", icon="ARMATURE_DATA")
            AlxOPS_AutoMode_POSE.DefaultBehaviour = False
            AlxOPS_AutoMode_POSE.TargetMode = "POSE"
            AlxOPS_AutoMode_POSE.TargetArmature = AlxContextArmature.name
        else:
            if (context.mode == "POSE"):
                PieUI.row().label(text="Currently in Pose")
            else:
                PSBox = PieUI.box()
                if (AlxContextArmature is None):
                    PSBox.label(text="Context Object Missing [Armature]")

        if (context.mode != "PAINT_WEIGHT") and (AlxContextObject is not None) and (AlxContextArmature is not None):
            AlxOPS_AutoMode_WEIGHT = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="A-WPAINT", icon="WPAINT_HLT")
            AlxOPS_AutoMode_WEIGHT.DefaultBehaviour = False
            AlxOPS_AutoMode_WEIGHT.TargetMode = "PAINT_WEIGHT"
            AlxOPS_AutoMode_WEIGHT.TargetObject = AlxUtils.AlxRetrieveContextObject(context=context).name
            AlxOPS_AutoMode_WEIGHT.TargetArmature = AlxContextArmature.name
        else:
            if (context.mode == "PAINT_WEIGHT"):
                PieUI.row().label(text="Currently in WPaint")
            else:
                WPBox = PieUI.box()
                if (AlxContextObject is None): 
                    WPBox.row().label(text="Context Object Missing [Mesh]")
                if (AlxContextArmature is None):
                    WPBox.row().label(text="Context Object Missing [Armature]")
        
        if (AlxContextObject is not None):
            VertexMode = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="Edge", icon="EDGESEL")
            VertexMode.DefaultBehaviour = True
            VertexMode.TargetObject = AlxContextObject.name
            VertexMode.TargetMode = "EDIT"
            VertexMode.TargetSubMode = "EDGE"

            VertexMode = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="Vertex", icon="VERTEXSEL")
            VertexMode.DefaultBehaviour = True
            VertexMode.TargetObject = AlxContextObject.name
            VertexMode.TargetMode = "EDIT"
            VertexMode.TargetSubMode = "VERT"
            
            VertexMode = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="Face", icon="FACESEL")
            VertexMode.DefaultBehaviour = True
            VertexMode.TargetObject = AlxContextObject.name
            VertexMode.TargetMode = "EDIT"
            VertexMode.TargetSubMode = "FACE"
        else:
            if (context.active_object is not None) and (context.active_object.type != "MESH"):
                PieUI.box().row().label(text="Object is not a Mesh")
                PieUI.box().row().label(text="Object is not a Mesh")
                PieUI.box().row().label(text="Object is not a Mesh")
        
        if (context.active_object is not None) and (len(context.selected_objects) != 0):
            GeneralEditMode = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="General Edit", icon="EDITMODE_HLT")
            GeneralEditMode.DefaultBehaviour = True
            GeneralEditMode.TargetMode = "EDIT"
            
        if (context.active_object is not None) and (context.active_object.type == "MESH"):
            SculptMode = PieUI.operator(AlxOperators.Alx_OT_Mode_UnlockedModes.bl_idname, text="Sculpt", icon="SCULPTMODE_HLT")
            SculptMode.DefaultBehaviour = True
            SculptMode.TargetMode = "SCULPT"
        else:
            if (len(context.selectable_objects) == 0):
                PieUI.box().row().label(text="No Selection")

class Alx_PT_Scene_GeneralPivot(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "alx_panel_scene_general_pivot"

    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"

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

                        BottomOrientationColumn.prop(context.tool_settings, "snap_elements_base", expand=True)
                        BottomOrientationColumn.prop(context.tool_settings, "snap_elements_individual", expand=True)

                        SnapSelAct = SnapMenuSection.row().operator(AlxOperators.Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Selected To Active")
                        SnapSelAct.SourceSnapping = "ACTIVE"
                        SnapSelAct.TargetSnapping = "SELECTED"

                        SnapSelCur = SnapMenuSection.row().operator(AlxOperators.Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Selected To Cursor")
                        SnapSelCur.SourceSnapping = "SCENE_CURSOR"
                        SnapSelCur.TargetSnapping = "SELECTED"
                        SnapSelCur.SubTargetSnapping = "OBJECT"

                        SnapCurAct = SnapMenuSection.row().operator(AlxOperators.Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Cursor To Active")
                        SnapCurAct.SourceSnapping = "ACTIVE"
                        SnapCurAct.TargetSnapping = "SCENE_CURSOR"

                        SnapOriCur = SnapMenuSection.row().operator(AlxOperators.Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Origin To Cursor")
                        SnapOriCur.SourceSnapping = "SCENE_CURSOR"
                        SnapOriCur.TargetSnapping = "SELECTED"
                        SnapOriCur.SubTargetSnapping = "ORIGIN"

                        SnapCurRes = SnapMenuSection.row().operator(AlxOperators.Alx_OT_Scene_UnlockedSnapping.bl_idname, text="Reset Cursor")
                        SnapCurRes.SourceSnapping = "RESET"
                        SnapCurRes.TargetSnapping = "SCENE_CURSOR"

class Alx_PT_Modifier_ModManager(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "alx_panel_modifier_mod_manager"

    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"

    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        pass