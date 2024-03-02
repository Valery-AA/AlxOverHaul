import bpy



def AlxRetirive_ModifierList(TargetObejct, TargetType):
    mod_type_list = bpy.types.Modifier.bl_rna.properties['type'].enum_items

    if (TargetType in mod_type_list):
        return [modifier for modifier in TargetObejct.modifiers if (modifier.type == TargetType)]

    return None

class Alx_OT_Modifier_Shrinkwrap(bpy.types.Operator):
    """"""

    bl_label = "Shrinkwrap Tool"
    bl_idname = "alx.operator_modifier_shrinkwrap"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    @classmethod
    def poll(self, context: bpy.types.Context):
        return True
    
    def execute(self, context: bpy.types.Context):
        try:
            context.selectable_objects[0]

            for selected_object in context.selected_objects:
                modifiers = AlxRetirive_ModifierList(selected_object, "SHRINKWRAP")
                modifier = modifiers[0]
                modifier_index = selected_object.modifiers.find(modifier)

        except:
            pass
        
        AlxRetirive_ModifierList()
        return {"FINISHED"}