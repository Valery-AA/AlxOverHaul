bl_info = {
    "name" : "AlxOverHaul",
    "author" : "Valery[.V Arhal]",
    "description" : "",
    "version" : (0, 2, 0),
    "warning" : "[Heavly(Not Frequently) Under Development] Minimum Supported BL Version 3.0",
    "description": "An Addon To Simplify Workflow By Reducing The Number of Click To Do Stuff, And More",
    "category" : "3D View",
    "location" : "[Alx 3D] Panel Tab, Changes Based on Active Mode And Other",
    "blender" : (3, 6, 2)
}

if "bpy" in locals():
    import importlib
    if "AlxPackage" in locals():
        importlib.reload(AlxPackage)

import bpy
import AlxPackage
from bpy.props import StringProperty

class Alx_Panel_Rigging(bpy.types.Panel):
    """"""

    bl_label = "Alx Rigging Panel"
    bl_idname = "Alx.Panel_PT_AlxRigging"

    bl_category = "Alx 3D"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
            return True
        
    def draw(self, context):

        AlxLayout = self.layout
        AlxRow = AlxLayout.row()

        AlxLayout.label(text="Pose:")
        
        if (context.active_object is not None):
            
            AlxParentArmature = None
            AlxContextObject = None

            if (context.active_object.type == "MESH") and (context.active_object.find_armature() is not None):
                AlxParentArmature = bpy.data.armatures[context.active_object.find_armature().data.name]
                AlxContextObject = context.active_object.data.name
            if (context.active_object.type == "ARMATURE") and (context.active_object is not None):
                AlxParentArmature = bpy.data.armatures[context.active_object.data.name]
            

            if (AlxParentArmature is not None):
                AlxLayout.row().prop(AlxParentArmature, "pose_position", expand=True)
            else:
                AlxLayout.row().label(text="No Influencing Armature Found")


            if (context.mode != "OBJECT"):
                OMSwitch = AlxLayout.row().operator(Alx_OT_AutoObjectModeSwitch.bl_idname, text="Object", emboss=True)

            if (context.mode != "POSE") and (AlxParentArmature is not None):
                PMSwitch = AlxLayout.row().operator(Alx_OT_AutoPoseModeSwitch.bl_idname, text="Pose", emboss=True)
                PMSwitch.PoseActiveArmature = AlxParentArmature.name

            if (context.mode != "PAINT_WEIGHT") and (AlxParentArmature is not None) and (AlxContextObject is not None):
                WPMSwitch = AlxLayout.row().operator(Alx_OT_AutoWeightPaintModeSwitch.bl_idname, text="Weight Paint", emboss=True, depress=True)
                WPMSwitch.WeightPaintActiveArmature = AlxParentArmature.name
                WPMSwitch.WeightPaintActiveObject = AlxContextObject
  
class Alx_OT_AutoObjectModeSwitch(bpy.types.Operator):
    """"""

    bl_label = "Auto Switch To Object Mode For Active Object"
    bl_idname = "alx.auto_object_mode_switch"

    @classmethod
    def poll (self, context):
        return True
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode="OBJECT")

        return {"FINISHED"}

class Alx_OT_AutoWeightPaintModeSwitch(bpy.types.Operator):
    """"""

    bl_label = "Auto-Select and enter weight paint based on selected object"
    bl_idname = "alx.auto_weightpaint_mode_switch"

    WeightPaintActiveArmature : StringProperty()
    WeightPaintActiveObject : StringProperty()

    @classmethod
    def poll (self, context):
        return (context.mode != "POSE")
    
    def execute(self, context):

        if (context.mode is not "PAINT_WEIGHT") and (self.WeightPaintActiveArmature is not None):
            bpy.context.selected_objects.append(bpy.data.armatures.get(self.WeightPaintActiveArmature))

            if (bpy.data.objects.get(self.WeightPaintActiveObject) is not None):
                bpy.context.view_layer.objects.active =  bpy.data.objects.get(self.WeightPaintActiveObject)  

            if (context.active_object.type == "MESH"):
                bpy.ops.object.mode_set(mode="WEIGHT_PAINT")

        return {"FINISHED"}
    
class Alx_OT_AutoPoseModeSwitch(bpy.types.Operator):
    """"""

    bl_label = "Auto Switch To Influencing Armature"
    bl_idname = "alx.auto_pose_mode_switch"

    PoseActiveArmature : StringProperty()

    @classmethod
    def poll (self, context):
        return (context.mode != "PAINT_WEIGHT")
    
    def execute(self, context):

        if (context.mode != "POSE") and (self.PoseActiveArmature != ""):
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[bpy.data.armatures.find(self.PoseActiveArmature)].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[bpy.data.armatures.find(self.PoseActiveArmature)]

            bpy.ops.object.mode_set(mode="POSE")
        return {"FINISHED"}

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

    bl_parent_id = "Alx.Panel_PT_AlxRigging"

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



def register():
    AlxPackage.AlxFeedToRegister()

def unregister():
    AlxPackage.AlxFeedToUnregister()

AlxClassQueue = [Alx_Panel_Rigging, 
                 Alx_Panel_SwapArmatureAction,
                 Alx_UL_ActionSelector,
                 Alx_OT_AutoObjectModeSwitch,
                 Alx_OT_AutoPoseModeSwitch,
                 Alx_OT_AutoWeightPaintModeSwitch
                 ]

def AlxFeedToRegister():
    for AlxQCls in AlxClassQueue:
        bpy.utils.register_class(AlxQCls)

    bpy.types.Object.UIActionIndex = bpy.props.IntProperty(update=AlxUpdateAddonActionList)
    print("AlxRegister Called")
    print("ALX_LIBRARY_LOADED")
    print(AlxClassQueue)

def AlxFeedToUnregister():
    for AlxQCls in AlxClassQueue:
        bpy.utils.unregister_class(AlxQCls)
    del bpy.types.Object.UIActionIndex
    print("AlxUnRegister Called")



if __name__ == "__main__":
    register()