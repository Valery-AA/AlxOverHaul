bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valery [.V Arhal]",
    "description" : "",
    "version" : (0, 3, 1),
    "warning" : "[Heavly Under Development] Minimum Supported BL Version 3.0",
    "category" : "3D View",
    "location" : "[Ctrl Alt A] PieMenu, [Alx 3D] Panel Tab",
    "blender" : (3, 6, 2)
}

if "bpy" in locals():
    import importlib
    if "AlxPackage" in locals():
        importlib.reload(AlxPackage)

import bpy
from bpy.types import Context
import AlxPackage
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty


class Alx_MT_AlexandriaToolPie(bpy.types.Menu):
    bl_label = "Alexandria Tool Pie"
    bl_idname = "alx.menu_alexandria_tool_pie"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        AlxLayout = self.layout

        PieUI = AlxLayout.menu_pie()

        if (context.active_object is not None):
            
            AlxParentArmature = None
            AlxContextObject = None

            if (context.active_object.type == "MESH") and (context.active_object.find_armature() is not None):
                AlxParentArmature = context.active_object.find_armature()
                AlxContextObject = context.active_object.name
            if (context.active_object.type == "ARMATURE") and (context.active_object is not None):
                AlxParentArmature = bpy.data.objects[context.active_object.name]

        PieUI.box().label(text = "PLACEHOLDER")

        RBoxMenuSpace = PieUI.box()
        OT_MBSelection = RBoxMenuSpace.row().operator(Alx_OT_ModifierBevelSelection.bl_idname, text="Bevel")
        OT_MSSelection = RBoxMenuSpace.row().operator(Alx_OT_ModifierSubdivisionSelection.bl_idname, text="SubDivision")

        BBoxMenuSpace = PieUI.box()

        BBoxMenuSpace.label(text="Available Mode:")

        ModeSwitchRow = BBoxMenuSpace.row(align=True)

        if (context.mode != "OBJECT"):
            OT_MOSwitch = ModeSwitchRow.operator(Alx_OT_ModeObjectSwitch.bl_idname, text="OBJECT", emboss=True)

        if (context.mode != "POSE") and (AlxParentArmature is not None):
            OT_MPSwitch = ModeSwitchRow.operator(Alx_OT_ModePoseSwitch.bl_idname, text="POSE", emboss=True)
            OT_MPSwitch.PoseActiveArmature = AlxParentArmature.name

        if (context.mode != "PAINT_WEIGHT") and (AlxParentArmature is not None) and (AlxContextObject is not None):
            OT_MWPSwitch = ModeSwitchRow.operator(Alx_OT_ModeWeightPaintSwitch.bl_idname, text="WEIGHT PAINT", emboss=True)
            OT_MWPSwitch.WeightPaintActiveArmature = AlxParentArmature.name
            OT_MWPSwitch.WeightPaintActiveObject = AlxContextObject

        BBoxMenuSpace.label(text="Render Mode:")
        BBoxMenuSpace.row(align=True).prop(context.area.spaces.active.shading, "type", text="", expand=True)

        TBoxMenuSpace = PieUI.box()

        if (AlxParentArmature is not None):
            TBoxMenuSpace.row().prop(bpy.data.armatures[AlxParentArmature.data.name], "pose_position", expand=True)
        else:
            TBoxMenuSpace.label(text="No Influencing Armature Found")

        if (context.active_object is not None):
            TBoxMenuSpace.row().prop(context.active_object, "display_type")

        BevelVisibilityRow = TBoxMenuSpace.row(align=True)

        OT_MBSwitch = BevelVisibilityRow.operator(Alx_OT_ModifierBevelSwitch.bl_idname, text="Bevel On", emboss=True)
        OT_MBSwitch.ModVisibility = True

        OT_MBSwitch = BevelVisibilityRow.operator(Alx_OT_ModifierBevelSwitch.bl_idname, text="Bevel Off", emboss=True)
        OT_MBSwitch.ModVisibility = False

        OverlayShadingRow = TBoxMenuSpace.row(align=True)
        OverlayShadingRow.prop(context.area.spaces.active.shading, "show_xray", text="Mesh", icon="XRAY")
        OverlayShadingRow.prop(context.space_data.overlay, "show_xray_bone", text="Bone", icon="XRAY")

        OverlayShadingRow.prop(context.space_data.overlay, "show_wireframes", text="", icon="MOD_WIREFRAME")

        ObjectIsolatorRow = TBoxMenuSpace.row(align=True) 
        OT_Isolate = ObjectIsolatorRow.operator(Alx_OT_ModeObjectIsolator.bl_idname, text="Isolate", emboss=True)
        OT_Isolate.IsolatorState = True
        OT_Isolate = ObjectIsolatorRow.operator(Alx_OT_ModeObjectIsolator.bl_idname, text="Show All", emboss=True)
        OT_Isolate.IsolatorState = False

        PieUI.box().label(text = "PLACEHOLDER")
        PieUI.box().label(text = "PLACEHOLDER")

