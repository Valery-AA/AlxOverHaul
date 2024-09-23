import bpy

FUNCTION_CALLER_NAME = """import sys \n sys._getframe().f_back.f_code.co_name"""


def developer_log_console(python_file_name : str, object_name : str, message : str):
    print(f"{object_name} in {python_file_name} has the following log: \n {message}")


def operator_log_info(self : bpy.types.Operator, log_message : str):
    self.report({"INFO"}, log_message)

def operator_log_warning(self : bpy.types.Operator, log_message : str):
    self.report({"WARNING"}, log_message)

def operator_log_error(self : bpy.types.Operator, log_message : str):
    self.report({"ERROR"}, log_message)

def GetEnumPropertyItems(data = None, data_name:str = ""):
    if ( data is not None ) and ( data_name != "" ):
        if ( hasattr( data, "rna_type" ) ) and ( hasattr( data.rna_type, "properties" ) ):
            enum = data.rna_type.properties.get(data_name)
            if ( enum is not None ) and ( hasattr( enum, "enum_items" ) ):
                return data.rna_type.properties.get(data_name).enum_items
    return None

def GetActiveObjectContextArmature(context : bpy.types.Context):
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
        return None
    return None