bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valeria Bosco[Valy Arhal]",
    "description" : "For proper functionality [Blender] keymaps preset shoudl be used, [Blender 27x and Industry Compatible] will result in severe keymap conflicts",
    "version" : (0, 5, 0),
    "warning" : "[Heavly Under Development] And Subject To Substantial Changes",
    "category" : "3D View",
    "location" : "[Ctrl Alt A] Tool Menu, [Shift S] Pivot Menu, [Tab] Mode Compact Menu",
    "blender" : (4, 0, 0)
}

# python warcrime
# AddonFiles = ["AlxPreferences", "AlxHandlers", "AlxKeymaps", "AlxOperators", "AlxPanels"]
# import importlib
# for AddonFile in AddonFiles:
#     if (AddonFile not in locals()):
#         exec(AddonFile + " = importlib.reload(AddonFile)")
#         importlib.import_module(AddonFile, "AlxOverHaul")
#     else:
#         exec(AddonFile + " = importlib.reload(AddonFile)")

if ("AlxKeymaps" not in locals()):
    from AlxOverHaul import AlxKeymaps
else:
    import importlib
    AlxKeymaps = importlib.reload(AlxKeymaps)

if ("AlxPreferences" not in locals()):
    from AlxOverHaul import AlxPreferences
else:
    import importlib
    AlxPreferences = importlib.reload(AlxPreferences)

if ("AlxHandlers" not in locals()):
    from AlxOverHaul import AlxHandlers
else:
    import importlib
    AlxHandlers = importlib.reload(AlxHandlers)

if ("AlxUtils" not in locals()):
    from AlxOverHaul import AlxUtils
else:
    import importlib
    AlxUtils = importlib.reload(AlxUtils)

if ("AlxPanels" not in locals()):
    from AlxOverHaul import AlxPanels
else:
    import importlib
    AlxPanels = importlib.reload(AlxPanels)

if ("AlxOperators" not in locals()):
    from AlxOverHaul import AlxOperators
else:
    import importlib
    AlxOperators = importlib.reload(AlxOperators)



import bpy

# multi version support
#if (0, 0, 0) > bpy.app.version:



        # if (context.mode == "POSE") and (AlxContextArmature is not None):
        #     AlxOPS_Armature_SymIK = MMenuSectionM.row().operator(Alx_OT_BoneMatchIKByName.bl_idname, text="Symmetric IK", icon="MOD_MIRROR")
        #     AlxOPS_Armature_SymIK.ActivePoseArmatureObject = AlxContextArmature.name

        # if (context.mode == "OBJECT") and (AlxContextObject is not None):
        #     AlxOPS_Armature_VxClean = MMenuSectionM.row().operator(Alx_OT_VertexGroupCleanEmpty.bl_idname, text="Clean VxGroups", emboss=True)
        #     AlxOPS_Armature_VxClean.VertexDataObject = AlxContextObject.name

        # AlxOPS_Armature_ATS = MMenuSectionM.row().operator(Alx_OT_ArmatureAssignToSelection.bl_idname, text="Assign Armature")








# class Alx_OT_Scene_FrameChange(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.scene_frame_change"

#     @classmethod
#     def poll(self, context):
#         return True
    
#     def execute(self, context):



class Alx_OT_ModifierBevelSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_bevel_selection"
    bl_options = {'REGISTER', 'UNDO'}

    Segments : bpy.props.IntProperty(name="Segments", default=1, min=1)
    Width : bpy.props.FloatProperty(name="Width", default=0.01000, unit="LENGTH", min=0.0)
    UseWeight : bpy.props.BoolProperty(name="Use Weight", default=True)
    HardenNormals : bpy.props.BoolProperty(name="Harden Normals", default=True)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        for SelObj in bpy.context.selected_objects:

                            HasModifier = False

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "BEVEL"):
                                        HasModifier = True

                                        ObjMOD.segments = self.Segments
                                        ObjMOD.width = self.Width
                
                                        match self.UseWeight:

                                            case True:
                                                ObjMOD.limit_method = "WEIGHT"

                                            case False:
                                                ObjMOD.limit_method = "ANGLE"
                                                ObjMOD.angle_limit = 30 * (3.14/180)

                                        ObjMOD.miter_outer = "MITER_ARC"
                                        ObjMOD.harden_normals = self.HardenNormals

                                if (HasModifier == False):        
                                
                                    BevelMod = SelObj.modifiers.new("Bevel", "BEVEL")
                                    BevelMod.segments = self.Segments
                                    BevelMod.width = self.Width

                                    match self.UseWeight:

                                        case True:
                                            BevelMod.limit_method = "WEIGHT"

                                        case False:
                                            BevelMod.limit_method = "ANGLE"
                                            BevelMod.angle_limit = 30 * (3.14/180)

                                    BevelMod.miter_outer = "MITER_ARC"
                                    BevelMod.harden_normals = self.HardenNormals

        return {"FINISHED"}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)



