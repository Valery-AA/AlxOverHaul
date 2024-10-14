from typing import Optional
from threading import Thread

from ..Utilities.AlxUtilities import developer_log_console, operator_log_error

from .pythonosc import dispatcher, osc_server


class Alx_VMC_RecieverServer():

    server_ip_target: str
    server_port_target: int

    server_runtime_thread: Thread

    def __init__(self):
        pass
        # self.server_ip_target = "127.0.0.1"
        # self.server_port_target = 39539

        # address = (TCP_IP, TCP_PORT)
        # server_dispatcher = dispatcher
        # server = osc_server.ThreadingOSCUDPServer(address, server_dispatcher)
        # server.serve_forever()

    def config(self, osc_ip: str = "127.0.0.1", osc_port: int = 39539):
        if (osc_port < 1025):
            developer_log_console(
                python_file_name=__file__,
                object_name=__name__,
                message="port number is within the priviledged ports range")
            return

        if (osc_port > 65535):
            developer_log_console(
                python_file_name=__file__,
                object_name=__name__,
                message="port number is exceeds 16 bit integer values (port number is outside range of possible ports)")
            return

        self.server_ip_target = osc_ip
        self.server_port_target = osc_port

    def threaded_server():
        pass

    def start(self, opt_external_thread: Optional[Thread] = None):
        if (opt_external_thread == None):
            self.server_runtime_thread = Thread(target=self.threaded_server)

    def stop():
        pass

        # import ctypes
        # import threading
        # import socket

        # import bpy

        # text = ""

        # def thread_update():
        #
        #     BUFFER_SIZE = 1024

        #     soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #     soc.bind((TCP_IP, TCP_PORT))
        #     soc.listen()

        #     connection, address = soc.accept()
        #     with connection:
        #         while True:
        #             data = connection.recv(BUFFER_SIZE)
        #             global text
        #             text += f"data, {data}"

        # class Alx_OT_TestDebugServerListener(bpy.types.Operator):
        #     """"""

        #     bl_label = ""
        #     bl_idname = "alx.operator_test_debug_server_listener"

        #     bl_options = {"REGISTER", "UNDO"}

        #     @classmethod
        #     def poll(self, context: bpy.types.Context):
        #         return True

        #     def execute(self, context: bpy.types.Context):
        #         print(ctypes.windll.shell32.IsUserAnAdmin())
        #         thread = threading.Thread(target=thread_update)
        #         thread.start()
        #         print("text: ", text)
        #         return {"FINISHED"}
