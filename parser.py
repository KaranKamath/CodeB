import constants
import socket
import sys


def runMod(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    output = []
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            output.append(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()
        
    return output


def getCurrCash():
    consoleOutput = runMod(constants.USER_NAME, constants.PASSWORD, "MY_CASH")
    consoleOutput = consoleOutput[0]
    consoleOutput = consoleOutput.split(" ")
    return float(consoleOutput[1])
    
print getCurrCash()