import bpy

class AlxAddonProperties(bpy.types.PropertyGroup):
    """"""

    scene_isolator_visibility_target : bpy.props.EnumProperty(options={'ENUM_FLAG'}, 
        items=[
            ("VIEWPORT", "Viewport", "", "RESTRICT_VIEW_OFF", 1), 
            ("RENDER", "Render", "", "RESTRICT_RENDER_OFF", 1<<1)
        ])
    
    scene_isolator_type_target : bpy.props.EnumProperty(options={'ENUM_FLAG'},
        items=[
                ("OBJECT", "Object", "", "OBJECT_DATAMODE", 1), 
                ("COLLECTION", "Collection", "", "OUTLINER_COLLECTION", 1<<1)
            ])
    
class AlxGenPanelProperties(bpy.types.PropertyGroup):
    """"""

    alx_panel_scale_x : bpy.props.FloatProperty(name="Scale Width", default=0.85, min=0.85, max=2.0)
    alx_panel_scale_y : bpy.props.FloatProperty(name="Scale Height", default=1.0, min=0.85, max=2.0)

    alx_panel_tab : bpy.props.EnumProperty(default="HOME", 
        items=[
            ("HOME", "Home", "", "HOME", 1),
            ("OBJECT", "Object", "", "OBJECT_DATAMODE", 1<<1),
            ("RENDER", "Render", "", "SCENE", 1<<2),
            ("UI_DESIGNER", "UI Designer", "", "WINDOW", 1<<3),
            ("SETTINGS", "Settings", "", "PREFERENCES", 1<<4)
        ])