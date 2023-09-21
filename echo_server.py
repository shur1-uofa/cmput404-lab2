# Taken from eClass

#!/usr/bin/env python3
import socket
import time 
from threading import Thread

#define address & buffer size
HOST = "127.0.0.1"  # localhost
PORT = 8080
BUFFER_SIZE = 1024

def handle_connection(conn, addr):
    print("Connected by", addr)
        
    #receive data, wait a bit, then send it back    
    full_data = conn.recv(BUFFER_SIZE)

    print("Data\n", full_data )

    time.sleep(0.5)
    conn.sendall(full_data)
    conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=[conn, addr])
            thread.run() 
            

if __name__ == "__main__":
    main()

