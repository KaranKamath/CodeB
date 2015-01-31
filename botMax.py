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

def optBuy(ticker, securities, cash):
    priceToBid=utils.getMinAsk(wrapper.getMarketOrder(securities[ticker])['ASK'])*1.00001
    print "Bidding..." + str(priceToBid) + " for " + str(ticker)
    wrapper.bid(securities[ticker], priceToBid, int(cash/(1.0*priceToBid)))

def optSell(ticker, securities):
    priceToAsk=utils.getMaxBid(wrapper.getMarketOrder(securities[ticker])['BID'])*0.99
    print "Selling " + str(ticker) + " at price " + str(priceToAsk)
    wrapper.ask(securities[ticker], priceToAsk, securities[ticker].numSharesOwned)

def main():
    cash = run(constants.USER_NAME, constants.PASSWORD, "MY_CASH")
    portfolio = data.Portfolio(cash.split(" ")[1])

    #print portfolio.cash

    securities=wrapper.getMySecurities({})
    maxBuyIndex = -3655

    learnTable = {}
    for security in securities.keys():
        learnTable[security] = [securities[security]._netWorth]*5

    learnCounter = 0

    while True:
        import copy
        previousSecurities=copy.deepcopy(securities)
        securities=wrapper.getMySecurities(securities)
        owned=[x for x in securities if securities[x].numSharesOwned>0]
        print owned

        if learnCounter == 5:
            for security in learnTable.keys():
                nwVals = learnTable[security]
                cmpVals = [0] * (len(nwVals)-1)
                for i in range(0, len(nwVals)-1):
                    cmpVals[i] = cmp(nwVals[i+1],nwVals[i])
                #print security + " " + str(cmpVals)

                trend = reduce(lambda x, y: x+y, cmpVals)
                #print trend
                if trend == 4:
                    optBuy(security, securities, portfolio.cash/2.0)
                elif trend == -4 and security in owned:
                    optSell(security, securities)

            learnTable[security][learnCounter%5] = securities[security]._netWorth
            learnCounter = 0
        else:
            for security in learnTable.keys():
                learnTable[security][learnCounter%5] = securities[security]._netWorth
            learnCounter = learnCounter+1

        #print "learn " + str(learnCounter)

        portfolio._cash=wrapper.getCurrCash()

        #print "Cash: " + str(portfolio.cash)

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

        toBuySorted = sorted(securities.values(), key=lambda x: x.buyIndex, reverse=True)
        toBuySorted = [x for x in toBuySorted if x.ticker not in owned]
        toBuySorted = toBuySorted[:3]

        for x in owned:
            wrapper.clearBid(x)

        for toBuy in toBuySorted[:2]:
            priceToBid=utils.getMinAsk(wrapper.getMarketOrder(toBuy)['ASK'])*1.00001
            #print str(priceToBid)
            #if portfolio.cash >= portfolio.initialCash/4 and len(securities.keys())/2.0 > len(owned):
                #print "Attempting to buy " + toBuy.ticker + " " + str(int(portfolio.cash/(8*priceToBid)))
                #wrapper.bid(toBuy, priceToBid, int(portfolio.cash/(8*priceToBid)))

        print owned

        for x in owned:
            if securities[x].currentDivRatio < 0.2 * securities[x].initialDivRatio:
                priceToAsk=utils.getMaxBid(wrapper.getMarketOrder(securities[x])['BID'])*0.99
                #print "Asking for " + x + " at price " + str(priceToAsk)
                wrapper.ask(securities[x], priceToAsk, securities[x].numSharesOwned)

        #for x in securities.values():
        #    print x.ticker + " " + str(float(1.0/(1.0+x._volatility)))

main()