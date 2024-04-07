from collections.abc import Iterable

import bpy
import bmesh

def all_false(iterable: Iterable[object]) -> bool:
    for item in iterable:
        if (item == True):
            return False
    return True

# loop_index_table = set()
# _unique_runner=[loop_index_table.add(index) for index in tuple(loop.index for vert in self.ContextBMesh.verts for loop in vert.link_loops)]
# del _unique_runner

class Alx_OT_UVRetopology(bpy.types.Operator):
    """"""

    bl_label = "Unlocked Modeling"
    bl_idname = "alx.operator_uv_retopology"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    bIsRunning : bpy.props.BoolProperty(name="", default=False) #type:ignore
    ContextBMesh : bmesh.types.BMesh = None
    bmesh_selection : list = []

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")

    def CancelModal(self, context: bpy.types.Context):
        self.bIsRunning = False
        if (self.ContextBMesh is not None):
            self.ContextBMesh.free()

        self.bmesh_selection = []



    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        override_window = context.window
        override_screen = override_window.screen
        override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
        override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']

        with context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):

            if (event.type == "ESC"):
                self.CancelModal(context)
                return {"CANCELLED"}
            elif (context.area is not None) and (context.area.type != "VIEW_3D"):
                self.CancelModal(context)
                return {"CANCELLED"}
            elif (context.mode != "EDIT_MESH"):
                self.CancelModal(context)
                return {"CANCELLED"}
            elif (context.mode == "EDIT_MESH") and (context.workspace.tools.from_space_view3d_mode("EDIT_MESH", create=False).idname != "alx.workspace_unlocked_modeling_tool"):
                self.CancelModal(context)
                return {"CANCELLED"}

            if (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH"):
                context.area.tag_redraw()

                if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
                    self.ContextMesh = context.edit_object.data
                    if (self.ContextBMesh is None) or (not self.ContextBMesh.is_valid):
                        self.ContextBMesh = bmesh.from_edit_mesh(self.ContextMesh)

                bmesh.update_edit_mesh(self.ContextMesh, loop_triangles=True, destructive=False)

                # boundary_face_corner = [face.index for face in self.ContextBMesh.faces if ([edge.is_boundary for edge in face.edges].count(True) >= 2)]
                # #boundary_split_corner = [face.index for face in self.ContextBMesh.faces if ([edge.is_boundary for edge in face.edges].count(True) >= 2)]
                # print(boundary_face_corner)
                # for face in boundary_face_corner: self.ContextBMesh.faces[face].select = True
                #bmesh.update_edit_mesh(self.ContextMesh, loop_triangles=True, destructive=False)


                return {"PASS_THROUGH"}
            else:
                return {"PASS_THROUGH"}


    def invoke(self, context, event):
        self.bIsRunning = True
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}



