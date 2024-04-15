import bpy

class Alx_Tool_SceneIsolator_Properties(bpy.types.PropertyGroup):
    """"""

    scene_isolator_visibility_target : bpy.props.EnumProperty(default={"VIEWPORT"},options={'ENUM_FLAG'}, 
        items=[
            ("VIEWPORT", "Viewport", "", "RESTRICT_VIEW_OFF", 1), 
            ("RENDER", "Render", "", "RESTRICT_RENDER_OFF", 1<<1)
        ]) #type:ignore
    
    scene_isolator_type_target : bpy.props.EnumProperty(default={"OBJECT"}, options={'ENUM_FLAG'},
        items=[
                ("OBJECT", "Object", "", "OBJECT_DATAMODE", 1), 
                ("COLLECTION", "Collection", "", "OUTLINER_COLLECTION", 1<<1)
            ]) #type:ignore



class Alx_OT_Scene_VisibilityIsolator(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_scene_visibility_isolator"
    bl_options = {"INTERNAL"}

    TargetVisibility : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"}) #type:ignore
    PanicReset : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"}) #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context.area.type == "VIEW_3D"

    def execute(self, context: bpy.types.Context):
        SelectedVisibility = context.scene.alx_tool_scene_isolator_properties.scene_isolator_visibility_target
        SelectedType = context.scene.alx_tool_scene_isolator_properties.scene_isolator_type_target

        if (len(SelectedVisibility) != 0) and (len(SelectedType) != 0):
            VisibilityType = []
            TargetType = []
            VisibilityType = [visibility for visibility in SelectedVisibility]
            TargetType = [type for type in SelectedType]

            try:
                VisibilityType[0]
                TargetType[0]

                if (self.PanicReset == True):
                    if ("OBJECT" in TargetType):
                        for Object in bpy.data.objects:
                            if (Object is not None):
                                if ("VIEWPORT" in VisibilityType):
                                    Object.hide_viewport = False
                                if ("RENDER" in VisibilityType):
                                    Object.hide_render = False

                    if ("COLLECTION" in TargetType): 
                        for Collection in bpy.data.collections:
                            if ("VIEWPORT" in VisibilityType):
                                Collection.hide_viewport = False
                            if ("RENDER" in VisibilityType):
                                Collection.hide_render = False
                    return {"FINISHED"}
            except:
                pass
        try:
            VisibilityType = []
            TargetType = []
            VisibilityType = [visibility for visibility in SelectedVisibility]
            TargetType = [type for type in SelectedType]

            try:
                VisibilityType[0]
                TargetType[0]

                IsolatorObjects = []
                ObjectsCollections = []
                IsolatorCollection = []
                try:
                    context.selected_objects[0]
                    IsolatorObjects = [Object for Object in context.scene.objects if ((Object is not None) and (Object not in context.selected_objects))]
                    ObjectsCollections = [Object.users_collection[0] for Object in context.selected_objects]
                    IsolatorCollection = [Collection for ObjectCollection in ObjectsCollections for Collection in bpy.data.collections if (ObjectCollection != Collection) and (ObjectCollection not in Collection.children_recursive)]
                except Exception as error:
                    print(error)

                if ("OBJECT" in TargetType):
                    try:
                        IsolatorObjects[0]
                        bpy.types.Scene.alx_scene_isolator_visibility_object_list = IsolatorObjects

                        for Object in IsolatorObjects:
                            if (Object is not None):
                                if ("VIEWPORT" in VisibilityType):
                                    Object.hide_viewport = not self.TargetVisibility
                                if ("RENDER" in VisibilityType):
                                    Object.hide_render = not self.TargetVisibility
                    except:
                        try:
                            context.scene.alx_scene_isolator_visibility_object_list[0]

                            for Object in context.scene.alx_scene_isolator_visibility_object_list:
                                if (Object is not None):
                                    if ("VIEWPORT" in VisibilityType):
                                        Object.hide_viewport = not self.TargetVisibility
                                    if ("RENDER" in VisibilityType):
                                        Object.hide_render = not self.TargetVisibility
                        except:
                            pass

                if ("COLLECTION" in TargetType): 
                    try:
                        
                        IsolatorCollection[0]
                        bpy.types.Scene.alx_scene_isolator_visibility_collection_list = IsolatorCollection

                        for Collection in IsolatorCollection:
                            if ("VIEWPORT" in VisibilityType):
                                Collection.hide_viewport = not self.TargetVisibility
                            if ("RENDER" in VisibilityType):
                                Collection.hide_render = not self.TargetVisibility
                    except:
                        try:
                            context.scene.alx_scene_isolator_visibility_collection_list[0]

                            for Collection in bpy.types.Scene.alx_scene_isolator_visibility_collection_list:
                                if ("VIEWPORT" in VisibilityType):
                                    Collection.hide_viewport = not self.TargetVisibility
                                if ("RENDER" in VisibilityType):
                                    Collection.hide_render = not self.TargetVisibility
                        except:
                            pass
            except:
                pass

        except Exception as error:
            print(error)

        return {"FINISHED"}
    
class Alx_OT_Object_VisibilitySwitch(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_object_visibility_switch"

    object_pointer_reference : bpy.props.StringProperty(name="", default="", options={"HIDDEN"}) #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True

    def execute(self, context: bpy.types.Context):
        if (self.object_pointer_reference != ""):
            Object : bpy.types.Object = bpy.data.objects.get(self.object_pointer_reference)
            if (Object is not None):
                Object.hide_set(not Object.hide_get())
        return {"FINISHED"}