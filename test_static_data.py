import socket
import sys
import constants
import data
import wrapper
import utils

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

    minSpread=portfolio.cash;
    minSpreadShare=securities.values()[0]

    while True:
        securities=wrapper.getMySecurities(securities)
        minSpreadOrder=[]
        for x in securities.values():
            orders=wrapper.getMarketOrder(x)
            spread=utils.getSpread(orders)
            if(spread < minSpread):
                minSpread=spread
                minSpreadShare=x
                minSpreadOrder=orders

        owned=[x for x in securities if securities[x].numSharesOwned>0]
        print owned

        if (minSpreadShare not in owned):
            priceToBid=utils.getMinAsk(minSpreadOrder['ASK'])*1.0001
            if portfolio.cash > portfolio.initialCash/2:
                wrapper.bid(minSpreadShare, priceToBid, (int)(portfolio.cash/(4*priceToBid)))

        #print owned

main()