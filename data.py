class Security(object):

    @property
    def numShares(self):
        return self.numShares

    def __init__(self, ticker, netWorth, divRatio, volatility):
        self.netWorth = netWorth
        self.divRatio = divRatio
        self.volatility = volatility
        self.ticker = ticker

class Orders(object):
    @property
    def price(self):
        return self.price

    @property
    def share(self):
        self.share

    def __init__(self, share, price):
        self.price=price
        self.share=share