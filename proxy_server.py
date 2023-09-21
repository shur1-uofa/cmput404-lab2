import socket
from threading import Thread 

BUFFER_SIZE = 4096
N_BACKLOG_CONNECTIONS = 2 

serverHost = "www.google.com"
serverPort = 80   # HTTP 

proxyHost = "localhost"
proxyPort = 8080 


def handle_connection(conn, addr):
    with conn: 
        # Receive data from proxy client 
        full_data = b""
        while True:
            data = conn.recv( BUFFER_SIZE )
            if not data:
                break
            full_data += data
        print("Read data from connection")

        resp = forward_to_server( full_data )

        # Send data to proxy client 
        conn.sendall( resp )
        print("Sent data to connection")



def forward_to_server(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        # Connect to server 
        serverSocket.connect( ( serverHost, serverPort) )
        print("Connected to server")
        # Relay proxy client's data to server 
        serverSocket.sendall( data )
        print("Sent data to server")
        # Relay response to proxy client 
        resp = serverSocket.recv( BUFFER_SIZE )
        print("Received response from server")
    return resp 


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxySocket: 
        proxySocket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxySocket.bind((proxyHost, proxyPort))

        proxySocket.listen( N_BACKLOG_CONNECTIONS )
        print(f'Proxy server is listening')

        while True: 
            conn, addr = proxySocket.accept() 
            print(f'Proxy server accepted connection ${addr}')
            thread = Thread(target=handle_connection, args=[conn, addr])
            thread.run() 
        



                

        





