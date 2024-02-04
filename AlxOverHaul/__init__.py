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

import bpy
import importlib



if ("AlxProperties" not in locals()):
    from . import AlxProperties
else:
    AlxProperties = importlib.reload(AlxProperties)

if ("AlxPreferences" not in locals()):
    from . import AlxPreferences
else:
    AlxPreferences = importlib.reload(AlxPreferences)

from .AlxPreferences import AlxGetPreferences


if ("AlxUtils" not in locals()):
    from . import AlxUtils
else:
    AlxUtils = importlib.reload(AlxUtils)

from .AlxUtils import AlxCheckBlenderVersion


if ("AlxKeymaps" not in locals()):
    from . import AlxKeymaps
else:
    AlxKeymaps = importlib.reload(AlxKeymaps)

from .AlxKeymaps import AlxAddonKeymaps, KeymapCreation

if ("AlxHandlers" not in locals()):
    from . import AlxHandlers
else:
    AlxHandlers = importlib.reload(AlxHandlers)

if ("AlxPanels" not in locals()):
    from . import AlxPanels
else:
    AlxPanels = importlib.reload(AlxPanels)

if ("AlxOperators" not in locals()):
    from . import AlxOperators
else:
    AlxOperators = importlib.reload(AlxOperators)

# Expansion Submodules

if (AlxCheckBlenderVersion([3], [6])):
    if (AlxGetPreferences().EnableStanfordExportSubmodule == True):
        if ("AlxStanfordBatchExporter" not in locals()):
            from . import AlxStanfordBatchExporter
        else:
            AlxStanfordBatchExporter = importlib.reload(AlxStanfordBatchExporter)

AlxClassQueue = [
                AlxProperties.AlxAddonProperties,
                AlxProperties.AlxGenPanelProperties,
                AlxPreferences.AlxOverHaulAddonPreferences,
                
                AlxPanels.Alx_MT_UnlockedModesPie,
                AlxPanels.Alx_PT_AlexandriaGeneralPanel,

                AlxOperators.Alx_OT_Scene_VisibilityIsolator,
                AlxOperators.Alx_OT_Mode_UnlockedModes,
                AlxOperators.Alx_OT_UI_SimpleDesigner,




                AlxPanels.ObjectSelectionListItem,
                AlxPanels.Alx_UL_Object_PropertiesList,

                # AlxTools sub-panels
                AlxPanels.Alx_PT_AlexandriaRenderPanel,
                AlxPanels.Alx_PT_AlexandriaObjectToolsPanel,

                

                
                
                AlxPanels.Alx_PT_Scene_GeneralPivot,

                
                AlxOperators.Alx_OT_Scene_UnlockedSnapping,
                

                AlxOperators.Alx_OT_Modifier_ManageOnSelected,
                AlxOperators.Alx_OT_Mesh_EditAttributes,

                AlxOperators.Alx_OT_Armature_MatchIKByMirroredName
                ]

def register():
    for AlxClass in AlxClassQueue:
        if (AlxClass is AlxPreferences.AlxOverHaulAddonPreferences) and (bpy.context.preferences.addons[__package__].preferences is None):
            bpy.utils.register_class(AlxPreferences.AlxOverHaulAddonPreferences)
        if (AlxClass is not AlxPreferences.AlxOverHaulAddonPreferences) and (hasattr(bpy.types, "%s" % AlxClass) == False):
            bpy.utils.register_class(AlxClass)



    if (AlxCheckBlenderVersion([4], [0, 1])):
        KeymapCreation()



    bpy.types.Scene.alx_addon_properties = bpy.props.PointerProperty(type=AlxProperties.AlxAddonProperties)
    bpy.types.Scene.alx_general_panel_properties = bpy.props.PointerProperty(type=AlxProperties.AlxGenPanelProperties)

    bpy.types.Scene.alx_object_selection_properties = bpy.props.CollectionProperty(type=AlxPanels.ObjectSelectionListItem)
    bpy.types.Scene.alx_object_selection_properties_index = bpy.props.IntProperty(default=0)

    bpy.types.Scene.alx_scene_isolator_visibility_object_list = []
    bpy.types.Scene.alx_scene_isolator_visibility_collection_list = []


    
    bpy.app.handlers.load_post.append(AlxHandlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.append(AlxHandlers.AlxUpdateSceneSelectionObjectList)
    bpy.app.handlers.depsgraph_update_post.append(AlxHandlers.AlxUpdateSceneSelectionObjectList)

    bpy.context.preferences.use_preferences_save = True

def unregister():
    for AlxQCls in AlxClassQueue:
        bpy.utils.unregister_class(AlxQCls)

    for km, kmi in AlxAddonKeymaps:
        km.keymap_items.remove(kmi)
    AlxAddonKeymaps.clear()

    del bpy.types.Scene.alx_addon_properties

    bpy.app.handlers.load_post.remove(AlxHandlers.AlxAddonKeymapHandler)
    bpy.app.handlers.depsgraph_update_post.remove(AlxHandlers.AlxUpdateSceneSelectionObjectList)


if __name__ == "__main__":
    register()