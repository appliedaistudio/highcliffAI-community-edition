__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to run the ai as a remote server in its own thread
import threading
import time

import rpyc
from rpyc.utils.server import ThreadedServer


class ExperimentalFaultTolerantServer(rpyc.Service):
    _client_list = []
    _server_started = False

    def on_connect(self, conn):
        print("client connected")

        # start the server after the first connection
        if not self._server_started:
            thread = threading.Thread(target=self.loop_server)
            thread.start()

        self._server_started = True

    def loop_server(self):
        while True:
            self.exposed_run_server()
            time.sleep(3)

    def on_disconnect(self, conn):
        print("client disconnected")

    def exposed_run_server(self):
        print("running fault tolerant processing")
        for client in self._client_list:
            try:
                print(f"executing client {client}")
                client.exec()
            except:
                # when we lose a client connection,
                # the protocol automatically cleans and clears the reference to the client
                pass

    def exposed_register_client(self, client):
        print(f"registered client {client}")
        self._client_list.append(client)

        while True:
            time.sleep(3)


def start_fault_tolerant_server():
    thread = ThreadedServer(ExperimentalFaultTolerantServer(),
                            port=12345,
                            protocol_config={"allow_all_attrs": True,
                                             "allow_public_attrs": True,
                                             "allow_setattr": True,
                                             "instantiate_custom_exceptions": True,
                                             "import_custom_exceptions": True,
                                             "allow_pickle": True
                                             }
                            )
    thread.start()


if __name__ == "__main__":
    print("starting server")
    start_fault_tolerant_server()
