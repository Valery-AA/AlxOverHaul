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



                    vertex_queue = [[vert for vert in self.ContextBMesh.verts if (vert.select == True) and (all_false(tuple(edge.seam for edge in vert.link_edges)))][0]]
                    vertex_done = set()

                    while len(vertex_queue) > 0:
                        start_vert : bmesh.types.BMVert = vertex_queue[0]

                        if (all_false(tuple(edge.seam for edge in start_vert.link_edges))):
                            start_vert.select = True
                            for edge in start_vert.link_edges:
                                for vert in edge.verts:
                                    if (vert is not start_vert) and (vert.index not in vertex_done):
                                        vert.select = True
                                        vertex_done.add(vert.index)
                                        vertex_queue.append(vert)

                        for edge in start_vert.link_edges:
                            for face in edge.link_faces:
                                seam_edge = tuple([vert.index for vert in edge.verts] for edge in face.edges if (edge.seam == True))
                                if (len(face.edges) == 3) and (len(seam_edge) == 2):
                                    index = [index for index in [vert_index for edge_verts in seam_edge for vert_index in edge_verts] if [vert_index for edge_verts in seam_edge for vert_index in edge_verts].count(index) == 2][0]
                                    for vert in face.verts:
                                        if (vert.index == index) and (vert.index not in vertex_done):
                                            vert.select = True
                                            vertex_done.add(vert.index)
                                

                        vertex_queue.pop(0)

                    else:
                        print(len(vertex_queue))

                    bmesh.update_edit_mesh(self.ContextMesh)

                    UVExtractMesh = bpy.data.meshes.new(f"UV Extract - {context.edit_object.name}") if bpy.data.meshes.get(f"UV Extract - {context.edit_object.name}") is None else bpy.data.meshes.get(f"UV Extract - {context.edit_object.name}")

                    UVExtractObject = bpy.data.objects.new(f"UV Extract - {context.edit_object.name}", UVExtractMesh) if bpy.data.objects.get(f"UV Extract - {context.edit_object.name}") is None else bpy.data.objects.get(f"UV Extract - {context.edit_object.name}")
                    if (UVExtractObject.name not in context.scene.collection.objects):
                        context.scene.collection.objects.link(UVExtractObject)


            #     UVExtractBMesh : bmesh.types.BMesh = bmesh.new()

            


            # if (uv_layer is not None):

                

                

                

                
            #     islands_index_table = tuple()

                


                # if (edge.seam == True):
                        # for loop in edge.link_loops:
                        #     if (loop.edge.seam == True):
                        #         uv_coord = loop[uv_layer].uv
                        #         uv_vert = UVExtractBMesh.verts.new((uv_coord[0], 0, uv_coord[1]))
                # for edge in SkeletonBmesh.edges:
                #     if (edge.seam == True):
                #         for loop in edge.link_loops:
                #             if (len(edge.link_loops) == 1):
                #                 
                #                 
                #             if (loop.edge.seam == True):
                #                 print(edge.index)
                                

                                # for sub_loop in loop.link_loops:
                                #     if (sub_loop is not loop) and (loop.edge.index == sub_loop.edge.index) and (sub_loop.edge.seam == True):
                                #         pair.append([])












                # perimeter_edges = [edge for edge in SkeletonBmesh.edges if edge.seam == True]
                # perimeter_loops = [loop for loop in [loop for edge in perimeter_edges for loop in edge.link_loops] if (loop.edge in perimeter_edges)]



                # uv_vert_loop_pair = []

                # for loop in perimeter_loops:                
                    
                #     
                    
                #     uv_vert_loop_pair.append([loop.edge.index, loop, uv_vert])

                # for loop_pair in uv_vert_loop_pair:
                #     local_loop = loop_pair[1]
                #     next_vert = [[loop, uv_vert] for loop_index , loop, uv_vert in uv_vert_loop_pair if loop_index == local_loop.edge.index]

                #     print(len(next_vert))

                #     for i in range(0, len(next_vert)):
                #         try:
                #             UVExtractBMesh.edges.new((loop_pair[2], next_vert[i][1]))
                #         except:
                #             pass

                #bmesh.ops.remove_doubles(UVExtractBMesh, verts=UVExtractBMesh.verts, dist=0.0001)
                

                
                # UVExtractBMesh.to_mesh(Extracted_Mesh)




                



            # obj=bpy.context.active_object
            # if obj.type=='MESH':
            #     obD=obj.data
            #     if obD.uv_layers.active:
            #         for poly in obD.polygons:
            #             for loop in poly.loop_indices:
            #                 uv=obD.uv_layers[0].data[loop].uv
            #                 print('Vertex[', obD.loops[loop].vertex_index, '].uv = ', uv)

        return {"FINISHED"}
