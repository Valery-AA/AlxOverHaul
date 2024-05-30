bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valeria Bosco[Valy Arhal]",
    "description" : "",
    "version" : (0, 6, 0, 1),
    "warning" : "[Heavly Under Development] And Subject To Substantial Changes",
    "category" : "3D View",
    "location" : "[Ctrl Alt A] General Menu, [Shift S] Pivot Menu, [Tab] Auto Mode Pie Menu",
    "blender" : (3, 6, 0),
    "tracker_url": "https://github.com/Valery-AA/AlxOverHaul/issues",
}


import bpy
from . import addon_updater_ops


import os
import importlib

folder_blacklist = ["__pycache__", "alxoverhaul_updater"]
file_blacklist = ["__init__.py", "addon_updater_ops", "addon_updater.py", "Extras.py", ]

addon_folders = list([__path__[0]])
addon_folders.extend( [os.path.join(__path__[0], folder_name) for folder_name in os.listdir(__path__[0]) if ( os.path.isdir( os.path.join(__path__[0], folder_name) ) ) and (folder_name not in folder_blacklist) ] )

addon_files = [[folder_path, file_name[0:-3]] for folder_path in addon_folders for file_name in os.listdir(folder_path) if (file_name not in file_blacklist) and (file_name.endswith(".py"))]

for folder_file_batch in addon_files:
    if (os.path.basename(folder_file_batch[0]) == os.path.basename(__path__[0])):
        file = folder_file_batch[1]

        if (file not in locals()):
            import_line = f"from . import {file}"
            exec(import_line)
        else:
            reload_line = f"{file} = importlib.reload({file})"
            exec(reload_line)
    
    else:
        if (os.path.basename(folder_file_batch[0]) != os.path.basename(__path__[0])):
            file = folder_file_batch[1]

            if (file not in locals()):
                import_line = f"from . {os.path.basename(folder_file_batch[0])} import {file}"
                exec(import_line)
            else:
                reload_line = f"{file} = importlib.reload({file})"
                exec(reload_line)


import inspect

class_blacklist = ["PSA_UL_SequenceList"]

bpy_class_object_list = tuple(bpy_class[1] for bpy_class in inspect.getmembers(bpy.types, inspect.isclass) if (bpy_class not in class_blacklist))
alx_class_object_list = tuple(alx_class[1] for file_batch in addon_files for alx_class in inspect.getmembers(eval(file_batch[1]), inspect.isclass) if issubclass(alx_class[1], bpy_class_object_list) and (not issubclass(alx_class[1], bpy.types.WorkSpaceTool)))

AlxClassQueue = alx_class_object_list


from . import AlxProperties
from . import AlxHandlers
from . import AlxKeymapUtils
from . import AlxGeneralPanel
from . import AlxVisibilityOperators
from . import AlxUnlockedModeling


AlxToolQueue = [
               [AlxUnlockedModeling.Alx_WT_WorkSpaceTool_UnlockedModeling, None, True, False] #tool_class, after, separator, group
               ]


def AlxRegisterClassQueue():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.register_class(AlxClass)
        except:
            try:
                bpy.utils.unregister_class(AlxClass)
                bpy.utils.register_class(AlxClass)
            except:
                pass
def AlxUnregisterClassQueue():
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.unregister_class(AlxClass)
        except:
            print("Can't Unregister", AlxClass)

def AlxRegisterToolQueue():
    for AlxTool in AlxToolQueue:
        try:
            bpy.utils.register_tool(AlxTool[0], after=AlxTool[1], separator=AlxTool[2], group=AlxTool[3])
        except:
            bpy.utils.unregister_tool(AlxTool[0])
            bpy.utils.register_tool(AlxTool[0], after=AlxTool[1], separator=AlxTool[2], group=AlxTool[3])
def AlxUnregisterToolQueue():
    for AlxTool in AlxToolQueue:
        try:
            bpy.utils.unregister_tool(AlxTool[0])
        except:
            print("Can't Unregister", AlxTool)


def RegisterProperties():
    bpy.types.WindowManager.alx_session_properties = bpy.props.PointerProperty(type=AlxProperties.Alx_PG_PropertyGroup_SessionProperties)


    bpy.types.Scene.alx_object_selection_properties = bpy.props.CollectionProperty(type=AlxGeneralPanel.Alx_PG_PropertyGroup_ObjectSelectionListItem)
    bpy.types.Scene.alx_object_selection_properties_index = bpy.props.IntProperty(default=0)

    bpy.types.Scene.alx_scene_isolator_visibility_object_list = []
    bpy.types.Scene.alx_scene_isolator_visibility_collection_list = []
    bpy.types.Scene.alx_tool_scene_isolator_properties = bpy.props.PointerProperty(type=AlxVisibilityOperators.Alx_Tool_SceneIsolator_Properties)

    bpy.types.Scene.alx_panel_alexandria_general_properties = bpy.props.PointerProperty(type=AlxGeneralPanel.Alx_PG_PropertyGroup_AlexandriaGeneral)

    bpy.types.Object.alx_self_bmesh_datablock = []
    bpy.types.Scene.alx_draw_handler_unlocked_modeling = None
    bpy.types.Scene.alx_tool_unlocked_modeling_properties = bpy.props.PointerProperty(type=AlxUnlockedModeling.Alx_PG_PropertyGroup_UnlockedModelingProperties)

    bpy.types.Object.alx_particle_surface_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Object.alx_particle_generator_source_object = bpy.props.PointerProperty(type=bpy.types.Object)

    bpy.types.Object.alx_modifier_expand_settings = bpy.props.BoolProperty(default=False)
    bpy.types.Object.alx_modifier_collection = bpy.props.CollectionProperty(type=AlxGeneralPanel.Alx_PG_PropertyGroup_ModifierSettings)
def UnRegisterProperties():
    del bpy.types.WindowManager.alx_session_properties



    del bpy.types.Scene.alx_object_selection_properties
    del bpy.types.Scene.alx_object_selection_properties_index

    del bpy.types.Scene.alx_scene_isolator_visibility_object_list
    del bpy.types.Scene.alx_scene_isolator_visibility_collection_list
    del bpy.types.Scene.alx_tool_scene_isolator_properties

    del bpy.types.Scene.alx_panel_alexandria_general_properties

    del bpy.types.Object.alx_self_bmesh_datablock
    del bpy.types.Scene.alx_draw_handler_unlocked_modeling
    del bpy.types.Scene.alx_tool_unlocked_modeling_properties

    del bpy.types.Object.alx_particle_surface_object
    del bpy.types.Object.alx_particle_generator_source_object

    del bpy.types.Object.alx_modifier_expand_settings
    del bpy.types.Object.alx_modifier_collection


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
    try:
        addon_updater_ops.register(bl_info)
    except:
        pass

    AlxRegisterClassQueue()
    AlxRegisterToolQueue()

    AlxKeymapUtils.AlxCreateKeymaps()

    RegisterProperties()
    RegisterHandlers()

    bpy.context.preferences.use_preferences_save = True


def unregister():
    addon_updater_ops.unregister()

    AlxUnregisterClassQueue()
    AlxUnregisterToolQueue()

    for km, kmi in AlxKeymapUtils.AlxAddonKeymaps:
        km.keymap_items.remove(kmi)
    AlxKeymapUtils.AlxAddonKeymaps.clear()

    UnRegisterProperties()
    UnRegisterHandlers()



if __name__ == "__main__":
    register()