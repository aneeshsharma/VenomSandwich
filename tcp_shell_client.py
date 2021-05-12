from pycomm.connection import Connection
import time
import subprocess

while True:
    try:
        conn = Connection("localhost", 7983)
        conn.connect()
        break
    except Exception as e:
        print(e)
    time.sleep(10)

while True:
    command = conn.recv()
    if command == "EXIT":
        break
    result = "No result"
    try:
        result = subprocess.check_output(command.split()).decode('utf-8')
    except Exception as err:
        print("Error running command")
        print(err)
        result = str(err)

    conn.send(result)

