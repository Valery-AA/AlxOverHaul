bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valery [.V Arhal]",
    "description" : "",
    "version" : (0, 4, 1),
    "warning" : "[Heavly Under Development] Minimum Supported BL Version 4.0",
    "category" : "3D View",
    "location" : "[Ctrl Alt A] PieMenu, [Alx 3D] Panel Tab",
    "blender" : (4, 0, 0)
}

if "bpy" in locals():
    import importlib
    if "AlxOverHaul" in locals():
        importlib.reload(AlxOverHaul)

import bpy
import AlxOverHaul
from bpy.types import Context, Event
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, CollectionProperty, EnumProperty, PointerProperty



class Alx_MT_AlexandriaToolPie(bpy.types.Menu):
    bl_label = "Alexandria Tool Pie"
    bl_idname = "alx_menu_alexandria_tool_pie"

    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        AlxLayout = self.layout

        AlxParentArmature = None
        AlxContextObject = None

        PieUI = AlxLayout.menu_pie()

        if (context.active_object is not None):

            if (context.active_object.type == "MESH"):
                if (context.active_object.find_armature() is not None):
                    AlxParentArmature = context.active_object.find_armature()
                AlxContextObject = context.active_object
            if (context.active_object.type == "ARMATURE") and (context.active_object is not None):
                AlxParentArmature = bpy.data.objects.get(context.active_object.name)

        LBoxMenuSpace = PieUI.box()

        # LBoxMenuSectionR = LBoxMenuSpace.box()
        # LBoxMenuSectionR.ui_units_x = 10.0
        # LBoxMenuSectionR.ui_units_y = 10.0
        # LBoxMenuSectionM = LBoxMenuSpace.box()
        # LBoxMenuSectionM.ui_units_x = 10.0
        # LBoxMenuSectionM.ui_units_y = 10.0
        # LBoxMenuSectionL = LBoxMenuSpace.box()
        # LBoxMenuSectionL.ui_units_x = 10.0
        # LBoxMenuSectionL.ui_units_y = 10.0


        RBoxMenuSpace = PieUI.box()
        RBoxMenuSpace.row().label(text="Poly Modifiers:")
        BasicDeformingMod = RBoxMenuSpace.row(align=True)
        OT_MBSelection = BasicDeformingMod.operator(Alx_OT_ModifierBevelSelection.bl_idname, text="Bevel")
        OT_MSSelection = BasicDeformingMod.operator(Alx_OT_ModifierSubdivisionSelection.bl_idname, text="SubDiv")
        OT_MWSelection = BasicDeformingMod.operator(Alx_OT_ModifierWeldSelection.bl_idname, text="Weld")

        BBoxMenuSpace = PieUI.box().row()
        BBoxMenuSectionR = BBoxMenuSpace.box()
        BBoxMenuSectionR.ui_units_x = 12.0
        BBoxMenuSectionR.ui_units_y = 10.0
        BBoxMenuSectionM = BBoxMenuSpace.box()
        BBoxMenuSectionM.ui_units_x = 15.0
        BBoxMenuSectionM.ui_units_y = 10.0
        BBoxMenuSectionL = BBoxMenuSpace.box()
        BBoxMenuSectionL.ui_units_x = 12.0
        BBoxMenuSectionL.ui_units_y = 10.0

        BBoxMenuSectionM.row().label(text="Mode:")

        AlxOPSMode = BBoxMenuSectionM.row()
        OPS_OBJMode = AlxOPSMode.operator(Alx_OT_ModeObjectSwitch.bl_idname, text="OBJECT", icon="OBJECT_DATAMODE")
        OPS_OBJMode.DefaultBehaviour = True
        OPS_OBJMode = AlxOPSMode.operator(Alx_OT_ModePoseSwitch.bl_idname, text="POSE", icon="ARMATURE_DATA")
        OPS_OBJMode.DefaultBehaviour = True
        OPS_OBJMode = AlxOPSMode.operator(Alx_OT_ModeWeightPaintSwitch.bl_idname, text="WEIGHT PAINT", icon="WPAINT_HLT")
        OPS_OBJMode.DefaultBehaviour = True

        BBoxMenuSectionM.row().label(text="Auto Mode:")

        ModeSwitchRow = BBoxMenuSectionM.row(align=True)
        if (context.mode != "OBJECT"):
            OT_MOSwitch = ModeSwitchRow.operator(Alx_OT_ModeObjectSwitch.bl_idname, text="OBJECT", emboss=True)
            OT_MOSwitch.DefaultBehaviour = False

        if (context.mode != "POSE") and (AlxParentArmature is not None):
            OT_MPSwitch = ModeSwitchRow.operator(Alx_OT_ModePoseSwitch.bl_idname, text="POSE", emboss=True)
            OT_MPSwitch.DefaultBehaviour = False
            OT_MPSwitch.PoseActiveArmature = AlxParentArmature.name

        if (context.mode != "PAINT_WEIGHT") and (AlxParentArmature is not None) and (AlxContextObject is not None):
            OT_MWPSwitch = ModeSwitchRow.operator(Alx_OT_ModeWeightPaintSwitch.bl_idname, text="WEIGHT PAINT", emboss=True)
            OT_MWPSwitch.DefaultBehaviour = False
            OT_MWPSwitch.WeightPaintActiveArmature = AlxParentArmature.name
            OT_MWPSwitch.WeightPaintActiveObject = AlxContextObject.name

        BBoxMenuSectionL.row().prop(context.scene.render, "engine", text="")
        BBoxMenuSectionL.row(align=True).prop(context.area.spaces.active.shading, "type", text="", expand=True)





        TBoxMenuSpace = PieUI.box().row()
        TBoxMenuSectionL = TBoxMenuSpace.box()
        TBoxMenuSectionL.ui_units_x = 10.0
        TBoxMenuSectionL.ui_units_y = 10.0
        TBoxMenuSectionM = TBoxMenuSpace.box()
        TBoxMenuSectionM.ui_units_x = 12.0
        TBoxMenuSectionM.ui_units_y = 10.0
        TBoxMenuSectionR = TBoxMenuSpace.box()
        TBoxMenuSectionR.ui_units_x = 10.0
        TBoxMenuSectionR.ui_units_y = 10.0
       
        # Menu Section Left
        if (bpy.context.mode == "EDIT_MESH") and (bpy.context.active_object.type == "MESH"):
            AlxEditMirror = TBoxMenuSectionL.row(align=True)
            AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_x", text="X", toggle=True)
            AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_y", text="Y", toggle=True)
            AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_z", text="Z", toggle=True)
            AlxEditMirror.prop(bpy.context.active_object.data, "use_mirror_topology", text="", icon="MESH_GRID", toggle=True)
            TBoxMenuSectionL.row().prop(context.tool_settings, "use_edge_path_live_unwrap", text="Auto Unwrap", icon="UV")

        if (context.mode == "POSE"):
            AlxPoseMirror = TBoxMenuSectionL.row(align=True)
            AlxPoseMirror.prop(context.active_object.pose, "use_mirror_x", text="X Mirror")
            AlxPoseMirror.prop(context.active_object.pose, "use_mirror_relative", text="Local Mirror")
            TBoxMenuSectionL.row().prop(context.active_object.pose, "use_auto_ik", text="Auto IK", icon="CON_KINEMATIC")

        if (context.mode == "PAINT_WEIGHT"):
            AlxWeightMirror = TBoxMenuSectionL.row(align=True)
            AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_x", text="X", toggle=True)
            AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_y", text="Y", toggle=True)
            AlxWeightMirror.prop(bpy.context.active_object, "use_mesh_mirror_z", text="Z", toggle=True)
            AlxWeightMirror.prop(bpy.context.active_object.data, "use_mirror_vertex_groups",text="", icon="GROUP_VERTEX")
            AlxWeightMirror.prop(bpy.context.active_object.data, "use_mirror_topology",text="", icon="MESH_GRID", expand=True)
            TBoxMenuSectionL.row(align=True).prop(context.tool_settings, "vertex_group_user", expand=True)
            TBoxMenuSectionL.row().prop(context.tool_settings, "use_auto_normalize", text="Auto Normalize", icon="MOD_VERTEX_WEIGHT")

        # Menu Section Middle
        if (AlxParentArmature is not None):
            TBoxMenuSectionM.row().prop(bpy.data.armatures[AlxParentArmature.data.name], "pose_position", expand=True)
        else:
            TBoxMenuSectionM.row().label(text="No Influencing Armature Found")

        if (context.active_object is not None):
            TBoxMenuSectionM.row(align=True).prop(context.active_object, "display_type", expand=True)



        AlxBevelVisibility = TBoxMenuSectionM.row(align=True)
        OT_MBSwitch = AlxBevelVisibility.operator(Alx_OT_ModifierBevelSwitch.bl_idname, text="Bevel ON", emboss=True)
        OT_MBSwitch.ModVisibility = True
        OT_MBSwitch = AlxBevelVisibility.operator(Alx_OT_ModifierBevelSwitch.bl_idname, text="Bevel OFF", emboss=True)
        OT_MBSwitch.ModVisibility = False
 
        AlxOverlayShading = TBoxMenuSectionM.row(align=True)
        AlxOverlayShading.prop(context.space_data.overlay, "show_overlays", text="", icon="OVERLAY")
        AlxOverlayShading.prop(context.area.spaces.active.shading, "show_xray", text="Mesh", icon="XRAY")
        AlxOverlayShading.prop(context.space_data.overlay, "show_xray_bone", text="Bone", icon="XRAY")
        AlxOverlayShading.prop(context.space_data.overlay, "show_retopology", text="", icon="MESH_GRID")
        AlxOverlayShading.prop(context.space_data.overlay, "show_wireframes", text="", icon="MOD_WIREFRAME")

        AlxObjectIsolator = TBoxMenuSectionM.row(align=True) 
        OT_OBJIsolate = AlxObjectIsolator.operator(Alx_OT_SceneObjectIsolator.bl_idname, text="Isolate", emboss=True)
        OT_OBJIsolate.IsolatorState = True
        OT_OBJIsolate = AlxObjectIsolator.operator(Alx_OT_SceneObjectIsolator.bl_idname, text="Show All", emboss=True)
        OT_OBJIsolate.IsolatorState = False
        OT_COLIsolate = AlxObjectIsolator.operator(Alx_OT_SceneCollectionIsolator.bl_idname, text="", icon="OUTLINER_COLLECTION")

        if (context.active_object.type == "MESH"):
            AlxObjectSmoothing = TBoxMenuSectionM.row(align=True)
            OT_ShadeS = AlxObjectSmoothing.operator("object.shade_smooth", text="Smooth", emboss=True)
            OT_ShadeAS = AlxObjectSmoothing.operator("object.shade_smooth", text="ASmooth", emboss=True)
            OT_ShadeAS.use_auto_smooth = True
            AlxObjectSmoothing.operator("object.shade_flat", text="Flat", emboss=True)

        # Menu Section Right
        if (context.mode == "OBJECT") and (AlxContextObject is not None):
            OT_VGCE = TBoxMenuSectionR.row().operator(Alx_OT_VertexGroupCleanEmpty.bl_idname, text="Clean VxGroups", emboss=True)
            OT_VGCE.VertexDataObject = AlxContextObject.name


        if (context.mode == "POSE") and (AlxParentArmature is not None):
            OT_BMIBN = TBoxMenuSectionR.row().operator(Alx_OT_BoneMatchIKByName.bl_idname, text="Symmetric IK", icon="MOD_MIRROR")
            OT_BMIBN.ActivePoseArmatureObject = AlxParentArmature.name
        

        PieUI.box()
        PieUI.box()
        PieUI.box()
        PieUI.box()

