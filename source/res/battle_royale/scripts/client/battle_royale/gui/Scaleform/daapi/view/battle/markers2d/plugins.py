# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: battle_royale/scripts/client/battle_royale/gui/Scaleform/daapi/view/battle/markers2d/plugins.py
from collections import defaultdict
import logging
import BigWorld
from account_helpers.settings_core.settings_constants import MARKERS
from battle_royale.gui.Scaleform.daapi.view.battle.markers2d import settings
from gui.Scaleform.daapi.view.battle.shared.markers2d import markers
from gui.Scaleform.daapi.view.battle.shared.markers2d.plugins import SettingsPlugin
from gui.Scaleform.daapi.view.battle.shared.markers2d.vehicle_plugins import VehicleMarkerPlugin
from gui.Scaleform.genConsts.BATTLE_MARKER_STATES import BATTLE_MARKER_STATES
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from helpers import dependency
from items.battle_royale import isSpawnedBot
from skeletons.gui.battle_session import IBattleSessionProvider
from gui.battle_control.battle_constants import VEHICLE_VIEW_STATE
_logger = logging.getLogger(__name__)
_BATTLE_ROYALE_STATUS_EFFECTS_PRIORITY = ((BATTLE_MARKER_STATES.FIRE_CIRCLE_STATE, BATTLE_MARKER_STATES.THUNDER_STRIKE_STATE),
 (BATTLE_MARKER_STATES.BERSERKER_STATE,),
 (BATTLE_MARKER_STATES.STUN_STATE,),
 (BATTLE_MARKER_STATES.DEBUFF_STATE,),
 (BATTLE_MARKER_STATES.SHOT_PASSION_STATE,),
 (BATTLE_MARKER_STATES.ADAPTATION_HEALTH_RESTORE_STATE,),
 (BATTLE_MARKER_STATES.HEALING_STATE,),
 (BATTLE_MARKER_STATES.INSPIRING_STATE,),
 (BATTLE_MARKER_STATES.INSPIRED_STATE,),
 (BATTLE_MARKER_STATES.REPAIRING_STATE,))
_MARKERS_WITH_TIMER = (BATTLE_MARKER_STATES.INSPIRING_STATE, BATTLE_MARKER_STATES.HEALING_STATE)

