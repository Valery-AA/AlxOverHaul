
from inspect import getmembers, isclass
from typing import Any

from pathlib import Path
from os import sep as os_separator

import bpy


def developer_gather_addon_folders(path: str, folder_blacklist: set[str] = {"__pycache__"}):
    """
    IN path: __path__[0] from __init__ \n
    IN folder_blacklist: set[str] \n

    RETURN addon_folders: set[Path] \n
    """

    path_object: Path = Path(path)
    addon_folders: set[Path] = set()

    if (path_object.exists()) and (path_object.is_dir()):
        path_iter_queue: list[Path] = [path_object]

        for folder_path in path_iter_queue:
            if (folder_path.is_dir()) and (folder_path.exists()) and (folder_path not in addon_folders) and (folder_path.name not in folder_blacklist):
                addon_folders.add(folder_path)

                for subfolder_path in folder_path.iterdir():
                    if (subfolder_path.is_dir()) and (subfolder_path.exists()) and (subfolder_path not in addon_folders) and (subfolder_path.name not in folder_blacklist):
                        path_iter_queue.append(subfolder_path)
                        addon_folders.add(subfolder_path)

    return addon_folders


def developer_gather_addon_files(folder_paths: set[Path], file_blacklist: set[str] = {"__init__.py"}):
    """
    IN folder_paths: set[Path] \n
    IN file_blacklist: set[str] \n

    RETRUN addon_files: set[str] \n
    """

    addon_files: dict[str, Path] = dict()

    for folder_path in folder_paths:
        for file in folder_path.iterdir():
            if (file.is_file()) and (file.name not in file_blacklist) and (file.suffix == ".py"):
                addon_files.update({file.name[0:-3]: folder_path})

    return addon_files


def developer_execute_locals_update(path: str, globals: dict[str, Any], addon_files: dict[str, Path]):
    for file_name in addon_files.keys():

        if (file_name not in globals):
            relative_path = str(addon_files.get(file_name).relative_to(path)).replace(os_separator, ".")

            import_line = f"from . {relative_path if relative_path != '.' else ''} import {file_name}"
            exec(import_line, globals)
        else:
            reload_line = f"{file_name} = importlib.reload({file_name})"
            exec(reload_line, globals)


def developer_gather_classes_from_files(globals: dict[str, Any], addon_files: dict[str, Path] = None):
    addon_classes: set[str] = set()

    for file_name in addon_files.keys():

        for addon_class in getmembers(eval(file_name, globals), isclass):
            addon_classes.add(addon_class[1])

    return addon_classes


def developer_register_addon_classes(addon_classes):
    for addon_class in addon_classes:
        try:
            bpy.utils.register_class(addon_class)
        except:
            pass


def developer_unregister_addon_classes(addon_classes):
    for addon_class in addon_classes:
        try:
            bpy.utils.unregister_class(addon_class)
        except:
            pass

# AlxToolQueue = [
#                [AlxUnlockedModeling.Alx_WT_WorkSpaceTool_UnlockedModeling,
#                    None, True, False]  # tool_class, after, separator, group
# ]

# def AlxRegisterToolQueue():
#     for AlxTool in AlxToolQueue:
#         try:
#             bpy.utils.register_tool(
#                 AlxTool[0], after=AlxTool[1], separator=AlxTool[2], group=AlxTool[3])
#         except:
#             bpy.utils.unregister_tool(AlxTool[0])
#             bpy.utils.register_tool(
#                 AlxTool[0], after=AlxTool[1], separator=AlxTool[2], group=AlxTool[3])


# def AlxUnregisterToolQueue():
#     for AlxTool in AlxToolQueue:
#         try:
#             bpy.utils.unregister_tool(AlxTool[0])
#         except:
#             print("Can't Unregister", AlxTool)


# def RegisterProperties():
#     bpy.types.WindowManager.alx_session_properties = bpy.props.PointerProperty(
#         type=AlxProperties.Alx_PG_PropertyGroup_SessionProperties)
#     bpy.types.WindowManager.alx_vmc_session_properties = bpy.props.PointerProperty(
#         type=AlxProperties.Alx_PG_VMC_SessionProperties)

