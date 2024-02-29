bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valeria Bosco[Valy Arhal]",
    "description" : "For proper functionality [Blender] keymaps preset shoudl be used, [Blender 27x and Industry Compatible] will result in severe keymap conflicts",
    "version" : (0, 5, 4),
    "warning" : "[Heavly Under Development] And Subject To Substantial Changes",
    "category" : "3D View",
    "location" : "[Ctrl Alt A] Tool Menu, [Shift S] Pivot Menu, [Tab] Mode Compact Menu",
    "blender" : (3, 6, 0)
}

__ALX_DEBUG__ = False

import importlib
import bpy

if ("AlxCallbacks" not in locals()):
    from . import AlxCallbacks
else:
    AlxCallbacks = importlib.reload(AlxCallbacks)

if ("AlxGpuUI" not in locals()):
    from . import AlxGpuUI
else:
    AlxGpuUI = importlib.reload(AlxGpuUI)

if ("AlxHandlers" not in locals()):
    from . import AlxHandlers
else:
    AlxHandlers = importlib.reload(AlxHandlers)

if ("AlxKeymaps" not in locals()):
    from . import AlxKeymaps
else:
    AlxKeymaps = importlib.reload(AlxKeymaps)

if ("AlxOperators" not in locals()):
    from . import AlxOperators
else:
    AlxOperators = importlib.reload(AlxOperators)

if ("AlxPanels" not in locals()):
    from . import AlxPanels
else:
    AlxPanels = importlib.reload(AlxPanels)

if ("AlxPreferences" not in locals()):
    from . import AlxPreferences
else:
    AlxPreferences = importlib.reload(AlxPreferences)

if ("AlxProperties" not in locals()):
    from . import AlxProperties
else:
    AlxProperties = importlib.reload(AlxProperties)

if ("AlxUnlockedModeling" not in locals()):
    from . import AlxUnlockedModeling
else:
    AlxUnlockedModeling = importlib.reload(AlxUnlockedModeling)

if ("AlxUtils" not in locals()):
    from . import AlxUtils
else:
    AlxUtils = importlib.reload(AlxUtils)
    

from .AlxCallbacks import notify_context_mode_update, notify_workspace_tool_update

from .AlxUtils import AlxCheckBlenderVersion
from .AlxKeymaps import AlxAddonKeymaps, AlxKeymapCreation

AlxClassQueue = [
                AlxPreferences.AlxOverHaulAddonPreferences,
                AlxProperties.Alx_Tool_UnlockedModeling_Properties,
                AlxUnlockedModeling.Alx_OT_Tool_UnlockedModeling,
                AlxUnlockedModeling.Alx_PT_Panel_UnlockedModeling,

                AlxOperators.Alx_OT_Armature_MatchIKByMirroredName,
                AlxOperators.Alx_OT_Mesh_EditAttributes,
                AlxOperators.Alx_OT_Mesh_BoundaryMultiTool,

                AlxProperties.Alx_Panel_AlexandriaGeneral_Properties,
                AlxProperties.Alx_Tool_SceneIsolator_Properties,
                AlxOperators.Alx_OT_Scene_VisibilityIsolator,
                AlxProperties.Alx_Object_Selection_ListItem,
                AlxPanels.Alx_UL_Object_PropertiesList,
                AlxOperators.Alx_OT_Modifier_ManageOnSelected,
                AlxPanels.Alx_UL_Object_ModifierList,
                AlxOperators.Alx_OT_UI_SimpleDesigner,
                AlxPanels.Alx_PT_AlexandriaModifierPanel,
                AlxPanels.Alx_PT_AlexandriaGeneralPanel,
                
                AlxOperators.Alx_OT_Mode_UnlockedModes,
                AlxPanels.Alx_MT_UnlockedModesPie,

                AlxPanels.Alx_PT_Scene_GeneralPivot,
                ]

