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
        AlxParentArmature = None
        AlxContextObject = None


        PieUI = AlxLayout.menu_pie()

        if (context.active_object is not None):
            
            

            if (context.active_object.type == "MESH") and (context.active_object.find_armature() is not None):
                AlxParentArmature = context.active_object.find_armature()
                AlxContextObject = context.active_object.name
            if (context.active_object.type == "ARMATURE") and (context.active_object is not None):
                AlxParentArmature = bpy.data.objects[context.active_object.name]

        PieUI.box().label(text = "PLACEHOLDER 1")

        RBoxMenuSpace = PieUI.box()
        RBoxMenuSpace.row().label(text="Poly Modifiers:")
        BasicDeformingMod = RBoxMenuSpace.row(align=True)
        OT_MBSelection = BasicDeformingMod.operator(Alx_OT_ModifierBevelSelection.bl_idname, text="Bevel")
        OT_MSSelection = BasicDeformingMod.operator(Alx_OT_ModifierSubdivisionSelection.bl_idname, text="SubDiv")
        OT_MWSelection = BasicDeformingMod.operator(Alx_OT_ModifierWeldSelection.bl_idname, text="Weld")

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

        CompoundIsolatorRow = TBoxMenuSpace.row(align=True) 
        OT_OBJIsolate = CompoundIsolatorRow.operator(Alx_OT_SceneObjectIsolator.bl_idname, text="Isolate", emboss=True)
        OT_OBJIsolate.IsolatorState = True
        OT_OBJIsolate = CompoundIsolatorRow.operator(Alx_OT_SceneObjectIsolator.bl_idname, text="Show All", emboss=True)
        OT_OBJIsolate.IsolatorState = False

        OT_COLIsolate = CompoundIsolatorRow.operator(Alx_OT_SceneCollectionIsolator.bl_idname, text="", icon="OUTLINER_COLLECTION")

        if (context.active_object.type == "MESH"):
            SmoothingRow = TBoxMenuSpace.row(align=True)
            OT_ShadeS = SmoothingRow.operator("object.shade_smooth", text="Smooth", emboss=True)
            OT_ShadeAS = SmoothingRow.operator("object.shade_smooth", text="ASmooth", emboss=True)
            OT_ShadeAS.use_auto_smooth = True
            SmoothingRow.operator("object.shade_flat", text="Flat", emboss=True)

        PieUI.box().label(text = "PLACEHOLDER 2")
        PieUI.box().label(text = "PLACEHOLDER 3")
        PieUI.box().label(text = "PLACEHOLDER 4")
        PieUI.box().label(text = "PLACEHOLDER 5")

class Alx_OT_SceneObjectIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.scene_object_isolator"

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

