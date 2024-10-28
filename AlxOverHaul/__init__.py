from .UnlockedTools import AlxUnlockedModeling
from . import AlxAlexandriaGeneralPanel
from . import AlxKeymapUtils
from . import AlxHandlers
from . import AlxProperties
import inspect
from . import addon_updater_ops
import bpy
from pathlib import Path
from os import sep as os_separator
import importlib
bl_info = {
    "name": "AlxOverHaul",
    "author": "Valeria Bosco[Valy Arhal]",
    "description": "",
    "warning": "[Heavly Under Development] And Subject To Substantial Changes",
    "version": (0, 7, 0),
    "blender": (3, 6, 0),
    "category": "3D View",
    "location": "[Ctrl Alt A] General Menu, [Shift Alt S] Pivot Menu, [Tab] Auto Mode Pie Menu",
    "doc_url": "https://github.com/Valery-AA/AlxOverHaul/wiki",
    "tracker_url": "https://github.com/Valery-AA/AlxOverHaul/issues",
}


folder_name_blacklist: list[str] = ["__pycache__", "pythonosc"]
file_name_blacklist: list[str] = ["__init__.py"]
file_name_blacklist.extend(["addon_updater", "addon_updater_ops"])


addon_folders = []
addon_files = []

addon_path_iter = [Path(__path__[0])]
addon_path_iter.extend(Path(__path__[0]).iterdir())

for folder_path in addon_path_iter:

    if (folder_path.is_dir()) and (folder_path.exists()) and (folder_path.name not in folder_name_blacklist):
        addon_folders.append(folder_path)

        for subfolder_path in folder_path.iterdir():
            if (subfolder_path.is_dir()) and (subfolder_path.exists()):
                addon_path_iter.append(subfolder_path)
                addon_folders.append(subfolder_path)

addon_files = [[folder_path, file_name.name[0:-3]] for folder_path in addon_folders for file_name in folder_path.iterdir(
) if (file_name.is_file()) and (file_name.name not in file_name_blacklist) and (file_name.suffix == ".py")]

for folder_file_batch in addon_files:
    file = folder_file_batch[1]

    if (file not in locals()):
        relative_path = str(folder_file_batch[0].relative_to(
            __path__[0])).replace(os_separator, ".")

        import_line = f"from . {relative_path if relative_path != '.' else ''} import {file}"
        exec(import_line)
    else:
        reload_line = f"{file} = importlib.reload({file})"
        exec(reload_line)

alx_class_object_list = tuple(alx_class[1] for file_batch in addon_files for alx_class in inspect.getmembers(
    eval(file_batch[1]), inspect.isclass))

AlxClassQueue = alx_class_object_list


AlxToolQueue = [
               [AlxUnlockedModeling.Alx_WT_WorkSpaceTool_UnlockedModeling,
                   None, True, False]  # tool_class, after, separator, group
]


def AlxRegisterClassQueue(AlxClassQueue):
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.register_class(AlxClass)
        except Exception as error:
            print(error)
            try:
                bpy.utils.unregister_class(AlxClass)
                bpy.utils.register_class(AlxClass)
            except Exception as error:
                print(error)


def AlxUnregisterClassQueue(AlxClassQueue):
    for AlxClass in AlxClassQueue:
        try:
            bpy.utils.unregister_class(AlxClass)
        except:
            print("Can't Unregister", AlxClass)


def AlxRegisterToolQueue():
    for AlxTool in AlxToolQueue:
        try:
            bpy.utils.register_tool(
                AlxTool[0], after=AlxTool[1], separator=AlxTool[2], group=AlxTool[3])
        except:
            bpy.utils.unregister_tool(AlxTool[0])
            bpy.utils.register_tool(
                AlxTool[0], after=AlxTool[1], separator=AlxTool[2], group=AlxTool[3])


def AlxUnregisterToolQueue():
    for AlxTool in AlxToolQueue:
        try:
            bpy.utils.unregister_tool(AlxTool[0])
        except:
            print("Can't Unregister", AlxTool)


