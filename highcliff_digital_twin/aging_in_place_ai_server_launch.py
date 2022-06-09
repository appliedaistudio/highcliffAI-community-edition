from ai_framework.ai_server import start_ai_server
from physarai import PhysarAI


def launch_ai_server() -> None:
    # start the ai server, this is blocking and should be the last command in this method
    start_ai_server(PhysarAI.instance(), "config/aging_in_place_ai_server_config.ini")


if __name__ == "__main__":
    launch_ai_server()
