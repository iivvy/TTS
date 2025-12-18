import subprocess
from pyngrok import ngrok
import time





# ----------------- First ngrok account -----------------
ngrok.set_auth_token("")  # your first account
port1 = 8501
subprocess.Popen(["streamlit", "run", "main.py", "--server.port", str(port1)])
url1 = ngrok.connect(port1)
print("Main app URL:", url1)

# ----------------- Second ngrok account -----------------

# Keep script alive
while True:
    time.sleep(60)
