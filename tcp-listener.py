from pycomm.connection import Connection

conn = Connection("0.0.0.0", 7983)

server = conn.get_server(10)

for client in server:
    while True :
        try:
            server_input=input(">>")
        except EOFError : 
            print("EOF Error")
            break
        client.send(server_input)
    client.close()
