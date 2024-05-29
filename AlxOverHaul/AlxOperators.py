# type:ignore

import bpy
import bmesh

from . import AlxUtils



class Alx_OT_UI_SimpleDesigner(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_ui_simple_designer"
    bl_options = {"INTERNAL"}

    UseAreaSplit : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})
    AreaSplitDirection : bpy.props.EnumProperty(name="", default="VERTICAL", items=[("VERTICAL", "Vertical", "", 1), ("HORIZONTAL", "Horizontal", "", 1<<1)])
    AreaSplitFactor : bpy.props.FloatProperty(name="", default=0.5, options={"HIDDEN"})

    UseCloseArea : bpy.props.BoolProperty(name="", default=False, options={"HIDDEN"})


    @classmethod
    def poll(self, context: bpy.types.Context):
        return True
    
    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        ScreenAreas = []
        if (context is not None) and (context.screen is not None):
            ScreenAreas = [area for area in context.screen.areas if (area is None) and (area.type != "EMPTY")]

        if (event.type == "MOUSE_MOVE"):
            try:
                ScreenAreas[0]
                
                for area in ScreenAreas:
                    if (area.x <= event.mouse_x) and ((area.x + area.width) >= event.mouse_x):
                        pass

            except Exception as error:
                print(error)
            
            event.mouse_x
            event.mouse_y

        if (event.type == "ESC"):
            return {"CANCELLED"}

        return {"RUNNING_MODAL"}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class Alx_OT_Armature_MatchIKByMirroredName(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.bone_match_ik_by_mirrored_name"

    bl_description = "Requires [Pose Mode] Mirrors IK Data from the source side to the opposite"

    bl_options = {"INTERNAL", "REGISTER", "UNDO"}

    SourceSide : bpy.props.EnumProperty(name="Mirror From", default=1, items=[("LEFT", "Left", "", 1), ("RIGHT", "Right", "", 2)])

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D" and context.mode == "POSE"

    def execute(self, context):
        if (context.active_object is not None) and (context.active_object.type == "ARMATURE") and (context.mode == "POSE"):

            ContextArmature = context.active_object

            if (ContextArmature is not None):

                PoseBoneData = ContextArmature.pose.bones

                SymmetricPairBones = []
                SymmetricUniqueBones = []
                
                if (self.SourceSide == "LEFT"):
                    SymmetricPairBones = [PoseBone for PoseBone in PoseBoneData if ((PoseBone.name[-1].lower() == "l"))]
                
                if (self.SourceSide == "RIGHT"):
                    SymmetricPairBones = [PoseBone for PoseBone in PoseBoneData if ((PoseBone.name[-1].lower() == "r"))]
                
                for PoseBone in SymmetricPairBones:
                    if (PoseBone not in SymmetricUniqueBones):
                        SymmetricUniqueBones.append(PoseBone)

                for UniquePoseBone in SymmetricUniqueBones:
                    ContextPoseBone = None
                    ContextOppositeBone = None

                    if (self.SourceSide == "LEFT"):
                        ContextPoseBone = AlxUtils.AlxGetBoneAlwaysLeft(UniquePoseBone, ContextArmature)
                        ContextOppositeBone = AlxUtils.AlxGetBoneOpposite(AlxUtils.AlxGetBoneAlwaysLeft(UniquePoseBone, ContextArmature), ContextArmature)
                    
                    if (self.SourceSide == "RIGHT"):
                        ContextPoseBone = AlxUtils.AlxGetBoneAlwaysRight(UniquePoseBone, ContextArmature)
                        ContextOppositeBone = AlxUtils.AlxGetBoneOpposite(AlxUtils.AlxGetBoneAlwaysRight(UniquePoseBone, ContextArmature), ContextArmature)

                    if (ContextPoseBone is not None) and (ContextOppositeBone is not None):
                        AlxUtils.AlxCloneIKSettings(ContextPoseBone, ContextOppositeBone)
                        AlxUtils.AlxCloneIKBoneLimitOnChain(ContextPoseBone, ContextArmature)
        
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

class Alx_OT_Mesh_BoundaryMultiTool(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_mesh_boundary_multi_tool"

    KeepDividingEdges : bpy.props.BoolProperty(name="Keep Non-Boundary", default=False)

    UseCrease : bpy.props.BoolProperty(name="Crease", default=False)
    UsePin : bpy.props.BoolProperty(name="Use as Pin", default=False)

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"
    
    def execute(self, context):
        ContextMesh = None
        ContextBMesh = None

        if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
            ContextMesh = context.edit_object.data
            ContextBMesh = bmesh.from_edit_mesh(context.edit_object.data)

            if (ContextBMesh is not None):
                BoundaryVertex = []
                BoundaryEdge = []
                DividingNonBoundaryEdge = []

                EdgeSelection = [edge for edge in ContextBMesh.edges if (edge.select)]


                for SelectedEdge in EdgeSelection:
                    
                    if (SelectedEdge is not None):
                        NonBoundaryEdge = []

                        if (SelectedEdge.is_boundary == True):
                            BoundaryVertex.extend([Vertex for Vertex in SelectedEdge.verts if (Vertex not in BoundaryVertex)])
                            if (SelectedEdge not in BoundaryEdge):
                                BoundaryEdge.append(SelectedEdge)

                        for Vertex in BoundaryVertex:
                            for LinkedEdge in Vertex.link_edges:
                                if (LinkedEdge.is_boundary == False):
                                    if (LinkedEdge not in NonBoundaryEdge):
                                        NonBoundaryEdge.append(LinkedEdge)
                                    if (LinkedEdge in NonBoundaryEdge):
                                        DividingNonBoundaryEdge.append(LinkedEdge)

                if (self.UsePin == True):
                    PinGroup = None

                    for VxGroup in context.edit_object.vertex_groups:
                        if (PinGroup is None) and (VxGroup.name.lower() == "pin"):
                            PinGroup = VxGroup
                    else:
                        if (PinGroup is None):
                            PinGroup = context.edit_object.vertex_groups.new(name="Pin")

                    if (PinGroup is not None):
                        PinGroup.name = "Pin"

                    AddVertex = [Vertex.index for Vertex in BoundaryVertex]
                    if (self.KeepDividingEdges == False):
                        RemoveVertex = [Vertex.index for Edge in DividingNonBoundaryEdge for Vertex in Edge.verts]

                if(self.UseCrease == True):
                    CreaseLayer = ContextBMesh.edges.layers.float.get('crease_edge', None)
                    if (CreaseLayer is None):
                        CreaseLayer = ContextBMesh.edges.layers.float.new('crease_edge')
                        ContextBMesh.verts.ensure_lookup_table()
                    for CreaseEdge in BoundaryEdge:
                        ContextBMesh.edges[CreaseEdge.index][CreaseLayer] = 1.0
                    bmesh.update_edit_mesh(ContextMesh, loop_triangles=False)

                if (self.UsePin):
                    bpy.ops.object.mode_set(mode="OBJECT")
                    PinGroup.add(index=AddVertex, weight=1.0, type="REPLACE")
                    bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)

class Alx_OT_Mesh_EditAttributes(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_mesh_edit_attributes"

    AttributeName : bpy.props.StringProperty(name="Attribute Name", default="")
    CreateMissingAttribute : bpy.props.BoolProperty(name="Create Missing Attribute")
    ShouldDeleteAttribute : bpy.props.BoolProperty(name="Delete Attribute", default=False)
    AttributeDomainType : bpy.props.EnumProperty(name="Attribute Type", default=0, items=[("POINT", "Vertex", ""), ("EDGE", "Edge", "")])
    AttributeType : bpy.props.EnumProperty(name="Attribute Type", default=0, items=[("FLOAT_COLOR", "Float Color", "")])
    ColorValue : bpy.props.FloatVectorProperty(name="Color", subtype="COLOR", size=4, default=[0.0, 0.0, 0.0, 1.0], min=0.0, max=1.0)

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D" and context.mode == "EDIT_MESH"
    
    def execute(self, context):
        try:            
            context.selected_objects[0]
            MeshSelection = [Object.data for Object in context.selected_objects if (Object is not None) and (Object.type == "MESH")]

            if (context.mode == "EDIT_MESH"):

                for MeshObject in MeshSelection:
                    ContextBMesh = bmesh.from_edit_mesh(MeshObject)

                    SelectedVertex = [Vertex.index for Vertex in ContextBMesh.verts if Vertex.select == True]

                    bpy.ops.object.mode_set(mode="OBJECT")

                    ContextAttribute = MeshObject.attributes.get(self.AttributeName)

                    if (ContextAttribute is None):
                        if (self.CreateMissingAttribute == True):
                            ContextAttribute = MeshObject.attributes.new(name=self.AttributeName, type=self.AttributeType, domain=self.AttributeDomainType)

                    if (ContextAttribute is not None):
                        if (self.ShouldDeleteAttribute == True):
                            MeshObject.attributes.remove(ContextAttribute)

                        if (self.AttributeDomainType == "POINT"):
                            for Vertex in SelectedVertex:
                                if (self.AttributeType == "FLOAT_COLOR"):
                                    ContextAttribute.data[Vertex].color = self.ColorValue

                    bpy.ops.object.mode_set(mode="EDIT")
        except Exception as e:
            print(e)
    
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)



class Alx_OT_Armature_AssignToSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.armature_assign_to_selection"
    bl_description = "Assigns any [Mesh] in the current selection to the [Armature] within said selection"

    bl_options = {"INTERNAL","REGISTER", "UNDO"}

    # def UpdateUseAutomaticWeight(self, context):
    #     if (self.UseAutomaticWeight == True):
    #         self.UseSingleVxGroup = False
    #         self.UsePurgeOtherGroups = False
    #         self.VxGroupName = ""

    # def UpdateUsePreserveExistingGroups(self, context):
    #     if (self.UsePreserveExistingGroups == True):
    #         self.UseAutomaticWeight = True
    #         self.UseSingleVxGroup = False
    #         self.UsePurgeOtherGroups = False
    #         self.VxGroupName = ""
        
    def UpdateUseSingleVxGroup(self, context):
        # if (self.UseSingleVxGroup == True):
        #     self.UseAutomaticWeight = False
        #     self.UsePreserveExistingGroups = False
        pass

    def UpdateUsePurgeOtherGroups(self, context):
        if (self.UsePurgeOtherGroups == True):
            self.UseSingleVxGroup = True
            #self.UseAutomaticWeight = False
            #self.UsePreserveExistingGroups = False

    def UpdateVxGroupName(self, context):
        if (self.VxGroupName != ""):
            self.UseSingleVxGroup = True

    UseParent : bpy.props.BoolProperty(name="Should Parent", default=False)

    #UseAutomaticWeight : BoolProperty(name="Automatic Weights", default=False, update=UpdateUseAutomaticWeight)
    #UsePreserveExistingGroups : BoolProperty(name="Preserve Existing VxGroups", default=False, update=UpdateUsePreserveExistingGroups)

    UseSingleVxGroup : bpy.props.BoolProperty(name="Single VxGroup", default=False, update=UpdateUseSingleVxGroup)
    CreateMissingVxGroups : bpy.props.BoolProperty(name="Create Missing VxGroups", default=False)
    UsePurgeOtherGroups : bpy.props.BoolProperty(name="PURGE Other VxGroups", description="PURGE any other VxGroup that does not correspon to the specified single VxGroup", default=False, update=UpdateUsePurgeOtherGroups)
    VxGroupName : bpy.props.StringProperty(name="Group", default="", update=UpdateVxGroupName)

    @classmethod
    def poll(self, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        Armature = None

        if (len(context.selected_objects) != 0):
            for SelectedObject in context.selected_objects:
                if (Armature is None) and (SelectedObject.type == "ARMATURE"):
                    Armature = SelectedObject
                    
            for SelectedObject in context.selected_objects:
                if (Armature is not None):
                    if (SelectedObject.type == "MESH"):
                        ArmatureModifier = AlxUtils.AlxRetiriveObjectModifier(SelectedObject, "ARMATURE")

                        if (ArmatureModifier is None):
                            ArmatureModifier = SelectedObject.modifiers.new(name="Armature", type="ARMATURE")

                        if (ArmatureModifier is not None):
                            ArmatureModifier.object = Armature

                        if (self.UseParent == True):
                            SelectedObject.parent = Armature
                            SelectedObject.matrix_parent_inverse = Armature.matrix_world.inverted()

                        # if (self.UseAutomaticWeight == True):
                        #     bpy.ops.alx.automatic_mode_changer(DefaultBehaviour=False, TargetMode="PAINT_WEIGHT", TargetObject=SelectedObject.name, TargetArmature=self.TargetArmature)
                        #     #bpy.ops.paint.weight_from_bones(type='AUTOMATIC')

                        if (self.UseSingleVxGroup == True):
                            if (self.CreateMissingVxGroups == True):
                                if (self.VxGroupName != "") and (self.VxGroupName not in SelectedObject.vertex_groups):
                                    VxGroup = SelectedObject.vertex_groups.new()
                                    VxGroup.name = self.VxGroupName
                            if (self.VxGroupName != "") and (self.VxGroupName in SelectedObject.vertex_groups):
                                VxGroup = SelectedObject.vertex_groups.get(self.VxGroupName)
                                
                                if (VxGroup is not None):
                                    VxGroup.add(range(0, len(SelectedObject.data.vertices)), 1.0, 'REPLACE')
                        
                        if (self.UsePurgeOtherGroups == True):
                            if (self.VxGroupName != "") and (self.VxGroupName in SelectedObject.vertex_groups):
                                for ObjectVxGroup in SelectedObject.vertex_groups:
                                    if (ObjectVxGroup.name != self.VxGroupName):
                                        SelectedObject.vertex_groups.remove(ObjectVxGroup)
                                                
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class Alx_OT_Modifier_HideOnSelected(bpy.types.Operator):
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
        return context.area.type == "VIEW_3D"

    def execute(self, context):
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
   

