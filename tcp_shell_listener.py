from pycomm.connection import Connection

conn = Connection("0.0.0.0", 7983)

server = conn.get_server(10)

for client in server:
    while True :
        try:
            server_input=input(">>> ")
        except EOFError : 
            print("Connection closed")
            client.send("EXIT")
            break
        client.send(server_input)
        print(client.recv())
    client.close()
    print("Waiting for connection...")
