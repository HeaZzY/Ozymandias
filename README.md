# Ozymandias project

This project consists of a reverse shell implementation, including a client and server for remote control and file transfer capabilities. The client connects to the server, allowing encrypted communication, file transfers, keylogging, and several other remote administration functionalities.

## Disclaimer

This project is for educational purposes only. Misuse of this software can lead to legal consequences. Use responsibly and only on systems you have explicit permission to access.


## Features

Encrypted communication using a simple XOR-based method
Remote command execution
File upload and download capabilities
Keylogging
Persistence techniques
Stealing Google Chrome passwords
Setup
Prerequisites
Python 3.x
pip for installing dependencies
Installation
Clone the repository or download the project files.

### Install the required dependencies:

`pip install pycryptodome pypiwin32` <br/><br/>
`pip install keyboard` <br/><br/>
`pip install pypiwin32` <br/><br/>

## Usage
Server
The server listens for incoming connections from the client and allows remote command execution and file transfers.

### Running the Server
Open a terminal or command prompt on your machine.
Run the server script:
`python3 OzymandiasClient.py`<br/><br/>
![image](https://github.com/HeaZzY/Ozymandias/assets/80423488/8e8a6127-4136-4dc8-b743-1d2ddc37961d)

### Running the Reverse Shell


Start the Reverse Shell Client:
`python3 OzymandiasClient.py`

## Change the IP on the reverse shell:<br/><br/>
![image](https://github.com/HeaZzY/Ozymandias/assets/80423488/7edfe3af-e0c7-43fa-ac80-928f68a14a75)


## (Optionnal) Compile the reverse to exe

`pyinstaller --onefile --noconsole OzymandiasClient.py`<br/><br/>
Now the target have to execute it<br/>

## #Excute it with python:
`python3 OzymandiasReverse.py`

The server will establish a connection with the client, enabling remote command execution, file transfers, and other administrative tasks.<br/><br/>
![image](https://github.com/HeaZzY/Ozymandias/assets/80423488/87ec58db-5681-43de-a375-ccf5c3182c38)

## Enhancing Stealth with Encrypted Communication:

### Hiding Network Activity:

Encrypting communications between the client and server makes it more difficult for intrusion detection systems (IDS) or traditional network monitoring software to detect network activity. Encrypted data can appear as random or indecipherable data streams to unauthorized parties.

## Avoiding Signature-Based Detection:

Security network tools often detect typical commands and responses of a reverse shell based on signatures or traffic patterns. Encryption can make these patterns harder to identify, allowing the reverse shell to operate without triggering alerts based on specific signatures.

![image](https://github.com/HeaZzY/Ozymandias/assets/80423488/6a81b840-30f7-4185-bd70-9a040daae598)

