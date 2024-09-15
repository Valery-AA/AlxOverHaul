import bpy

def operator_log_info(self : bpy.types.Operator, log_message : str):
    self.report({"INFO"}, log_message)

def operator_log_warning(self : bpy.types.Operator, log_message : str):
    self.report({"WARNING"}, log_message)

def operator_log_error(self : bpy.types.Operator, log_message : str):
    self.report({"ERROR"}, log_message)