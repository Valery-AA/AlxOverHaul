# type:ignore

import bpy



class Alx_Object_Selection_ListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

