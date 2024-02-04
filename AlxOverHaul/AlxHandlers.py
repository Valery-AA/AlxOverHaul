import bpy
from .AlxKeymaps import KeymapCreation

@bpy.app.handlers.persistent
def AlxAddonKeymapHandler(self, context):
    KeymapCreation()

@bpy.app.handlers.persistent
def AlxUpdateSceneSelectionObjectList(self, context: bpy.types.Context):
    for scene in bpy.data.scenes:
        scene.alx_object_selection_properties.clear()

    SelectedObjects = [object for scene in bpy.data.scenes for object in scene.objects if (object.select_get() == True)]
    
    for scene in bpy.data.scenes:
        for Object in SelectedObjects:
            Item = scene.alx_object_selection_properties.add()
            Item.name = Object.name
            Item.ObjectPointer = Object