import subprocess
from pyngrok import ngrok
import time



ngrok.set_auth_token("")  # your second account
port2 = 8502
subprocess.Popen(["streamlit", "run", "voice_clone.py", "--server.port", str(port2)])
url2 = ngrok.connect(port2)
print("Second app URL:", url2)


while True:
    time.sleep(60)