class Alx_OT_UVExtractIsland(bpy.types.Operator):
    """"""

    bl_label = "UV - Extract Island"
    bl_idname = "alx.operator_uv_extract_island"
    bl_options = {"REGISTER", "UNDO"}

    ContextMesh : bpy.types.Mesh = None
    ContextBMesh : bmesh.types.BMesh = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")
    
    def execute(self, context: bpy.types.Context):
        if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
            self.ContextMesh = context.edit_object.data
            if (self.ContextBMesh is None) or (not self.ContextBMesh.is_valid):
                self.ContextBMesh = bmesh.from_edit_mesh(self.ContextMesh)

            self.ContextBMesh.verts.ensure_lookup_table()
            self.ContextBMesh.edges.ensure_lookup_table()
            self.ContextBMesh.faces.ensure_lookup_table()

            if (self.ContextBMesh is not None) and (len(self.ContextMesh.uv_layers) > 0):
                uv_layer = self.ContextBMesh.loops.layers.uv[0]

                if (uv_layer is not None):
                    vert : bmesh.types.BMVert
                    edge : bmesh.types.BMEdge
                    face : bmesh.types.BMFace
                    loop : bmesh.types.BMLoop



                    vertex_island_mapping = list()

                    vertex_unprocessed = set(vert.index for vert in self.ContextBMesh.verts)

                    while len(vertex_unprocessed) > 0:
                        vertex_index_island = set()

                        vertex  = [vert for vert in tuple(vert for vert in self.ContextBMesh.verts if (vert.index in vertex_unprocessed) and (all_false(tuple(edge.seam for edge in vert.link_edges))))][0]
                        vertex_queue = [vertex]

                        if (vertex_queue[0] not in vertex_index_island):
                            while len(vertex_queue) > 0:
                                start_vert : bmesh.types.BMVert = vertex_queue[0]

                                if (all_false(tuple(edge.seam for edge in start_vert.link_edges))):
                                    for edge in start_vert.link_edges:
                                        for vert in edge.verts:
                                            if (vert is not start_vert) and (vert.index not in vertex_index_island):
                                                vertex_index_island.add(start_vert.index)
                                                vertex_index_island.add(vert.index)
                                                vertex_queue.append(vert)

                                for edge in start_vert.link_edges:
                                    for face in edge.link_faces:
                                        seam_edge = tuple([vert.index for vert in edge.verts] for edge in face.edges if (edge.seam == True))
                                        if (len(face.edges) == 3) and (len(seam_edge) == 2):
                                            index = [index for index in [vert_index for edge_verts in seam_edge for vert_index in edge_verts] if [vert_index for edge_verts in seam_edge for vert_index in edge_verts].count(index) == 2][0]
                                            for vert in face.verts:
                                                if (vert.index == index) and (vert.index not in vertex_index_island):
                                                    vertex_index_island.add(vert.index)

                                vertex_queue.pop(0)

                            else:
                                vertex_unprocessed.difference_update(vertex_index_island)
                                vertex_island_mapping.append(vertex_index_island)

                    bmesh.update_edit_mesh(self.ContextMesh)



                    UVExtractMesh = bpy.data.meshes.new(f"UV Extract - {context.edit_object.name}") if bpy.data.meshes.get(f"UV Extract - {context.edit_object.name}") is None else bpy.data.meshes.get(f"UV Extract - {context.edit_object.name}")

                    if (uv_layer is not None):
                        UVExtractBMesh : bmesh.types.BMesh = bmesh.new()

                        vert_loop_done = set()

                        for vert_island in vertex_island_mapping:
                            for vert_index in vert_island:
                                for face in self.ContextBMesh.verts[vert_index].link_faces:
                                    verts = set()
                                    for loop in face.loops:
                                        if (loop.index not in vert_loop_done):
                                            uv_coord = loop[uv_layer].uv
                                            uv_vert = UVExtractBMesh.verts.new((uv_coord[0], 0, uv_coord[1]))

                                            verts.add(uv_vert)
                                            vert_loop_done.add(loop.index)
                                    if (len(verts) >= 3):
                                        UVExtractBMesh.faces.new(verts)
                                            
                    bmesh.ops.remove_doubles(UVExtractBMesh, verts=UVExtractBMesh.verts, dist=0.0001)

                    UVExtractBMesh.to_mesh(UVExtractMesh)

                    UVExtractObject = bpy.data.objects.new(f"UV Extract - {context.edit_object.name}", UVExtractMesh) if bpy.data.objects.get(f"UV Extract - {context.edit_object.name}") is None else bpy.data.objects.get(f"UV Extract - {context.edit_object.name}")
                    
                    if (UVExtractObject.name not in context.scene.collection.objects):
                        context.scene.collection.objects.link(UVExtractObject)

        return {"FINISHED"}



class Alx_OT_VXGroupBySeams(bpy.types.Operator):
    """"""

    bl_label = "VX - Group By Seams"
    bl_idname = "alx.operator_vx_group_by_seam"
    bl_options = {"REGISTER", "UNDO"}

    ContextMesh : bpy.types.Mesh = None
    ContextBMesh : bmesh.types.BMesh = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")
    
    def execute(self, context: bpy.types.Context):
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

            seam_vert = set(vert for edge in self.ContextBMesh.edges for vert in edge.verts if ([edge.seam for edge in vert.link_edges].count(True) > 0))
            non_seam_vert = set(vert for edge in self.ContextBMesh.edges for vert in edge.verts if (all_false([edge.seam for edge in vert.link_edges])))

            sculpt_mask_layer = self.ContextBMesh.verts.layers.float.get(".sculpt_mask")
            if (sculpt_mask_layer is None):
                sculpt_mask_layer = self.ContextBMesh.verts.layers.float.new(".sculpt_mask")

            for vert in seam_vert:
                vert[sculpt_mask_layer] = 1.0

            deform_layer = self.ContextBMesh.verts.layers.deform.verify()

            seam_group_index = context.edit_object.vertex_groups.find("AlxSeamGroup") if (context.edit_object.vertex_groups.find("AlxSeamGroup") != -1) else None
            if (seam_group_index is None):
                seam_group_index = context.edit_object.vertex_groups.new(name="AlxSeamGroup").index

            non_seam_group_index = context.edit_object.vertex_groups.find("AlxNonSeamGroup") if (context.edit_object.vertex_groups.find("AlxNonSeamGroup") != -1) else None
            if (non_seam_group_index is None):
                non_seam_group_index = context.edit_object.vertex_groups.new(name="AlxNonSeamGroup").index

            if (seam_group_index is not None) and (non_seam_group_index is not None):
                for vert in seam_vert:
                    vert[deform_layer][seam_group_index] = 1
                    vert[deform_layer][non_seam_group_index] = 0
                for vert in non_seam_vert:
                    vert[deform_layer][seam_group_index] = 0
                    vert[deform_layer][non_seam_group_index] = 1

            bmesh.update_edit_mesh(self.ContextMesh)

            return {"FINISHED"}