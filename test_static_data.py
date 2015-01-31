import socket
import sys
import constants
import data
import wrapper

def run(user, password, *commands):
    HOST, PORT = "codebb.cloudapp.net", 17429

    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    result=""

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()

        while rline:
            result=(rline.strip())
            rline = sfile.readline()

    finally:
        sock.close()

    return result

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429

    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def main():
    cash = run(constants.USER_NAME, constants.PASSWORD, "MY_CASH")
    portfolio = data.Portfolio(cash.split(" ")[1])

    print portfolio.cash

    securities=wrapper.getMySecurities({})

    wrapper.bid(securities["GOOG"], 76.0, 3)

    print securities

    while True:
        inputCMD=raw_input();
        run(constants.USER_NAME, constants.PASSWORD, inputCMD)

main()