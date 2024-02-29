__ALX_DEBUG__ = False

import bpy
import bmesh

from .AlxGpuUI import draw_unlocked_modeling_ui

class Alx_PT_Panel_UnlockedModeling(bpy.types.Panel):
    """"""

    bl_label = ""
    bl_idname = "ALX_PT_panel_tool_unlocked_modeling"

    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        if (context is not None):
            return (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")
        else:
            return False

    def draw(self, context: bpy.types.Context):
        Properties = context.scene.alx_tool_unlocked_modeling_properties

        AlxLayout = self.layout
        AlxLayout.ui_units_x = 12.0

        AlxLayout.label(text="Delete:")
        poly_delete_grid_flow = AlxLayout.grid_flow(columns=3, align=True)
        poly_delete_grid_flow.prop(Properties, "poly_delete_type", expand=True)
        AlxLayout.label(text="Mark:")
        edge_mark_grid_flow = AlxLayout.grid_flow(columns=3, align=True)
        edge_mark_grid_flow.prop(Properties, "edge_mark_type", expand=True)



class Alx_OT_Tool_UnlockedModeling(bpy.types.Operator):
    """"""

    bl_label = "Unlocked Modeling"
    bl_idname = "alx.operator_unlocked_modeling_tool"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    bIsRunning : bpy.props.BoolProperty(name="", default=False)
    ContextBmesh : bmesh.types.BMesh = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True

    def CancelModal(self, context: bpy.types.Context):
        self.bIsRunning = False
        try:
            bpy.types.SpaceView3D.draw_handler_remove(context.scene.alx_draw_handler_unlocked_modeling, "WINDOW")
            bpy.types.Scene.alx_draw_handler_unlocked_modeling = None
            context.area.tag_redraw()

        except Exception as error:
            print(f"info-cancel: unlocked modeling ui {error}")

        context.area.tag_redraw()

        if (self.ContextBmesh is not None):
            self.ContextBmesh.free()
        

    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        context.area.tag_redraw()

        if (event.type == "ESC"):
            self.CancelModal(context)
            return {"CANCELLED"}
        elif ((context.area is not None) and (context.area.type != "VIEW_3D")):
            self.CancelModal(context)
            return {"CANCELLED"}
        elif (context.mode != "EDIT_MESH"):
            self.CancelModal(context)
            return {"CANCELLED"}
        elif (context.mode == "EDIT_MESH") and (context.workspace.tools.from_space_view3d_mode("EDIT_MESH", create=False).idname != "alx.workspace_unlocked_modeling_tool"):
            self.CancelModal(context)
            return {"CANCELLED"}

        if (context.mode == "EDIT_MESH") and (context.edit_object.type == "MESH"):
            self.ContextMesh = context.edit_object.data
            if (self.ContextBmesh is None) or (not self.ContextBmesh.is_valid):
                self.ContextBmesh = bmesh.from_edit_mesh(self.ContextMesh)

            self.ContextBmesh.edges.ensure_lookup_table()

            self.crease_mark_layer = self.ContextBmesh.edges.layers.float.get('crease_edge', None)
            if (self.crease_mark_layer is None):
                self.crease_mark_layer = self.ContextBmesh.edges.layers.float.new('crease_edge')

            self.crease_mark_layer = self.ContextBmesh.edges.layers.float.get('crease_edge', None)
            if (self.crease_mark_layer is None):
                self.crease_mark_layer = self.ContextBmesh.edges.layers.float.new('crease_edge')

            self.ContextBmesh.edges.ensure_lookup_table()

        if (event.type == "S"):
            bpy.ops.wm.call_panel(name=Alx_PT_Panel_UnlockedModeling.bl_idname, keep_open=True)
            return {"RUNNING_MODAL"}
        


        if (event.type == "LEFTMOUSE") and (event.ctrl == False):
            if (context.mode == "EDIT_MESH"):
                override_window = context.window
                override_screen = override_window.screen
                override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
                override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']

                with context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):
                    bpy.ops.mesh.loop_select("INVOKE_DEFAULT", extend=True, deselect=False, toggle=False, ring=False)
            return {"RUNNING_MODAL"}

        if (event.type == "LEFTMOUSE") and (event.ctrl == True):
            if (context.mode == "EDIT_MESH"):
                override_window = context.window
                override_screen = override_window.screen
                override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
                override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']

                with context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):
                    bpy.ops.mesh.loop_select("INVOKE_DEFAULT", extend=False, deselect=True, toggle=False, ring=False)
            return {"RUNNING_MODAL"}

        edge_mark_as = [mark_type for mark_type in context.scene.alx_tool_unlocked_modeling_properties.edge_mark_type]
        poly_delete_type = context.scene.alx_tool_unlocked_modeling_properties.poly_delete_type

        if (event.type == "RIGHTMOUSE") and (event.ctrl == False):
            if (context.edit_object is not None) and (self.ContextBmesh is not None):
                    selection_type = ""
                    if (poly_delete_type in ["FACES", "FACES_ONLY"]):
                        selection_type = "faces"
                    if (poly_delete_type in ["EDGES"]):
                        selection_type = "edges"
                    if (poly_delete_type in ["VERTS"]):
                        selection_type = "verts"

                    if (poly_delete_type != "NONE") and (selection_type != ""):
                        bmesh.ops.delete(self.ContextBmesh, geom=[mesh_poly for mesh_poly in getattr(self.ContextBmesh, f"{selection_type}") if (mesh_poly.select == True)], context=poly_delete_type)
                        bmesh.update_edit_mesh(self.ContextMesh, loop_triangles=True, destructive=True)
                    self.ContextBmesh.edges.ensure_lookup_table()

                    if (poly_delete_type not in ["VERTS", "EDGES"]):
                        for selected_edge in [mesh_edge.index for mesh_edge in self.ContextBmesh.edges if (mesh_edge.select == True)]:
                            if ("bevel_weight_edge" in edge_mark_as):
                                self.ContextBmesh.edges[selected_edge][self.bevel_mark_layer] = 1.0
                            if ("crease_edge" in edge_mark_as):
                                self.ContextBmesh.edges[selected_edge][self.crease_mark_layer] = 1.0
                            if ("seam_edge" in edge_mark_as):
                                self.ContextBmesh.edges[selected_edge].seam = False
                            if ("sharp_edge" in edge_mark_as):
                                self.ContextBmesh.edges[selected_edge].smooth = False

                            bmesh.update_edit_mesh(self.ContextMesh, loop_triangles=True, destructive=True)  

            return {"RUNNING_MODAL"}

        if (event.type == "RIGHTMOUSE") and (event.ctrl == True):
            if (context.edit_object is not None) and (self.ContextBmesh is not None):
                for selected_edge in [mesh_edge.index for mesh_edge in self.ContextBmesh.edges if (mesh_edge.select == True)]:
                    if ("bevel_weight_edge" in edge_mark_as):
                        self.ContextBmesh.edges[selected_edge][self.bevel_mark_layer] = 0.0
                    if ("crease_edge" in edge_mark_as):
                        self.ContextBmesh.edges[selected_edge][self.crease_mark_layer] = 0.0
                    if ("seam_edge" in edge_mark_as):
                        self.ContextBmesh.edges[selected_edge].seam = False
                    if ("sharp_edge" in edge_mark_as):
                        self.ContextBmesh.edges[selected_edge].smooth = True

                    bmesh.update_edit_mesh(self.ContextMesh, loop_triangles=True, destructive=True)  

            return {"RUNNING_MODAL"}

        return {"PASS_THROUGH"}

    

    def invoke(self, context, event):
        print("invoke called")
        self.bIsRunning = True

        position_x = 100
        position_y = 100

        if (context.scene.alx_draw_handler_unlocked_modeling is None):
            bpy.types.Scene.alx_draw_handler_unlocked_modeling = bpy.types.SpaceView3D.draw_handler_add(draw_unlocked_modeling_ui, (position_x, position_y, self.bIsRunning), "WINDOW", 'POST_PIXEL')
        else:
            print("From Invoke: alx_draw_handler_unlocked_modeling is not None")

        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}



class Alx_WT_WorkSpaceTool_UnlockedModeling(bpy.types.WorkSpaceTool):
    """"""

    bl_space_type = "VIEW_3D"
    bl_context_mode = "EDIT_MESH"
    bl_icon = "ops.gpencil.draw.poly"

    bl_idname = "alx.workspace_unlocked_modeling_tool"
    bl_label = "Alx Unlocked Modeling"

    bl_keymap = (
        ("alx.operator_unlocked_modeling_tool", {"type": "RIGHTMOUSE", "value": "PRESS"},
    {"properties": []}),
        )