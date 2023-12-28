import bpy
from AlxOverHaul import AlxKeymaps, AlxPreferences, AlxPanels

@bpy.app.handlers.persistent
def AlxAddonKeymapHandler(self, context):
    AlxKeymaps.KeymapCreation()