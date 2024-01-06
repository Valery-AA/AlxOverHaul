import bpy
from AlxOverHaul import AlxKeymaps, AlxPreferences, AlxPanels

@bpy.app.handlers.persistent
def AlxAddonKeymapHandler(self, context):
    AlxKeymaps.KeymapCreation()

@bpy.app.handlers.persistent
def AlxUpdateSceneSelectionObjectList(self, context):
    bpy.context.scene.alx_object_selection_properties.clear()
    for SelectedObject in bpy.context.selected_objects:
        Item = bpy.context.scene.alx_object_selection_properties.add()
        Item.name = SelectedObject.name
        Item.ObjectPointer = SelectedObject