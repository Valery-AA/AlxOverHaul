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

                context.view_layer.objects.active = selected_object

                for modifier in modifiers:
                    backup_modifier = dict()
                    for attr in dir(modifier):
                        backup_modifier[attr] = getattr(modifier, attr)

                    modifier_index = selected_object.modifiers.find(modifier.name)
                    _mode = context.mode if (context.mode[0:4] != "EDIT") else "EDIT"
                    bpy.ops.object.mode_set(mode="OBJECT")
                    bpy.ops.object.modifier_apply(modifier=modifier.name)
                    bpy.ops.object.mode_set(mode=_mode)

                    new_modifier = selected_object.modifiers.new(name=backup_modifier["name"], type=backup_modifier["type"])

                    for mod_setting in dir(new_modifier):
                        try:
                            setattr(new_modifier, mod_setting, backup_modifier[mod_setting])
                        except:
                            pass

                    new_index = selected_object.modifiers.find(new_modifier.name)
                    try:
                        selected_object.modifiers.move(new_index, modifier_index)
                    except Exception as error:
                        print(error)

        except Exception as error:
            print(error)

        return {"FINISHED"}