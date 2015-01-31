class Security(object):

    @property
    def numSharesOwned(self):
        return self.numSharesOwned

    @property
    def priceBoughtAt(self):
        return self.priceBoughtAt

    @property
    def currentDivRatio(self):
        return self.currentDivRatio

    @property
    def dividend(self):
        return self.netWorth * self.currentDivRatio * self.numSharesOwned

    @property
    def numShares(self):
        return self.numShares

    def __init__(self, netWorth, initialDivRatio, volatility):
        self.netWorth = netWorth
        self.initalDivRatio = initialDivRatio
        self.volatility=volatility

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