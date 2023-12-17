import bpy

# class Alx_PT_AlexandriaToolPanel(bpy.types.Panel):
#     bl_label = "Alexandria Tool Panel"
#     bl_idname = "alx_panel_alexandria_tool"

#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     @classmethod
#     def poll(cls, context):
#         return True

#     def draw(self, context):
#         AlxLayout = self.layout
#         AlxLayout.ui_units_x = 55.0
#         AlexandriaToolPanel = AlxLayout.grid_flow(columns=3, even_columns=True, align=False)

#         AlxContextObject = None
#         AlxContextArmature = None
#         AlxVerifiedContextObject = None

#         if (context.active_object is not None):
#             if (context.active_object.type == "MESH"):
#                 if (context.active_object.find_armature() is not None):
#                     AlxContextArmature = context.active_object.find_armature()
#                 AlxContextObject = context.active_object
#             if (context.active_object.type == "ARMATURE") and (context.active_object is not None):
#                 AlxContextArmature = bpy.data.objects.get(context.active_object.name)



#         LMenuColumnSpace = AlexandriaToolPanel.box()
#         MMenuColumnSpace = AlexandriaToolPanel.box()
#         RMenuColumnSpace = AlexandriaToolPanel.box()

#         TMenuSectionL = LMenuColumnSpace.row().box()

#         if (bpy.context.mode == "EDIT_MESH") and (bpy.context.active_object.type == "MESH"):
#             AlxEditMirror = TMenuSectionL.row(align=True)
#             AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_x", text="X", toggle=True)
#             AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_y", text="Y", toggle=True)
#             AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_z", text="Z", toggle=True)
#             AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_topology", text="", icon="MESH_GRID", toggle=True)
#             TMenuSectionL.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

#         if (context.mode == "POSE"):
#             AlxPoseMirror = TMenuSectionL.row(align=True)
#             AlxPoseMirror.prop(context.active_object.pose, "use_mirror_x", text="X Mirror")
#             AlxPoseMirror.prop(context.active_object.pose, "use_mirror_relative", text="Local Mirror")
#             TMenuSectionL.row().prop(context.active_object.pose, "use_auto_ik", text="Auto IK", icon="CON_KINEMATIC")

#         if (context.mode == "PAINT_WEIGHT"):
#             AlxWeightMirror = TMenuSectionL.row(align=True)
#             AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_x", text="X", toggle=True)
#             AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_y", text="Y", toggle=True)
#             AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_z", text="Z", toggle=True)
#             AlxWeightMirror.prop(bpy.context.active_object.data, "use_mirror_vertex_groups",text="", icon="GROUP_VERTEX")
#             AlxWeightMirror.prop(bpy.context.active_object.data, "use_mirror_topology",text="", icon="MESH_GRID", expand=True)
#             TMenuSectionL.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
#             TMenuSectionL.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")

#         TMenuSectionM = MMenuColumnSpace.row().box()

#         if (AlxContextArmature is not None):
#             TMenuSectionM.row().prop(bpy.data.armatures.get(AlxContextArmature.data.name), "pose_position", expand=True)
#         else:
#             TMenuSectionM.row().label(text="Mesh Has No Armature")

#         AddonProperties = context.scene.alx_addon_properties
#         TMenuSectionM.row().prop(AddonProperties, "SceneIsolatorVisibilityTarget", expand=True)
#         AlxOPS_OBJECT_Isolator = TMenuSectionM.row().split(factor=0.25, align=True)
#         AlxOPS_OBJECT_Isolator_Isolate = AlxOPS_OBJECT_Isolator.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="OBJECT_DATA", emboss=True)
#         AlxOPS_OBJECT_Isolator_Isolate.TargetVisibility = False
#         AlxOPS_OBJECT_Isolator_Isolate.UseObject = True
#         AlxOPS_OBJECT_Isolator_Isolate.UseCollection = False

#         AlxOPS_OBJECT_Isolator_ShowAll = AlxOPS_OBJECT_Isolator.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="OBJECT_DATA", emboss=True)
#         AlxOPS_OBJECT_Isolator_ShowAll.TargetVisibility = True
#         AlxOPS_OBJECT_Isolator_ShowAll.UseObject = True
#         AlxOPS_OBJECT_Isolator_ShowAll.UseCollection = False

#         AlxOPS_COLLECTION_Isolator_Isolate = AlxOPS_OBJECT_Isolator.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Isolate", icon="OUTLINER_COLLECTION", emboss=True)
#         AlxOPS_COLLECTION_Isolator_Isolate.TargetVisibility = False
#         AlxOPS_COLLECTION_Isolator_Isolate.UseObject = False
#         AlxOPS_COLLECTION_Isolator_Isolate.UseCollection = True

#         AlxOPS_COLLECTION_Isolator_ShowAll = AlxOPS_OBJECT_Isolator.operator(Alx_OT_Scene_VisibilityIsolator.bl_idname, text="Show", icon="OUTLINER_COLLECTION", emboss=True)
#         AlxOPS_COLLECTION_Isolator_ShowAll.TargetVisibility = True
#         AlxOPS_COLLECTION_Isolator_ShowAll.UseObject = False
#         AlxOPS_COLLECTION_Isolator_ShowAll.UseCollection = True

