# type:ignore

import bpy

class Alx_Tool_SceneIsolator_Properties(bpy.types.PropertyGroup):
    """"""

    scene_isolator_visibility_target : bpy.props.EnumProperty(default={"VIEWPORT"},options={'ENUM_FLAG'}, 
        items=[
            ("VIEWPORT", "Viewport", "", "RESTRICT_VIEW_OFF", 1), 
            ("RENDER", "Render", "", "RESTRICT_RENDER_OFF", 1<<1)
        ])
    
    scene_isolator_type_target : bpy.props.EnumProperty(default={"OBJECT"}, options={'ENUM_FLAG'},
        items=[
                ("OBJECT", "Object", "", "OBJECT_DATAMODE", 1), 
                ("COLLECTION", "Collection", "", "OUTLINER_COLLECTION", 1<<1)
            ])

class Alx_Object_Selection_ListItem(bpy.types.PropertyGroup):
    """"""
    name : bpy.props.StringProperty()
    ObjectPointer : bpy.props.PointerProperty(type=bpy.types.Object)

class Alx_Panel_AlexandriaGeneral_Properties(bpy.types.PropertyGroup):
    """"""

    alx_panel_scale_x : bpy.props.FloatProperty(name="Scale Width", default=0.85, min=0.85, max=2.0)

    alx_panel_tab : bpy.props.EnumProperty(default="VISIBILITY", 
        items=[
            ("VISIBILITY", "Visibility", "", "HIDE_OFF", 1),
            ("OBJECT", "Object", "", "OBJECT_DATAMODE", 1<<1),
            ("ARMATURE", "Armature", "", "ARMATURE_DATA", 1<<2),
            ("MODIFIER", "Modifier", "", "PLUGIN", 1<<3),
            ("ALXOPERATORS", "AlxOPS", "", "MODIFIER", 1<<4),
            ("RENDER", "Render", "", "SCENE", 1<<5),
            ("UI_DESIGNER", "UI Designer", "", "WINDOW", 1<<6),
            ("SETTINGS", "Settings", "", "PREFERENCES", 1<<7)
        ])