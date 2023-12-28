import bpy

from AlxOverHaul import AlxPreferences, AlxUtils

class Alx_OT_Mode_UnlockedModes(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_mode_unlocked_modes"
    bl_options = {"INTERNAL"}

    DefaultBehaviour : bpy.props.BoolProperty(name="", default=True, options={"HIDDEN"})
    TargetMode : bpy.props.StringProperty(name="", default="OBJECT", options={"HIDDEN"})
    TargetSubMode : bpy.props.StringProperty(name="", default="VERT", options={"HIDDEN"})
    
    TargetObject : bpy.props.StringProperty(name="", options={"HIDDEN"})
    TargetArmature : bpy.props.StringProperty(name="", options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return (context.area.type == "VIEW_3D")
    
    def execute(self, context):
        if (self.DefaultBehaviour == True):
            match self.TargetMode:
                case "OBJECT":
                    if (context.mode != "OBJECT"):
                        bpy.ops.object.mode_set(mode="OBJECT")
                    return {"FINISHED"}

                case "EDIT":
                    if (context.mode not in ["EDIT_CURVE", "EDIT_CURVES", "EDIT_SURFACE", "EDIT_TEXT", "EDIT_METABALL", "EDIT_LATTICE", "EDIT_GREASE_PENCIL", "EDIT_POINT_CLOUD"]) and (len(context.selected_objects) != 0):
                        for Object in context.selected_objects:
                            if (Object.type == "MESH"):
                                if (self.TargetSubMode in ["VERT", "EDGE", "FACE"]):
                                    bpy.context.view_layer.objects.active = Object
                                    bpy.ops.object.mode_set_with_submode(mode="EDIT", mesh_select_mode=set([self.TargetSubMode]))
                            if (Object.type in ["ARMATURE", "CURVE"]):
                                bpy.context.view_layer.objects.active = Object
                                bpy.ops.object.mode_set(mode="EDIT")

                    return {"FINISHED"}
                
                case "SCULPT":
                    if (context.mode != "SCULPT"):
                        if (context.active_object is not None) and (context.active_object.type == "MESH"):
                            bpy.ops.object.mode_set(mode="SCULPT")
                    
                    return {"FINISHED"}       

        if (self.DefaultBehaviour == False):
            match self.TargetMode:
                case "POSE":
                    if (context.mode != "POSE"):
                        if (self.TargetArmature != "") and (bpy.data.objects[self.TargetArmature] is not None):                       
                            if (context.mode == "PAINT_WEIGHT"):
                                bpy.ops.object.mode_set(mode="OBJECT")

                            bpy.data.objects.get(self.TargetArmature).hide_set(False)
                            bpy.data.objects.get(self.TargetArmature).hide_viewport = False

                            bpy.context.view_layer.objects.active = bpy.data.objects.get(self.TargetArmature)
                            bpy.ops.object.mode_set(mode="POSE")

                    return {"FINISHED"}
                
                case "PAINT_WEIGHT":
                    if (context.mode != "PAINT_WEIGHT"):
                        if (self.TargetObject != "") and (self.TargetArmature != ""):
                            if (bpy.data.objects[self.TargetObject] is not None) and (bpy.data.objects[self.TargetArmature] is not None):
                                if (context.mode == "POSE"):
                                    bpy.ops.object.mode_set(mode="OBJECT")
                                
                                bpy.data.objects.get(self.TargetArmature).hide_set(False)
                                bpy.data.objects.get(self.TargetArmature).hide_viewport = False

                                bpy.data.objects.get(self.TargetArmature).select_set(True)

                                bpy.context.view_layer.objects.active = bpy.data.objects.get(self.TargetObject)
                                bpy.ops.object.mode_set(mode="WEIGHT_PAINT")

                    return {"FINISHED"}

        return {"FINISHED"}

class Alx_OT_Scene_UnlockedSnapping(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_scene_unlocked_snapping"
    bl_options = {"INTERNAL"}

    SourceSnapping : bpy.props.StringProperty(name="", default="NONE", options={"HIDDEN"})
    TargetSnapping : bpy.props.StringProperty(name="", default="NONE", options={"HIDDEN"})
    SubTargetSnapping : bpy.props.StringProperty(name="", default="NONE", options={"HIDDEN"})

    ShouldOffset : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"
    
    def execute(self, context):
        if (context.mode == "OBJECT"):
            if (self.SourceSnapping == "ACTIVE"):
                if (self.TargetSnapping == "SELECTED"):
                    if (len(context.selected_objects) != 0):
                        for Object in context.selected_objects:
                            if (context.active_object is not None) and (Object is not context.active_object):
                                Object.location = context.active_object.location
                    return {"FINISHED"}
                
                if (self.TargetSnapping == "SCENE_CURSOR"):
                    if (context.active_object is not None):
                        context.scene.cursor.location = context.active_object.location
                    return {"FINISHED"}

            if (self.SourceSnapping == "SCENE_CURSOR"):
                if (self.TargetSnapping == "SELECTED"):
                    if (self.SubTargetSnapping == "OBJECT"):
                        if (len(context.selected_objects) != 0):
                            for Object in context.selected_objects:
                                    Object.location = context.scene.cursor.location
                    if (self.SubTargetSnapping == "ORIGIN"):
                        if (len(context.selected_objects) != 0):
                            for Object in context.selected_objects:
                                bpy.context.view_layer.objects.active = Object
                                bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

                        

                        return {"FINISHED"}
            
            if (self.SourceSnapping == "RESET"):
                if (self.TargetSnapping == "SCENE_CURSOR"):
                    context.scene.cursor.location = [0.0, 0.0, 0.0]
                    return {"FINISHED"}

                return {"FINISHED"}

        return {"FINISHED"}

class Alx_OT_Scene_VisibilityIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_scene_visibility_isolator"
    bl_options = {"INTERNAL"}

    TargetVisibility : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})
    UseObject : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})
    UseCollection : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        if (len(context.scene.alx_addon_properties.SceneIsolatorVisibilityTarget) != 0):
            TargetType = set(Target for Target in context.scene.alx_addon_properties.SceneIsolatorVisibilityTarget)
            TemporaryList = set(Object for Object in context.scene.objects if ((Object is not None) and (len(context.selected_objects) != 0) and (Object not in context.selected_objects)))

            if (len(TemporaryList) != 0):
                SafeList = TemporaryList

                if (len(TemporaryList) == 0):
                    for Object in SafeList:
                        if (Object is not None):
                            if ("VIEWPORT" in TargetType):
                                Object.hide_viewport = not self.TargetVisibility
                            if ("RENDER" in TargetType):
                                Object.hide_render = not self.TargetVisibility

                if (len(TemporaryList) != 0):
                    for Object in TemporaryList:
                        if (Object is not None):
                            if ("VIEWPORT" in TargetType):
                                Object.hide_viewport = not self.TargetVisibility
                            if ("RENDER" in TargetType):
                                Object.hide_render = not self.TargetVisibility

                



            #         for Object in bpy.data.objects:
            #             if (Object is not None ) and (Object.name not in ObjectSelection):
            #                 

            #     if (self.UseCollection == True):
            #         ActiveCollection = bpy.data.objects[bpy.context.view_layer.objects.active.name].users_collection[0]
            #         for collection in bpy.data.collections:
            #             if (collection is not ActiveCollection) and (collection is not ActiveCollection) and (ActiveCollection not in collection.children_recursive):
            #                 if ("VIEWPORT" in TargetType):
            #                     collection.hide_viewport = not self.TargetVisibility
            #                 if ("RENDER" in TargetType):
            #                     collection.hide_render = not self.TargetVisibility
            # if (context.active_object is None):
            #     if (self.UseObject == True):
            #         ObjectSelection = []
            #         for Object in context.selected_objects:
            #             if (Object is not None):
            #                 ObjectSelection.append(Object.name)
                        
            #             for Object in bpy.data.objects:
            #                 if (Object is not None ) and (Object.name not in ObjectSelection):
            #                     if ("VIEWPORT" in TargetType):
            #                         Object.hide_viewport = not self.TargetVisibility
            #                     if ("RENDER" in TargetType):
            #                         Object.hide_render = not self.TargetVisibility
        return {"FINISHED"}
    
