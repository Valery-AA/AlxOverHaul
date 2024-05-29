# type:ignore

import bpy

class Alx_PG_PropertyGroup_SessionProperties(bpy.types.PropertyGroup):
    """"""

    vertex_reproject_target_object : bpy.props.PointerProperty(type=bpy.types.Object)
    vertex_reproject_object_use_deform : bpy.props.BoolProperty(default=False)
    vertex_reproject_object_use_cage : bpy.props.BoolProperty(default=False)

    shapekey_transfer_source_object : bpy.props.PointerProperty(type=bpy.types.Object)
    shapekey_transfer_target_object : bpy.props.PointerProperty(type=bpy.types.Object)







class Alx_Object_Selection_ListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

