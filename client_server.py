import socket
import threading
from pymongo import MongoClient

def db_connection():
    try:
        client = MongoClient("mongodb+srv://cmurray901:Mccade1102@327database.wv31l.mongodb.net/?retryWrites=true&w=majority&appName=327Database")
        db = client[test]
        return db
    except Exception as e
        print(f"error connecting to database: {e}")
        return None

def start_server():
    host = input("Enter server IP address (e.g., '0.0.0.0' for all interfaces): ")
    port = int(input("Enter server port: "))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is up and running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connected to client {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if data.lower() == "exit":
                print("Client disconnected.")
                break
            print(f"Received from client: {data}")
            client_socket.sendall(f"Server's reply: {data}".encode())
    finally:
        client_socket.close()

def start_client():
    server_ip = input("Please enter the server's IP address: ")
    server_port = int(input("Please enter the server's port: "))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    print("Connected to the server.")

    try:
        while True:
            message = input("Enter message to send to the server (or type 'exit' to quit): ")
            if message.lower() == "exit":
                print("Exiting...")
                break
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server's reply: {response}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    mode = input("Do you want to run as a (s)erver or (c)lient? ").strip().lower()
    if mode == "s":
        start_server()
    elif mode == "c":
        start_client()
    else:
        print("Invalid input. Please choose 's' for server or 'c' for client.")