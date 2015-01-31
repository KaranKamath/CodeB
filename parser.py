import constants
import socket
import sys
import data


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
    
def clearBid(ticker):
    runMod(constants.USER_NAME, constants.PASSWORD, "CLEAR_BID" + ticker)

def clearAsk(ticker):
    runMod(constants.USER_NAME, constants.PASSWORD, "CLEAR_ASK" + ticker)
    
def getMySecurities(mySecurities):
    consoleOutput = runMod(constants.USER_NAME, constants.PASSWORD, "MY_SECURITIES")
    consoleOutput = consoleOutput.split(" ")
    lenInput = len(consoleOutput)
    numSecurities = (lenInput - 1)/3
    for i in range(numSecurities):
        

print getCurrCash()