class Alx_OT_ModeObjectIsolator(bpy.types.Operator):
    """"""

    # Missing Auto Restore Visibility List

    bl_label = ""
    bl_idname = "alx.mode_object_isolator"

    IsolatorState: BoolProperty()

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        ActiveOBJName = bpy.data.objects[bpy.context.view_layer.objects.active.name].data.name
        for SceneOBJ in bpy.data.objects:
            if SceneOBJ.data.name != ActiveOBJName:
                bpy.data.objects[SceneOBJ.name].hide_viewport = self.IsolatorState
        return {"FINISHED"}

class Alx_OT_ModeObjectSwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.mode_object_switch"

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")

        return {"FINISHED"}

class Alx_OT_ModePoseSwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.mode_pose_switch"

    PoseActiveArmature : StringProperty()

    @classmethod
    def poll (self, context):
        return (context.mode != "PAINT_WEIGHT")
    
    def execute(self, context):

        if (context.mode != "POSE") and (self.PoseActiveArmature != ""):

            if (bpy.data.objects[self.PoseActiveArmature] is not None):
                bpy.context.view_layer.objects.active = bpy.data.objects[self.PoseActiveArmature]

            if (context.active_object.type == "ARMATURE"):
                bpy.ops.object.mode_set(mode="POSE")
        return {"FINISHED"}

class Alx_OT_ModeWeightPaintSwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.mode_weight_paint_switch"

    WeightPaintActiveArmature : StringProperty()
    WeightPaintActiveObject : StringProperty()

    @classmethod
    def poll (self, context):
        return (context.mode != "POSE")
    
    def execute(self, context):

        if (context.mode != "PAINT_WEIGHT") and (self.WeightPaintActiveArmature != ""):
            
            bpy.data.objects[self.WeightPaintActiveArmature].select_set(True)

            if (bpy.data.objects[self.WeightPaintActiveArmature] is not None):
                bpy.context.view_layer.objects.active =  bpy.data.objects[self.WeightPaintActiveObject]

            if (context.active_object.type == "MESH"):
                bpy.ops.object.mode_set(mode="WEIGHT_PAINT")

        return {"FINISHED"}



class Alx_OT_ModifierBevelSwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_bevel_switch_visibility"

    ModVisibility : BoolProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for ObjWmod in bpy.data.objects:
            objMODs = getattr(ObjWmod, "modifiers", [])
            for objMOD in objMODs:
                if (objMOD.type == "BEVEL"):
                    objMOD.show_viewport = self.ModVisibility

        return {"FINISHED"}