class Alx_OT_SceneCollectionIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.scene_collection_isolator"

    IsolatorState: BoolProperty(default=False)

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        ActiveCollection = bpy.data.objects[bpy.context.view_layer.objects.active.name].users_collection[0]

        for collection in bpy.data.collections:
            if (collection is not ActiveCollection) and (collection is not ActiveCollection) and (ActiveCollection not in collection.children_recursive):
                collection.hide_viewport = self.IsolatorState

        self.IsolatorState = not self.IsolatorState
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

    Segments : IntProperty(name="Segments", default=1, min=1)
    Width : FloatProperty(name="Width", default=0.01000, unit="LENGTH", min=0.0)
    UseWeight : BoolProperty(name="Use Weight", default=True)
    HardenNormals : BoolProperty(name="Harden Normals", default=True)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        BevelMod = None

                        for SelObj in bpy.context.selected_objects:

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "BEVEL"):
                                        
                                        BevelMod = ObjMOD
                                        BevelMod.segments = self.Segments
                                        BevelMod.width = self.Width
                
                                        match self.UseWeight:

                                            case True:
                                                BevelMod.limit_method = "WEIGHT"

                                            case False:
                                                BevelMod.limit_method = "ANGLE"
                                                BevelMod.angle_limit = 30 * (3.14/180)

                                        BevelMod.miter_outer = "MITER_ARC"
                                        BevelMod.harden_normals = self.HardenNormals

                                        return {"FINISHED"}
                                
                                BevelMod = SelObj.modifiers.new("Bevel", "BEVEL")
                                BevelMod.segments = self.Segments
                                BevelMod.width = self.Width

                                match self.UseWeight:

                                    case True:
                                        BevelMod.limit_method = "WEIGHT"

                                    case False:
                                        BevelMod.limit_method = "ANGLE"
                                        BevelMod.angle_limit = 30 * (3.14/180)

                                BevelMod.miter_outer = "MITER_ARC"
                                BevelMod.harden_normals = self.HardenNormals
                        break

        return {"FINISHED"}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class Alx_OT_ModifierSubdivisionSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_subdivision_selection"

    UseSimple : BoolProperty(name="Simple", default=False)
    ViewportLevel : IntProperty(name="Viewport", default=1)
    RenderLevel : IntProperty(name="Render", default=1)
    Complex : BoolProperty(name="Complex", default=True)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        SubDivMod = None

                        for SelObj in bpy.context.selected_objects:

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "SUBSURF"):
                                        SubDivMod = ObjMOD

                                        match self.UseSimple:
                                            case True:
                                                SubDivMod.subdivision_type = "SIMPLE"

                                            case False:
                                                SubDivMod.subdivision_type = "CATMULL_CLARK"

                                        SubDivMod.levels = self.ViewportLevel
                                        SubDivMod.render_levels = self.RenderLevel
                                        SubDivMod.show_only_control_edges = not self.Complex

                                        return {"FINISHED"}

                        SubDivMod = SelObj.modifiers.new("Subdivision Surface", "SUBSURF")
          
                        match self.UseSimple:
                            case True:
                                SubDivMod.subdivision_type = "SIMPLE"
                            case False:
                                SubDivMod.subdivision_type = "CATMULL_CLARK"

                        SubDivMod.levels = self.ViewportLevel
                        SubDivMod.render_levels = self.RenderLevel
                        SubDivMod.show_only_control_edges = not self.Complex

        return {"FINISHED"}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class Alx_OT_ModifierWeldSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_weld_selection"

    UseMergeAll : BoolProperty(name="Merge All", default=True)
    UseMergeOnlyLooseEdges : BoolProperty(name="Only Loose Edges", default=True)

    MergeDistance : FloatProperty(name="Distance", default=0.00100, unit="LENGTH", min=0.0)

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):

        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        WeldMod = None

                        for SelObj in bpy.context.selected_objects:

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "WELD"):
                                        WeldMod = ObjMOD

                                        match self.UseMergeAll:
                                            case True:
                                                WeldMod.mode = "ALL"

                                            case False:
                                                WeldMod.mode = "CONNECTED"
                                                WeldMod.loose_edges = self.UseMergeOnlyLooseEdges

                                        WeldMod.merge_threshold = self.MergeDistance

                                        return {"FINISHED"}

                                WeldMod = SelObj.modifiers.new("Weld", "WELD")
          
                                match self.UseMergeAll:
                                    case True:
                                        WeldMod.mode = "ALL"

                                    case False:
                                        WeldMod.mode = "CONNECTED"
                                        WeldMod.loose_edges = self.UseMergeOnlyLooseEdges

                                WeldMod.merge_threshold = self.MergeDistance
            
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

                Alx_OT_SceneObjectIsolator,
                Alx_OT_SceneCollectionIsolator,
                Alx_OT_ModeObjectSwitch,
                Alx_OT_ModePoseSwitch,
                Alx_OT_ModeWeightPaintSwitch,

                Alx_OT_ModifierBevelSwitch,
                
                Alx_OT_ModifierBevelSelection,
                Alx_OT_ModifierSubdivisionSelection,
                Alx_OT_ModifierWeldSelection
                ]

addon_keymaps = []

def register():
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    km = kc.keymaps.new(name='3D View')
    kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="A", value="CLICK", ctrl=True, shift=False, alt=True)
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