#     bpy.types.Scene.alx_object_selection_properties = bpy.props.CollectionProperty(
#         type=AlxAlexandriaGeneralPanel.Alx_PG_PropertyGroup_ObjectSelectionListItem)
#     bpy.types.Scene.alx_object_selection_properties_index = bpy.props.IntProperty(
#         default=0)

#     bpy.types.Scene.alx_object_selection_modifier = bpy.props.CollectionProperty(
#         type=AlxAlexandriaGeneralPanel.Alx_PG_PropertyGroup_ObjectSelectionListItem)
#     bpy.types.Scene.alx_object_selection_modifier_index = bpy.props.IntProperty(
#         default=0)

#     bpy.types.Scene.alx_scene_isolator_visibility_object_list = []
#     bpy.types.Scene.alx_scene_isolator_visibility_collection_list = []

#     bpy.types.Object.alx_self_bmesh_datablock = []
#     bpy.types.Scene.alx_draw_handler_unlocked_modeling = None
#     bpy.types.Scene.alx_tool_unlocked_modeling_properties = bpy.props.PointerProperty(
#         type=AlxUnlockedModeling.Alx_PG_PropertyGroup_UnlockedModelingProperties)

#     bpy.types.Object.alx_particle_surface_object = bpy.props.PointerProperty(
#         type=bpy.types.Object)
#     bpy.types.Object.alx_particle_generator_source_object = bpy.props.PointerProperty(
#         type=bpy.types.Object)

#     bpy.types.Object.alx_modifier_expand_settings = bpy.props.BoolProperty(
#         default=False)
#     bpy.types.Object.alx_modifier_collection = bpy.props.CollectionProperty(
#         type=AlxAlexandriaGeneralPanel.Alx_PG_PropertyGroup_ModifierSettings)


# def UnRegisterProperties():
#     del bpy.types.WindowManager.alx_session_properties

#     del bpy.types.Scene.alx_object_selection_properties
#     del bpy.types.Scene.alx_object_selection_properties_index

#     del bpy.types.Scene.alx_object_selection_modifier
#     del bpy.types.Scene.alx_object_selection_modifier_index

#     del bpy.types.Scene.alx_scene_isolator_visibility_object_list
#     del bpy.types.Scene.alx_scene_isolator_visibility_collection_list

#     del bpy.types.Object.alx_self_bmesh_datablock
#     del bpy.types.Scene.alx_draw_handler_unlocked_modeling
#     del bpy.types.Scene.alx_tool_unlocked_modeling_properties

#     del bpy.types.Object.alx_particle_surface_object
#     del bpy.types.Object.alx_particle_generator_source_object

#     del bpy.types.Object.alx_modifier_expand_settings
#     del bpy.types.Object.alx_modifier_collection


# def RegisterHandlers():
#     bpy.app.handlers.load_post.append(AlxHandlers.AlxMain_load_post)
#     bpy.app.handlers.depsgraph_update_post.append(
#         AlxHandlers.AlxMain_depsgraph_update_post)

#     bpy.app.handlers.load_post.append(AlxHandlers.AlxMsgBusSubscriptions)
#     bpy.app.handlers.load_post.append(AlxHandlers.AlxAddonKeymapHandler)
#     bpy.app.handlers.load_post.append(
#         AlxHandlers.AlxUpdateSceneSelectionObjectList)
#     bpy.app.handlers.depsgraph_update_post.append(
#         AlxHandlers.AlxUpdateSceneSelectionObjectList)


# def UnRegisterHandlers():
#     bpy.app.handlers.load_post.remove(AlxHandlers.AlxMsgBusSubscriptions)
#     bpy.app.handlers.load_post.remove(AlxHandlers.AlxAddonKeymapHandler)
#     bpy.app.handlers.load_post.remove(
#         AlxHandlers.AlxUpdateSceneSelectionObjectList)
#     bpy.app.handlers.depsgraph_update_post.remove(
#         AlxHandlers.AlxUpdateSceneSelectionObjectList)