class Alx_OT_ModifierBevelSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_bevel_selection"

    ShouldOverride : BoolProperty(name="Should Override", default=True)

    Segments : IntProperty(name="Segments", default=1)
    Width : FloatProperty(name="Width", default=0.01000, unit="LENGTH")
    UseWeight : BoolProperty(name="Use Weight", default=True)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        for SelObj in bpy.context.selected_objects:
            if (SelObj.type == "MESH"):
                match self.ShouldOverride:
                    case True:
                        objMODs = getattr(SelObj, "modifiers", [])
                        for objMOD in objMODs:
                            if (objMOD.type == "BEVEL"):

                                objMOD.segments = self.Segments
                                objMOD.width = self.Width
                                
                                match self.UseWeight:
                                    case True:
                                        objMOD.limit_method = "WEIGHT"
                                    case False:
                                        objMOD.limit_method = "ANGLE"
                                        objMOD.angle_limit = 30 * (3.14/180)

                                objMOD.miter_outer = "MITER_ARC"
                                objMOD.harden_normals = True

                    case False:

                        NewBMod = SelObj.modifiers.new("Bevel", "BEVEL")
                        NewBMod.segments = self.Segments
                        NewBMod.width = self.Width

                        match self.UseWeight:
                                    case True:
                                        NewBMod.limit_method = "WEIGHT"
                                    case False:
                                        NewBMod.limit_method = "ANGLE"
                                        NewBMod.angle_limit = 30 * (3.14/180)

                        NewBMod.miter_outer = "MITER_ARC"
                        NewBMod.harden_normals = True      
        return {"FINISHED"}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class Alx_OT_ModifierSubdivisionSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_subdivision_selection"

    ShouldOverride : BoolProperty(name="Should Override", default=True)

    UseSimple : BoolProperty(name="Simple", default=False)
    ViewportLevel : IntProperty(name="Viewport", default=1)
    RenderLevel : IntProperty(name="Render", default=1)
    Complex : BoolProperty(name="Complex", default=True)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        for SelObj in bpy.context.selected_objects:
            if (SelObj.type == "MESH"):
                match self.ShouldOverride:
                    case True:
                        objMODs = getattr(SelObj, "modifiers", [])
                        for objMOD in objMODs:
                            if (objMOD.type == "SUBSURF"):

                                match self.UseSimple:
                                    case True:
                                        objMOD.subdivision_type = "SIMPLE"
                                    case False:
                                        objMOD.subdivision_type = "CATMULL_CLARK"

                                objMOD.levels = self.ViewportLevel
                                objMOD.render_levels = self.RenderLevel
                                objMOD.show_only_control_edges = self.Complex

                    case False:

                        NewBMod = SelObj.modifiers.new("Subdivision Surface", "SUBSURF")

                        match self.UseSimple:
                                    case True:
                                        NewBMod.subdivision_type = "SIMPLE"
                                    case False:
                                        NewBMod.subdivision_type = "CATMULL_CLARK"

                        NewBMod.levels = self.ViewportLevel
                        NewBMod.render_levels = self.RenderLevel
                        NewBMod.show_only_control_edges = self.Complex

        return {"FINISHED"}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class Alx_PT_PanelIDMapping(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "alx.panel_vertex_idmapping"

    bl_category = "Alx 3D"

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        
        AlxLayout = self.layout






















  



class Alx_UL_ActionSelector(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            pass

class Alx_Panel_SwapArmatureAction(bpy.types.Panel):
    """"""

    bl_label = "Alx Action Selector"
    bl_idname = "Alx.Action_OT_Selector"

    bl_category = "Alx 3D"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        if (context.mode == "OBJECT") or (context.mode == "PAINT_WEIGHT") or (context.mode =="POSE"):
            return True

    def draw(self, context):
        Alxlayout = self.layout
        obj = context.object
        Alxlayout.template_list("Alx_UL_ActionSelector", "", bpy.data, "actions", obj, "UIActionIndex")

@bpy.app.handlers.persistent
def AlxUpdateActionUI(context):
        if (bpy.context.view_layer.objects.active is not None) and (bpy.context.view_layer.objects.active.find_armature() is not None):
            AlxActionParentArmature = bpy.data.armatures[bpy.context.view_layer.objects.active.find_armature().data.name]
        
            if (AlxActionParentArmature is not None) and (AlxActionParentArmature.animation_data is not None):
                ActiveActionIndex = bpy.data.actions.find(AlxActionParentArmature.animation_data.action.name)

                if ActiveActionIndex != AlxActionParentArmature.UIActionIndex:
                    AlxActionParentArmature.UIActionIndex = ActiveActionIndex

def AlxUpdateAddonActionList(self, context):
    if(bpy.context.view_layer.objects.active is not None):
        if (bpy.context.view_layer.objects.active.find_armature() is not None):
            AlxActionParentArmature = bpy.data.armatures[bpy.context.view_layer.objects.active.find_armature().data.name]

            if (AlxActionParentArmature is not None):
                if (AlxActionParentArmature is not None) and (AlxActionParentArmature.animation_data is not None):
                    AlxActionParentArmature.animation_data.action = bpy.data.actions[AlxActionParentArmature.UIActionIndex]
                    bpy.context.scene.frame_current = 0

bpy.app.handlers.depsgraph_update_post.append(AlxUpdateActionUI)





AlxClassQueue = [
                Alx_MT_AlexandriaToolPie,

                Alx_OT_ModeObjectIsolator,
                Alx_OT_ModeObjectSwitch,
                Alx_OT_ModePoseSwitch,
                Alx_OT_ModeWeightPaintSwitch,

                Alx_OT_ModifierBevelSwitch,
                
                Alx_OT_ModifierBevelSelection,
                Alx_OT_ModifierSubdivisionSelection,
                ]

addon_keymaps = []

def register():
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    km = kc.keymaps.new(name='3D View')
    kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="A", value="PRESS", ctrl=True, shift=False, alt=True, head=True)
    kmi.properties.name = Alx_MT_AlexandriaToolPie.bl_idname

    addon_keymaps.append((km,kmi))

    #bpy.types.Object.UIActionIndex = bpy.props.IntProperty(update=AlxUpdateAddonActionList)
    print("AlxRegister Called")
    print("ALX_LIBRARY_LOADED")
    print(AlxClassQueue)

def unregister():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for AlxQCls in AlxClassQueue:
        bpy.utils.unregister_class(AlxQCls)

    #del bpy.types.Object.UIActionIndex
    print("AlxUnRegister Called")

if __name__ == "__main__":
    register()