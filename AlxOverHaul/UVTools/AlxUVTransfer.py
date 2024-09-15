import copy

import bpy
import bmesh
from mathutils import  kdtree

class Alx_OT_UVTools_uv_map_transfer(bpy.types.Operator):
    """"""

    bl_label = "UVTools - UV Map Transfer"
    bl_idname = "alx.operator_uvtools_uv_map_transfer"

    b_use_modifier_stack : bool = False


    def DYNAMIC_source_uv_layers(self, context: bpy.types.Context):
        source_object : bpy.types.Object = context.window_manager.alx_session_properties.operator_uvtools_uv_map_transfer__source_object
        unique_uvlayers_set = {("NONE", "none", "")}

        if ( source_object is not None ) and ( source_object.type == "MESH" ) and ( source_object.data is not None ) and ( len( source_object.data.uv_layers ) != 0 ):
            _retriever = [ unique_uvlayers_set.add( (layers.name, layers.name, "") ) for layers in source_object.data.uv_layers ]
            del _retriever

        return unique_uvlayers_set
    source_uv_layer : bpy.props.EnumProperty(items=DYNAMIC_source_uv_layers) #type:ignore

    def DYNAMIC_target_uv_layers(self, context: bpy.types.Context):
        target_object : bpy.types.Object = context.window_manager.alx_session_properties.operator_uvtools_uv_map_transfer__target_object
        unique_uvlayers_set = {("NONE", "none", "")}

        if ( target_object is not None ) and ( target_object.type == "MESH" ) and ( target_object.data is not None ) and ( len( target_object.data.uv_layers ) != 0 ):
            _retriever = [ unique_uvlayers_set.add( (layers.name, layers.name, "") ) for layers in target_object.data.uv_layers ]
            del _retriever

        return unique_uvlayers_set
    target_uv_layer : bpy.props.EnumProperty(items=DYNAMIC_target_uv_layers) #type:ignore


    def execute(self, context: bpy.types.Context):
        source_object : bpy.types.Object = context.window_manager.alx_session_properties.operator_uvtools_uv_map_transfer__source_object
        target_object : bpy.types.Object = context.window_manager.alx_session_properties.operator_uvtools_uv_map_transfer__target_object


        if (source_object is not None) and (source_object.type == "MESH") and (source_object.data is not None) and (target_object is not None) and (target_object.type == "MESH") and (target_object.data is not None):
            source_bmesh = bmesh.new()
            target_bmesh = bmesh.new()

            if ( self.b_use_modifier_stack == True ):
                source_bmesh.from_object(source_object, context.evaluated_depsgraph_get, True, True)
                target_bmesh.from_object(target_object, context.evaluated_depsgraph_get, True, True)
            else:
                source_bmesh.from_mesh(source_object.data, face_normals=True, vertex_normals=True, use_shape_key=False, shape_key_index=0)
                target_bmesh.from_mesh(target_object.data, face_normals=True, vertex_normals=True, use_shape_key=False, shape_key_index=0)


            target_verts = {vert.index : vert for vert in target_bmesh.verts}

            target_kdtree = kdtree.KDTree(len(target_verts))
            for index, vert in enumerate(target_verts.values()):
                target_kdtree.insert(vert.co, index)
            target_kdtree.balance()


            source_uv_layer = source_bmesh.loops.layers.uv.new(self.source_uv_layer) if source_bmesh.loops.layers.uv.get(self.source_uv_layer) is None else source_bmesh.loops.layers.uv.get(self.source_uv_layer)
            target_uv_layer = target_bmesh.loops.layers.uv.new(self.target_uv_layer) if target_bmesh.loops.layers.uv.get(self.target_uv_layer) is None else target_bmesh.loops.layers.uv.get(self.target_uv_layer)

            if (source_uv_layer is not None) and (target_uv_layer is not None):
                pass



            target_bmesh.to_mesh(target_object.data)

        return {"FINISHED"}
    
    def draw(self, context: bpy.types.Context):
        layout = self.layout

        _wm_props = context.window_manager.alx_session_properties

        layout.prop(_wm_props, "operator_uvtools_uv_map_transfer__source_object")
        layout.prop(_wm_props, "operator_uvtools_uv_map_transfer__target_object")
        layout.prop(self, "source_uv_layer")
        layout.prop(self, "target_uv_layer")
        


    def invoke(self, context: bpy.types.Context, event: bpy.types.Event):
        return context.window_manager.invoke_props_dialog(self, width=300)