class Alx_OT_Armature_AssignToSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.armature_assign_to_selection"
    bl_description = "Assigns any [Mesh] in the current selection to the [Armature] within said selection"

    bl_options = {"INTERNAL","REGISTER", "UNDO"}

    # def UpdateUseAutomaticWeight(self, context):
    #     if (self.UseAutomaticWeight == True):
    #         self.UseSingleVxGroup = False
    #         self.UsePurgeOtherGroups = False
    #         self.VxGroupName = ""

    # def UpdateUsePreserveExistingGroups(self, context):
    #     if (self.UsePreserveExistingGroups == True):
    #         self.UseAutomaticWeight = True
    #         self.UseSingleVxGroup = False
    #         self.UsePurgeOtherGroups = False
    #         self.VxGroupName = ""
        
    def UpdateUseSingleVxGroup(self, context):
        # if (self.UseSingleVxGroup == True):
        #     self.UseAutomaticWeight = False
        #     self.UsePreserveExistingGroups = False
        pass

    # def UpdateUsePurgeOtherGroups(self, context):
    #     if (self.UsePurgeOtherGroups == True):
    #         self.UseSingleVxGroup = True
    #         self.UseAutomaticWeight = False
    #         self.UsePreserveExistingGroups = False

    def UpdateVxGroupName(self, context):
        if (self.VxGroupName != ""):
            self.UseSingleVxGroup = True
            

    TargetArmature : bpy.props.StringProperty(name="", options={"HIDDEN"})
    UseParent : bpy.props.BoolProperty(name="Should Parent", default=False)

    #UseAutomaticWeight : BoolProperty(name="Automatic Weights", default=False, update=UpdateUseAutomaticWeight)
    #UsePreserveExistingGroups : BoolProperty(name="Preserve Existing VxGroups", default=False, update=UpdateUsePreserveExistingGroups)

    UseSingleVxGroup : bpy.props.BoolProperty(name="Single VxGroup", default=False, update=UpdateUseSingleVxGroup)
    #UsePurgeOtherGroups : BoolProperty(name="Purge Other VxGroups", default=False, update=UpdateUsePurgeOtherGroups)
    VxGroupName : bpy.props.StringProperty(name="Group", default="", update=UpdateVxGroupName)

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        for SelectedObject in context.selected_objects:

            if (SelectedObject.type == "ARMATURE") and (self.TargetArmature == ""):
                self.TargetArmature = SelectedObject.name

            if (SelectedObject.type == "MESH"):
                ArmatureModifier = AlxUtils.AlxRetiriveObjectModifier(SelectedObject, "ARMATURE")

                if (ArmatureModifier is None):
                    ArmatureModifier = SelectedObject.modifiers.new(name="Armature", type="ARMATURE")

                if (ArmatureModifier is not None):
                    ArmatureModifier.object = bpy.data.objects.get(self.TargetArmature)

                if (self.UseParent == True):
                    SelectedObject.parent = bpy.data.objects.get(self.TargetArmature)
                    SelectedObject.matrix_parent_inverse = bpy.data.objects.get(self.TargetArmature).matrix_world.inverted()

                # if (self.UseAutomaticWeight == True):
                #     bpy.ops.alx.automatic_mode_changer(DefaultBehaviour=False, TargetMode="PAINT_WEIGHT", TargetObject=SelectedObject.name, TargetArmature=self.TargetArmature)
                #     #bpy.ops.paint.weight_from_bones(type='AUTOMATIC')

                if (self.UseSingleVxGroup == True):
                    if (self.VxGroupName != "") and (self.VxGroupName not in SelectedObject.vertex_groups):
                        VxGroup = SelectedObject.vertex_groups.new()
                        VxGroup.name = self.VxGroupName
                    if (self.VxGroupName != "") and (self.VxGroupName in SelectedObject.vertex_groups):
                        VxGroup = SelectedObject.vertex_groups.get(self.VxGroupName)
                        
                        if (VxGroup is not None):
                            VxGroup.add(range(0, len(SelectedObject.data.vertices)), 1.0, 'REPLACE')
                                                
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