#         AlxOverlayShading = TMenuSectionM.row().split(factor=0.20, align=True)
#         AlxOverlayShading.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
#         AlxOverlayShading.prop(context.area.spaces.active.shading, "show_xray", text="Mesh", icon="XRAY")
#         AlxOverlayShading.prop(context.space_data.overlay, "show_xray_bone", text="Bone", icon="XRAY")
#         AlxOverlayShading.prop(context.space_data.overlay, "show_retopology", text="", icon="MESH_GRID")
#         AlxOverlayShading.prop(context.space_data.overlay, "show_wireframes", text="", icon="MOD_WIREFRAME")

#         if (context.active_object is not None) and (context.active_object.type == "MESH"):
#             AlxObjectSmoothing = TMenuSectionM.row().split(factor=0.33, align=True)
#             ShadeSmooth = AlxObjectSmoothing.operator("object.shade_smooth", text="Smooth", emboss=True)
#             ShadeSmoothAuto = AlxObjectSmoothing.operator("object.shade_smooth", text="Auto Smooth", emboss=True)
#             ShadeSmoothAuto.use_auto_smooth = True
#             AlxObjectSmoothing.operator("object.shade_flat", text="Flat", emboss=True)

#         AlxOPS_ModeRow = TMenuSectionM.row(align=True)
#         AlxOPS_DEFMode_OBJECT = AlxOPS_ModeRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="OBJECT", icon="OBJECT_DATAMODE")
#         AlxOPS_DEFMode_OBJECT.DefaultBehaviour = True
#         AlxOPS_DEFMode_OBJECT.TargetMode = "OBJECT"

#         AlxOPS_DEFMode_WEIGHT = AlxOPS_ModeRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="WPAINT", icon="WPAINT_HLT")
#         AlxOPS_DEFMode_WEIGHT.DefaultBehaviour = True
#         AlxOPS_DEFMode_WEIGHT.TargetMode = "WEIGHT_PAINT"

#         AlxOPS_AutoModeRow = TMenuSectionM.row(align=True)
#         AlxOPS_AutoMode_OBJECT = AlxOPS_AutoModeRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="A-OBJECT", icon="OBJECT_DATAMODE")
#         AlxOPS_AutoMode_OBJECT.DefaultBehaviour = False
#         AlxOPS_AutoMode_OBJECT.TargetMode = "OBJECT"

#         if (AlxContextArmature is not None):
#             AlxOPS_AutoMode_POSE = AlxOPS_AutoModeRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="A-POSE", icon="ARMATURE_DATA")
#             AlxOPS_AutoMode_POSE.DefaultBehaviour = False
#             AlxOPS_AutoMode_POSE.TargetMode = "POSE"
#             AlxOPS_AutoMode_POSE.TargetArmature = AlxContextArmature.name


#         if  (AlxContextArmature is not None):
#             AlxOPS_AutoMode_WEIGHT = AlxOPS_AutoModeRow.operator(Alx_OT_Mode_UnlockedModes.bl_idname, text="A-WPAINT", icon="WPAINT_HLT")
#             AlxOPS_AutoMode_WEIGHT.DefaultBehaviour = False
#             AlxOPS_AutoMode_WEIGHT.TargetMode = "PAINT_WEIGHT"

#             AlxVerifiedContextObject = AlxContextObject

#             if (context.mode == "POSE") and (AlxContextObject is None):
#                 for Object in bpy.context.selected_objects:
#                     if (Object.type == "MESH") and (Object.find_armature() is not None) and (Object.find_armature() is AlxContextArmature):
#                         AlxVerifiedContextObject = Object
#                         AlxOPS_AutoMode_WEIGHT.TargetObject = AlxVerifiedContextObject.name
#             if (AlxContextObject is not None):
#                 AlxOPS_AutoMode_WEIGHT.TargetObject = AlxContextObject.name
#             AlxOPS_AutoMode_WEIGHT.TargetArmature = AlxContextArmature.name

#         TMenuSectionR = RMenuColumnSpace.row().box()

#         EngineRow = TMenuSectionR.row()
#         EngineRow.prop(context.scene.render, "engine", text="")
#         EngineRow.prop(context.area.spaces.active.shading, "type", text="", expand=True)

#         if (context.scene.render.engine == "BLENDER_EEVEE"):
#             EeveeSampleRow = TMenuSectionR.row(align=True)
#             EeveeSampleRow.prop(context.scene.eevee, "use_taa_reprojection", text="Denoise")
#             EeveeSampleRow.prop(context.scene.eevee, "taa_samples", text="Viewport")
#             EeveeSampleRow.prop(context.scene.eevee, "taa_render_samples", text="Render")
        
#         if (context.scene.render.engine == "CYCLES"):
#             CyclesSampleRow = TMenuSectionR.row(align=True)
#             CyclesSampleRow.prop(context.scene.cycles, "preview_samples", text="Viewport")
#             CyclesSampleRow.prop(context.scene.cycles, "samples", text="Render")
#             CyclesSampleRow.prop(context.scene.cycles, "taa_render_samples", text="Render")

#         FrameRow = TMenuSectionR.row(align=True)
#         FrameRow.prop(bpy.context.scene, "frame_current", text="Frame")
#         FrameRow.prop(bpy.context.scene, "frame_start", text="Start")
#         FrameRow.prop(bpy.context.scene, "frame_end", text="End")

#         MMenuSectionM = MMenuColumnSpace.row().box()
#         AlxOPS_Modifier_VisibilityControl = MMenuSectionM.row().operator(Alx_OT_ModifierHideOnSelected.bl_idname, text="Modifier Visibility", emboss=True)