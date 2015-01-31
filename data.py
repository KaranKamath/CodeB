class Security(object):

    @property
    def ticker(self):
        return self._ticker

    @property
    def numSharesOwned(self):
        return self._numSharesOwned

    @property
    def priceBoughtAt(self):
        return self._priceBoughtAt

    @property
    def currentDivRatio(self):
        return self._currentDivRatio

    @property
    def dividend(self):
        return self.netWorth * self.currentDivRatio * self.numSharesOwned

    @property
    def numShares(self):
        return self._numShares

    def __init__(self, ticker, netWorth, initialDivRatio, volatility):
        self._netWorth = netWorth
        self._initialDivRatio = initialDivRatio
        self._volatility=volatility
        self._ticker=ticker

class Orders(object):
    @property
    def price(self):
        return self._price

    @property
    def share(self):
        self._share

    def __init__(self, share, price):
        self._price=price
        self._share=share

class Portfolio(object):
    @property
    def cash(self):
        return self._cash

    def __init__(self, cash):
        self._cash=cash