class Alx_OT_SceneObjectIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.scene_object_isolator"

    IsolatorState: BoolProperty()

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        ActiveOBJName = bpy.data.objects[bpy.context.view_layer.objects.active.name].name
        for SceneOBJ in bpy.data.objects:
            if SceneOBJ.name != ActiveOBJName:
                bpy.data.objects[SceneOBJ.name].hide_viewport = self.IsolatorState
        return {"FINISHED"}

class Alx_OT_SceneCollectionIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.scene_collection_isolator"

    IsolatorState: BoolProperty(default=True)

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

    DefaultBehaviour : BoolProperty(default=True)  

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):
                        bpy.ops.object.mode_set(mode="OBJECT")

        return {"FINISHED"}

class Alx_OT_ModePoseSwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.mode_pose_switch"

    DefaultBehaviour : BoolProperty(default=True)
    PoseActiveArmature : StringProperty()

    @classmethod
    def poll (self, context):
        return (context.mode != "PAINT_WEIGHT")
    
    def execute(self, context):
        if (self.DefaultBehaviour is True):
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'VIEW_3D':
                        with context.temp_override(window=window, area=area):
                            for Object in bpy.context.selected_objects:
                                if Object.type == "ARMATURE":
                                    bpy.context.view_layer.objects.active = Object
                                    bpy.ops.object.mode_set(mode="POSE")
                                    break
            return {"FINISHED"}

        if (self.DefaultBehaviour == False) and (context.mode != "POSE") and (self.PoseActiveArmature != ""):
            if (bpy.data.objects[self.PoseActiveArmature].hide_get() == True):
                bpy.data.objects[self.PoseActiveArmature].hide_set(False)

            if (bpy.data.objects[self.PoseActiveArmature] is not None) and (bpy.data.objects[self.PoseActiveArmature].hide_get() == False):
                bpy.context.view_layer.objects.active = bpy.data.objects[self.PoseActiveArmature]


            if (context.active_object.type == "ARMATURE"):
                bpy.ops.object.mode_set(mode="POSE")
        return {"FINISHED"}

