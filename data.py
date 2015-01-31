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
    def buyIndex(self):
        return self._buyIndex

    @property
    def dividend(self):
        return self._dividend

    @property
    def numShares(self):
        return self._numShares

    @property
    def initialDivRatio(self):
        return self._initialDivRatio

    def __init__(self, ticker, netWorth, initialDivRatio, volatility):
        self._netWorth = netWorth
        self._initialDivRatio = initialDivRatio
        self._volatility=volatility
        self._ticker=ticker
        self._dividend=0
        from sys import maxint
        self._buyIndex=-maxint-1

class Orders(object):
    @property
    def price(self):
        return self._price

    @property
    def share(self):
        return self._share

    def __init__(self, share, price):
        self._price=price
        self._share=share

class Portfolio(object):
    @property
    def cash(self):
        return self._cash

    @property
    def initialCash(self):
        return self._initialCash

    @property
    def securities(self):
        return self._securities

    def addSecurity(self, x):
        self._securities[x.ticker] = x

    def removeSecurity(self, x):
        del self._securities[x.ticker]

    def update(self, owned):
        for share in owned:
            portShare=self.securities[share.ticker]
            portShare.netWorth=share.netWorth
            portShare.currentDivRatio=share.currentDivRatio

    def updateDividends(self):
        for x in self.securities.keys():
            currentSecurity=self.securities[x]
            if currentSecurity._numSharesOwned == 0:
                currentSecurity._dividend=0

            #if currentSecurity._numSharesOwned > 0:
             #   divAdd=currentSecurity.currentDivRatio * currentSecurity._netWorth * 1.0 / (1.0 * currentSecurity._numSharesOwned)
              #  print divAdd
               # currentSecurity._dividend += divAdd

    def __init__(self, cash):
        self._cash=float(cash)
        self._initialCash=float(cash)
