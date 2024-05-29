import bpy
import bmesh
from mathutils import bvhtree

class Alx_PT_Panel_ReProjectVertex(bpy.types.Panel):
    """"""

    bl_label = "Alx Mesh Reprojection"
    bl_idname = "ALX_PT_panel_reproject_vertex"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Alx3D"

    bl_order = 0

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True
    
    def draw(self, context: bpy.types.Context):
        properties = context.window_manager.alx_session_properties

        self.layout.row().prop(properties, "vertex_reproject_target_object", text="Target")
        self.layout.row().operator(Alx_OT_Operator_ReProjectVertex.bl_idname, text="re-projection")

class Alx_OT_Operator_ReProjectVertex(bpy.types.Operator):
    """"""

    bl_label = ""
    bl_idname = "alx.operator_reproject_vertex"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}


    retopo_mesh : bpy.types.Mesh = None
    retopo_bmesh : bmesh.types.BMesh = None



    reproject_target_object : bpy.types.Object = None

    target_bvh_tree : bvhtree.BVHTree = None

    @classmethod
    def poll(self, context: bpy.types.Context):
        return (context.area is not None) and (context.area.type == "VIEW_3D") and (context.object is not None) and (context.object.type == "MESH")


    def modal(self, context: bpy.types.Context, event: bpy.types.Event):
        if (event.type == "ESC"):
            return {"CANCELLED"}
        elif (context.area is not None) and (context.area.type != "VIEW_3D"):
            return {"CANCELLED"}

        self.retopo_mesh = context.object.data
        tree_source = context.window_manager.alx_session_properties.vertex_reproject_target_object

    
        self.retopo_bmesh = bmesh.new()
        if (context.mode in ["OBJECT", "SCULPT"]):
            self.retopo_bmesh.from_mesh(self.retopo_mesh)
        if (context.mode in ["EDIT"]):
            self.retopo_bmesh = bmesh.from_edit_mesh(self.retopo_mesh)

        if (self.retopo_bmesh is None) or (self.retopo_bmesh.is_valid == False):
            self.retopo_bmesh.verts.ensure_lookup_table()
            self.retopo_bmesh.edges.ensure_lookup_table()
            self.retopo_bmesh.faces.ensure_lookup_table()


        if (self.target_bvh_tree is None):
            self.target_bvh_tree = bvhtree.BVHTree.FromObject(tree_source, context.evaluated_depsgraph_get())

        if (self.target_bvh_tree is not None):
            b_has_changed = False
            if (self.retopo_bmesh is not None) or (self.retopo_bmesh.is_valid == True):
                for vert in self.retopo_bmesh.verts:
                    hit_location, hit_normal, hit_index, hit_distance = self.target_bvh_tree.find_nearest(vert.co)
                    
                    if (hit_location is not None) and (hit_distance != 0):
                        vert.co = (hit_location.x, hit_location.y, hit_location.z)
                        b_has_changed = True
        
            if (context.mode in ["OBJECT", "SCULPT"]):
                self.retopo_bmesh.to_mesh(self.retopo_mesh)
            if (context.mode == "EDIT"):
                bmesh.update_edit_mesh(self.retopo_mesh)
            else:
                self.report({"WARNING"}, "no bmesh")
        else:
            self.report({"WARNING"}, "target missing")

        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
    

# def AlxHandler_ReprojectMesh(invoke_context: bpy.types.Context):
#     override_window = invoke_context.window
#     override_screen = override_window.screen
#     override_area = [area for area in override_screen.areas if area.type == "VIEW_3D"]
#     override_region = [region for region in override_area[0].regions if region.type == 'WINDOW']

#     with invoke_context.temp_override(window=override_window, area=override_area[0], region=override_region[0]):
