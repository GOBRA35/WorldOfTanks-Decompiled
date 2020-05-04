# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/views/lobby/secret_event/general_filter_item_model.py
from gui.impl.gen import R
from frameworks.wulf import ViewModel

class GeneralFilterItemModel(ViewModel):
    __slots__ = ()

    def __init__(self, properties=2, commands=0):
        super(GeneralFilterItemModel, self).__init__(properties=properties, commands=commands)

    def getGeneralId(self):
        return self._getNumber(0)

    def setGeneralId(self, value):
        self._setNumber(0, value)

    def getGeneralName(self):
        return self._getResource(1)

    def setGeneralName(self, value):
        self._setResource(1, value)

    def _initialize(self):
        super(GeneralFilterItemModel, self)._initialize()
        self._addNumberProperty('generalId', 0)
        self._addResourceProperty('generalName', R.invalid())
