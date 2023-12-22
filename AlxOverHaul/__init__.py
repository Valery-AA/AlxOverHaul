bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valeria Bosco[Valy Arhal]",
    "description" : "",
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
from bpy.types import Context, Event
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, CollectionProperty, EnumProperty, PointerProperty

# multi version support
#if (0, 0, 0) > bpy.app.version:



        # if (context.mode == "POSE") and (AlxContextArmature is not None):
        #     AlxOPS_Armature_SymIK = MMenuSectionM.row().operator(Alx_OT_BoneMatchIKByName.bl_idname, text="Symmetric IK", icon="MOD_MIRROR")
        #     AlxOPS_Armature_SymIK.ActivePoseArmatureObject = AlxContextArmature.name

        # if (context.mode == "OBJECT") and (AlxContextObject is not None):
        #     AlxOPS_Armature_VxClean = MMenuSectionM.row().operator(Alx_OT_VertexGroupCleanEmpty.bl_idname, text="Clean VxGroups", emboss=True)
        #     AlxOPS_Armature_VxClean.VertexDataObject = AlxContextObject.name

        # AlxOPS_Armature_ATS = MMenuSectionM.row().operator(Alx_OT_ArmatureAssignToSelection.bl_idname, text="Assign Armature")





def AlxRetiriveObjectModifier(TargetObejct, TargetType):
    ModifierTypes = ["ARMATURE"]
    if (TargetType in ModifierTypes):
        for Modifier in TargetObejct.modifiers:
            if (Modifier.type == TargetType):
                return Modifier
    return None


# class Alx_OT_Scene_FrameChange(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.scene_frame_change"

#     @classmethod
#     def poll(self, context):
#         return True
    
#     def execute(self, context):


class Alx_OT_ArmatureAssignToSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.armature_assign_to_selection"
    bl_description = "Assigns any [Mesh] in the current selection to the [ACTIVE Armature] that was selected last"

    bl_options = {'REGISTER', 'UNDO'}

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
            

    TargetArmature : StringProperty(name="", options={"HIDDEN"})
    UseParent : BoolProperty(name="Should Parent", default=False)

    #UseAutomaticWeight : BoolProperty(name="Automatic Weights", default=False, update=UpdateUseAutomaticWeight)
    #UsePreserveExistingGroups : BoolProperty(name="Preserve Existing VxGroups", default=False, update=UpdateUsePreserveExistingGroups)

    UseSingleVxGroup : BoolProperty(name="Single VxGroup", default=False, update=UpdateUseSingleVxGroup)
    #UsePurgeOtherGroups : BoolProperty(name="Purge Other VxGroups", default=False, update=UpdateUsePurgeOtherGroups)
    VxGroupName : StringProperty(name="Group", default="", update=UpdateVxGroupName)

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        if (context.active_object is not None) and (context.active_object.type == "ARMATURE"):
                            self.TargetArmature = context.active_object.name

                        if (self.TargetArmature != ""):
                            for SelectedObject in context.selected_objects:
                                if (SelectedObject.type == "MESH"):
                                    ArmatureModifier = AlxRetiriveObjectModifier(SelectedObject, "ARMATURE")
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



class Alx_OT_ModifierBevelSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_bevel_selection"
    bl_options = {'REGISTER', 'UNDO'}

    Segments : IntProperty(name="Segments", default=1, min=1)
    Width : FloatProperty(name="Width", default=0.01000, unit="LENGTH", min=0.0)
    UseWeight : BoolProperty(name="Use Weight", default=True)
    HardenNormals : BoolProperty(name="Harden Normals", default=True)

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

    UseMergeAll : BoolProperty(name="Merge All", default=True)
    UseMergeOnlyLooseEdges : BoolProperty(name="Only Loose Edges", default=True)

    MergeDistance : FloatProperty(name="Distance", default=0.00100, unit="LENGTH", min=0.0)

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

    VertexDataObject : StringProperty(options={"HIDDEN"})

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

def AlxGetBoneAlwaysLeft(Bone, Armature):
    LeftBone = ""
    if (len(Bone.name) != 0) and (len(Bone.name) > 2):
        if (Bone.name[-2] == "."):
            
            match Bone.name[-1]:
                case "R":
                    LeftBone = Bone.name[0:-1] + "L"
                case "L":
                    LeftBone = Bone.name[0:-1] + "L"
                case "r":
                    LeftBone = Bone.name[0:-1] + "l"
                case "l":
                    OppositeBoneName = Bone.name[0:-1] + "l"

    return bpy.data.objects.get(Armature).pose.bones.get(LeftBone)

