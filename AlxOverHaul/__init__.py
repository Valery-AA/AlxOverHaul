bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valeria Bosco[Valy Arhal]",
    "description" : "For proper functionality [Blender] keymaps preset shoudl be used, [Blender 27x and Industry Compatible] will result in severe keymap conflicts",
    "version" : (0, 5, 6),
    "warning" : "[Heavly Under Development] And Subject To Substantial Changes",
    "category" : "3D View",
    "location" : "[Ctrl Alt A] General Menu, [Shift S] Pivot Menu, [Tab] Auto Mode Pie Menu",
    "blender" : (3, 6, 0)
}



import bpy

# Class Import/Reload
import os
import importlib

addon_files = [file_name[0:-3] for file_name in os.listdir(__path__[0]) if (file_name[0:3] == "Alx") and (file_name.endswith(".py"))]

for file in addon_files:
    if (file not in locals()):
        import_line = f"from . import {file}"
        exec(import_line)
    else:
        reload_line = f"{file} = importlib.reload({file})"
        exec(reload_line)

# Class Queue
import inspect

bpy_class_object_list = tuple(bpy_class[1] for bpy_class in inspect.getmembers(bpy.types, inspect.isclass))
alx_class_object_list = tuple(alx_class[1] for file in addon_files for alx_class in inspect.getmembers(eval(file), inspect.isclass) if issubclass(alx_class[1], bpy_class_object_list) and (not issubclass(alx_class[1], bpy.types.WorkSpaceTool)))

AlxClassQueue = alx_class_object_list


from . import AlxHandlers
from . import AlxKeymapUtils

from .import AlxGeneralPanel
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
            bpy.utils.unregister_class(AlxClass)
            bpy.utils.register_class(AlxClass)
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
    bpy.types.Object.alx_modifier_collection = bpy.props.CollectionProperty(type=AlxGeneralPanel.Alx_PG_PropertyGroup_ModifierSettings)
def UnRegisterProperties():
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
    AlxRegisterClassQueue()
    AlxRegisterToolQueue()

    AlxKeymapUtils.AlxCreateKeymaps()

    RegisterProperties()
    RegisterHandlers()

    bpy.context.preferences.use_preferences_save = True

def unregister():
    AlxUnregisterClassQueue()
    AlxUnregisterToolQueue()

    for km, kmi in AlxKeymapUtils.AlxAddonKeymaps:
        km.keymap_items.remove(kmi)
    AlxKeymapUtils.AlxAddonKeymaps.clear()

    UnRegisterProperties()
    UnRegisterHandlers()



if __name__ == "__main__":
    register()