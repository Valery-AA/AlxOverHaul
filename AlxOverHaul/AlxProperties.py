# type:ignore

import bpy

class Alx_PG_PropertyGroup_SessionProperties(bpy.types.PropertyGroup):
    """"""

    ui_simple_designer_user_ui_type : bpy.props.EnumProperty(items=[
        ("VIEW_3D", "View 3d", "", "VIEW3D", 1),
        ("IMAGE_EDITOR", "Image Editor", "", "IMAGE", 1<<1),
        ("UV", "UV Editor", "", "UV", 1<<2),
        ("CompositorNodeTree", "Compositor", "", "NODE_COMPOSITING", 1<<3),
        ("TextureNodeTree", "Texture Editor", "", "NODE_TEXTURE", 1<<4),
        ("GeometryNodeTree", "GeoNode Editor", "", "GEOMETRY_NODES", 1<<5),
        ("ShaderNodeTree", "Shader Editor", "", "NODE_MATERIAL", 1<<6),
        ("SEQUENCE_EDITOR", "Sequencer", "", "SEQUENCE", 1<<7),
        ("CLIP_EDITOR", "Clip Editor", "", "TRACKER", 1<<8),
        ("DOPESHEET", "DopeSheet", "", "ACTION", 1<<9),
        ("TIMELINE", "Timeline", "", "TIME", 1<<10),
        ("FCURVES", "FCurve Editor", "", "GRAPH", 1<<11),
        ("DRIVERS", "Drivers Editor", "", "DRIVER", 1<<12),
        ("NLA_EDITOR", "NLA Editor", "", "NLA", 1<<13),
        ("TEXT_EDITOR", "Text Editor", "", "TEXT", 1<<14),
        ("CONSOLE", "Console", "", "CONSOLE", 1<<15),
        ("INFO", "Info Panel", "", "INFO", 1<<16),
        ("OUTLINER", "Outliner", "", "OUTLINER", 1<<17),
        ("PROPERTIES", "Properties", "", "PROPERTIES", 1<<18),
        ("FILES", "Files", "", "FILEBROWSER", 1<<19),
        ("ASSETS", "Assets", "", "ASSET_MANAGER", 1<<20),
        ("SPREADSHEET", "Spreadsheet", "", "SPREADSHEET", 1<<21),
        ("PREFERENCES", "Preferences", "", "PREFERENCES", 1<<22)
    ]) #type:ignore

    vertex_reproject_target_object : bpy.props.PointerProperty(type=bpy.types.Object)
    vertex_reproject_object_use_deform : bpy.props.BoolProperty(default=False)
    vertex_reproject_object_use_cage : bpy.props.BoolProperty(default=False)

    shapekey_transfer_source_object : bpy.props.PointerProperty(type=bpy.types.Object)
    shapekey_transfer_target_object : bpy.props.PointerProperty(type=bpy.types.Object)







class Alx_Object_Selection_ListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

