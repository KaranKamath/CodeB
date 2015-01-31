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

def runCMDWithParam(cmd, *params):
    params=[str(x) for x in params]
    paramString=' '.join(params)
    return runMod(constants.USER_NAME, constants.PASSWORD, cmd + " " + paramString)

def getCurrCash():
    consoleOutput = runMod(constants.USER_NAME, constants.PASSWORD, "MY_CASH")
    consoleOutput = consoleOutput[0]
    consoleOutput = consoleOutput.split(" ")
    return float(consoleOutput[1])
    
def clearBid(ticker):
    runMod(constants.USER_NAME, constants.PASSWORD, "CLEAR_BID " + ticker)

def clearAsk(ticker):
    runMod(constants.USER_NAME, constants.PASSWORD, "CLEAR_ASK " + ticker)

def bid(share, price, n):
    runCMDWithParam("BID", share.ticker, price, n)

def ask(share, price, n):
    runCMDWithParam("ASK", share.ticker, price, n)

def getMarketOrder(share):
    consoleOutput = runCMDWithParam("ORDERS", share.ticker)
    consoleOutput = consoleOutput[0].split(" ")
    numOrders = (len(consoleOutput) - 1)/4
    order = {}
    order['BID'] = []
    order['ASK'] = []
    for i in range(numOrders):
        if(consoleOutput[1 + i*4] == "BID"):
            order['BID'].append(data.Orders(share,float(consoleOutput[1 + i*4 + 2])))
        if(consoleOutput[1 + i*4] == "ASK"):
            order['ASK'].append(data.Orders(share,float(consoleOutput[1 + i*4 + 2])))
    return order

def getMySecurities(mySecurities):
    #get marketSecurities first
    marketSecurities = {}
    consoleOutput = runMod(constants.USER_NAME, constants.PASSWORD, "SECURITIES")
    consoleOutput = consoleOutput[0].split(" ")
    lenInput = len(consoleOutput)
    numSecurities = (lenInput - 1)/4
    for i in range(numSecurities):
        marketSecurities[consoleOutput[1 + i*4]] = []
        marketSecurities[consoleOutput[1 + i*4]].append(float(consoleOutput[1 + i*4 + 1]))
        marketSecurities[consoleOutput[1 + i*4]].append(float(consoleOutput[1 + i*4 + 2]))
        marketSecurities[consoleOutput[1 + i*4]].append(float(consoleOutput[1 + i*4 + 3]))
    
    consoleOutput = runMod(constants.USER_NAME, constants.PASSWORD, "MY_SECURITIES")
    consoleOutput = consoleOutput[0].split(" ")
    lenInput = len(consoleOutput)
    numSecurities = (lenInput - 1)/3
    for i in range(numSecurities):
        ticker = consoleOutput[1 + i*3]
        if ticker in mySecurities:
            mySecurities[ticker]._netWorth = marketSecurities[ticker][0]
            mySecurities[ticker]._currentDivRatio = float(consoleOutput[1 + i*3 + 2])
            mySecurities[ticker]._numSharesOwned = int(consoleOutput[1 + i*3 + 1])
        else:
            #create new Security
            mySecurities[ticker] = data.Security(ticker, marketSecurities[ticker][0], marketSecurities[ticker][1], marketSecurities[ticker][2])
            mySecurities[ticker]._currentDivRatio = float(consoleOutput[1 + i*3 + 2])
            mySecurities[ticker]._numSharesOwned = int(consoleOutput[1 + i*3 + 1])
            
    return mySecurities

def printStats(oldSecurities, newSecurities):
    if not oldSecurities or not newSecurities:
        return

    for security in oldSecurities.keys():
        changeNumShares = newSecurities[security]._numSharesOwned - oldSecurities[security]._numSharesOwned
        if(changeNumShares > 0):
            print security + " | Bought " + str(changeNumShares)
        elif(changeNumShares < 0):
            print security + " | Sold " + str(changeNumShares)
