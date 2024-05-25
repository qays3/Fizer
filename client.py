import socket
import os
from colorama import init, Fore, Style

 
init()

def upload_file(client_socket, server_address, filename):
    client_socket.sendto(f"UPLOAD {filename}".encode('utf-8'), server_address)
    with open(filename, 'rb') as f:
        while (data := f.read(1024)):
            client_socket.sendto(data, server_address)
    client_socket.sendto(b'DONE', server_address)
    print(f"{Fore.BLUE}File {filename} uploaded successfully.{Style.RESET_ALL}")

def download_file(client_socket, server_address, filename):
    client_socket.sendto(f"DOWNLOAD {filename}".encode('utf-8'), server_address)
    with open(f"downloaded_{filename}", 'wb') as f:
        while True:
            data, _ = client_socket.recvfrom(1024)
            if data == b'DONE':
                break
            if data == b'FILE NOT FOUND':
                print(f"{Fore.RED}File {filename} not found on server.{Style.RESET_ALL}")
                return
            f.write(data)
    print(f"{Fore.GREEN}File {filename} downloaded successfully.{Style.RESET_ALL}")

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", 9999)
    client_socket.sendto(b'CONNECT', server_address)
    response, _ = client_socket.recvfrom(1024)
    if response == b'ACK':
        return client_socket, server_address
    else:
        print(f"{Fore.RED}Failed to connect to the server.{Style.RESET_ALL}")
        return None, None

if __name__ == "__main__":
    client_socket, server_address = connect_to_server()
    if client_socket:
        while True:
            command = input(f"{Fore.YELLOW}Enter command (UPLOAD <filename> / DOWNLOAD <filename> / EXIT): {Style.RESET_ALL}")
            cmd_parts = command.split(' ', 1)
            cmd = cmd_parts[0].upper()
            
            if cmd == "UPLOAD" and len(cmd_parts) == 2:
                filename = cmd_parts[1]
                if os.path.exists(filename):
                    upload_file(client_socket, server_address, filename)
                else:
                    print(f"{Fore.RED}File {filename} does not exist.{Style.RESET_ALL}")
            elif cmd == "DOWNLOAD" and len(cmd_parts) == 2:
                filename = cmd_parts[1]
                download_file(client_socket, server_address, filename)
            elif cmd == 'EXIT':
                print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid command.{Style.RESET_ALL}")
