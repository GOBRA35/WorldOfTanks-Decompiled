# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/views/lobby/new_year/tooltips/new_year_collection_table_value.py
from frameworks.wulf import ViewModel
from gui.impl.wrappers.user_list_model import UserListModel

class NewYearCollectionTableValue(ViewModel):
    __slots__ = ()

    def __init__(self, properties=3, commands=0):
        super(NewYearCollectionTableValue, self).__init__(properties=properties, commands=commands)

    @property
    def collectionBonuses(self):
        return self._getViewModel(0)

    def getInterval(self):
        return self._getString(1)

    def setInterval(self, value):
        self._setString(1, value)

    def getIsEnabled(self):
        return self._getBool(2)

    def setIsEnabled(self, value):
        self._setBool(2, value)

    def _initialize(self):
        super(NewYearCollectionTableValue, self)._initialize()
        self._addViewModelProperty('collectionBonuses', UserListModel())
        self._addStringProperty('interval', '1-10')
        self._addBoolProperty('isEnabled', False)