class BattleRoyaleVehicleMarkerPlugin(VehicleMarkerPlugin):
    __sessionProvider = dependency.descriptor(IBattleSessionProvider)

    def __init__(self, parentObj, clazz=markers.VehicleMarker):
        super(BattleRoyaleVehicleMarkerPlugin, self).__init__(parentObj, clazz)
        self.__markersStatesExtended = defaultdict(list)
        self.__cache = {}

    def start(self):
        super(BattleRoyaleVehicleMarkerPlugin, self).start()
        player = BigWorld.player()
        if player is not None and player.inputHandler is not None:
            player.inputHandler.onCameraChanged += self.__onCameraChanged
        self.__sessionProvider.onUpdateObservedVehicleData += self._onUpdateObservedVehicleData
        return

    def stop(self):
        player = BigWorld.player()
        if player is not None and player.inputHandler is not None:
            player.inputHandler.onCameraChanged -= self.__onCameraChanged
        self.__sessionProvider.onUpdateObservedVehicleData -= self._onUpdateObservedVehicleData
        super(BattleRoyaleVehicleMarkerPlugin, self).stop()
        self.__cache = {}
        return

    def invalidateVehicleStatus(self, flags, vInfo, arenaDP):
        if not vInfo.isAlive() and isSpawnedBot(vInfo.vehicleType.tags):
            self._hideVehicleMarker(vInfo.vehicleID)

    def updateVehiclesInfo(self, updated, arenaDP):
        super(BattleRoyaleVehicleMarkerPlugin, self).updateVehiclesInfo(updated, arenaDP)
        for _, vInfo in updated:
            if not vInfo.isAlive() and isSpawnedBot(vInfo.vehicleType.tags):
                self._hideVehicleMarker(vInfo.vehicleID)

    def _getMarkerSymbol(self, vehicleID):
        vehicleArenaInfoVO = self.__sessionProvider.getArenaDP().getVehicleInfo(vehicleID)
        return settings.BRmarkersSymbolsNames.BRANDER_BOT_SYMBOL if isSpawnedBot(vehicleArenaInfoVO.vehicleType.tags) else super(BattleRoyaleVehicleMarkerPlugin, self)._getMarkerSymbol(vehicleID)

    def _getMarkerStatusPriority(self, statusID):
        try:
            for index, priorities in enumerate(_BATTLE_ROYALE_STATUS_EFFECTS_PRIORITY):
                if statusID in priorities:
                    return index

        except ValueError:
            return -1

    def _onVehicleFeedbackReceived(self, eventID, vehicleID, value):
        super(BattleRoyaleVehicleMarkerPlugin, self)._onVehicleFeedbackReceived(eventID, vehicleID, value)
        if vehicleID not in self._markers:
            return
        else:
            if eventID == FEEDBACK_EVENT_ID.VEHICLE_REPAIR_POINT:
                if value.get('duration') is None:
                    state = self.__getStateByFeedbackID(eventID)
                    if state:
                        self.__updateCache(vehicleID, state, value, 0, isRemove=True)
            handle = self._markers[vehicleID].getMarkerID()
            if eventID == FEEDBACK_EVENT_ID.VEHICLE_CUSTOM_MARKER:
                self.__updateMarker(vehicleID, handle, **value)
            return

    def _onVehicleStateUpdated(self, state, value):
        super(BattleRoyaleVehicleMarkerPlugin, self)._onVehicleStateUpdated(state, value)
        vehicle = BigWorld.player().getVehicleAttached()
        if vehicle is None:
            return
        else:
            if state == VEHICLE_VIEW_STATE.REPAIR_POINT:
                if vehicle.id in self._markers:
                    markerID = self._markers[vehicle.id].getMarkerID()
                    self.__updateCache(vehicle.id, state, value, markerID)
            return

    def __updateCache(self, vehicleID, state, value, markerID, isRemove=False):
        if isRemove:
            self.__cache.pop(vehicleID, {}).pop(state, None)
        else:
            self.__cache.setdefault(vehicleID, {})[state] = (value, markerID)
        return

    def __getStateByFeedbackID(self, eventID):
        data = {FEEDBACK_EVENT_ID.VEHICLE_REPAIR_POINT: VEHICLE_VIEW_STATE.REPAIR_POINT}
        return data.get(eventID)

    def __updateMarker(self, vehicleID, handle, isShown, isSourceVehicle, duration, animated, markerID):
        self._updateStatusMarkerState(vehicleID, isShown, handle, markerID, duration, animated, isSourceVehicle)
        if markerID in _MARKERS_WITH_TIMER:
            self._updateMarkerTimer(vehicleID, handle, duration, markerID)

    def _updateStunMarker(self, vehicleID, handle, value):
        super(BattleRoyaleVehicleMarkerPlugin, self)._updateStunMarker(vehicleID, handle, value)
        if vehicleID == BigWorld.player().getObservedVehicleID() and vehicleID in self._markers:
            self.__hideStunMarker(vehicleID, self._markers[vehicleID].getMarkerID())

    def _updateStatusMarkerState(self, vehicleID, isShown, handle, statusID, duration, animated, isSourceVehicle):
        extendedStatuses = self.__markersStatesExtended[vehicleID]
        if isShown and not self.__statusInActive(vehicleID, statusID):
            hasNeighbor = self.__hasNeighborInPrioritizes
            extendedStatuses.append((statusID, -BigWorld.serverTime() if hasNeighbor(statusID) else 0.0))
            self.__markersStatesExtended[vehicleID] = extendedStatuses
        elif not isShown and self.__statusInActive(vehicleID, statusID):
            self.__removeStatus(vehicleID, statusID)
        if self.__markersStatesExtended[vehicleID]:
            activeStatuses = sorted(self.__markersStatesExtended[vehicleID], key=lambda x: (x[1], self._getMarkerStatusPriority(x[0])))
            self.__markersStatesExtended[vehicleID] = activeStatuses
        self._markersStates[vehicleID] = [ state for state, _ in self.__markersStatesExtended[vehicleID] ]
        currentlyActiveStatusID = self._markersStates[vehicleID][0] if self._markersStates[vehicleID] else -1
        if statusID in (BATTLE_MARKER_STATES.STUN_STATE, BATTLE_MARKER_STATES.HEALING_STATE, BATTLE_MARKER_STATES.INSPIRING_STATE):
            isSourceVehicle = True
        elif statusID == BATTLE_MARKER_STATES.DEBUFF_STATE:
            isSourceVehicle = False
        if isShown:
            self._invokeMarker(handle, 'showStatusMarker', statusID, self._getMarkerStatusPriority(statusID), isSourceVehicle, duration, currentlyActiveStatusID, self._getMarkerStatusPriority(currentlyActiveStatusID), animated)
        else:
            self._invokeMarker(handle, 'hideStatusMarker', statusID, currentlyActiveStatusID, animated)

    def __statusInActive(self, vehicleID, statusID):
        for status, _ in self.__markersStatesExtended[vehicleID]:
            if status == statusID:
                return True

        return False

    def __removeStatus(self, vehicleID, statusID):
        for data in self.__markersStatesExtended[vehicleID]:
            if data[0] == statusID:
                self.__markersStatesExtended[vehicleID].remove(data)
                return

    def __hasNeighborInPrioritizes(self, statusID):
        for statuses in _BATTLE_ROYALE_STATUS_EFFECTS_PRIORITY:
            if statusID in statuses and len(statuses) > 1:
                return True

        return False

    def __onCameraChanged(self, cameraName, currentVehicleId=None):
        if currentVehicleId is None:
            return
        else:
            vehicle = BigWorld.entities.get(currentVehicleId)
            if vehicle is None:
                return
            if cameraName == 'video':
                if self.__hasRepairingMarker(currentVehicleId):
                    self.__updateRepairingMarker(currentVehicleId)
                if vehicle.stunInfo:
                    marker = self._markers.get(currentVehicleId)
                    if marker and BATTLE_MARKER_STATES.STUN_STATE in self._markerTimers.get(marker.getMarkerID(), {}):
                        self.__showStunMarker(currentVehicleId, marker.getMarkerID(), vehicle.getStunInfo())
            else:
                if self.__hasRepairingMarker(currentVehicleId):
                    self.__updateRepairingMarker(currentVehicleId, isShow=False)
                vehicle.updateStunInfo()
            return

    def _onUpdateObservedVehicleData(self, vehicleID, _):
        for keyVehID, marker in self._markers.iteritems():
            if keyVehID != vehicleID:
                if self.__hasRepairingMarker(keyVehID):
                    self.__updateRepairingMarker(keyVehID)
                if BATTLE_MARKER_STATES.STUN_STATE in self._markerTimers.get(marker.getMarkerID(), {}):
                    vehicle = BigWorld.entities.get(keyVehID)
                    if vehicle:
                        vehicle.updateStunInfo()
            self.__hideStunMarker(keyVehID, marker.getMarkerID())

    def __updateRepairingMarker(self, vehicleID, isShow=True):
        repairData = self.__cache.get(vehicleID, {}).get(VEHICLE_VIEW_STATE.REPAIR_POINT)
        if repairData is not None:
            value, markerID = repairData
            marker = self._markers[vehicleID]
            if markerID == marker.getMarkerID():
                duration = value.get('duration', 0) if isShow else 0.0
                self._updateRepairingMarker(vehicleID, markerID, duration)
        return

    def __hasRepairingMarker(self, vehicleID):
        return VEHICLE_VIEW_STATE.REPAIR_POINT in self.__cache.get(vehicleID, {})

    def __hideStunMarker(self, vehicleID, handle):
        self._updateStatusMarkerState(vehicleID, False, handle, BATTLE_MARKER_STATES.STUN_STATE, 0, False, False)

    def __showStunMarker(self, vehicleID, handle, stunInfo):
        self._updateStatusMarkerState(vehicleID, True, handle, BATTLE_MARKER_STATES.STUN_STATE, stunInfo.duration, False, False)


class BattleRoyaleSettingsPlugin(SettingsPlugin):
    __CUSTOM = (('markerBaseLevel', 0), ('markerAltLevel', 0))

    def _setMarkerSettings(self, notify=False):
        getter = self.settingsCore.getSetting
        result = {}
        for name in MARKERS.ALL():
            stgs = getter(name)
            for custOptName, custOptVal in self.__CUSTOM:
                if custOptName not in stgs:
                    _logger.warning('Option "%s" is not in list of options', custOptName)
                stgs[custOptName] = custOptVal

            result[name] = stgs

        self._parentObj.setMarkerSettings(result, notify=notify)
