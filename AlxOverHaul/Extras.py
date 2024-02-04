# class Alx_OT_VertexGroupCleanEmpty(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.vertex_group_clean_empty"

#     VertexDataObject : bpy.props.StringProperty(options={"HIDDEN"})

#     @classmethod
#     def poll(self, context):
#         return True
    
#     def execute(self, context):
#         if (self.VertexDataObject != "") and (bpy.data.objects.get(self.VertexDataObject) is not None):
#             for VGroup in bpy.data.objects.get(self.VertexDataObject).vertex_groups:
#                 i = 0
#                 HasAtLeastOneVertex = False
#                 while i < len(bpy.data.objects.get(self.VertexDataObject).data.vertices):
#                     if(i < 0): break
#                     try:
#                         VGroup.weight(i)
#                     except:
#                         pass

#                     else:
#                         HasAtLeastOneVertex = True    
#                     i += 1
#                 if(HasAtLeastOneVertex == False):
#                     bpy.data.objects.get(self.VertexDataObject).vertex_groups.remove(VGroup)
#         return{"FINISHED"}


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

    # def execute(self, context):
    #     if (len(bpy.context.scene.alx_materials) != 0) and (bpy.context.scene.alx_active_material_index < len(bpy.context.scene.alx_materials)):
    #         MaterialID = bpy.data.materials.get(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name)

    #         MaterialUserMap = bpy.data.user_map(key_types={"MATERIAL"}, value_types={"MESH"})
    #         MaterialUsers = MaterialUserMap.get(bpy.data.materials[MaterialID.name], None)

    #         for User in MaterialUsers:
    #             MaterialUser = User
    #             if (MaterialUser.name not in ["Scene", "Airbrush"]):
    #                 MeshUserMap = bpy.data.user_map(key_types={"MESH"}, value_types={"OBJECT"})
    #                 MeshUsers = MeshUserMap.get(bpy.data.meshes[MaterialUser.name], None)

    #                 for MeshUser in MeshUsers:
    #                     print(MeshUsers)
    #                     MeshUser.active_material_index = MeshUser.material_slots.find(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name)
    #                     print(MeshUser)
    #                     print(MeshUser.active_material_index)
    #                     bpy.ops.object.material_slot_select()
    #                     bpy.ops.object.material_slot_remove()

    #         if ((bpy.context.scene.alx_active_material_index -1) != -1):
    #             bpy.context.scene.alx_active_material_index = bpy.context.scene.alx_active_material_index - 1

    #     return {"FINISHED"}
    
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

    # bpy.types.Scene.alx_materials = CollectionProperty(type=Alx_Material)
    # bpy.types.Scene.alx_active_material_index = IntProperty()
    # bpy.types.Scene.alx_material_collection_library = CollectionProperty(type=Alx_MaterialCollection)

    #bpy.app.handlers.depsgraph_update_post.append(AlxMaterialRegisterChanges)
    #bpy.msgbus.subscribe_rna(key=(bpy.types.Object, "material_slots"), owner="owner", args=(), notify=AlxMaterialRegisterChanges)

    
    
    # del bpy.types.Scene.alx_materials
    # del bpy.types.Scene.alx_active_material_index