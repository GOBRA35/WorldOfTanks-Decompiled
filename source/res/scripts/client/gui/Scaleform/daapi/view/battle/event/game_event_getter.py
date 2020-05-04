# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/event/game_event_getter.py
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

class GameEventGetterMixin(object):
    sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self):
        self.__gameEventStorage = None
        return

    @property
    def storage(self):
        storage = self.__gameEventStorage
        if not storage:
            componentSystem = self.sessionProvider.arenaVisitor.getComponentSystem()
            self.__gameEventStorage = storage = getattr(componentSystem, 'gameEventComponent', None)
        return storage

    @property
    def teammateVehicleHealth(self):
        return self.storage.getTeammateVehicleHealth()

    @property
    def scenarioAnimationTriggers(self):
        return self.storage.scenarioAnimationTriggers()

    @property
    def souls(self):
        return self.storage.getSouls()

    @property
    def soulCollector(self):
        return self.storage.getSoulCollector()

    @property
    def getAreaVehicleMarker(self):
        return self.storage.getAreaVehicleMarker()

    @property
    def getAreaPointMarker(self):
        return self.storage.getAreaPointMarker()

    @property
    def teammateResurrectEquipment(self):
        return self.storage.getTeammateResurrectEquipment()

    @property
    def enemySpottedData(self):
        return self.storage.getEnemySpottedData()

    @property
    def environmentData(self):
        return self.storage.getEnvironmentData()

    @property
    def ecpState(self):
        return self.storage.ecpState

    @property
    def nearbyIndicatorData(self):
        return self.storage.getNearbyIndicator()

    @property
    def activeTimers(self):
        return self.storage.activeTimers

    @property
    def behaviorMarker(self):
        return self.storage.getBehaviorMarker()

    @property
    def highlightMarkers(self):
        return self.storage.getHighlightMarkers()

    @property
    def teammateLifecycle(self):
        return self.storage.getTeammateLifecycle()

    @property
    def scenarioGoals(self):
        return self.storage.getScenarioGoals()

    @property
    def minimapInfo(self):
        return self.storage.minimapInfo