class Alx_OT_ModeWeightPaintSwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.mode_weight_paint_switch"

    DefaultBehaviour : BoolProperty(default=True)
    WeightPaintActiveArmature : StringProperty()
    WeightPaintActiveObject : StringProperty(options={"HIDDEN"})

    @classmethod
    def poll (self, context):
        return (context.mode != "POSE")
    
    def execute(self, context):
        if (self.DefaultBehaviour is True):
            for window in context.window_manager.windows:
                screen = window.screen
                for area in screen.areas:
                    if area.type == 'VIEW_3D':
                        with context.temp_override(window=window, area=area):

                            for Object in bpy.context.selected_objects:
                                if Object.type == "MESH":
                                    bpy.context.view_layer.objects.active = Object
                                    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
                                    break
            return {"FINISHED"}

        if (self.DefaultBehaviour is False) and (context.mode != "PAINT_WEIGHT") and (self.WeightPaintActiveArmature != ""):
            if (bpy.data.objects[self.WeightPaintActiveArmature].hide_get() == True):
                bpy.data.objects[self.WeightPaintActiveArmature].hide_set(False)

            bpy.data.objects[self.WeightPaintActiveArmature].hide_viewport = False

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
    bl_options = {'REGISTER', 'UNDO'}

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

                        for SelObj in bpy.context.selected_objects:

                            HasModifier = False

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "BEVEL"):
                                        HasModifier = True

                                        ObjMOD.segments = self.Segments
                                        ObjMOD.width = self.Width
                
                                        match self.UseWeight:

                                            case True:
                                                ObjMOD.limit_method = "WEIGHT"

                                            case False:
                                                ObjMOD.limit_method = "ANGLE"
                                                ObjMOD.angle_limit = 30 * (3.14/180)

                                        ObjMOD.miter_outer = "MITER_ARC"
                                        ObjMOD.harden_normals = self.HardenNormals

                                if (HasModifier == False):        
                                
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

        return {"FINISHED"}
    

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

