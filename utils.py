
def getSpread(orders):
    maxBid=getMaxBid(orders['BID'])
    minAsk=getMinAsk(orders['ASK'])
    return minAsk-maxBid

def getMaxBid(bids):
    return sorted(bids, reverse=True, key=lambda x: x.price)[0].price

def getMinAsk(asks):
    return sorted(asks, key=lambda x: x.price)[0].price