def AlxGetBoneOpposite(Bone, Armature):
    OppositeBoneName = ""
    if (len(Bone.name) != 0) and (len(Bone.name) > 2):
        if (Bone.name[-2] == "."):
            
            match Bone.name[-1]:
                case "R":
                    OppositeBoneName = Bone.name[0:-1] + "L"
                case "L":
                    OppositeBoneName = Bone.name[0:-1] + "R"
                case "r":
                    OppositeBoneName = Bone.name[0:-1] + "l"
                case "l":
                    OppositeBoneName = Bone.name[0:-1] + "r"

    return bpy.data.objects.get(Armature).pose.bones.get(OppositeBoneName)

def AlxGetBoneNameOpposite(BoneName):
    OppositeBoneName = ""
    if (len(BoneName) != 0) and (len(BoneName) > 2):
        if (BoneName[-2] == "."):
            
            match BoneName[-1]:
                case "R":
                    OppositeBoneName = BoneName[0:-1] + "L"
                case "L":
                    OppositeBoneName = BoneName[0:-1] + "R"
                case "r":
                    OppositeBoneName = BoneName[0:-1] + "l"
                case "l":
                    OppositeBoneName = BoneName[0:-1] + "r"
    return OppositeBoneName

def AlxGetIKConstraint(Bone):
    for Constraint in Bone.constraints:
        if (Constraint.type == "IK"):
            return Constraint

def AlxCloneIKBoneLimitOnChain(IKHead, Armature):
    i = 0
    if (AlxGetIKConstraint(IKHead) is not None):
        ChainLength = AlxGetIKConstraint(IKHead).chain_count
        ParentOnChain = None

        IKHeadOpposite = AlxGetBoneOpposite(IKHead, Armature)

        IKHeadOpposite.use_ik_limit_x = IKHead.use_ik_limit_x
        IKHeadOpposite.ik_min_x = IKHead.ik_min_x
        IKHeadOpposite.ik_max_x = IKHead.ik_max_x

        IKHeadOpposite.use_ik_limit_y = IKHead.use_ik_limit_y
        IKHeadOpposite.ik_min_y = IKHead.ik_min_y
        IKHeadOpposite.ik_max_y = IKHead.ik_max_y

        IKHeadOpposite.use_ik_limit_z = IKHead.use_ik_limit_z
        IKHeadOpposite.ik_min_z = IKHead.ik_max_z * -1
        IKHeadOpposite.ik_max_z = IKHead.ik_min_z * -1

        ParentOnChain = IKHead
        ParentOnChainOpposite = AlxGetBoneOpposite(IKHead, Armature)
        if (ParentOnChain is not None) and (ParentOnChainOpposite is not None):
            while i < ChainLength:
                if (i < 0): break

                ParentOnChainOpposite.use_ik_limit_x = ParentOnChain.use_ik_limit_x
                ParentOnChainOpposite.ik_min_x = ParentOnChain.ik_min_x
                ParentOnChainOpposite.ik_max_x = ParentOnChain.ik_max_x


                ParentOnChainOpposite.use_ik_limit_y = ParentOnChain.use_ik_limit_y
                ParentOnChainOpposite.ik_min_y = ParentOnChain.ik_min_y
                ParentOnChainOpposite.ik_max_y = ParentOnChain.ik_max_y

                ParentOnChainOpposite.use_ik_limit_z = ParentOnChain.use_ik_limit_z
                ParentOnChainOpposite.ik_min_z = ParentOnChain.ik_max_z * -1
                ParentOnChainOpposite.ik_max_z = ParentOnChain.ik_min_z * -1

                ParentOnChain = ParentOnChain.parent
                ParentOnChainOpposite = ParentOnChainOpposite.parent
                i += 1