class Alx_OT_ModifierSubdivisionSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_subdivision_selection"
    bl_options = {'REGISTER', 'UNDO'}

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

                        for SelObj in bpy.context.selected_objects:

                            HasModifier = False

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "SUBSURF"):
                                        HasModifier = True

                                        match self.UseSimple:
                                            case True:
                                                ObjMOD.subdivision_type = "SIMPLE"

                                            case False:
                                                ObjMOD.subdivision_type = "CATMULL_CLARK"

                                        ObjMOD.levels = self.ViewportLevel
                                        ObjMOD.render_levels = self.RenderLevel
                                        ObjMOD.show_only_control_edges = not self.Complex

                                if (HasModifier == False):    

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
        return context.window_manager.invoke_props_popup(self, event)

class Alx_OT_ModifierWeldSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_weld_selection"
    bl_options = {'REGISTER', 'UNDO'}

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

                        for SelObj in bpy.context.selected_objects:

                            HasModifier = False

                            if (SelObj.type == "MESH"):
                                ObjMODs = SelObj.modifiers
                                
                                for ObjMOD in ObjMODs:
                                
                                    if (ObjMOD.type == "WELD"):
                                        HasModifier = True

                                        match self.UseMergeAll:
                                            case True:
                                                ObjMOD.mode = "ALL"

                                            case False:
                                                ObjMOD.mode = "CONNECTED"
                                                ObjMOD.loose_edges = self.UseMergeOnlyLooseEdges

                                        ObjMOD.merge_threshold = self.MergeDistance

                                if (HasModifier == False):    
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
        return context.window_manager.invoke_props_popup(self, event)

