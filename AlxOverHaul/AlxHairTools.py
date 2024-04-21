import bpy
import bmesh

from .AlxUtils import AlxRetiriveObjectModifier

class Alx_OT_Armature_BoneChainOnSelection(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_armature_bone_chain_on_selection"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    user_armature_name : bpy.props.StringProperty(name="New armature name:") #type:ignore
    reverse : bpy.props.BoolProperty(name="Reverse direction") #type:ignore

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")
    
    def execute(self, context: bpy.types.Context):
        self.ContextObject : bpy.types.Object = context.edit_object
        self.ContextMesh : bpy.types.Mesh = None
        self.ContextBMesh : bmesh.types.BMesh = None

        if (AlxRetiriveObjectModifier(self.ContextObject, "SUBSURF") is not None):
            self.report({"ERROR"}, message="Strip has a subdivision modifier")
            return {"CANCELLED"}



        if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
            self.ContextMesh = context.edit_object.data
            if (self.ContextBMesh is None) or (not self.ContextBMesh.is_valid):
                self.ContextBMesh = bmesh.from_edit_mesh(self.ContextMesh)

            self.ContextBMesh.verts.ensure_lookup_table()
            self.ContextBMesh.edges.ensure_lookup_table()
            self.ContextBMesh.faces.ensure_lookup_table()

            vert : bmesh.types.BMVert
            edge : bmesh.types.BMEdge
            face : bmesh.types.BMFace
            loop : bmesh.types.BMLoop

            

            edge_selection = [edge.index for edge in self.ContextBMesh.edges if (edge.select == True)]
            edge_selection_validity = all([True if (len([0 for vert in self.ContextBMesh.edges[edge_index].verts for edge in vert.link_edges if (edge.select == True) and (edge.index != self.ContextBMesh.edges[edge_index].index)]) in range(1, 3)) else False for edge_index in edge_selection])

            if (edge_selection_validity == False):
                self.report({"ERROR"}, "Selection is invalid - no more than one connected edge selected per vertex")
                return {"CANCELLED"}

            if (edge_selection_validity == True):
                chain_ends = [vert.index for edge_index in edge_selection for vert in self.ContextBMesh.edges[edge_index].verts if (len([0 for edge in vert.link_edges if (edge.select == True)]) == 1)]
                
                starting_vert : bmesh.types.BMVert
                ending_vert : bmesh.types.BMVert

                if (self.ContextBMesh.verts[chain_ends[0]].co.z > self.ContextBMesh.verts[chain_ends[1]].co.z) and (self.reverse == False):
                    starting_vert = self.ContextBMesh.verts[chain_ends[0]]
                    ending_vert = self.ContextBMesh.verts[chain_ends[1]]
                elif (self.ContextBMesh.verts[chain_ends[1]].co.z > self.ContextBMesh.verts[chain_ends[0]].co.z) and (self.reverse == False):
                    starting_vert = self.ContextBMesh.verts[chain_ends[1]]
                    ending_vert = self.ContextBMesh.verts[chain_ends[0]]
                elif (self.ContextBMesh.verts[chain_ends[0]].co.z > self.ContextBMesh.verts[chain_ends[1]].co.z) and (self.reverse == True):
                    starting_vert = self.ContextBMesh.verts[chain_ends[1]]
                    ending_vert = self.ContextBMesh.verts[chain_ends[0]]
                elif (self.ContextBMesh.verts[chain_ends[1]].co.z > self.ContextBMesh.verts[chain_ends[0]].co.z) and (self.reverse == True):
                    starting_vert = self.ContextBMesh.verts[chain_ends[0]]
                    ending_vert = self.ContextBMesh.verts[chain_ends[1]]

                ordered_vert_chain = list()
                ordered_vert_chain.append(starting_vert.index)

                for i in range(0, len(edge_selection)):
                    for edge in starting_vert.link_edges:
                        if (edge.index in edge_selection):
                            for vert in edge.verts:
                                if (vert.index not in ordered_vert_chain) and (vert.index != starting_vert.index):
                                    next_vert = vert

                                    ordered_vert_chain.append(next_vert.index)
                                    starting_vert = next_vert

                ordered_bone_position = list()
                ordered_normal_vector = list()

                for i in range(0, len(ordered_vert_chain)):
                    if (i < len(ordered_vert_chain)-1):
                        head = self.ContextObject.matrix_world @ self.ContextBMesh.verts[ordered_vert_chain[i]].co
                        tail = self.ContextObject.matrix_world @ self.ContextBMesh.verts[ordered_vert_chain[i+1]].co

                        vertex_normal = self.ContextBMesh.verts[ordered_vert_chain[i]].normal

                        ordered_bone_position.append([head, tail])
                        ordered_normal_vector.append(vertex_normal)
                
                

                if (self.user_armature_name != ""):
                    armature_object = bpy.data.objects.get(self.user_armature_name)
                    if (armature_object is None):
                        new_armature_data = bpy.data.armatures.new(name=self.user_armature_name)
                        armature_object = bpy.data.objects.new(name=self.user_armature_name, object_data=new_armature_data)

                    if (armature_object.name not in context.scene.collection.objects):
                        context.scene.collection.objects.link(armature_object)

                    armature_data : bpy.types.Armature = armature_object.data

                    bpy.ops.object.mode_set(mode="OBJECT")
                    context.view_layer.objects.active = armature_object
                    bpy.ops.object.mode_set(mode="EDIT")


                    for i in range(0, len(ordered_vert_chain)):
                        identifier = f"bone.v_index_{ordered_vert_chain[i]}"

                        bone = armature_data.edit_bones.get(identifier) if armature_data.edit_bones.get(identifier) else armature_data.edit_bones.new(identifier)
                        if (bone is not None) and i < len(ordered_vert_chain)-1:
                            head_vert = ordered_bone_position[i][0]
                            bone.head.xyz = head_vert

                            tail_vert = ordered_bone_position[i][1]
                            bone.tail.xyz = tail_vert

                            bone.use_connect = True
                            bone.parent = armature_data.edit_bones.get(f"bone.v_index_{ordered_vert_chain[i-1]}")
                            bone.align_roll(vector=ordered_normal_vector[i])



            return {"FINISHED"}

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.row().label(text="Options:")
        layout.row().prop(self, "user_armature_name")
        layout.row().prop(self, "reverse")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    