def AlxCloneIKSettings(CheckBone, OppositeBone):
    if (CheckBone is not None) and (OppositeBone is not None):
        CheckBoneIK = AlxGetIKConstraint(CheckBone)
        OppositeBoneIK = AlxGetIKConstraint(OppositeBone)



        if (CheckBoneIK is not None) and (OppositeBoneIK is not None):
            if (CheckBoneIK.target is not None):
                OppositeBoneIK.target = CheckBoneIK.target
                if (CheckBoneIK.target.type == "ARMATURE"):
                    if (CheckBoneIK.subtarget is not None):
                        OppositeBoneIK.subtarget = AlxGetBoneNameOpposite(CheckBoneIK.subtarget)

            if (CheckBoneIK.pole_target is not None):
                OppositeBoneIK.pole_target = CheckBoneIK.pole_target
                if (CheckBoneIK.pole_target.type == "ARMATURE"):
                    if (CheckBoneIK.pole_subtarget is not None):
                        OppositeBoneIK.pole_subtarget = AlxGetBoneNameOpposite(CheckBoneIK.pole_subtarget)
                OppositeBoneIK.pole_angle = (CheckBoneIK.pole_angle + 180)

            OppositeBoneIK.chain_count = CheckBoneIK.chain_count
            OppositeBoneIK.use_tail = CheckBoneIK.use_tail

        if (CheckBoneIK is None) and (OppositeBoneIK is not None):
            NewIK = CheckBone.constraints.new("IK")

            if (OppositeBoneIK.target is not None):
                NewIK.target = OppositeBoneIK.target

                if (OppositeBoneIK.target.type == "ARMATURE"):
                    if (OppositeBoneIK.subtarget is not None):
                        NewIK.subtarget = AlxGetBoneNameOpposite(OppositeBoneIK.subtarget)

            if (OppositeBoneIK.pole_target is not None):
                NewIK.pole_target = OppositeBoneIK.pole_target

                if (OppositeBoneIK.pole_target.type == "ARMATURE"):
                    if (OppositeBoneIK.pole_subtarget is not None):
                        NewIK.pole_subtarget = AlxGetBoneNameOpposite(OppositeBoneIK.pole_subtarget)

                NewIK.pole_angle = OppositeBoneIK.pole_angle - 180

            NewIK.chain_count = OppositeBoneIK.chain_count
            NewIK.use_tail = OppositeBoneIK.use_tail

        if (CheckBoneIK is not None) and (OppositeBoneIK is None):
            NewIK = OppositeBone.constraints.new("IK")

            if (CheckBoneIK.target is not None):
                NewIK.target = CheckBoneIK.target

                if (CheckBoneIK.target.type == "ARMATURE"):
                    if (CheckBoneIK.subtarget is not None):
                        NewIK.subtarget = AlxGetBoneNameOpposite(CheckBoneIK.subtarget)

            if (CheckBoneIK.pole_target is not None):
                NewIK.pole_target = CheckBoneIK.pole_target

                if (CheckBoneIK.pole_target.type == "ARMATURE"):
                    if (CheckBoneIK.pole_subtarget is not None):
                        NewIK.pole_subtarget = AlxGetBoneNameOpposite(CheckBoneIK.pole_subtarget)

                NewIK.pole_angle = (CheckBoneIK.pole_angle + 180)


            NewIK.chain_count = CheckBoneIK.chain_count
            NewIK.use_tail = CheckBoneIK.use_tail

class Alx_OT_BoneMatchIKByName(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.bone_match_ik_by_name"
    bl_options = {'REGISTER', 'UNDO'}

    ActivePoseArmatureObject : StringProperty(options={"HIDDEN"})

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
                                    PoseBoneLeft = AlxGetBoneAlwaysLeft(PoseBone, self.ActivePoseArmatureObject)
                                    OppositeBoneLeft = AlxGetBoneOpposite(AlxGetBoneAlwaysLeft(PoseBone, self.ActivePoseArmatureObject), self.ActivePoseArmatureObject)
                                    
                                    AlxCloneIKSettings(PoseBoneLeft, OppositeBoneLeft)
                                    AlxCloneIKBoneLimitOnChain(PoseBoneLeft, self.ActivePoseArmatureObject)


        return {"FINISHED"}

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







class AlxAddonProperties(bpy.types.PropertyGroup):
    """"""
    SceneIsolatorVisibilityTarget : EnumProperty(name="Isolator Visibility Target", options={'ENUM_FLAG'}, items=[("VIEWPORT", "Viewport", "", 1), ("RENDER", "Render", "", 2)])

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
                AlxPreferences.AlxOverHaulAddonPreferences,
                AlxAddonProperties,

                AlxPanels.Alx_PT_AlexandriaToolPanel,
                AlxPanels.Alx_PT_Scene_GeneralPivot,
                AlxPanels.Alx_MT_UnlockedModesPie,

                AlxOperators.Alx_OT_Mode_UnlockedModes,
                AlxOperators.Alx_OT_Scene_VisibilityIsolator,
                AlxOperators.Alx_OT_ModifierHideOnSelected,

                Alx_OT_ArmatureAssignToSelection,
                
                Alx_OT_ModifierBevelSelection,
                #AlxOperators.Alx_OT_ModifierSubdivisionSelection,
                Alx_OT_ModifierWeldSelection,

                Alx_OT_VertexGroupCleanEmpty,
                Alx_OT_BoneMatchIKByName,
                ]

bpy.app.handlers.load_post.append(AlxHandlers.AlxAddonKeymapHandler)

def register():
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    AlxKeymaps.KeymapCreation()
    bpy.types.Scene.alx_addon_properties = PointerProperty(type=AlxAddonProperties)

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