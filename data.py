class Security(object):

    @property()
    def timeHeld(self):
        return self.timeHeld

    @property
    def numShares(self):
        return self.numShares

    def __init__(self, netWorth, divRatio, volatility):
        self.netWorth = netWorth
        self.divRatio = divRatio
        self.volatility=volatility
        self.timeHeld=0

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