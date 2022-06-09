__author__ = "Jerry Overton"
__copyright__ = "Copyright (C) 2022 appliedAIstudio LLC"
__version__ = "0.0.1"


# needed to connect to the remote server and run it periodically
import rpyc
import time


def start_monitor():

    print("starting fault tolerant monitor")

    connection = _connect()

    while True:
        print("processor run")
        try:
            connection.root.run_server()
        except:
            del connection
            connection = _connect()
            connection.root.run_server()

        time.sleep(3)


def _connect():
    # create a connection
    connection = rpyc.connect("localhost",
                              12345,
                              config={"allow_all_attrs": True,
                                      "allow_public_attrs": True,
                                      "allow_setattr": True,
                                      "instantiate_custom_exceptions": True,
                                      "import_custom_exceptions": True
                                      })
    print("connected to the experimental processing server")
    return connection


if __name__ == "__main__":
    start_monitor()