AlxToolQueue = [
               dict(tool_class=AlxUnlockedModeling.Alx_WT_WorkSpaceTool_UnlockedModeling, after=None, separator=True, group=False)
               ]

def RegisterProperties():
    bpy.types.Scene.alx_tool_unlocked_modeling_properties = bpy.props.PointerProperty(type=AlxProperties.Alx_Tool_UnlockedModeling_Properties)

    bpy.types.Scene.alx_panel_alexandria_general_properties = bpy.props.PointerProperty(type=AlxProperties.Alx_Panel_AlexandriaGeneral_Properties)
    bpy.types.Scene.alx_tool_scene_isolator_properties = bpy.props.PointerProperty(type=AlxProperties.Alx_Tool_SceneIsolator_Properties)

    bpy.types.Scene.alx_object_selection_properties = bpy.props.CollectionProperty(type=AlxProperties.Alx_Object_Selection_ListItem)
    bpy.types.Scene.alx_object_selection_properties_index = bpy.props.IntProperty(default=0)

    bpy.types.Scene.alx_scene_isolator_visibility_object_list = []
    bpy.types.Scene.alx_scene_isolator_visibility_collection_list = []

    bpy.types.Object.alx_self_bmesh_datablock = []
    bpy.types.Scene.alx_draw_handler_unlocked_modeling = None

def UnRegisterProperties():
    del bpy.types.Scene.alx_tool_unlocked_modeling_properties
    del bpy.types.Scene.alx_panel_alexandria_general_properties
    del bpy.types.Scene.alx_tool_scene_isolator_properties

    del bpy.types.Scene.alx_scene_isolator_visibility_object_list
    del bpy.types.Scene.alx_scene_isolator_visibility_collection_list

    del bpy.types.Object.alx_self_bmesh_datablock
    del bpy.types.Scene.alx_draw_handler_unlocked_modeling

def RegisterHandlers():
    bpy.app.handlers.load_post.append(AlxHandlers.AlxMsgBusSubscriptions)
    bpy.app.handlers.load_post.append(AlxHandlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.append(AlxHandlers.AlxUpdateSceneSelectionObjectList)
    bpy.app.handlers.depsgraph_update_post.append(AlxHandlers.AlxUpdateSceneSelectionObjectList)

def UnRegisterHandlers():
    bpy.app.handlers.load_post.remove(AlxHandlers.AlxMsgBusSubscriptions)
    bpy.app.handlers.load_post.remove(AlxHandlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.remove(AlxHandlers.AlxUpdateSceneSelectionObjectList)
    bpy.app.handlers.depsgraph_update_post.remove(AlxHandlers.AlxUpdateSceneSelectionObjectList)

def register():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.register_class(AlxClass)
        except:
            bpy.utils.unregister_class(AlxClass)
            bpy.utils.register_class(AlxClass)

    for AlxTool in AlxToolQueue:
        try:
            bpy.utils.register_tool(AlxTool.get("tool_class"), after=AlxTool.get("after"), separator=AlxTool.get("separator"), group=AlxTool.get("group"))
        except:
            bpy.utils.unregister_tool(AlxTool.get("tool_class"))
            bpy.utils.register_tool(AlxTool.get("tool_class"), after=AlxTool.get("after"), separator=AlxTool.get("separator"), group=AlxTool.get("group"))

    AlxKeymapCreation()

    RegisterProperties()
    RegisterHandlers()

    bpy.context.preferences.use_preferences_save = True



def unregister():
    for AlxClass in AlxClassQueue:
        bpy.utils.unregister_class(AlxClass)

    for AlxTool in AlxToolQueue:
        bpy.utils.unregister_tool(AlxTool.get("tool_class"))

    for km, kmi in AlxAddonKeymaps:
        km.keymap_items.remove(kmi)
    AlxAddonKeymaps.clear()

    UnRegisterProperties()
    UnRegisterHandlers()


if __name__ == "__main__":
    register()

