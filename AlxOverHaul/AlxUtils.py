import bpy

def AlxRetrieveContextObject(context):
    try:
        if (context is not None):
            if (context.active_object is not None):
                if (context.active_object.type == "MESH"):
                    AlxContextObject = context.active_object
                    return AlxContextObject
            for Object in bpy.context.selected_objects:
                if (Object.type == "MESH") and (Object.find_armature() is not None) and (Object.find_armature() is AlxRetrieveContextArmature(context=context)):
                    AlxContextObject = Object
                    return AlxContextObject
    except:
        return None
    return None

def AlxRetrieveContextArmature(context):
    try:
        if (context is not None):
            if (context.active_object is not None):
                if (context.active_object.type == "MESH"):
                    if (context.active_object.find_armature() is not None):
                        AlxContextArmature = context.active_object.find_armature()
                        return AlxContextArmature
                if (context.active_object.type == "ARMATURE"):
                    AlxContextArmature = bpy.data.objects.get(context.active_object.name)
                    return AlxContextArmature
    except:
        return None
    return None