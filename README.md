# Reverse Shell Project

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

`pip install pycryptodome pypiwin32` <br/>
`pip install keyboard` <br/>
`pip install pypiwin32` <br/>

## Usage
Server
The server listens for incoming connections from the client and allows remote command execution and file transfers.

### Running the Server
Open a terminal or command prompt on your machine.
Run the server script:
`python3 server.py`