class Alx_OT_ModifierWeldSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_weld_selection"
    bl_options = {'REGISTER', 'UNDO'}

    UseMergeAll : bpy.props.BoolProperty(name="Merge All", default=True)
    UseMergeOnlyLooseEdges : bpy.props.BoolProperty(name="Only Loose Edges", default=True)

    MergeDistance : bpy.props.FloatProperty(name="Distance", default=0.00100, unit="LENGTH", min=0.0)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        for SelObj in bpy.context.selected_objects:

                            HasModifier = False

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "WELD"):
                                        HasModifier = True

                                        match self.UseMergeAll:
                                            case True:
                                                ObjMOD.mode = "ALL"

                                            case False:
                                                ObjMOD.mode = "CONNECTED"
                                                ObjMOD.loose_edges = self.UseMergeOnlyLooseEdges

                                        ObjMOD.merge_threshold = self.MergeDistance

                                if (HasModifier == False):    
                                    WeldMod = SelObj.modifiers.new("Weld", "WELD")
            
                                    match self.UseMergeAll:
                                        case True:
                                            WeldMod.mode = "ALL"

                                        case False:
                                            WeldMod.mode = "CONNECTED"
                                            WeldMod.loose_edges = self.UseMergeOnlyLooseEdges

                                    WeldMod.merge_threshold = self.MergeDistance
            
            return {"FINISHED"}
                        


    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

