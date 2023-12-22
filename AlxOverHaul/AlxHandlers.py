import bpy
from AlxOverHaul import AlxKeymaps, AlxPreferences, AlxPanels

@bpy.app.handlers.persistent
def AlxAddonKeymapHandler(self, context):
    AlxKeymaps.KeymapCreation()








    #AlxKeymaps.AlxEditKeymaps(KeyconfigSource="Blender", ConfigSpaceName="Object Mode", ItemidName="object.select_more", MapType="MOUSE", Key="WHEELUPMOUSE", UseCtrl=True, Active=True)
    

