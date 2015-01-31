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
    #print "Bidding..." + str(priceToBid) + " for " + str(ticker)
    wrapper.bid(securities[ticker], priceToBid, int(cash/(1.0*priceToBid)))

def optSell(ticker, securities):
    priceToAsk=utils.getMaxBid(wrapper.getMarketOrder(securities[ticker])['BID'])*0.99
    #print "Selling " + str(ticker) + " at price " + str(priceToAsk)
    wrapper.ask(securities[ticker], priceToAsk, securities[ticker].numSharesOwned)

def main():
    cash = run(constants.USER_NAME, constants.PASSWORD, "MY_CASH")
    portfolio = data.Portfolio(cash.split(" ")[1])

    securities=wrapper.getMySecurities({})

    learnTable = {}

    tableOrder=5

    for security in securities.keys():
        learnTable[security] = [securities[security]._netWorth]*tableOrder

    learnCounter = 0

    while True:
        portfolio._cash=wrapper.getCurrCash()
        portfolio._securities=securities
        import copy
        previousSecurities=copy.deepcopy(securities)
        securities=wrapper.getMySecurities(securities)
        wrapper.printStats(previousSecurities, securities)

        owned=[x for x in securities if securities[x].numSharesOwned>0]

        if learnCounter == tableOrder:
            for security in learnTable.keys():
                nwVals = learnTable[security]
                cmpVals = [0] * (len(nwVals)-1)
                for i in range(0, len(nwVals)-1):
                    com=cmp(nwVals[i+1], nwVals[i])
                    if com == 0:
                        com=1
                    cmpVals[i] = com
                print security + " " + str(cmpVals)

                trend = reduce(lambda x, y: x+y, cmpVals)
                #print cmpVals
                if trend == tableOrder-1:
                    optBuy(security, securities, portfolio.cash/2.0)
                #elif trend == tableOrder-3 and cmpVals[0]==-1:
                #    optBuy(security, securities, portfolio.cash/2.0)
                #lif trend == -1*(tableOrder-3) and cmpVals[0]==1:
                #    optSell(security, securities)
                elif trend == -1*(tableOrder-1) and security in owned:
                    optSell(security, securities)
                #print nwVals
            learnTable[security][learnCounter%(tableOrder-1)] = securities[security]._netWorth
            learnCounter = 0
        else:
            for security in learnTable.keys():
                learnTable[security][learnCounter%tableOrder] = securities[security]._netWorth
            learnCounter = learnCounter+1

        #print "learn " + str(learnCounter)


        for x in owned:
            wrapper.clearBid(x)

        print owned

        for x in owned:
            if securities[x].currentDivRatio < 0.1 * securities[x].initialDivRatio:
                priceToAsk=utils.getMaxBid(wrapper.getMarketOrder(securities[x])['BID'])*0.99
                #print "Asking for " + x + " at price " + str(priceToAsk)
                wrapper.ask(securities[x], priceToAsk, securities[x].numSharesOwned)

main()