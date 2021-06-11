# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/skeletons/gui/cdn.py
import adisp

class IPurchaseCache(object):

    def init(self):
        raise NotImplementedError

    def fini(self):
        raise NotImplementedError

    @adisp.async
    def requestPurchaseByID(self, pId, callback=None):
        pass

    def getCachedPurchase(self, pId):
        return None

    def getProductCode(self, pId):
        return None

    def canBeRequestedFromProduct(self, data):
        return False
