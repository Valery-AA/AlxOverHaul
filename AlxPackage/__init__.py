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

    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
            return True
        
    def draw(self, context):
        Alxlayout = self.layout
        Alxrow = Alxlayout.row()

        Alxlayout.label(text="Pose:")
        
        if (context.active_object is not None):
            
            InfluencingArmature = None
            PrePoseSwitchObject = None

            if (context.active_object.find_armature() is not None) and (context.active_object.type == "MESH"):
                InfluencingArmature = context.active_object.find_armature()
                PrePoseSwitchObject = context.active_object
                
            elif (context.active_object.find_armature() is None) and (context.active_object.type == "ARMATURE"):
                InfluencingArmature = context.active_object

                if (InfluencingArmature is not None):
                    if (bpy.data.armatures[InfluencingArmature.data.name] is not None):
                        ParentArmature = bpy.data.armatures[InfluencingArmature.data.name]

                        Alxrow.prop(ParentArmature, "pose_position", expand=True)

            else:
                Alxrow.label(text="No Influencing Armature Found")


            if (context.mode != "PAINT_WEIGHT") and (InfluencingArmature is not None) and(PrePoseSwitchObject is not None):
                ObjectOPSwitch = self.layout.operator(Alx_OT_AutoWeightPaintSwitch.bl_idname, text="Weight Paint")
                ObjectOPSwitch.ParentArmatureTarget = InfluencingArmature.data.name
                ObjectOPSwitch.ParentArmatureName = InfluencingArmature.name
                ObjectOPSwitch.WeightPaintTarget = PrePoseSwitchObject.data.name
                ObjectOPSwitch.WeightPaintName = PrePoseSwitchObject.name

            if (context.mode != "OBJECT"):
                self.layout.operator("object.mode_set", text="Object")
                
            if  (context.mode !="POSE") and (InfluencingArmature is not None):
                PoseOPSwitch = self.layout.operator(Alx_OT_AutoSwitchToPose.bl_idname, text="Pose")
                PoseOPSwitch.SwitchArmatureTarget = InfluencingArmature.data.name
                PoseOPSwitch.SwitchArmatureName = InfluencingArmature.name
        
class Alx_OT_AutoWeightPaintSwitch(bpy.types.Operator):
    """"""

    bl_label = "Auto Switch To Influencing Armature"
    bl_idname = "alx.weightpaint_auto_switch"

    ParentArmatureTarget : StringProperty()
    ParentArmatureName : StringProperty()

    WeightPaintTarget : StringProperty()
    WeightPaintName : StringProperty()

    @classmethod
    def poll (self, context):
        return True
    
    def execute(self, context):

        if (context.mode !="PAINT_WEIGHT") and (((self.ParentArmatureTarget != "") or (self.ParentArmatureName != "")) and ((self.WeightPaintTarget != "") or (self.WeightPaintName != ""))):

            if (bpy.data.objects.get(self.ParentArmatureTarget) is not None):
                bpy.data.objects.get(self.ParentArmatureTarget).select_set(True)

            if (bpy.data.objects.get(self.ParentArmatureName) is not None):
                bpy.data.objects.get(self.ParentArmatureName).select_set(True)


            if (bpy.data.objects.get(self.WeightPaintName) is not None):
                bpy.context.view_layer.objects.active =  bpy.data.objects.get(self.WeightPaintName)

            if (bpy.data.objects.get(self.WeightPaintName) is not None):
                bpy.context.view_layer.objects.active =  bpy.data.objects.get(self.WeightPaintName)

            
            if (context.active_object.type == "MESH"):
                bpy.ops.object.mode_set(mode="WEIGHT_PAINT")

        return {"FINISHED"}
    
class Alx_OT_AutoSwitchToPose(bpy.types.Operator):
    """"""

    bl_label = "Auto Switch To Influencing Armature"
    bl_idname = "alx.pose_auto_switch"

    SwitchArmatureTarget : StringProperty()
    SwitchArmatureName : StringProperty()

    @classmethod
    def poll (self, context):
        return True
    
    def execute(self, context):

        if (context.mode !="POSE") and ((self.SwitchArmatureTarget != "") or (self.SwitchArmatureName != "")):
            if (bpy.data.objects.get(self.SwitchArmatureTarget) is not None):
                bpy.context.view_layer.objects.active =  bpy.data.objects.get(self.SwitchArmatureTarget)

            if (bpy.data.objects.get(self.SwitchArmatureName) is not None):
                bpy.context.view_layer.objects.active =  bpy.data.objects.get(self.SwitchArmatureName)

            if (context.active_object.type == "ARMATURE"):
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
            InfluencingArmature = bpy.context.view_layer.objects.active.find_armature()
            if (InfluencingArmature is not None):
                if (bpy.data.armatures[InfluencingArmature.data.name] is not None):
                    ParentArmature = bpy.data.armatures[InfluencingArmature.data.name]

                    if (ParentArmature is not None) and (ParentArmature.animation_data is not None) and (ParentArmature.animation_data.action is not None):
                        ActiveActionIndex = bpy.data.actions.find(ParentArmature.animation_data.action.name)

                        if ActiveActionIndex != ParentArmature.UIActionIndex:
                            ParentArmature.UIActionIndex = ActiveActionIndex

def AlxUpdateAddonActionList(self, context):
         if(context.active_object is not None):
            InfluencingArmature = bpy.context.view_layer.objects.active.find_armature()
            if (InfluencingArmature is not None):
                if (bpy.data.armatures[InfluencingArmature.data.name] is not None):
                    ParentArmature = bpy.data.armatures[InfluencingArmature.data.name]
            
                    if (ParentArmature is not None) and (ParentArmature.animation_data is not None) and (ParentArmature.animation_data.action is not None):
                        ParentArmature.animation_data.action = bpy.data.actions[ParentArmature.UIActionIndex]
                        bpy.context.scene.frame_current = 0

bpy.app.handlers.depsgraph_update_post.append(AlxUpdateActionUI)



def register():
    AlxPackage.AlxFeedToRegister()

def unregister():
    AlxPackage.AlxFeedToUnregister()

AlxClassQueue = [Alx_Panel_Rigging, 
                 Alx_Panel_SwapArmatureAction,
                 Alx_UL_ActionSelector,
                 Alx_OT_AutoSwitchToPose,
                 Alx_OT_AutoWeightPaintSwitch
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