import bpy

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



def AlxRetrieveContextArmature(context: bpy.types.Context):
    try:
        if (context is not None) and (context.active_object is not None):
            if (context.active_object.type == "MESH"):
                if (context.active_object.find_armature() is not None):
                    return context.active_object.find_armature()
                
            if (context.active_object.type == "ARMATURE"):
                return bpy.data.objects.get(context.active_object.name)
    except:
        print("Can't Retrieve Context Armature")
    return None