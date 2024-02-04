import bpy
import time
from AlxOverHaul import AlxPreferences, AlxPanels



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
        except Exception as e:
            print(e)
            print("KEYMAP FAILED: " + ItemidName + " " + OperatorID)

def AlxKeymapRegister(KeymapCallType="", SpaceType="EMPTY", RegionType="WINDOW", ItemidName="", Key="", KeyModifier="", UseShift=False, UseCtrl=False, UseAlt=False, TriggerType="PRESS"):
    """
    Keymap Call Type: [OPERATOR, MENU, PANEL, PIE]
    Region Type: [WINDOW]
    """
    if (ItemidName != ""):
        WindowManager = bpy.context.window_manager
        KeyConfigs = WindowManager.keyconfigs.addon

        if KeyConfigs:

            CallType = ""
            if (KeymapCallType == "OPERATOR"):
                CallType = ItemidName
            if (KeymapCallType == "MENU"):
                CallType = "wm.call_menu"
            if (KeymapCallType == "PANEL"):
                CallType = "wm.call_panel"
            if (KeymapCallType == "PIE"):
                CallType = "wm.call_menu_pie"

            KeymapName = ""
            if (RegionType == "WINDOW") and (SpaceType != "VIEW_3D"):
                KeymapName = "Window"
                SpaceType = "EMPTY"
            if (SpaceType == "VIEW_3D"):
                KeymapName = "3D View"
            
            if (KeyModifier == ""):
                KeyModifier = "NONE"

            if (CallType != "") and (SpaceType != ""):
                Keymap = KeyConfigs.keymaps.new(name=KeymapName, space_type=SpaceType, region_type=RegionType)
                KeymapItem = Keymap.keymap_items.new(CallType, type=Key, key_modifier=KeyModifier, shift=UseShift, ctrl=UseCtrl, alt=UseAlt, value=TriggerType, head=True)
                if (KeymapCallType in ["PANEL", "PIE"]):
                    KeymapItem.properties.name = ItemidName
                AlxAddonKeymaps.append((Keymap, KeymapItem))

def KeymapCreation():
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

    AlxKeymapRegister(KeymapCallType="OPERATOR", RegionType="WINDOW", ItemidName="wm.window_fullscreen_toggle", Key="F11", UseAlt=True, TriggerType="PRESS")
    AlxKeymapRegister(KeymapCallType="OPERATOR", RegionType="WINDOW", ItemidName="scripts.reload", Key="F8", TriggerType="PRESS")

    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Mesh", ItemidName="mesh.select_more", MapType="MOUSE", Key="WHEELUPMOUSE", UseCtrl=True, Active=True)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Mesh", ItemidName="mesh.select_less", MapType="MOUSE", Key="WHEELDOWNMOUSE", UseCtrl=True, Active=True)
    

    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Object Non-modal", ItemidName="object.mode_set", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Image", ItemidName="object.mode_set", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Object Non-modal", ItemidName="view3d.object_mode_pie_or_toggle", Active=False)
    AlxEditKeymaps(KeyconfigSource="Blender addon", ConfigSpaceName="Object Non-modal", ItemidName="wm.call_menu_pie", OperatorID="MACHIN3_MT_modes_pie", Active=False)
    AlxKeymapRegister(KeymapCallType="PIE", SpaceType="VIEW_3D", ItemidName=AlxPanels.Alx_MT_UnlockedModesPie.bl_idname, Key="TAB", TriggerType="PRESS")

   
    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Armature", ItemidName="armature.align", Active=False)
    AlxKeymapRegister(KeymapCallType="PANEL", RegionType="WINDOW", ItemidName=AlxPanels.Alx_PT_AlexandriaGeneralPanel.bl_idname, Key="A", UseCtrl=True, UseAlt=True, TriggerType="CLICK")

    AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="3D View", ItemidName="wm.call_menu_pie", OperatorID="VIEW3D_MT_snap_pie", Active=False)
    AlxKeymapRegister(KeymapCallType="PANEL", RegionType="WINDOW", ItemidName=AlxPanels.Alx_PT_Scene_GeneralPivot.bl_idname, Key="S", UseShift=True, TriggerType="CLICK")