class Alx_OT_Armature_MatchIKByMirroredName(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.bone_match_ik_by_name"
    bl_options = {"INTERNAL", "REGISTER", "UNDO"}

    ActivePoseArmatureObject : bpy.props.StringProperty(options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return (context.mode == "POSE")

    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        if (bpy.data.objects.get(self.ActivePoseArmatureObject).type == "ARMATURE"):
                            PoseBoneData = bpy.data.objects.get(self.ActivePoseArmatureObject).pose.bones

                            CorrectPairBones = []

                            for PoseBone in PoseBoneData:
                                if (PoseBone.name[-2] == ".") and (PoseBone.name[0:-2] not in CorrectPairBones):
                                    CorrectPairBones.append(PoseBone.name[0:-2])
                                    PoseBoneLeft = AlxUtils.AlxGetBoneAlwaysLeft(PoseBone, self.ActivePoseArmatureObject)
                                    OppositeBoneLeft = AlxUtils.AlxGetBoneOpposite(AlxUtils.AlxGetBoneAlwaysLeft(PoseBone, self.ActivePoseArmatureObject), self.ActivePoseArmatureObject)
                                    
                                    AlxUtils.AlxCloneIKSettings(PoseBoneLeft, OppositeBoneLeft)
                                    AlxUtils.AlxCloneIKBoneLimitOnChain(PoseBoneLeft, self.ActivePoseArmatureObject)

class Alx_OT_ModifierHideOnSelected(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_selection_visibility"

    ShowModiferEdit : bpy.props.BoolProperty(name="Show Edit:", default=True)
    ShowModiferViewport : bpy.props.BoolProperty(name="Show Viewport:", default=True)
    ShowModiferRender : bpy.props.BoolProperty(name="Show Render:", default=True)

    BevelMod : bpy.props.BoolProperty(name="Bevel", default=False)
    SubdivisionMod : bpy.props.BoolProperty(name="Subdivision", default=False)
    SolidifyMod : bpy.props.BoolProperty(name="Solidify", default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        ModifiersList = []

                        if (self.BevelMod == True):
                            ModifiersList.append("BEVEL")
                        if (self.SubdivisionMod == True):
                            ModifiersList.append("SUBSURF")
                        if (self.SolidifyMod == True):
                            ModifiersList.append("SOLIDIFY")

                        for Object in bpy.context.selected_objects:
                            if (Object is not None) and (len(Object.modifiers) != 0) and (Object.type in ["MESH", "ARMATURE", "CURVE"]):
                                ObjectModfiers = getattr(Object, "modifiers", [])

                                for ObjectModifier in ObjectModfiers:
                                    if (ObjectModifier is not None) and (ObjectModifier.type in ModifiersList):
                                        ObjectModifier.show_in_editmode = self.ShowModiferEdit
                                        ObjectModifier.show_viewport = self.ShowModiferViewport
                                        ObjectModifier.show_render = self.ShowModiferRender                
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)
    
