import bpy

from . MeshTools import AlxVertexGroupTools, AlxShapekeyTools
from . ArmatureTools import AlxPoseTools, AlxRiggingTools

class ALX_PT_UI_Addon_ToolShelf(bpy.types.Panel):
    """"""

    bl_label = "Alx Toolshelf"
    bl_idname = "ALX_PT_panel_ui_addon_tool_shelf"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Alx3D"
    bl_order = 0
    

    def draw(self, context: bpy.types.Context):
        mainlayout = self.layout

        mesh_tools_panel : bpy.types.UILayout
        mesh_tools_header, mesh_tools_panel = mainlayout.panel("ALX_PT_compact_panel_mesh_tools", default_closed=True)
        mesh_tools_header.label(text="Mesh Tools:")
        if ( mesh_tools_panel is not None ):
            row = mesh_tools_panel.row()
            row.separator()
            layout = row.column()

            layout.label(text="Vertex Groups:")
            layout.operator(AlxVertexGroupTools.Alx_OT_Mesh_VertexGroup_Clean.bl_idname, text="clean mesh vertex group")
            layout.label(text="ShapeKeys:")
            layout.operator(AlxShapekeyTools.Alx_OT_Shapekey_TransferShapekeysToTarget.bl_idname, text="transfer shapekeys by vertex position")


        armature_tools_panel : bpy.types.UILayout
        armature_tools_header, armature_tools_panel = mainlayout.panel("ALX_PT_compact_panel_armature_tools", default_closed=True)
        armature_tools_header.label(text="Armature Tools:")
        if ( armature_tools_panel is not None ):
            row = armature_tools_panel.row()
            row.separator()
            layout = row.column()

            layout.label(text="Pose:")
            layout.operator(AlxPoseTools.Alx_OT_Armature_Pose_ToggleConstraints.bl_idname, text="toggle armature pose constraints")
            layout.operator(AlxPoseTools.Alx_OT_Armature_MatchIKByMirroredName.bl_idname, text="symmetrize IK chains across armature")


        vtuber_panel : bpy.types.UILayout
        vtuber_header, vtuber_panel = mainlayout.panel("ALX_PT_compact_panel_vtuber_tools", default_closed=True)
        vtuber_header.label(text="VTuber Tools:")
        if ( vtuber_panel is not None ):
            row = vtuber_panel.row()
            row.separator()
            layout = row.column()

            layout.label(text="ShapeKeys:")
            layout.operator(AlxShapekeyTools.Alx_OT_Shapekey_AddEmptyShapeKeys.bl_idname, text="add empty VRM 0/ARKit shapekeys")
            
            layout.label(text="rigging:")
            layout.operator(AlxRiggingTools.Alx_OT_Armature_BoneChainOnSelection.bl_idname)