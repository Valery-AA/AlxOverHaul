import bpy

class Alx_OT_Mode_UnlockedModes(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_mode_unlocked_modes"
    bl_options = {"INTERNAL"}

    DefaultBehaviour : bpy.props.BoolProperty(name="", default=True, options={"HIDDEN"})
    TargetMode : bpy.props.StringProperty(name="", default="OBJECT", options={"HIDDEN"})
    TargetSubMode : bpy.props.StringProperty(name="", default="VERT", options={"HIDDEN"})
    
    TargetObject : bpy.props.StringProperty(name="", options={"HIDDEN"})
    TargetArmature : bpy.props.StringProperty(name="", options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if (area.type == 'VIEW_3D'):
                    with context.temp_override(window=window, area=area):

                        if (self.DefaultBehaviour == True):
                            match self.TargetMode:
                                case "OBJECT":
                                    if (context.mode != "OBJECT"):
                                        bpy.ops.object.mode_set(mode="OBJECT")
                                    return {"FINISHED"}

                                case "EDIT":
                                    if (context.mode not in ["EDIT_CURVE", "EDIT_CURVES", "EDIT_SURFACE", "EDIT_TEXT", "EDIT_METABALL", "EDIT_LATTICE", "EDIT_GREASE_PENCIL", "EDIT_POINT_CLOUD"]):
                                        for Object in bpy.context.selected_objects:
                                            if (Object.type == "MESH"):
                                                if (self.TargetSubMode in ["VERT", "EDGE", "FACE"]):
                                                    bpy.context.view_layer.objects.active = Object
                                                    bpy.ops.object.mode_set_with_submode(mode="EDIT", mesh_select_mode=set([self.TargetSubMode]))
                                            if (Object.type in ["ARMATURE"]):
                                                bpy.context.view_layer.objects.active = Object
                                                bpy.ops.object.mode_set(mode="EDIT")

                                    return {"FINISHED"}
                                case "POSE":
                                    if (context.mode != "POSE"):
                                        for Object in bpy.context.selected_objects:
                                            if (Object.type == "ARMATURE"):
                                                bpy.context.view_layer.objects.active = Object
                                                bpy.ops.object.mode_set(mode="POSE")
                                    return {"FINISHED"}
                                
                                case "PAINT_WEIGHT":
                                    if (context.mode != "PAINT_WEIGHT"):
                                        for Object in bpy.context.selected_objects:
                                            if Object.type == "MESH":
                                                bpy.context.view_layer.objects.active = Object
                                                bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
                                    return {"FINISHED"}

                        if (self.DefaultBehaviour == False):
                            match self.TargetMode:
                                case "OBJECT":
                                    if (context.mode != "OBJECT"):
                                        bpy.ops.object.mode_set(mode="OBJECT")
                                    return {"FINISHED"}

                                case "POSE":
                                    if (context.mode != "POSE"):
                                        if (self.TargetArmature != ""):
                                            if (bpy.data.objects[self.TargetArmature] is not None):
                                                
                                                if (context.mode == "PAINT_WEIGHT"):
                                                    bpy.ops.object.mode_set(mode="OBJECT")

                                                bpy.data.objects.get(self.TargetArmature).hide_set(False)
                                                bpy.data.objects.get(self.TargetArmature).hide_viewport = False

                                                if (bpy.data.objects[self.TargetArmature] is not None):
                                                    bpy.context.view_layer.objects.active = bpy.data.objects.get(self.TargetArmature)
                                                    if (context.active_object.type == "ARMATURE"):
                                                        bpy.ops.object.mode_set(mode="POSE")
                                    return {"FINISHED"}
                                
                                case "PAINT_WEIGHT":
                                    if (context.mode != "PAINT_WEIGHT"):
                                        if (self.TargetObject != "") and (self.TargetArmature != ""):
                                            if (bpy.data.objects[self.TargetObject] is not None) and (bpy.data.objects[self.TargetArmature] is not None):

                                                if (context.mode == "POSE"):
                                                    bpy.ops.object.mode_set(mode="OBJECT")
                                                
                                                bpy.data.objects.get(self.TargetArmature).hide_set(False)
                                                bpy.data.objects.get(self.TargetArmature).hide_viewport = False

                                                bpy.data.objects.get(self.TargetArmature).select_set(True)

                                                bpy.context.view_layer.objects.active = bpy.data.objects.get(self.TargetObject)

                                                if (context.active_object.type == "MESH"):
                                                    bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
                                    return {"FINISHED"}

        return {"FINISHED"}

class Alx_OT_Scene_VisibilityIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.scene_visibility_isolator"
    bl_options = {"INTERNAL"}

    TargetVisibility : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})
    UseObject : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})
    UseCollection : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})

    @classmethod
    def poll(self, context):
        return True
    
    def execute(self, context):
        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        TargetType = []
                        for Target in context.scene.alx_addon_properties.SceneIsolatorVisibilityTarget:
                            TargetType.append(Target)
                            
                        
                        if (context.active_object is not None):
                            if (self.UseObject == True):
                                ObjectSelection = []
                                for Object in context.selected_objects:
                                    if (Object is not None):
                                        ObjectSelection.append(Object.name)

                                for Object in bpy.data.objects:
                                    if (Object is not None ) and (Object.name not in ObjectSelection):
                                        if ("VIEWPORT" in TargetType):
                                            Object.hide_viewport = not self.TargetVisibility
                                        if ("RENDER" in TargetType):
                                            Object.hide_render = not self.TargetVisibility

                            if (self.UseCollection == True):
                                ActiveCollection = bpy.data.objects[bpy.context.view_layer.objects.active.name].users_collection[0]
                                for collection in bpy.data.collections:
                                    if (collection is not ActiveCollection) and (collection is not ActiveCollection) and (ActiveCollection not in collection.children_recursive):
                                        if ("VIEWPORT" in TargetType):
                                            collection.hide_viewport = not self.TargetVisibility
                                        if ("RENDER" in TargetType):
                                            collection.hide_render = not self.TargetVisibility
        return {"FINISHED"}
    
class Alx_OT_ModifierHideOnSelected(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.modifier_selection_visibility"

    ShowModiferEdit : bpy.props.BoolProperty(name="Show Edit:", default=True)
    ShowModiferViewport : bpy.props.BoolProperty(name="Show Viewport:", default=True)
    ShowModiferRender : bpy.props.BoolProperty(name="Show Render:", default=True)

    BevelMod : bpy.props.BoolProperty(name="Bevel", default=False)
    SubdivisionMod : bpy.props.BoolProperty(name="Subdivision", default=False)
    SolidifyMod : bpy.props.BoolProperty(name="Solidify", default=False)

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        for window in context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    with context.temp_override(window=window, area=area):

                        ModifiersList = []

                        if (self.BevelMod == True):
                            ModifiersList.append("BEVEL")
                        if (self.SubdivisionMod == True):
                            ModifiersList.append("SUBSURF")
                        if (self.SolidifyMod == True):
                            ModifiersList.append("SOLIDIFY")

                        for Object in bpy.context.selected_objects:
                            if (Object is not None) and (len(Object.modifiers) != 0) and (Object.type in ["MESH", "ARMATURE", "CURVE"]):
                                ObjectModfiers = getattr(Object, "modifiers", [])

                                for ObjectModifier in ObjectModfiers:
                                    if (ObjectModifier is not None) and (ObjectModifier.type in ModifiersList):
                                        ObjectModifier.show_in_editmode = self.ShowModiferEdit
                                        ObjectModifier.show_viewport = self.ShowModiferViewport
                                        ObjectModifier.show_render = self.ShowModiferRender                
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)