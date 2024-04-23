import socket
import threading


msg_lst = []

connections = []

PORT = 7070

FORMAT = "utf_8"

HEADER = 64

SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

server.bind((SERVER , PORT))

     
s = ''


def handle_client(connection , address , id):
    print(f"NEW CONNECTION {address}")
    
    while True:
        msg = connection.recv(HEADER).decode(FORMAT)
        if msg:
            msg = int(msg)
            msg = connection.recv(msg).decode(FORMAT)
            if msg == "disconnect":
                break
            
            msg_lst.append([connection , msg])
            
            for  client in connections:
                if client != connection:
                    client.send(msg.encode(FORMAT))
            
    connection.close()
    print(f"[CONNECTION CLOSED] connection with the id of {id} was disconnected ")
    
count = 1

def start():
    
    global count
    
    print("[SERVER IS RUNNING] server is starting... ")
    server.listen()
    while True:   
        conection , address = server.accept()
        connections.append(conection)
        
        thread = threading.Thread(target=handle_client , args=(conection , address , count))
        thread.start()
        
        # thread_msg = threading.Thread(target=sendMESSAGE , args=(conection))
        # thread_msg.start()
        
        
        
        count = threading.active_count() - 1

        
        print(f"ACTiVE CONNECTIONS =====> {threading.active_count() - 1} \n")
start()

