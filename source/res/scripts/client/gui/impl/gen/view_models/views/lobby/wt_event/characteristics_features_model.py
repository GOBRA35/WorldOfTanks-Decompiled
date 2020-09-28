# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/views/lobby/wt_event/characteristics_features_model.py
from frameworks.wulf import ViewModel

class CharacteristicsFeaturesModel(ViewModel):
    __slots__ = ()

    def __init__(self, properties=1, commands=0):
        super(CharacteristicsFeaturesModel, self).__init__(properties=properties, commands=commands)

    def getText(self):
        return self._getString(0)

    def setText(self, value):
        self._setString(0, value)

    def _initialize(self):
        super(CharacteristicsFeaturesModel, self)._initialize()
        self._addStringProperty('text', '')
