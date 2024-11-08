from .AlxHandlers import AlxMain_depsgraph_update_post
from pathlib import Path
import importlib
import bpy

from .AlxModuleAutoloader import (
    developer_gather_addon_folders,
    developer_gather_addon_files,
    developer_execute_locals_update,
    developer_gather_classes_from_files,
    developer_register_addon_classes,
    developer_unregister_addon_classes
)

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


addon_path = __path__[0]
addon_folders: set[Path] = set()
addon_files: dict[str, Path] = dict()
addon_classes: set[str] = set()

folder_blacklist: set[str] = {"__pycache__"}
file_blacklist: set[str] = {"__init__.py"}


def register():
    try:
        addon_updater_ops.update_path_fix = __path__
        addon_updater_ops.register(bl_info)
    except:
         pass

    addon_folders = developer_gather_addon_folders(addon_path, folder_blacklist)
    addon_files = developer_gather_addon_files(addon_folders, file_blacklist)
    developer_execute_locals_update(addon_path, globals(), addon_files)

    addon_classes = developer_gather_classes_from_files(globals(), addon_files)

    developer_register_addon_classes(addon_classes)

    bpy.app.handlers.depsgraph_update_post.append(AlxMain_depsgraph_update_post)


    bpy.context.preferences.use_preferences_save = True


def unregister():
    developer_unregister_addon_classes(addon_classes)
    addon_updater_ops.unregister()


if __name__ == "__main__":
    register()
