import bpy

def UIPreset_ModifierSettings(layout:bpy.types.UILayout = None, modifier:bpy.types.Modifier = None, context:bpy.types.Context = None, object:bpy.types.Object = None):
    if (layout is not None) and (modifier is not None):
        indented_layout = layout.row()
        indented_layout.separator(factor=2.0)

        mod_layout = indented_layout.column()
        match modifier.type:
            case "DATA_TRANSFER":
                modifier : bpy.types.DataTransferModifier = modifier

                row = mod_layout.row()
                row.prop(modifier, "object", text="")
                row = mod_layout.row(align=True).split(factor=0.75)
                data_row = row.row()
                data_row.label(text="Type:")
                data_row.prop(modifier, "use_vert_data", text="vertex")
                data_row.prop(modifier, "use_edge_data", text="edge")
                data_row.prop(modifier, "use_poly_data", text="face")
                data_row.prop(modifier, "use_loop_data", text="loop")

                if (modifier.use_vert_data == True):
                    column = mod_layout.column()
                    column.row().prop(modifier, "data_types_verts")
                    column.prop(modifier, "vert_mapping", text="Mapping")
                    
                    row = column.row().split(factor=0.5)

                    if ("VGROUP_WEIGHTS" in modifier.data_types_verts):
                        column = row.column()
                        column.label(text="VGroup Source:")
                        column.prop(modifier, "layers_vgroup_select_src", text="")
                        column.label(text="VGroup Mapping:")
                        column.prop(modifier, "layers_vgroup_select_dst", text="")
                    if ("COLOR_VERTEX" in modifier.data_types_verts):
                        column = row.column()
                        column.label(text="Color Source:")
                        column.prop(modifier, "layers_vcol_vert_select_src", text="")
                        column.label(text="Color Mapping:")
                        column.prop(modifier, "layers_vcol_vert_select_dst", text="")

            case "SMOOTH":
                pass


            case "SHRINKWRAP":
                modifier : bpy.types.ShrinkwrapModifier = modifier
                row = layout.row().split(factor=0.5, align=True)
                row.prop(modifier, "target", text="")

                row = layout.row().split(factor=0.5, align=True)
                row.prop(modifier, "wrap_method", text="")
                row.prop(modifier, "wrap_mode", text="")

                row = layout.row()
                row.prop(modifier, "use_negative_direction")
                row.prop(modifier, "use_positive_direction")

        # if (modifier.type == "DATA_TRANSFER"):
        #     row = layout.row()  
        #     row.prop(modifier, "object", text="")
        #     split = row.row(align=True)
        #     split.prop(modifier, "use_object_transform", text="", toggle=True, icon="OBJECT_ORIGIN")
        #     

        #     row = layout.row()
        #     row.prop(modifier, "use_vert_data", text="")
            

        #     row = layout.row()
        #     row.prop(modifier, "use_edge_data", text="")
        #     row.prop(modifier, "data_types_edges")

        #     row = layout.row()
            
        #     row.prop(modifier, "data_types_loops")
            
        #     row = layout.row()
            
        #     row.prop(modifier, "data_types_polys")

        if (modifier.type == "MIRROR"):
            row = layout.column()

            row.prop(modifier, "mirror_object", text="object")
            row.prop(modifier, "use_clip", text="clip")
            row.prop(modifier, "use_mirror_merge", text="merge")
            row.prop(modifier, "merge_threshold", text="")
            

        if (modifier.type == "SUBSURF"):
            layout.row().prop(modifier, "show_only_control_edges", text="optimal")

        if (modifier.type == "ARMATURE"):
            layout.row().prop(modifier, "object", text="")
            layout.row().prop(modifier, "use_deform_preserve_volume", text="preserve volume")

        if (modifier.type == "BEVEL"):
            row = layout.row().split(factor=0.33, align=True)

            row.prop(modifier, "offset_type", text="")
            row.prop(modifier, "width", text="width")
            row.prop(modifier, "segments", text="segments")
            layout.row().prop(modifier, "limit_method", text="")

            layout.row().prop(modifier, "miter_outer", text="miter outer")
            layout.row().prop(modifier, "harden_normals", text="harden")

        if (modifier.type == "BOOLEAN"):
            row = layout.row()
            row.prop(modifier, "object", text="")
            row.prop(modifier, "operation", expand=True)

        if (modifier.type == "TRIANGULATE"):
            layout.row().prop(modifier, "keep_custom_normals", text="keep normals")

        if (modifier.type == "SOLIDIFY"):
            row = layout.row().split(factor=0.5, align=True)
            row.prop(modifier, "thickness")
            row.prop(modifier, "offset")








        if (modifier.type == "DISPLACE"):
            row = layout.row().split(factor=0.034)
            row.separator()

            options_layout = row.box()
            row = options_layout.row()
            row.prop(modifier, "strength")
            row.prop(modifier, "mid_level")