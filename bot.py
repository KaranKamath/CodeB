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

    maxBuyIndex = -3

    while True:
        portfolio._cash=wrapper.getCurrCash()

        import copy
        previousSecurities=copy.deepcopy(securities)
        securities=wrapper.getMySecurities(securities)

        wrapper.printStats(previousSecurities, securities)

        for x in securities.values():
            orders=wrapper.getMarketOrder(x)
            spread=utils.getSpread(orders)
            buyIndex = x._currentDivRatio/spread
            
            if(buyIndex > maxBuyIndex):
                maxBuyIndex=buyIndex
                toBuy=x
                toBuyOrders=orders

        owned=[x for x in securities if securities[x].numSharesOwned>0]

        if (toBuy.ticker not in owned):
            #print minSpreadOrder
            priceToBid=utils.getMinAsk(toBuyOrders['ASK'])*1.0001
            if portfolio.cash > portfolio.initialCash/2:
                wrapper.bid(toBuy, priceToBid, (int)(portfolio.cash/(4*priceToBid)))

        #print owned

        for x in owned:
            if securities[x].currentDivRatio < 0.0001:
                priceToAsk=utils.getMaxBid(wrapper.getMarketOrder(securities[x])['BID'])*0.95
                print "Asking for " + x + " at price" + str(priceToAsk)
                wrapper.ask(securities[x], priceToAsk, securities[x].numSharesOwned)



main()