class Alx_OT_VertexGroupCleanEmpty(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.vertex_group_clean_empty"

    VertexDataObject : bpy.props.StringProperty(options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        if (self.VertexDataObject != "") and (bpy.data.objects.get(self.VertexDataObject) is not None):
            for VGroup in bpy.data.objects.get(self.VertexDataObject).vertex_groups:
                i = 0
                HasAtLeastOneVertex = False
                while i < len(bpy.data.objects.get(self.VertexDataObject).data.vertices):
                    if(i < 0): break
                    try:
                        VGroup.weight(i)
                    except:
                        pass

                    else:
                        HasAtLeastOneVertex = True    
                    i += 1
                if(HasAtLeastOneVertex == False):
                    bpy.data.objects.get(self.VertexDataObject).vertex_groups.remove(VGroup)
        return{"FINISHED"}


# class Alx_OT_ArmatureCloneIKPuppet(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.armature_clone_ik_puppet"

#     TargetArmature : bpy.props.StringProperty(name="", options={"HIDDEN"})

#     @classmethod
#     def poll(self, context):
#         return context.mode == "OBJECT"
    
#     def execute(self, context):
#         for window in context.window_manager.windows:
#             screen = window.screen
#             for area in screen.areas:
#                 if area.type == 'VIEW_3D':
#                     with context.temp_override(window=window, area=area):

#                         if (context.active_object is not None) and (context.active_object.type == "ARMATURE"):
#                             self.TargetArmature = context.active_object.name

#                             if (bpy.data.objects.get(self.TargetArmature) is not None):
#                                 ArmatureIKPuppet = None
#                                 if (bpy.data.objects.get(self.TargetArmature + "_IK_Puppet")  is None):
#                                     ArmatureIKPuppet = bpy.data.objects.new(bpy.data.objects.get(self.TargetArmature).name + "_IK_Puppet", bpy.data.objects.get(self.TargetArmature).data.copy())
#                                     ArmatureIKPuppet.location = bpy.data.objects.get(self.TargetArmature).location
#                                     context.collection.objects.link(ArmatureIKPuppet)
#                                 if (bpy.data.objects.get(self.TargetArmature + "_IK_Puppet")  is not None):
#                                     ArmatureIKPuppet = bpy.data.objects.get(self.TargetArmature + "_IK_Puppet")

#                                 if (ArmatureIKPuppet is not None):
#                                     IKPuppetPoseBoneData = bpy.data.objects.get(self.TargetArmature).pose.bones
#                                     for PoseBone in IKPuppetPoseBoneData:
#                                         AlxGetIKConstraint(PoseBone)

#         return {"FINISHED"}

# ### Alx Material Property Groups
# class Alx_Material(bpy.types.PropertyGroup):
#     def GetMaterialName(self):
#         return self.material.name
    
#     name : StringProperty()
#     material_name : StringProperty(get=GetMaterialName)
#     material : PointerProperty(type=bpy.types.Material)

# class Alx_MaterialCollection(bpy.types.PropertyGroup):
#     name : StringProperty()
#     pass

# def AlxMaterialAssignFromScene(self):
#     for Material in bpy.data.materials:
#         if (Material is not None) and (bpy.context.scene.alx_materials.find(Material.name) == -1):
#             AlxMaterial = bpy.context.scene.alx_materials.add()
#             AlxMaterial.name = Material.name
#             AlxMaterial.material = Material

# ### Alx Material Operators
# class Alx_OT_MaterialRegisterChanges(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_register_changes"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context):
#         AlxMaterialAssignFromScene(self)
        
#         for AlxMaterial in bpy.context.scene.alx_materials:
#             if (AlxMaterial.name not in bpy.data.materials):
#                 NewMaterial = bpy.data.materials.new(AlxMaterial.name)
#                 NewMaterial = AlxMaterial
#         return {"FINISHED"}

# class Alx_OT_MaterialAppendToScene(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_append_to_scene"

#     @classmethod
#     def poll(self, context):
#         return True
    
#     def execute(self, context: Context):
#         bpy.data.materials.new("Material")

#         return {"FINISHED"}

# class Alx_OT_MaterialRemoveFromScene(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_remove_from_scene"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context):
#         if (len(bpy.context.scene.alx_materials) != 0) and (bpy.context.scene.alx_active_material_index < len(bpy.context.scene.alx_materials)):
#             MaterialID = bpy.data.materials.get(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name)

#             MaterialUserMap = bpy.data.user_map(key_types={"MATERIAL"}, value_types={"MESH"})
#             MaterialUsers = MaterialUserMap.get(bpy.data.materials[MaterialID.name], None)

#             for User in MaterialUsers:
#                 MaterialUser = User
#                 if (MaterialUser.name not in ["Scene", "Airbrush"]):
#                     MeshUserMap = bpy.data.user_map(key_types={"MESH"}, value_types={"OBJECT"})
#                     MeshUsers = MeshUserMap.get(bpy.data.meshes[MaterialUser.name], None)

#                     for MeshUser in MeshUsers:
#                         print(MeshUsers)
#                         MeshUser.active_material_index = MeshUser.material_slots.find(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name)
#                         print(MeshUser)
#                         print(MeshUser.active_material_index)
#                         bpy.ops.object.material_slot_select()
#                         bpy.ops.object.material_slot_remove()

#             if ((bpy.context.scene.alx_active_material_index -1) != -1):
#                 bpy.context.scene.alx_active_material_index = bpy.context.scene.alx_active_material_index - 1

#         return {"FINISHED"}
    
# class Alx_OT_MaterialAssignToSelection(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_assign_to_selection"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context):
#         for Object in bpy.context.selected_objects:
#             if (Object.type == "MESH"):
#                 if (len(bpy.context.scene.alx_materials) != 0) and (bpy.context.scene.alx_active_material_index < len(bpy.context.scene.alx_materials)):
#                     if bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name not in Object.data.materials:
#                         Object.data.materials.append(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].material)

#         return {"FINISHED"}

# ### Alx Material UI
# class Alx_UL_MaterialSlotList(bpy.types.UIList):
#     bl_idname = "alx.material_slot_list"

#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             layout.prop(item, "name", text="", emboss=False, icon_value=icon)

# class Alx_PT_MaterialSlotSelector(bpy.types.Panel):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_slot_selector"

#     bl_category = "Alx 3D"

#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     @classmethod
#     def poll(cls, context):
#             return True

#     def draw(self, context):
#         AlxLayout = self.layout

#         MaterialOutlinerRow = AlxLayout.row(align=True)
        
        
#         SM_ToolsColumn = MaterialOutlinerRow.column()
#         SM_ToolsColumn.operator(Alx_OT_MaterialAppendToScene.bl_idname, text="", icon="ADD") 
#         SM_ToolsColumn.operator(Alx_OT_MaterialRemoveFromScene.bl_idname, text="", icon="FAKE_USER_OFF")


#         SceneMaterialColumn = MaterialOutlinerRow.column()
#         SceneMaterialColumn.template_list(listtype_name=Alx_UL_MaterialSlotList.bl_idname, list_id="", dataptr=bpy.context.scene, propname="alx_materials", active_dataptr=bpy.context.scene, active_propname="alx_active_material_index")
        
        
#         SM_ToolsColumn.operator(Alx_OT_MaterialRegisterChanges.bl_idname, text="", icon="FILE_REFRESH")
        
        
#         SM_ToolsColumn.label(icon="RIGHTARROW")

#         SceneMaterialColumn.operator(Alx_OT_MaterialAssignToSelection.bl_idname, text="Assign Material To Selection")

#         MaterialCollectionColumn = MaterialOutlinerRow.column()

#         MaterialCollectionColumn.template_list(listtype_name=Alx_UL_MaterialSlotList.bl_idname, list_id="", dataptr=bpy.context.scene, propname="alx_material_collection_library", active_dataptr=bpy.context.scene, active_propname="alx_active_material_index")
        
#         MC_ToolsColumn = MaterialOutlinerRow.column()

#         MaterialCollectionColumn.label(text="Operator Here")
        







# class Alx_UL_ActionSelector(bpy.types.UIList):

#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             layout.prop(item, "name", text="", emboss=False, icon_value=icon)
#         elif self.layout_type in {'GRID'}:
#             pass

# class Alx_Panel_SwapArmatureAction(bpy.types.Panel):
#     """"""

#     bl_label = "Alx Action Selector"
#     bl_idname = "Alx.Action_OT_Selector"

#     bl_category = "Alx 3D"

#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     @classmethod
#     def poll(cls, context):
#         if (context.mode == "OBJECT") or (context.mode == "PAINT_WEIGHT") or (context.mode =="POSE"):
#             return True

#     def draw(self, context):
#         Alxlayout = self.layout
#         obj = context.object
#         Alxlayout.template_list("Alx_UL_ActionSelector", "", bpy.data, "actions", obj, "UIActionIndex")

# @bpy.app.handlers.persistent
# def AlxUpdateActionUI(context):
#         if (bpy.context.view_layer.objects.active is not None) and (bpy.context.view_layer.objects.active.find_armature() is not None):
#             AlxActionParentArmature = bpy.data.armatures[bpy.context.view_layer.objects.active.find_armature().data.name]
        
#             if (AlxActionParentArmature is not None) and (AlxActionParentArmature.animation_data is not None):
#                 ActiveActionIndex = bpy.data.actions.find(AlxActionParentArmature.animation_data.action.name)

#                 if ActiveActionIndex != AlxActionParentArmature.UIActionIndex:
#                     AlxActionParentArmature.UIActionIndex = ActiveActionIndex

# def AlxUpdateAddonActionList(self, context):
#     if(bpy.context.view_layer.objects.active is not None):
#         if (bpy.context.view_layer.objects.active.find_armature() is not None):
#             AlxActionParentArmature = bpy.data.armatures[bpy.context.view_layer.objects.active.find_armature().data.name]

#             if (AlxActionParentArmature is not None):
#                 if (AlxActionParentArmature is not None) and (AlxActionParentArmature.animation_data is not None):
#                     AlxActionParentArmature.animation_data.action = bpy.data.actions[AlxActionParentArmature.UIActionIndex]
#                     bpy.context.scene.frame_current = 0

# bpy.app.handlers.depsgraph_update_post.append(AlxUpdateActionUI)








# class AlxOverHaulAddonSettings(bpy.types.PropertyGroup):
#     """"""

#     def PropertyUpdate(self, context):
#         if (self.View3d_Pan_Use_Shift_GRLess == True):
#             AlxEditDefaultKeymap(ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="KEYBOARD", Key="GRLESS", UseShift=True, Active=True)
#         if (self.View3d_Pan_Use_Shift_GRLess == False):
#             AlxEditDefaultKeymap(ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="MOUSE", Key="MIDDLEMOUSE", UseShift=True, Active=True)

#         if (self.View3d_Rotate_Use_GRLess == True):
#             AlxEditDefaultKeymap(ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="KEYBOARD", Key="GRLESS", Active=True)
#         if (self.View3d_Rotate_Use_GRLess == False):
#             AlxEditDefaultKeymap(ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="MOUSE", Key="MIDDLEMOUSE", Active=True)

#         if (self.View3d_Zoom_Use_GRLess == True):
#             AlxEditDefaultKeymap(ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="KEYBOARD", Key="GRLESS", UseCtrl=True, Active=True)
#         if (self.View3d_Zoom_Use_GRLess == False):
#             AlxEditDefaultKeymap(ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="MOUSE", Key="MIDDLEMOUSE", UseCtrl=True, Active=True)






class Alx_OT_ScriptReload(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.script_reload"

    @classmethod
    def poll(self, context):
        return
    
    def execute(self, context):
        bpy.ops.script.reload()
        return {"FINISHED"}

AlxClassQueue = [
                Alx_OT_ScriptReload,
                AlxPreferences.AlxAddonProperties,
                AlxPreferences.AlxOverHaulAddonPreferences,
                

                AlxPanels.Alx_PT_AlexandriaToolPanel,
                AlxPanels.Alx_MT_UnlockedModesPie,
                AlxPanels.Alx_PT_Scene_GeneralPivot,

                AlxOperators.Alx_OT_Mode_UnlockedModes,
                AlxOperators.Alx_OT_Scene_UnlockedSnapping,
                AlxOperators.Alx_OT_Scene_VisibilityIsolator,
                AlxOperators.Alx_OT_ModifierHideOnSelected,
                AlxOperators.Alx_OT_Camera_MultiTool,


                AlxOperators.Alx_OT_Armature_AssignToSelection,
                AlxOperators.Alx_OT_Armature_MatchIKByMirroredName,

                
                Alx_OT_ModifierBevelSelection,
                #AlxOperators.Alx_OT_ModifierSubdivisionSelection,
                Alx_OT_ModifierWeldSelection,
                Alx_OT_VertexGroupCleanEmpty,
                ]

bpy.app.handlers.load_post.append(AlxHandlers.AlxAddonKeymapHandler)



def register():
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    AlxKeymaps.KeymapCreation()
    bpy.types.Scene.alx_addon_properties = bpy.props.PointerProperty(type=AlxPreferences.AlxAddonProperties)
    bpy.types.Scene.alx_scene_isolator_visibility_object_list = []
    bpy.types.Scene.alx_scene_isolator_visibility_collection_list = []

    bpy.context.preferences.use_preferences_save = True

def unregister():
    for AlxQCls in AlxClassQueue:
        bpy.utils.unregister_class(AlxQCls)

    for km, kmi in AlxKeymaps.AlxAddonKeymaps:
        km.keymap_items.remove(kmi)
    AlxKeymaps.AlxAddonKeymaps.clear()

    bpy.app.handlers.load_post.remove(AlxHandlers.AlxAddonKeymapHandler)

if __name__ == "__main__":
    register()

    # bpy.types.Scene.alx_materials = CollectionProperty(type=Alx_Material)
    # bpy.types.Scene.alx_active_material_index = IntProperty()
    # bpy.types.Scene.alx_material_collection_library = CollectionProperty(type=Alx_MaterialCollection)

    #bpy.app.handlers.depsgraph_update_post.append(AlxMaterialRegisterChanges)
    #bpy.msgbus.subscribe_rna(key=(bpy.types.Object, "material_slots"), owner="owner", args=(), notify=AlxMaterialRegisterChanges)

    
    
    # del bpy.types.Scene.alx_materials
    # del bpy.types.Scene.alx_active_material_index