import bpy
import bmesh

from .AlxGpuUI import draw_unlocked_modeling_ui

class Alx_Tool_UnlockedModeling_Properties(bpy.types.PropertyGroup):
    """"""
    leftclick_behaviour : bpy.props.EnumProperty(default="NONE", 
        items=[
            ("NONE", "Standard", "", 1),
            ("RIGHTCLICK_AUTO", "Auto Rightclick", "", 1<<1)
        ]) #type:ignore

    leftclick_selection_mode : bpy.props.EnumProperty(default="NONE", 
        items=[
            ("NONE", "Standard", "", 1),
            ("LOOP_SELECTION", "Loop", "", 1<<1)
        ]) #type:ignore

    leftclick_selection_state_mode : bpy.props.EnumProperty(default="NONE", 
        items=[
            ("NONE", "Single", "", 1),
            ("EXTEND", "Extend", "", 1<<1)
        ]) #type:ignore

    leftclick_retopology : bpy.props.EnumProperty(default="NONE", 
        items=[
            ("NONE", "Normal", "", 1),
            ("SURFACE_UNDER_POINTER", "On Sruface", "", 1<<1)
        ]) #type:ignore

    poly_delete_type : bpy.props.EnumProperty(default="NONE",
        items=[
            ("NONE", "None", "", 1),
            ("VERTS", "Vertex", "", 1<<1),
            ("EDGES", "Edge", "", 1<<2),
            ("FACES", "Face", "", 1<<3),
            ("FACES_ONLY", "Face Only", "", 1<<4)
        ]) #type:ignore

    edge_mark_type : bpy.props.EnumProperty(default={"NONE"}, options={"ENUM_FLAG"},
        items=[
            ("NONE", "None", "", 1),
            ("seam_edge", "Seam", "", 1<<1),
            ("sharp_edge", "Sharp", "", 1<<2),
            ("bevel_weight_edge", "Bevel", "", 1<<3),
            ("crease_edge", "Crease", "", 1<<4)
        ]) #type:ignore

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

        AlxLayout.label(text="Select:")
        leftclick_behaviour_mode_grid_flow = AlxLayout.grid_flow(columns=3, align=True)
        leftclick_behaviour_mode_grid_flow.prop(Properties, "leftclick_behaviour", expand=True)

        leftclick_selection_mode_grid_flow = AlxLayout.grid_flow(columns=3, align=True)
        leftclick_selection_mode_grid_flow.prop(Properties, "leftclick_selection_mode", expand=True)

        leftclick_selection_state_mode_grid_flow = AlxLayout.grid_flow(columns=3, align=True)
        leftclick_selection_state_mode_grid_flow.prop(Properties, "leftclick_selection_state_mode", expand=True)

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

    bIsRunning : bpy.props.BoolProperty(name="", default=False) #type:ignore
    ContextBmesh : bmesh.types.BMesh = None
    bmesh_selection : list = []
    average_bevel_weight : float = 0.00
    average_crease_weight : float = 0.00

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.mode == "EDIT_MESH")

    def CancelModal(self, context: bpy.types.Context):
        self.bIsRunning = False
        if (self.ContextBmesh is not None):
            self.ContextBmesh.free()

        self.bmesh_selection = []
        self.average_bevel_weight = 0.00
        self.average_crease_weight = 0.00
            
        try:
            bpy.types.SpaceView3D.draw_handler_remove(context.scene.alx_draw_handler_unlocked_modeling, "WINDOW")
            bpy.types.Scene.alx_draw_handler_unlocked_modeling = None

        except Exception as error:
            print(f"info-cancel: unlocked modeling ui {error}")

        context.area.tag_redraw()

    def Call_Special_Action(self, context: bpy.types.Context, poly_delete_type, edge_mark_as, pass_through: bool):
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

        return {"RUNNING_MODAL"} if (pass_through == False) else {"PASS_THROUGH"}
        
    def Call_Special_Alter(self, context: bpy.types.Context, poly_delete_type, edge_mark_as, pass_through: bool):
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

        return {"RUNNING_MODAL"} if (pass_through == False) else {"PASS_THROUGH"}


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

            self.bevel_mark_layer = self.ContextBmesh.edges.layers.float.get('bevel_weight_edge', None)
            if (self.bevel_mark_layer is None):
                self.bevel_mark_layer = self.ContextBmesh.edges.layers.float.new('bevel_weight_edge')

            self.crease_mark_layer = self.ContextBmesh.edges.layers.float.get('crease_edge', None)
            if (self.crease_mark_layer is None):
                self.crease_mark_layer = self.ContextBmesh.edges.layers.float.new('crease_edge')

            self.ContextBmesh.edges.ensure_lookup_table()



        if (event.type == "S"):
            bpy.ops.wm.call_panel(name=Alx_PT_Panel_UnlockedModeling.bl_idname, keep_open=True)
            return {"RUNNING_MODAL"}
        



        # if (context.mode == "EDIT_MESH"):
        #     tool = bpy.context.workspace.tools.from_space_view3d_mode("EDIT_MESH", create=False)
        #     props = tool.operator_properties(tool.idname) if (tool.idname in ["builtin.select_box"]) and (hasattr(tool, "operator_properties")) else None
        #     if (props is not None):
        #         props.mode = 1


        leftclick_behaviour = context.scene.alx_tool_unlocked_modeling_properties.leftclick_behaviour
        leftclick_selection_mode = context.scene.alx_tool_unlocked_modeling_properties.leftclick_selection_mode
        leftclick_selection_state_mode = context.scene.alx_tool_unlocked_modeling_properties.leftclick_selection_state_mode

        edge_mark_as = [mark_type for mark_type in context.scene.alx_tool_unlocked_modeling_properties.edge_mark_type]
        poly_delete_type = context.scene.alx_tool_unlocked_modeling_properties.poly_delete_type

        bExtend = True if (leftclick_selection_state_mode == "EXTEND") else False

        if (event.type == "LEFTMOUSE") and (event.ctrl == False) and (leftclick_behaviour == "NONE"):
            if (context.mode == "EDIT_MESH"):
                override_window = context.window
                override_screen = override_window.screen
                override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
                override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']
                
                
                
                with context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):
                    if (leftclick_selection_mode == "NONE"):
                        return {"PASS_THROUGH"}

                    elif (leftclick_selection_mode == "LOOP_SELECTION"):
                        bpy.ops.mesh.loop_select("INVOKE_DEFAULT", extend=bExtend, deselect=False, toggle=False, ring=False)
            return {"RUNNING_MODAL"}

        if (event.type == "LEFTMOUSE") and (event.ctrl == True) and (leftclick_behaviour == "NONE"):
            if (context.mode == "EDIT_MESH"):
                override_window = context.window
                override_screen = override_window.screen
                override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
                override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']

                with context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):
                    if (leftclick_selection_mode == "NONE"):
                        return {"PASS_THROUGH"}

                    elif (leftclick_selection_mode == "LOOP_SELECTION"):
                        bpy.ops.mesh.loop_select("INVOKE_DEFAULT", extend=False, deselect=True, toggle=False, ring=False)
            return {"RUNNING_MODAL"}



        if (event.type == "RIGHTMOUSE") and (event.ctrl == False):
            return self.Call_Special_Action(context, poly_delete_type, edge_mark_as, pass_through=False)

        if ((event.type == "RIGHTMOUSE") and (event.ctrl == True)):
            return self.Call_Special_Alter(context, poly_delete_type, edge_mark_as, pass_through=False)

         

        self.bmesh_selection = [bmesh_edge.index for bmesh_edge in self.ContextBmesh.edges if (bmesh_edge.select == True)]

        weight_values = [self.ContextBmesh.edges[selected_edge][self.bevel_mark_layer] for selected_edge in self.bmesh_selection]
        self.average_bevel_weight = round(sum(weight_values)/float(len(weight_values)), 2) if (len(weight_values) > 0) else 0.00

        crease_values = [self.ContextBmesh.edges[selected_edge][self.crease_mark_layer] for selected_edge in self.bmesh_selection]
        self.average_crease_weight = round(sum(crease_values)/float(len(crease_values)), 2) if (len(crease_values) > 0) else 0.00

        return {"PASS_THROUGH"}


    def invoke(self, context, event):
        print("invoke called")
        self.bIsRunning = True

        position_x = 100
        position_y = 100



        if (context.scene.alx_draw_handler_unlocked_modeling is None):
            bpy.types.Scene.alx_draw_handler_unlocked_modeling = bpy.types.SpaceView3D.draw_handler_add(draw_unlocked_modeling_ui, (position_x, position_y, self), "WINDOW", 'POST_PIXEL')
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
        ("alx.operator_unlocked_modeling_tool", {"type": "MIDDLEMOUSE", "value": "PRESS"},
    {"properties": []}),
        )