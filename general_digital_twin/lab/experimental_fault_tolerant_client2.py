__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"

# needed to connect to the remote server
import rpyc

# needed to keep the action alive in it's thread
import time
from threading import Thread


class Client:
    def __init__(self, name):
        self._name = name

    def exec(self):
        print(f"client class {self._name} executed")


def stay_alive():
    # keep the client alive in it's thread
    while True:
        time.sleep(5)


# create a connection
connection = rpyc.connect("localhost",
                          12345,
                          config={"allow_all_attrs": True,
                                  "allow_public_attrs": True,
                                  "allow_setattr": True,
                                  "instantiate_custom_exceptions": True,
                                  "import_custom_exceptions": True,
                                  "sync_request_timeout": None,
                                  "allow_pickle": True
                                  })

print("connected to the experimental fault tolerant server")

# register a client with the server
client = Client("experimental fault tolerance client")
connection.root.register_client(client)

# keep the action alive while still able to process incoming requests from the AI
thread = Thread(target=stay_alive)
thread.start()
