ECHO OFF
ECHO Hello World

:: Set Java variable
SET ai_server="localhost"
SET ai_server_port="12345"

C:\GitHub\appliedAIstudio\Highcliff\venv\Scripts\python.exe C:\GitHub\appliedAIstudio\Highcliff\digital_twin\aging_in_place\aging_in_place_ai_server_launch.py
PAUSE