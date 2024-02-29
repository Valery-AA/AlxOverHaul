import bpy

from . import AlxPreferences
from .AlxPanels import Alx_PT_AlexandriaGeneralPanel, Alx_MT_UnlockedModesPie, Alx_PT_Scene_GeneralPivot

AlxAddonKeymaps = []

def AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="", ItemidName="", OperatorID="", MapType="", Key="", UseShift=False, UseCtrl=False, UseAlt=False, TriggerType="PRESS", Active=False):
    """KeyconfigSource : [Blender, Blender addon, Blender user]"""
    if (KeyconfigSource != "") and (ConfigSpaceName != ""):
        try:
            WindowManager = bpy.context.window_manager
            match KeyconfigSource:
                case "Blender":
                    DefaultKeyConfigs = WindowManager.keyconfigs.default
                case "Blender addon":
                    DefaultKeyConfigs = WindowManager.keyconfigs.addon
                case "Blender user":
                    DefaultKeyConfigs = WindowManager.keyconfigs.user

            DefaultKeyMaps = DefaultKeyConfigs.keymaps
            KeymapItems = DefaultKeyMaps[ConfigSpaceName].keymap_items
            for KeymapItem in KeymapItems:
                if (OperatorID == ""):
                    if (KeymapItem is not None) and (KeymapItem.idname == ItemidName):
                        if (MapType != ""):
                            KeymapItem.map_type = MapType
                        if (Key != ""):
                            KeymapItem.type = Key
                        KeymapItem.shift = UseShift
                        KeymapItem.ctrl = UseCtrl
                        KeymapItem.alt = UseAlt
                        KeymapItem.value = TriggerType
                        KeymapItem.active = Active

                if (OperatorID != ""):
                    if (KeymapItem is not None) and (KeymapItem.properties is not None) and (KeymapItem.idname == ItemidName) and (KeymapItem.properties.name == OperatorID):
                        if (MapType != ""):
                            KeymapItem.map_type = MapType
                        if (Key != ""):
                            KeymapItem.type = Key
                        KeymapItem.shift = UseShift
                        KeymapItem.ctrl = UseCtrl
                        KeymapItem.alt = UseAlt
                        KeymapItem.value = TriggerType
                        KeymapItem.active = Active
        except Exception as error:
            pass

def AlxKeymapRegister(keymap_call_type="", space_type="EMPTY", region_type="WINDOW", item_idname="", key="NONE", key_modifier="", use_shift=False, use_ctrl=False, use_alt=False, trigger_type="PRESS", **kwargs):
    """
    Available keymap_call_type: ["OPERATOR", "MENU", "PANEL", "PIE"]
    """
    
    WindowManager = bpy.context.window_manager
    KeymapConfigs = WindowManager.keyconfigs.addon

    keymap_name = ""
    if (region_type == "WINDOW") and (space_type != "VIEW_3D"):
        keymap_name = "Window"
        space_type = "EMPTY"
    if (space_type == "VIEW_3D"):
        keymap_name = "3D View"

    keymap_call_id = ""
    if (keymap_call_type == "OPERATOR"):
        keymap_call_id = item_idname
    if (keymap_call_type == "MENU"):
        keymap_call_id = "wm.call_menu"
    if (keymap_call_type == "PANEL"):
        keymap_call_id = "wm.call_panel"
    if (keymap_call_type == "PIE"):
        keymap_call_id = "wm.call_menu_pie"

    if (key_modifier == ""):
        key_modifier = "NONE"


    if KeymapConfigs is not None:

        if (keymap_call_id != "") and (item_idname != ""):
            Keymap = KeymapConfigs.keymaps.new(name=keymap_name, space_type=space_type, region_type=region_type)
            KeymapItem = Keymap.keymap_items.new(idname=keymap_call_id, type=key, key_modifier=key_modifier, shift=use_shift, ctrl=use_ctrl, alt=use_alt, value=trigger_type, head=True)

            if (KeymapItem.properties is not None):

                if (keymap_call_type in ["PANEL", "MENU", "PIE"]):
                    KeymapItem.properties.name = item_idname

                for property, value in kwargs.items():
                    if (hasattr(KeymapItem.properties, f"{property}")):
                        setattr(KeymapItem.properties, property, value)

            else:
                print(f"KeymapItem.properties: {KeymapItem.properties}")

            AlxAddonKeymaps.append((Keymap, KeymapItem))
    else:
        print(f"keyconfigs: {KeymapConfigs}")