class Alx_OT_VertexGroupCleanEmpty(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.vertex_group_clean_empty"

    VertexDataObject : StringProperty(options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        if (self.VertexDataObject != "") and (bpy.data.objects.get(self.VertexDataObject) is not None):
            for VGroup in bpy.data.objects.get(self.VertexDataObject).vertex_groups:
                i = 0
                HasAtLeastOneVertex = False
                while i < len(bpy.data.objects.get(self.VertexDataObject).data.vertices):
                    if(i < 0): break
                    try:
                        VGroup.weight(i)
                    except:
                        pass

                    else:
                        HasAtLeastOneVertex = True    
                    i += 1
                if(HasAtLeastOneVertex == False):
                    bpy.data.objects.get(self.VertexDataObject).vertex_groups.remove(VGroup)
        return{"FINISHED"}

def AlxGetBoneAlwaysLeft(Bone, Armature):
    LeftBone = ""
    if (len(Bone.name) != 0) and (len(Bone.name) > 2):
        if (Bone.name[-2] == "."):
            
            match Bone.name[-1]:
                case "R":
                    LeftBone = Bone.name[0:-1] + "L"
                case "L":
                    LeftBone = Bone.name[0:-1] + "L"
                case "r":
                    LeftBone = Bone.name[0:-1] + "l"
                case "l":
                    OppositeBoneName = Bone.name[0:-1] + "l"

    return bpy.data.objects.get(Armature).pose.bones.get(LeftBone)

def AlxGetBoneOpposite(Bone, Armature):
    OppositeBoneName = ""
    if (len(Bone.name) != 0) and (len(Bone.name) > 2):
        if (Bone.name[-2] == "."):
            
            match Bone.name[-1]:
                case "R":
                    OppositeBoneName = Bone.name[0:-1] + "L"
                case "L":
                    OppositeBoneName = Bone.name[0:-1] + "R"
                case "r":
                    OppositeBoneName = Bone.name[0:-1] + "l"
                case "l":
                    OppositeBoneName = Bone.name[0:-1] + "r"

    return bpy.data.objects.get(Armature).pose.bones.get(OppositeBoneName)

def AlxGetBoneNameOpposite(BoneName):
    OppositeBoneName = ""
    if (len(BoneName) != 0) and (len(BoneName) > 2):
        if (BoneName[-2] == "."):
            
            match BoneName[-1]:
                case "R":
                    OppositeBoneName = BoneName[0:-1] + "L"
                case "L":
                    OppositeBoneName = BoneName[0:-1] + "R"
                case "r":
                    OppositeBoneName = BoneName[0:-1] + "l"
                case "l":
                    OppositeBoneName = BoneName[0:-1] + "r"
    return OppositeBoneName

def AlxGetIKConstraint(Bone):
    for Constraint in Bone.constraints:
        if (Constraint.type == "IK"):
            return Constraint

def AlxCloneIKBoneLimitOnChain(IKHead, Armature):
    i = 0
    if (AlxGetIKConstraint(IKHead) is not None):
        ChainLength = AlxGetIKConstraint(IKHead).chain_count
        ParentOnChain = None

        IKHeadOpposite = AlxGetBoneOpposite(IKHead, Armature)

        IKHeadOpposite.use_ik_limit_x = IKHead.use_ik_limit_x
        IKHeadOpposite.ik_min_x = IKHead.ik_min_x
        IKHeadOpposite.ik_max_x = IKHead.ik_max_x

        IKHeadOpposite.use_ik_limit_y = IKHead.use_ik_limit_y
        IKHeadOpposite.ik_min_y = IKHead.ik_min_y
        IKHeadOpposite.ik_max_y = IKHead.ik_max_y

        IKHeadOpposite.use_ik_limit_z = IKHead.use_ik_limit_z
        IKHeadOpposite.ik_min_z = IKHead.ik_max_z * -1
        IKHeadOpposite.ik_max_z = IKHead.ik_min_z * -1

        ParentOnChain = IKHead
        ParentOnChainOpposite = AlxGetBoneOpposite(IKHead, Armature)
        if (ParentOnChain is not None) and (ParentOnChainOpposite is not None):
            while i < ChainLength:
                if (i < 0): break

                ParentOnChainOpposite.use_ik_limit_x = ParentOnChain.use_ik_limit_x
                ParentOnChainOpposite.ik_min_x = ParentOnChain.ik_min_x
                ParentOnChainOpposite.ik_max_x = ParentOnChain.ik_max_x


                ParentOnChainOpposite.use_ik_limit_y = ParentOnChain.use_ik_limit_y
                ParentOnChainOpposite.ik_min_y = ParentOnChain.ik_min_y
                ParentOnChainOpposite.ik_max_y = ParentOnChain.ik_max_y

                ParentOnChainOpposite.use_ik_limit_z = ParentOnChain.use_ik_limit_z
                ParentOnChainOpposite.ik_min_z = ParentOnChain.ik_max_z * -1
                ParentOnChainOpposite.ik_max_z = ParentOnChain.ik_min_z * -1

                ParentOnChain = ParentOnChain.parent
                ParentOnChainOpposite = ParentOnChainOpposite.parent
                i += 1

def AlxCloneIKSettings(CheckBone, OppositeBone):
    if (CheckBone is not None) and (OppositeBone is not None):
        CheckBoneIK = AlxGetIKConstraint(CheckBone)
        OppositeBoneIK = AlxGetIKConstraint(OppositeBone)



        if (CheckBoneIK is not None) and (OppositeBoneIK is not None):
            if (CheckBoneIK.target is not None):
                OppositeBoneIK.target = CheckBoneIK.target
            if (CheckBoneIK.subtarget is not None):
                if (CheckBoneIK.target.type == "ARMATURE"):
                    OppositeBoneIK.subtarget = AlxGetBoneNameOpposite(CheckBoneIK.subtarget)

            OppositeBoneIK.chain_count = CheckBoneIK.chain_count
            OppositeBoneIK.use_tail = CheckBoneIK.use_tail

        if (CheckBoneIK is None) and (OppositeBoneIK is not None):
            NewIK = CheckBone.constraints.new("IK")

            if (OppositeBoneIK.target is not None):
                NewIK.target = OppositeBoneIK.target

                if (OppositeBoneIK.subtarget is not None):
                    if (OppositeBoneIK.target.type == "ARMATURE"):
                        NewIK.subtarget = AlxGetBoneNameOpposite(OppositeBoneIK.subtarget)

            NewIK.chain_count = OppositeBoneIK.chain_count
            NewIK.use_tail = OppositeBoneIK.use_tail

        if (CheckBoneIK is not None) and (OppositeBoneIK is None):
            NewIK = OppositeBone.constraints.new("IK")

            if (CheckBoneIK.target is not None):
                NewIK.target = CheckBoneIK.target

                if (CheckBoneIK.subtarget is not None):
                    if (CheckBoneIK.target.type == "ARMATURE"):
                        NewIK.subtarget = AlxGetBoneNameOpposite(CheckBoneIK.subtarget)

            NewIK.chain_count = CheckBoneIK.chain_count
            NewIK.use_tail = CheckBoneIK.use_tail

class Alx_OT_BoneMatchIKByName(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.bone_match_ik_by_name"
    bl_options = {'REGISTER', 'UNDO'}

    ActivePoseArmatureObject : StringProperty(options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return (context.mode == "POSE")

    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        if (bpy.data.objects.get(self.ActivePoseArmatureObject).type == "ARMATURE"):
                            PoseBoneData = bpy.data.objects.get(self.ActivePoseArmatureObject).pose.bones

                            CorrectPairBones = []

                            for PoseBone in PoseBoneData:
                                if (PoseBone.name[-2] == ".") and (PoseBone.name[0:-2] not in CorrectPairBones):
                                    CorrectPairBones.append(PoseBone.name[0:-2])
                                    PoseBoneLeft = AlxGetBoneAlwaysLeft(PoseBone, self.ActivePoseArmatureObject)
                                    OppositeBoneLeft = AlxGetBoneOpposite(AlxGetBoneAlwaysLeft(PoseBone, self.ActivePoseArmatureObject), self.ActivePoseArmatureObject)
                                    
                                    AlxCloneIKSettings(PoseBoneLeft, OppositeBoneLeft)
                                    AlxCloneIKBoneLimitOnChain(PoseBoneLeft, self.ActivePoseArmatureObject)


        return {"FINISHED"}

# ### Alx Material Property Groups
# class Alx_Material(bpy.types.PropertyGroup):
#     def GetMaterialName(self):
#         return self.material.name
    
#     name : StringProperty()
#     material_name : StringProperty(get=GetMaterialName)
#     material : PointerProperty(type=bpy.types.Material)

# class Alx_MaterialCollection(bpy.types.PropertyGroup):
#     name : StringProperty()
#     pass

# def AlxMaterialAssignFromScene(self):
#     for Material in bpy.data.materials:
#         if (Material is not None) and (bpy.context.scene.alx_materials.find(Material.name) == -1):
#             AlxMaterial = bpy.context.scene.alx_materials.add()
#             AlxMaterial.name = Material.name
#             AlxMaterial.material = Material

# ### Alx Material Operators
# class Alx_OT_MaterialRegisterChanges(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_register_changes"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context):
#         AlxMaterialAssignFromScene(self)
        
#         for AlxMaterial in bpy.context.scene.alx_materials:
#             if (AlxMaterial.name not in bpy.data.materials):
#                 NewMaterial = bpy.data.materials.new(AlxMaterial.name)
#                 NewMaterial = AlxMaterial
#         return {"FINISHED"}

# class Alx_OT_MaterialAppendToScene(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_append_to_scene"

#     @classmethod
#     def poll(self, context):
#         return True
    
#     def execute(self, context: Context):
#         bpy.data.materials.new("Material")

#         return {"FINISHED"}

# class Alx_OT_MaterialRemoveFromScene(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_remove_from_scene"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context):
#         if (len(bpy.context.scene.alx_materials) != 0) and (bpy.context.scene.alx_active_material_index < len(bpy.context.scene.alx_materials)):
#             MaterialID = bpy.data.materials.get(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name)

#             MaterialUserMap = bpy.data.user_map(key_types={"MATERIAL"}, value_types={"MESH"})
#             MaterialUsers = MaterialUserMap.get(bpy.data.materials[MaterialID.name], None)

#             for User in MaterialUsers:
#                 MaterialUser = User
#                 if (MaterialUser.name not in ["Scene", "Airbrush"]):
#                     MeshUserMap = bpy.data.user_map(key_types={"MESH"}, value_types={"OBJECT"})
#                     MeshUsers = MeshUserMap.get(bpy.data.meshes[MaterialUser.name], None)

#                     for MeshUser in MeshUsers:
#                         print(MeshUsers)
#                         MeshUser.active_material_index = MeshUser.material_slots.find(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name)
#                         print(MeshUser)
#                         print(MeshUser.active_material_index)
#                         bpy.ops.object.material_slot_select()
#                         bpy.ops.object.material_slot_remove()

#             if ((bpy.context.scene.alx_active_material_index -1) != -1):
#                 bpy.context.scene.alx_active_material_index = bpy.context.scene.alx_active_material_index - 1

#         return {"FINISHED"}
    
# class Alx_OT_MaterialAssignToSelection(bpy.types.Operator):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_assign_to_selection"

#     @classmethod
#     def poll(self, context):
#         return True

#     def execute(self, context):
#         for Object in bpy.context.selected_objects:
#             if (Object.type == "MESH"):
#                 if (len(bpy.context.scene.alx_materials) != 0) and (bpy.context.scene.alx_active_material_index < len(bpy.context.scene.alx_materials)):
#                     if bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].name not in Object.data.materials:
#                         Object.data.materials.append(bpy.context.scene.alx_materials[bpy.context.scene.alx_active_material_index].material)

#         return {"FINISHED"}

# ### Alx Material UI
# class Alx_UL_MaterialSlotList(bpy.types.UIList):
#     bl_idname = "alx.material_slot_list"

#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             layout.prop(item, "name", text="", emboss=False, icon_value=icon)

# class Alx_PT_MaterialSlotSelector(bpy.types.Panel):
#     """"""

#     bl_label = ""
#     bl_idname = "alx.material_slot_selector"

#     bl_category = "Alx 3D"

#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     @classmethod
#     def poll(cls, context):
#             return True

#     def draw(self, context):
#         AlxLayout = self.layout

#         MaterialOutlinerRow = AlxLayout.row(align=True)
        
        
#         SM_ToolsColumn = MaterialOutlinerRow.column()
#         SM_ToolsColumn.operator(Alx_OT_MaterialAppendToScene.bl_idname, text="", icon="ADD") 
#         SM_ToolsColumn.operator(Alx_OT_MaterialRemoveFromScene.bl_idname, text="", icon="FAKE_USER_OFF")


#         SceneMaterialColumn = MaterialOutlinerRow.column()
#         SceneMaterialColumn.template_list(listtype_name=Alx_UL_MaterialSlotList.bl_idname, list_id="", dataptr=bpy.context.scene, propname="alx_materials", active_dataptr=bpy.context.scene, active_propname="alx_active_material_index")
        
        
#         SM_ToolsColumn.operator(Alx_OT_MaterialRegisterChanges.bl_idname, text="", icon="FILE_REFRESH")
        
        
#         SM_ToolsColumn.label(icon="RIGHTARROW")

#         SceneMaterialColumn.operator(Alx_OT_MaterialAssignToSelection.bl_idname, text="Assign Material To Selection")

#         MaterialCollectionColumn = MaterialOutlinerRow.column()

#         MaterialCollectionColumn.template_list(listtype_name=Alx_UL_MaterialSlotList.bl_idname, list_id="", dataptr=bpy.context.scene, propname="alx_material_collection_library", active_dataptr=bpy.context.scene, active_propname="alx_active_material_index")
        
#         MC_ToolsColumn = MaterialOutlinerRow.column()

#         MaterialCollectionColumn.label(text="Operator Here")
        







# class Alx_UL_ActionSelector(bpy.types.UIList):

#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             layout.prop(item, "name", text="", emboss=False, icon_value=icon)
#         elif self.layout_type in {'GRID'}:
#             pass

# class Alx_Panel_SwapArmatureAction(bpy.types.Panel):
#     """"""

#     bl_label = "Alx Action Selector"
#     bl_idname = "Alx.Action_OT_Selector"

#     bl_category = "Alx 3D"

#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"

#     @classmethod
#     def poll(cls, context):
#         if (context.mode == "OBJECT") or (context.mode == "PAINT_WEIGHT") or (context.mode =="POSE"):
#             return True

#     def draw(self, context):
#         Alxlayout = self.layout
#         obj = context.object
#         Alxlayout.template_list("Alx_UL_ActionSelector", "", bpy.data, "actions", obj, "UIActionIndex")

# @bpy.app.handlers.persistent
# def AlxUpdateActionUI(context):
#         if (bpy.context.view_layer.objects.active is not None) and (bpy.context.view_layer.objects.active.find_armature() is not None):
#             AlxActionParentArmature = bpy.data.armatures[bpy.context.view_layer.objects.active.find_armature().data.name]
        
#             if (AlxActionParentArmature is not None) and (AlxActionParentArmature.animation_data is not None):
#                 ActiveActionIndex = bpy.data.actions.find(AlxActionParentArmature.animation_data.action.name)

#                 if ActiveActionIndex != AlxActionParentArmature.UIActionIndex:
#                     AlxActionParentArmature.UIActionIndex = ActiveActionIndex

# def AlxUpdateAddonActionList(self, context):
#     if(bpy.context.view_layer.objects.active is not None):
#         if (bpy.context.view_layer.objects.active.find_armature() is not None):
#             AlxActionParentArmature = bpy.data.armatures[bpy.context.view_layer.objects.active.find_armature().data.name]

#             if (AlxActionParentArmature is not None):
#                 if (AlxActionParentArmature is not None) and (AlxActionParentArmature.animation_data is not None):
#                     AlxActionParentArmature.animation_data.action = bpy.data.actions[AlxActionParentArmature.UIActionIndex]
#                     bpy.context.scene.frame_current = 0

# bpy.app.handlers.depsgraph_update_post.append(AlxUpdateActionUI)





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
                Alx_OT_ModifierWeldSelection,

                Alx_OT_VertexGroupCleanEmpty,
                Alx_OT_BoneMatchIKByName



                # Alx_Material,
                # Alx_MaterialCollection,

                # Alx_OT_MaterialRegisterChanges,
                # Alx_OT_MaterialAssignToSelection,
                # Alx_OT_MaterialAppendToScene,
                # Alx_OT_MaterialRemoveFromScene,

                
                # Alx_UL_MaterialSlotList,
                # Alx_PT_MaterialSlotSelector
                ]

addon_keymaps = []

def register():


    print("AlxOverHaul Registering...")
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:

        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type="A", ctrl=True, alt=True, value="CLICK")
        kmi.properties.name = Alx_MT_AlexandriaToolPie.bl_idname
        addon_keymaps.append((km, kmi))

    # bpy.types.Scene.alx_materials = CollectionProperty(type=Alx_Material)
    # bpy.types.Scene.alx_active_material_index = IntProperty()
    # bpy.types.Scene.alx_material_collection_library = CollectionProperty(type=Alx_MaterialCollection)

    #bpy.app.handlers.depsgraph_update_post.append(AlxMaterialRegisterChanges)
    #bpy.msgbus.subscribe_rna(key=(bpy.types.Object, "material_slots"), owner="owner", args=(), notify=AlxMaterialRegisterChanges)



    print("AlxOverHaul Registered:")
    print(AlxClassQueue)

def unregister():
    print("AlxOverHaul Un-Registering...")
    for AlxQCls in AlxClassQueue:
        bpy.utils.unregister_class(AlxQCls)

    # del bpy.types.Scene.alx_materials
    # del bpy.types.Scene.alx_active_material_index

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()