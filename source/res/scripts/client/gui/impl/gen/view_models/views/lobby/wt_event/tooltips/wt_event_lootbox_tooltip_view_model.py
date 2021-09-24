# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/views/lobby/wt_event/tooltips/wt_event_lootbox_tooltip_view_model.py
from frameworks.wulf import ViewModel

class WtEventLootboxTooltipViewModel(ViewModel):
    __slots__ = ()

    def __init__(self, properties=2, commands=0):
        super(WtEventLootboxTooltipViewModel, self).__init__(properties=properties, commands=commands)

    def getLootBoxesAmount(self):
        return self._getNumber(0)

    def setLootBoxesAmount(self, value):
        self._setNumber(0, value)

    def getIsHunterLootBox(self):
        return self._getBool(1)

    def setIsHunterLootBox(self, value):
        self._setBool(1, value)

    def _initialize(self):
        super(WtEventLootboxTooltipViewModel, self)._initialize()
        self._addNumberProperty('lootBoxesAmount', 0)
        self._addBoolProperty('isHunterLootBox', False)