def AlxKeymapCreation():
    if (AlxPreferences.AlxGetPreferences().View3d_Pan_Use_Shift_GRLess == True):
        AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="KEYBOARD", Key="GRLESS", UseShift=True, Active=True)
    if (AlxPreferences.AlxGetPreferences().View3d_Pan_Use_Shift_GRLess == False):
        AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.move", MapType="MOUSE", Key="MIDDLEMOUSE", UseShift=True, Active=True)

    if (AlxPreferences.AlxGetPreferences().View3d_Rotate_Use_GRLess == True):
        AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="KEYBOARD", Key="GRLESS", Active=True)
    if (AlxPreferences.AlxGetPreferences().View3d_Rotate_Use_GRLess == False):
        AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.rotate", MapType="MOUSE", Key="MIDDLEMOUSE", Active=True)

    if (AlxPreferences.AlxGetPreferences().View3d_Zoom_Use_GRLess == True):
        AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="KEYBOARD", Key="GRLESS", UseCtrl=True, Active=True)
    if (AlxPreferences.AlxGetPreferences() .View3d_Zoom_Use_GRLess == False):
        AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="view3d.zoom", MapType="MOUSE", Key="MIDDLEMOUSE", UseCtrl=True, Active=True)

    AlxKeymapRegister(keymap_call_type="OPERATOR", region_type="WINDOW", item_idname="wm.window_fullscreen_toggle", key="F11", use_alt=True, trigger_type="PRESS")
    AlxKeymapRegister(keymap_call_type="OPERATOR", region_type="WINDOW", item_idname="scripts.reload", key="F8", trigger_type="PRESS")

    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Mesh", ItemidName="mesh.select_more", MapType="MOUSE", Key="WHEELUPMOUSE", UseCtrl=True, Active=True)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Mesh", ItemidName="mesh.select_less", MapType="MOUSE", Key="WHEELDOWNMOUSE", UseCtrl=True, Active=True)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Mesh", ItemidName="wm.call_menu", OperatorID="VIEW3D_MT_edit_mesh_merge", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Mesh", ItemidName="mesh.dupli_extrude_cursor", Active=False)
    


    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Armature", ItemidName="armature.align", Active=False)
    AlxKeymapRegister(keymap_call_type="PANEL", region_type="WINDOW", item_idname=Alx_PT_AlexandriaGeneralPanel.bl_idname, key="A", use_ctrl=True, use_alt=True, trigger_type="CLICK")

    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Object Non-modal", ItemidName="object.mode_set", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Image", ItemidName="object.mode_set", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Object Non-modal", ItemidName="view3d.object_mode_pie_or_toggle", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender addon", ConfigSpaceName="Object Non-modal", ItemidName="wm.call_menu_pie", OperatorID="MACHIN3_MT_modes_pie", Active=False)
    AlxKeymapRegister(keymap_call_type="PIE", space_type="VIEW_3D", item_idname=Alx_MT_UnlockedModesPie.bl_idname, key="TAB", trigger_type="PRESS")

   

    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="wm.call_menu_pie", OperatorID="VIEW3D_MT_snap_pie", Active=False)
    AlxKeymapRegister(keymap_call_type="PANEL", region_type="WINDOW", item_idname=Alx_PT_Scene_GeneralPivot.bl_idname, key="S", use_shift=True, trigger_type="CLICK")