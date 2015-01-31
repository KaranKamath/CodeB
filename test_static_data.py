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

    #minSpread=portfolio.cash;
    #minSpreadShare=securities.values()[0]
    maxBuyIndex = -3655

    while True:

        portfolio._cash=wrapper.getCurrCash()

        print "Cash: " + str(portfolio.cash)

        import copy
        previousSecurities=copy.deepcopy(securities)
        securities=wrapper.getMySecurities(securities)

        #updatepfolio
        portfolio._securities=securities

        #portfolio.updateDividends()

        #for x in portfolio.securities.values():
        #    if x.numSharesOwned > 0:
        #        print x.ticker
        #        print "Num: " + str(x.numSharesOwned)
        #        print "Worth: " + str(x._netWorth)
        #        print "Ratio " + str(x.currentDivRatio)
        #       print "Div: " + str(x.dividend) + "\n"

        wrapper.printStats(previousSecurities, securities)

        for x in securities.values():
            orders=wrapper.getMarketOrder(x)
            spread=utils.getSpread(orders)
            x._buyIndex = -spread

        #for x in toBuySorted:
        #    print x.ticker + " " + str(x.buyIndex)

        owned=[x for x in securities if securities[x].numSharesOwned>0]

        toBuySorted = sorted(securities.values(), key=lambda x: x.buyIndex, reverse=True)
        toBuySorted = [x for x in toBuySorted if x.ticker not in owned]
        toBuySorted = toBuySorted[:3]

        for x in owned:
            wrapper.clearBid(x)

        for toBuy in toBuySorted[:3]:
            priceToBid=utils.getMinAsk(wrapper.getMarketOrder(toBuy)['ASK'])*1.0001
            print str(priceToBid)
            if portfolio.cash >= portfolio.initialCash/4:
                print "Attempting to buy " + toBuy.ticker + " " + str(int(portfolio.cash/(12*priceToBid)))
                wrapper.bid(toBuy, priceToBid, int(portfolio.cash/(12*priceToBid)))

        print owned

        for x in owned:
            if securities[x].currentDivRatio < 0.2 * securities[x].initialDivRatio:
                priceToAsk=utils.getMaxBid(wrapper.getMarketOrder(securities[x])['BID'])*0.95
                print "Asking for " + x + " at price " + str(priceToAsk)
                wrapper.ask(securities[x], priceToAsk, securities[x].numSharesOwned)

main()