import bpy

AlxAddonKeymaps = []

def AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="", ItemidName="", OperatorID="", MapType="", Key="", UseShift=False, UseCtrl=False, UseAlt=False, TriggerType="PRESS", Active=False):
    """KeyconfigSource : [Blender, Blender addon, Blender user]"""
    if (KeyconfigSource != "") and (ConfigSpaceName != ""):
        WindowManager = bpy.context.window_manager
        DefaultKeyConfigs = WindowManager.keyconfigs[KeyconfigSource]
        DefaultKeyMaps = DefaultKeyConfigs.keymaps

        try:
            for KeymapItem in DefaultKeyMaps[ConfigSpaceName].keymap_items:
                if (OperatorID == ""):
                    if (KeymapItem is not None) and (KeymapItem.idname == ItemidName):
                        KeymapItem.map_type = MapType
                        KeymapItem.type = Key
                        KeymapItem.shift = UseShift
                        KeymapItem.ctrl = UseCtrl
                        KeymapItem.alt = UseAlt
                        KeymapItem.value = TriggerType
                        KeymapItem.active = Active

                if (OperatorID != ""):
                    if (KeymapItem is not None) and (KeymapItem.properties is not None) and (KeymapItem.idname == ItemidName) and (KeymapItem.properties.name == OperatorID):
                        KeymapItem.map_type = MapType
                        KeymapItem.type = Key
                        KeymapItem.shift = UseShift
                        KeymapItem.ctrl = UseCtrl
                        KeymapItem.alt = UseAlt
                        KeymapItem.value = TriggerType
                        KeymapItem.active = Active
        except:
            print("KEYMAP FAILED: " + ItemidName + " " + OperatorID)

def AlxKeymapRegister(KeymapCallType="", SpaceType="EMPTY", RegionType="WINDOW", ItemidName="", Key="", KeyModifier="", UseShift=False, UseCtrl=False, UseAlt=False, TriggerType="PRESS"):
    """
    Keymap Call Type: [OPERATOR, PANEL, PIE]
    Region Type: [WINDOW]
    """
    if (ItemidName != ""):
        WindowManager = bpy.context.window_manager
        KeyConfigs = WindowManager.keyconfigs.addon

        if KeyConfigs:

            CallType = ""
            if (KeymapCallType == "OPERATOR"):
                CallType = ItemidName
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
