# type:ignore

import bpy

def AlxCheckBlenderVersion(Version: [int] = [bpy.app.version[0]], SubVersion: [int] = [bpy.app.version[1]], TrailingVersion: [int] = [bpy.app.version[2]]):
    if (bpy.app.version[0] in Version) and (bpy.app.version[1] in SubVersion) and (bpy.app.version[2] in TrailingVersion):
        return True
    return False



AlxModifier_DataEditing_ListItemsPreset = ["DATA_TRANSFER", "WEIGHTED_NORMAL"]
AlxModifier_Generation_ListItemsPreset = ["MIRROR", "BEVEL", "SUBSURF", "BOOLEAN", "WELD", "DECIMATE", "TRIANGULATE", "SOLIDIFY", "WIREFRAME", 
                                          "SKIN", "SCREW", "ARRAY", "MULTIRES", "REMESH",
                                          ]
AlxModifier_Smoothing_ListItemsPreset = ["SMOOTH", "CORRECTIVE_SMOOTH", "LAPLACIANSMOOTH"]
AlxModifier_Displacement_ListItemsPreset = ["CAST", "CURVE", "DISPLACE"]
AlxModifier_Deformation_ListItemsPreset = ["ARMATURE", "SHRINKWRAP", "LATTICE", "SIMPLE_DEFORM", "MESH_DEFORM", "SURFACE_DEFORM", "OCEAN"]
AlxModifier_Particles_ListItemsPreset = ["PARTICLE_SYSTEM", "PARTICLE_INSTANCE"]
AlxModifier_Simulation_ListItemsPreset = ["COLLISION", "CLOTH", "SOFT_BODY", "FLUID"]

AlxModifier_Modifier_ListItemsPreset = []
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_DataEditing_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_Generation_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_Smoothing_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_Displacement_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_Deformation_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_Particles_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_DataEditing_ListItemsPreset)
AlxModifier_Modifier_ListItemsPreset.extend(AlxModifier_DataEditing_ListItemsPreset)

AlxModifier_DataEditing_EnumItemsPreset = [("DATA_TRANSFER", "Data Transfer", "", 1), ("WEIGHTED_NORMAL", "Weighted Normal", "", 1 << 1)]
AlxModifier_Generation_EnumItemsPreset = [("MIRROR", "Mirror", "", 1), ("BEVEL", "Bevel", "", 1 << 1), ("SUBSURF", "Subdivision Surface", "", 1 << 2), ("BOOLEAN", "Boolean", "", 1 << 3), 
                                          ("WELD", "Weld", "", 1 << 4), ("DECIMATE", "Decimate", "", 1 << 5), ("TRIANGULATE", "Triangulate","", 1 << 6), ("SOLIDIFY", "Solidify", "", 1 << 7),
                                          ("WIREFRAME", "Wireframe", "", 1 << 8), ("SKIN", "Skin", "", 1 << 9), ("SCREW", "Screw", "", 1 << 10), ("ARRAY", "Array", "", 1 << 11), 
                                          ("MULTIRES", "Multiresolution", "", 1 << 12), ("REMESH", "Remesh", "", 1 << 13)
                                          ]
AlxModifier_Smoothing_EnumItemsPreset = [("SMOOTH", "Smooth", "", 1), ("CORRECTIVE_SMOOTH", "Corrective Smooth", "", 1 << 1), ("LAPLACIANSMOOTH", "Lapacian Smooth", "", 1 << 2)]
AlxModifier_Displacement_EnumItemsPreset = [("CAST", "Cast", "", 1), ("CURVE", "Curve" ,"", 1 << 1), ("DISPLACE", "Displace", "", 1 << 2)]
AlxModifier_Deformation_EnumItemsPreset = [("ARMATURE", "Armature", "", 1), ("SHRINKWRAP", "Shrinkwrap", "", 1 << 1), ("LATTICE", "Lattice", "", 1 << 2), ("SIMPLE_DEFORM", "Simple Deform", "", 1 << 3), 
                                           ("MESH_DEFORM", "Mesh Deform", "", 1 << 4), ("SURFACE_DEFORM", "Surface Deform", "", 1 << 5), ("OCEAN", "Ocean", "", 1 << 6)]
AlxModifier_Particles_EnumItemsPreset = [("PARTICLE_SYSTEM", "Particle System", "", 1), ("PARTICLE_INSTANCE", "Particle Instance", "", 1 << 1)]
AlxModifier_Simulation_EnumItemsPreset = [("COLLISION", "Collision", "", 1), ("CLOTH", "Cloth", "", 1 << 1), ("SOFT_BODY", "Soft Body", "", 1 << 2), ("FLUID", "Fluid", "", 1 << 3)]


