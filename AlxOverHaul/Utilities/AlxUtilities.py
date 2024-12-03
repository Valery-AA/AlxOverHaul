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
