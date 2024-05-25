import socket
import threading
import os
from colorama import init, Fore, Style
from datetime import datetime

 
init()

def log_action(action, client_address, filename=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip, port = client_address
    if action == 'exit':
        log_message = f"[{timestamp}] {ip}:{port} has exited"
    elif action == 'shutdown':
        log_message = f"[{timestamp}] Server shutdown"
    else:
        log_message = f"[{timestamp}] {ip}:{port} has {action} {filename}"
    print(log_message)
    with open("server_log.txt", "a") as log_file:
        log_file.write(log_message + "\n")

def handle_upload(client_socket, client_address, filename):
    upload_filename = "upload_" + filename
    with open(upload_filename, 'wb') as f:
        while True:
            data, _ = client_socket.recvfrom(1024)
            if data == b'DONE':
                break
            f.write(data)
    log_action("uploaded", client_address, filename)

def handle_download(client_socket, client_address, filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            while (data := f.read(1024)):
                client_socket.sendto(data, client_address)
        client_socket.sendto(b'DONE', client_address)
        log_action("downloaded", client_address, filename)
    else:
        client_socket.sendto(b'FILE NOT FOUND', client_address)

def handle_client(client_socket, client_address):
    while running:
        try:
            data, _ = client_socket.recvfrom(1024)
            if data:
                command_parts = data.decode('utf-8').split(' ', 1)
                if len(command_parts) == 2:
                    command, filename = command_parts
                    if command == 'UPLOAD':
                        log_action("started upload", client_address, filename)
                        handle_upload(client_socket, client_address, filename)
                    elif command == 'DOWNLOAD':
                        handle_download(client_socket, client_address, filename)
                else:
                    print(f"Received unexpected message: {data}")
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break

def start_server():
    global server_socket, running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 9999))
    print(f"{Fore.YELLOW}Server is listening on port 9999...{Style.RESET_ALL}")

    while running:
        try:
            server_socket.settimeout(1.0)
            message, client_address = server_socket.recvfrom(1024)
            if message:
                if message.decode('utf-8') == 'CONNECT':
                    server_socket.sendto(b'ACK', client_address)
                    thread = threading.Thread(target=handle_client, args=(server_socket, client_address))
                    thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Server error: {e}")
            break

def shutdown_server():
    global running
    print(f"{Fore.RED}Enter EXIT if you want to shut down the server.{Style.RESET_ALL}")
    while running:
        command = input()
        if command.strip().upper() == 'EXIT':
            running = False
            print(f"{Fore.RED}Shutting down the server...{Style.RESET_ALL}")
            log_action("shutdown", ('localhost', 9999))
            server_socket.close()
            break

if __name__ == "__main__":
    running = True
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    shutdown_thread = threading.Thread(target=shutdown_server)
    shutdown_thread.start()

    server_thread.join()
    shutdown_thread.join()
    print("Server has been shut down.")
