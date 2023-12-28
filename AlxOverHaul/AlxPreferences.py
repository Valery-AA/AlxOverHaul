import bpy

from AlxOverHaul import AlxKeymaps

class AlxAddonProperties(bpy.types.PropertyGroup):
    """"""
    
    SceneIsolatorVisibilityTarget : bpy.props.EnumProperty(name="SceneIsolatorVisibilityTarget", options={'ENUM_FLAG'}, items=[("VIEWPORT", "Viewport", "", 1), ("RENDER", "Render", "", 2)])
    

class AlxOverHaulAddonPreferences(bpy.types.AddonPreferences):
    """"""

    bl_idname = __package__

    def UPDATE_View3d_Pan_Use_Shift_GRLess(self, context):
        if (self.View3d_Pan_Use_Shift_GRLess == True):
            AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="KEYBOARD", Key="GRLESS", UseShift=True, Active=True)
        if (self.View3d_Pan_Use_Shift_GRLess == False):
            AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="MOUSE", Key="MIDDLEMOUSE", UseShift=True, Active=True)

    def UPDATE_View3d_Rotate_Use_GRLess(self, context):
        if (self.View3d_Rotate_Use_GRLess == True):
            AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="KEYBOARD", Key="GRLESS", Active=True)
        if (self.View3d_Rotate_Use_GRLess == False):
            AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="MOUSE", Key="MIDDLEMOUSE", Active=True)

    def UPDATE_View3d_Zoom_Use_GRLess(self, context):
        if (self.View3d_Zoom_Use_GRLess == True):
            AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="KEYBOARD", Key="GRLESS", UseCtrl=True, Active=True)
        if (self.View3d_Zoom_Use_GRLess == False):
            AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="MOUSE", Key="MIDDLEMOUSE", UseCtrl=True, Active=True)

    View3d_Pan_Use_Shift_GRLess : bpy.props.BoolProperty(name="Alx Preset: Change View3D Pan", description="Replace [Shift + Middle-Mouse] with [shift + GRLess] for 3D View Pan", update=UPDATE_View3d_Pan_Use_Shift_GRLess)
    View3d_Rotate_Use_GRLess : bpy.props.BoolProperty(name="Alx Preset: Change View3D Rotate", description="Replace [Middle-Mouse] with [GRLess] for 3D View Rotation", update=UPDATE_View3d_Rotate_Use_GRLess)
    View3d_Zoom_Use_GRLess : bpy.props.BoolProperty(name="Alx Preset: Change View3D Zoom", description="Replace [Ctrl + Middle-Mouse] with [Ctrl + GRLess] for 3D View Zoom", update=UPDATE_View3d_Zoom_Use_GRLess)

    def draw(self, context):
        AlxLayout = self.layout

        AlxLayout.prop(self, "View3d_Pan_Use_Shift_GRLess", toggle=True)
        AlxLayout.prop(self, "View3d_Rotate_Use_GRLess", toggle=True)
        AlxLayout.prop(self, "View3d_Zoom_Use_GRLess", toggle=True)

def GetPreferences():
    return bpy.context.preferences.addons[__package__].preferences