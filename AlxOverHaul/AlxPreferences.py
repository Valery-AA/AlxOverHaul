# type:ignore

import bpy
from . import addon_updater_ops

from . import AlxKeymapUtils


@addon_updater_ops.make_annotations
class AlxOverHaulAddonPreferences(bpy.types.AddonPreferences):
    """"""

    bl_idname = __package__


    addon_preference_tabs : bpy.props.EnumProperty(name="", default="HOME", 
        items=[
            ("HOME", "home", "", "HOME", 1),
            ("KEYBINDS", "keybinds", "", "EVENT_K", 1<<1),
            ("SETTINGS", "settings" , "", "PREFERENCES", 1<<2)
        ])


    auto_check_update : bpy.props.BoolProperty(name="Auto-check for Update", description="If enabled, auto-check for updates using an interval", default=False)

    updater_interval_months : bpy.props.IntProperty(name='Months', description="Number of months between checking for updates", default=0, min=0)
    updater_interval_days : bpy.props.IntProperty(name='Days', description="Number of days between checking for updates", default=7, min=0, max=31)
    updater_interval_hours : bpy.props.IntProperty(name='Hours', description="Number of hours between checking for updates", default=0, min=0, max=23)
    updater_interval_minutes : bpy.props.IntProperty(name='Minutes', description="Number of minutes between checking for updates", default=0, min=0, max=59)


    def UPDATE_View3d_Pan_Use_Shift_GRLess(self, context):
        if (self.View3d_Pan_Use_Shift_GRLess == True):
            AlxKeymapUtils.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="KEYBOARD", Key="GRLESS", UseShift=True, Active=True)
        
        if (self.View3d_Pan_Use_Shift_GRLess == False):
            AlxKeymapUtils.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="MOUSE", Key="MIDDLEMOUSE", UseShift=True, Active=True)

    def UPDATE_View3d_Rotate_Use_GRLess(self, context):
        if (self.View3d_Rotate_Use_GRLess == True):
            AlxKeymapUtils.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="KEYBOARD", Key="GRLESS", Active=True)
        if (self.View3d_Rotate_Use_GRLess == False):
            AlxKeymapUtils.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="MOUSE", Key="MIDDLEMOUSE", Active=True)

    def UPDATE_View3d_Zoom_Use_GRLess(self, context):
        if (self.View3d_Zoom_Use_GRLess == True):
            AlxKeymapUtils.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="KEYBOARD", Key="GRLESS", UseCtrl=True, Active=True)
        if (self.View3d_Zoom_Use_GRLess == False):
            AlxKeymapUtils.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="MOUSE", Key="MIDDLEMOUSE", UseCtrl=True, Active=True)


    View3d_Pan_Use_Shift_GRLess : bpy.props.BoolProperty(name="Alx Optional Keybind: Change View3D Pan", description="Replace [Shift + Middle-Mouse] with [shift + GRLess] for 3D View Pan", update=UPDATE_View3d_Pan_Use_Shift_GRLess)
    View3d_Rotate_Use_GRLess : bpy.props.BoolProperty(name="Alx Optional Keybind: Change View3D Rotate", description="Replace [Middle-Mouse] with [GRLess] for 3D View Rotation", update=UPDATE_View3d_Rotate_Use_GRLess)
    View3d_Zoom_Use_GRLess : bpy.props.BoolProperty(name="Alx Optional Keybind: Change View3D Zoom", description="Replace [Ctrl + Middle-Mouse] with [Ctrl + GRLess] for 3D View Zoom", update=UPDATE_View3d_Zoom_Use_GRLess)


    def draw(self, context):
        preference_box = self.layout
        
        preference_box.grid_flow(row_major=True, align=True).prop(self, "addon_preference_tabs", expand=True)

        if (self.addon_preference_tabs == "KEYBINDS"):
            preference_box.prop(self, "View3d_Pan_Use_Shift_GRLess", toggle=True)
            preference_box.prop(self, "View3d_Rotate_Use_GRLess", toggle=True)
            preference_box.prop(self, "View3d_Zoom_Use_GRLess", toggle=True)

        if (self.addon_preference_tabs == "SETTINGS"):
            addon_updater_ops.update_settings_ui(self,context)


def AlxGetPreferences():
    return bpy.context.preferences.addons[__package__].preferences