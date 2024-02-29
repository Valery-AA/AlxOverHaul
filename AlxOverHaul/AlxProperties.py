# type:ignore

import bpy

class Alx_Tool_UnlockedModeling_Properties(bpy.types.PropertyGroup):
    """"""

    poly_delete_type : bpy.props.EnumProperty(default="NONE",
        items=[
            ("NONE", "None", "", 1),
            ("VERTS", "Vertex", "", 1<<1),
            ("EDGES", "Edge", "", 1<<2),
            ("FACES", "Face", "", 1<<3),
            ("FACES_ONLY", "Face Only", "", 1<<4)
        ])

    edge_mark_type : bpy.props.EnumProperty(default={"NONE"}, options={"ENUM_FLAG"},
        items=[
            ("NONE", "None", "", 1),
            ("seam_edge", "Seam", "", 1<<1),
            ("sharp_edge", "Sharp", "", 1<<2),
            ("bevel_weight_edge", "Bevel", "", 1<<3),
            ("crease_edge", "Crease", "", 1<<4)
        ])

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