def RegisterProperties():
    bpy.types.WindowManager.alx_session_properties = bpy.props.PointerProperty(
        type=AlxProperties.Alx_PG_PropertyGroup_SessionProperties)
    bpy.types.WindowManager.alx_vmc_session_properties = bpy.props.PointerProperty(
        type=AlxProperties.Alx_PG_VMC_SessionProperties)

    bpy.types.Scene.alx_object_selection_properties = bpy.props.CollectionProperty(
        type=AlxAlexandriaGeneralPanel.Alx_PG_PropertyGroup_ObjectSelectionListItem)
    bpy.types.Scene.alx_object_selection_properties_index = bpy.props.IntProperty(
        default=0)

    bpy.types.Scene.alx_object_selection_modifier = bpy.props.CollectionProperty(
        type=AlxAlexandriaGeneralPanel.Alx_PG_PropertyGroup_ObjectSelectionListItem)
    bpy.types.Scene.alx_object_selection_modifier_index = bpy.props.IntProperty(
        default=0)

    bpy.types.Scene.alx_scene_isolator_visibility_object_list = []
    bpy.types.Scene.alx_scene_isolator_visibility_collection_list = []

    bpy.types.Object.alx_self_bmesh_datablock = []
    bpy.types.Scene.alx_draw_handler_unlocked_modeling = None
    bpy.types.Scene.alx_tool_unlocked_modeling_properties = bpy.props.PointerProperty(
        type=AlxUnlockedModeling.Alx_PG_PropertyGroup_UnlockedModelingProperties)

    bpy.types.Object.alx_particle_surface_object = bpy.props.PointerProperty(
        type=bpy.types.Object)
    bpy.types.Object.alx_particle_generator_source_object = bpy.props.PointerProperty(
        type=bpy.types.Object)

    bpy.types.Object.alx_modifier_expand_settings = bpy.props.BoolProperty(
        default=False)
    bpy.types.Object.alx_modifier_collection = bpy.props.CollectionProperty(
        type=AlxAlexandriaGeneralPanel.Alx_PG_PropertyGroup_ModifierSettings)


def UnRegisterProperties():
    del bpy.types.WindowManager.alx_session_properties

    del bpy.types.Scene.alx_object_selection_properties
    del bpy.types.Scene.alx_object_selection_properties_index

    del bpy.types.Scene.alx_object_selection_modifier
    del bpy.types.Scene.alx_object_selection_modifier_index

    del bpy.types.Scene.alx_scene_isolator_visibility_object_list
    del bpy.types.Scene.alx_scene_isolator_visibility_collection_list

    del bpy.types.Object.alx_self_bmesh_datablock
    del bpy.types.Scene.alx_draw_handler_unlocked_modeling
    del bpy.types.Scene.alx_tool_unlocked_modeling_properties

    del bpy.types.Object.alx_particle_surface_object
    del bpy.types.Object.alx_particle_generator_source_object

    del bpy.types.Object.alx_modifier_expand_settings
    del bpy.types.Object.alx_modifier_collection


def RegisterHandlers():
    bpy.app.handlers.load_post.append(AlxHandlers.AlxMain_load_post)
    bpy.app.handlers.depsgraph_update_post.append(
        AlxHandlers.AlxMain_depsgraph_update_post)

    bpy.app.handlers.load_post.append(AlxHandlers.AlxMsgBusSubscriptions)
    bpy.app.handlers.load_post.append(AlxHandlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.append(
        AlxHandlers.AlxUpdateSceneSelectionObjectList)
    bpy.app.handlers.depsgraph_update_post.append(
        AlxHandlers.AlxUpdateSceneSelectionObjectList)


def UnRegisterHandlers():
    bpy.app.handlers.load_post.remove(AlxHandlers.AlxMsgBusSubscriptions)
    bpy.app.handlers.load_post.remove(AlxHandlers.AlxAddonKeymapHandler)
    bpy.app.handlers.load_post.remove(
        AlxHandlers.AlxUpdateSceneSelectionObjectList)
    bpy.app.handlers.depsgraph_update_post.remove(
        AlxHandlers.AlxUpdateSceneSelectionObjectList)


def register():
    addon_updater_ops.update_path_fix = __path__
    addon_updater_ops.register(bl_info)

    AlxRegisterClassQueue(AlxClassQueue)
    AlxRegisterToolQueue()

    AlxKeymapUtils.AlxCreateKeymaps()

    RegisterProperties()
    RegisterHandlers()

    bpy.context.preferences.use_preferences_save = True


def unregister():
    addon_updater_ops.unregister()

    AlxUnregisterClassQueue(AlxClassQueue)
    AlxUnregisterToolQueue()

    for km, kmi in AlxKeymapUtils.AlxAddonKeymaps:
        km.keymap_items.remove(kmi)
    AlxKeymapUtils.AlxAddonKeymaps.clear()

    UnRegisterProperties()
    UnRegisterHandlers()


if __name__ == "__main__":
    register()