def AlxRetrieveContextObject(context: bpy.types.Context):
    try:
        if (context is not None) and (context.active_object is not None):
            if (context.active_object.type == "MESH"): 
                return context.active_object 

            else:
                for Object in bpy.context.selected_objects:
                    if (Object.type == "MESH") and (Object.find_armature() is not None) and (Object.find_armature() is AlxRetrieveContextArmature(context=context)):
                        return Object
    except:
        print("Can't Retrieve Context Object")
    return None


def AlxRetiriveObjectModifier(TargetObejct, TargetType):
    if (TargetType in AlxModifier_Modifier_ListItemsPreset):
        for Modifier in TargetObejct.modifiers:
            if (Modifier.type == TargetType):
                return Modifier
    return None

def AlxGetBoneAlwaysLeft(Bone, Armature):
    LeftBone = ""
    if (len(Bone.name) > 2):
        if (Bone.name[-2] == "."):
            
            match Bone.name[-1]:
                case "R":
                    LeftBone = Bone.name[0:-1] + "L"
                case "L":
                    LeftBone = Bone.name[0:-1] + "L"
                case "r":
                    LeftBone = Bone.name[0:-1] + "l"
                case "l":
                    LeftBone = Bone.name[0:-1] + "l"


    return Armature.pose.bones.get(LeftBone)

def AlxGetBoneAlwaysRight(Bone, Armature):
    RightBone = ""
    if (len(Bone.name) > 2):
        if (Bone.name[-2] == "."):
            
            match Bone.name[-1]:
                case "R":
                    RightBone = Bone.name[0:-1] + "R"
                case "L":
                    RightBone = Bone.name[0:-1] + "R"
                case "r":
                    RightBone = Bone.name[0:-1] + "r"
                case "l":
                    RightBone = Bone.name[0:-1] + "r"

    return Armature.pose.bones.get(RightBone)

def AlxGetBoneOpposite(Bone, Armature):
    OppositeBoneName = ""
    if (Bone is not None) and (len(Bone.name) > 2):
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

    return Armature.pose.bones.get(OppositeBoneName)

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

def AlxInvertPoleAngle(Angle):
    CorrectedAngle = Angle * (180 / 3.14)
    if (CorrectedAngle == 0):
        return 180.0 * (3.14 / 180)
    if (CorrectedAngle == 180):
        return 0.0 * (3.14 / 180)
    if (CorrectedAngle  == -180):
        return 0.0 * (3.14 / 180)
    if(CorrectedAngle > 0) and (CorrectedAngle < 180):
        Value = (180.0 - abs(CorrectedAngle))
        return Value * (3.14 / 180)
    if(CorrectedAngle < 0) and (CorrectedAngle > -180):
        Value = (-180.0 + abs(CorrectedAngle))
        return Value * (3.14 / 180)
    return 0.0

def AlxCloneIKBoneLimitOnChain(IKHead, Armature):
    i = 0

    if (IKHead is not None) and (AlxGetIKConstraint(IKHead) is not None):
        if (AlxGetIKConstraint(IKHead).use_tail == False):
            ChainLength = AlxGetIKConstraint(IKHead).chain_count + 1
        else:
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
                OppositeBoneIK.pole_angle = AlxInvertPoleAngle(CheckBoneIK.pole_angle)

            OppositeBoneIK.chain_count = CheckBoneIK.chain_count
            OppositeBoneIK.use_tail = CheckBoneIK.use_tail
            OppositeBoneIK.use_stretch = CheckBoneIK.use_stretch

        if (CheckBoneIK is None) and (OppositeBoneIK is not None):
            NewIK = CheckBone.constraints.new("IK")

            try:
                CheckBone.constraints.move(CheckBone.constraints.find(NewIK.name), OppositeBone.constraints.find(OppositeBoneIK.name))

            except:
                pass

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

                NewIK.pole_angle = AlxInvertPoleAngle(CheckBoneIK.pole_angle)

            NewIK.chain_count = OppositeBoneIK.chain_count
            NewIK.use_tail = OppositeBoneIK.use_tail
            NewIK.use_stretch = OppositeBoneIK.use_stretch

        if (CheckBoneIK is not None) and (OppositeBoneIK is None):
            NewIK = OppositeBone.constraints.new("IK")

            try:
                OppositeBone.constraints.move(OppositeBone.constraints.find(NewIK.name), CheckBone.constraints.find(CheckBoneIK.name))

            except:
                pass

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

                NewIK.pole_angle = AlxInvertPoleAngle(CheckBoneIK.pole_angle)


            NewIK.chain_count = CheckBoneIK.chain_count
            NewIK.use_tail = CheckBoneIK.use_tail
            NewIK.use_stretch = CheckBoneIK.use_stretch



        return {"FINISHED"}