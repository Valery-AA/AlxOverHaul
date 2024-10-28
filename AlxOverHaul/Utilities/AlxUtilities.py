import bpy


def developer_log_console(python_file_name: str, object_name: str, message: str):
    print(f"{object_name} in {python_file_name} has the following log: \n {message}")


def operator_log_info(self: bpy.types.Operator, log_message: str):
    self.report({"INFO"}, log_message)


def operator_log_warning(self: bpy.types.Operator, log_message: str):
    self.report({"WARNING"}, log_message)


def operator_log_error(self: bpy.types.Operator, log_message: str):
    self.report({"ERROR"}, log_message)


def is_data_struct_empty(data_struct: list | set | dict | tuple):
    match type(data_struct):
        case "list":
            return (data_struct.__sizeof__() == 40)
        case "set":
            return (data_struct.__sizeof__() == 200)
        case "dict":
            return (data_struct.__sizeof__() == 48)
        case "tuple":
            return (data_struct.__sizeof__() == 24)
        case _:
            return (len(data_struct) > 0)


def get_active_object_skeleton(context: bpy.types.Context):
    try:
        if (context is not None) and (context.active_object is not None):
            match context.active_object.type:
                case "MESH":
                    return context.active_object.find_armature()

                case "ARMATURE":
                    return context.scene.objects.get(context.active_object.name)

                case _:
                    return None
    except:
        pass
    return None


def get_modifiers_types():
    return [item.identifier for item in bpy.types.Modifier.bl_rna.properties['type'].enum_items]


def get_modifiers_of_type(target_object: bpy.types.Object = None, target_type: str = ""):
    if (target_object is not None) and (target_type in get_modifiers_types()):
        return [modifier for modifier in target_object.modifiers
                if (modifier.type == target_type)]
    return None


def get_enum_property_items(data=None, data_name: str = ""):
    if (data is not None) and (data_name != ""):
        if (hasattr(data, "rna_type")) and (hasattr(data.rna_type, "properties")):
            enum = data.rna_type.properties.get(data_name)
            if (enum is not None) and (hasattr(enum, "enum_items")):
                return data.rna_type.properties.get(data_name).enum_items
    return None


def get_bone_always_left(bone: bpy.types.Bone, skeleton_object: bpy.types.Object):

    if (len(bone.name) > 2):
        if (bone.name[-2] == "."):

            match bone.name[-1]:
                case "R":
                    LeftBone = bone.name[0:-1] + "L"
                case "L":
                    LeftBone = bone.name[0:-1] + "L"
                case "r":
                    LeftBone = bone.name[0:-1] + "l"
                case "l":
                    LeftBone = bone.name[0:-1] + "l"

    return skeleton_object.pose.bones.get(LeftBone)


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


def AlxGetIKConstraint(bone: bpy.types.Bone = None):
    if (bone is not None):
        for Constraint in bone.constraints:
            if (Constraint.type == "IK"):
                return Constraint


def AlxInvertPoleAngle(Angle):
    CorrectedAngle = Angle * (180 / 3.14)
    if (CorrectedAngle == 0):
        return 180.0 * (3.14 / 180)
    if (CorrectedAngle == 180):
        return 0.0 * (3.14 / 180)
    if (CorrectedAngle == -180):
        return 0.0 * (3.14 / 180)
    if (CorrectedAngle > 0) and (CorrectedAngle < 180):
        Value = (180.0 - abs(CorrectedAngle))
        return Value * (3.14 / 180)
    if (CorrectedAngle < 0) and (CorrectedAngle > -180):
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
                if (i < 0):
                    break

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
                        OppositeBoneIK.subtarget = AlxGetBoneNameOpposite(
                            CheckBoneIK.subtarget)

            if (CheckBoneIK.pole_target is not None):
                OppositeBoneIK.pole_target = CheckBoneIK.pole_target
                if (CheckBoneIK.pole_target.type == "ARMATURE"):
                    if (CheckBoneIK.pole_subtarget is not None):
                        OppositeBoneIK.pole_subtarget = AlxGetBoneNameOpposite(
                            CheckBoneIK.pole_subtarget)
                OppositeBoneIK.pole_angle = AlxInvertPoleAngle(
                    CheckBoneIK.pole_angle)

            OppositeBoneIK.chain_count = CheckBoneIK.chain_count
            OppositeBoneIK.use_tail = CheckBoneIK.use_tail
            OppositeBoneIK.use_stretch = CheckBoneIK.use_stretch

        if (CheckBoneIK is None) and (OppositeBoneIK is not None):
            NewIK = CheckBone.constraints.new("IK")

            try:
                CheckBone.constraints.move(CheckBone.constraints.find(
                    NewIK.name), OppositeBone.constraints.find(OppositeBoneIK.name))

            except:
                pass

            if (OppositeBoneIK.target is not None):
                NewIK.target = OppositeBoneIK.target

                if (OppositeBoneIK.target.type == "ARMATURE"):
                    if (OppositeBoneIK.subtarget is not None):
                        NewIK.subtarget = AlxGetBoneNameOpposite(
                            OppositeBoneIK.subtarget)

            if (OppositeBoneIK.pole_target is not None):
                NewIK.pole_target = OppositeBoneIK.pole_target

                if (OppositeBoneIK.pole_target.type == "ARMATURE"):
                    if (OppositeBoneIK.pole_subtarget is not None):
                        NewIK.pole_subtarget = AlxGetBoneNameOpposite(
                            OppositeBoneIK.pole_subtarget)

                NewIK.pole_angle = AlxInvertPoleAngle(CheckBoneIK.pole_angle)

            NewIK.chain_count = OppositeBoneIK.chain_count
            NewIK.use_tail = OppositeBoneIK.use_tail
            NewIK.use_stretch = OppositeBoneIK.use_stretch

        if (CheckBoneIK is not None) and (OppositeBoneIK is None):
            NewIK = OppositeBone.constraints.new("IK")

            try:
                OppositeBone.constraints.move(OppositeBone.constraints.find(
                    NewIK.name), CheckBone.constraints.find(CheckBoneIK.name))

            except:
                pass

            if (CheckBoneIK.target is not None):
                NewIK.target = CheckBoneIK.target

                if (CheckBoneIK.target.type == "ARMATURE"):
                    if (CheckBoneIK.subtarget is not None):
                        NewIK.subtarget = AlxGetBoneNameOpposite(
                            CheckBoneIK.subtarget)

            if (CheckBoneIK.pole_target is not None):
                NewIK.pole_target = CheckBoneIK.pole_target

                if (CheckBoneIK.pole_target.type == "ARMATURE"):
                    if (CheckBoneIK.pole_subtarget is not None):
                        NewIK.pole_subtarget = AlxGetBoneNameOpposite(
                            CheckBoneIK.pole_subtarget)

                NewIK.pole_angle = AlxInvertPoleAngle(CheckBoneIK.pole_angle)

            NewIK.chain_count = CheckBoneIK.chain_count
            NewIK.use_tail = CheckBoneIK.use_tail
            NewIK.use_stretch = CheckBoneIK.use_stretch

        return {"FINISHED"}
