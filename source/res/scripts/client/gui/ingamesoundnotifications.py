# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/IngameSoundNotifications.py
import logging
from collections import namedtuple
from functools import partial
import BigWorld
import Math
import ResMgr
import BattleReplay
import SoundGroups
import WWISE
from debug_utils import LOG_WARNING
from Math import Matrix
_logger = logging.getLogger(__name__)

class IngameSoundNotifications(object):
    __CFG_SECTION_PATH = 'gui/sound_notifications.xml'
    QueueItem = namedtuple('QueueItem', ('soundPath', 'time', 'minTimeBetweenEvents', 'idToBind', 'checkFn', 'soundPos', 'soundObjectName', 'matrixProvider'))

    def __init__(self):
        self.__activeEvents = None
        self.__soundQueues = None
        self.__isEnabled = False
        self.__enabledSoundCategories = set()
        self.__lastEnqueuedTime = {}
        self.__remappedNotifications = {}
        self.__readConfig()
        return

    def start(self):
        self.__soundQueues = {'fx': [],
         'voice': []}
        self.__enabledSoundCategories = set(('fx', 'voice'))
        self.__isEnabled = True
        self.__activeEvents = {'fx': None,
         'voice': None}
        self.__lastEnqueuedTime = {}
        return

    def destroy(self):
        if self.__activeEvents:
            for event in self.__activeEvents.itervalues():
                if event is not None:
                    event['sound'].stop()

        self.__activeEvents = None
        self.__soundQueues = None
        self.__isEnabled = False
        return

    def cancel(self, eventName, continuePlaying=True):
        for category in ('fx', 'voice'):
            eventDesc = self.__events[eventName].get(category, None)
            if eventDesc is not None:
                activeEvent = self.__activeEvents[category]
                soundPath = eventDesc['sound']
                if activeEvent is not None and activeEvent['soundPath'] == soundPath:
                    activeEvent['sound'].stop()
                    self.__activeEvents[category] = None
                    if continuePlaying:
                        self.__playFirstFromQueue(category)
                if soundPath in self.__soundQueues[category]:
                    self.__soundQueues[category].remove(soundPath)

        return

    def play(self, eventName, vehicleIdToBind=None, checkFn=None, eventPos=None, soundObjectName=None, matrixProvider=None):
        replayCtrl = BattleReplay.g_replayCtrl
        if replayCtrl.isPlaying and replayCtrl.isTimeWarpInProgress:
            return
        elif not self.__isEnabled or BigWorld.isWindowVisible() is False:
            return
        else:
            eventName = self.__remappedNotifications.get(eventName, eventName)
            if eventName is None:
                return
            event = self.__events.get(eventName, None)
            if event is None:
                LOG_WARNING("Couldn't find %s event" % eventName)
                return
            queues = self.__soundQueues
            enabledCategories = self.__enabledSoundCategories
            time = BigWorld.time()
            for category, soundDesc in event.iteritems():
                if category in enabledCategories and soundDesc['sound'] != '':
                    rules = soundDesc['playRules']
                    idToBind = vehicleIdToBind
                    if idToBind is None and soundDesc['shouldBindToPlayer']:
                        if BigWorld.player().vehicle is not None:
                            idToBind = BigWorld.player().vehicle.id
                    soundPath = soundDesc['sound']
                    minTimeBetweenEvents = soundDesc['minTimeBetweenEvents']
                    queueItem = IngameSoundNotifications.QueueItem(soundPath, time + soundDesc['timeout'], minTimeBetweenEvents, idToBind, checkFn, eventPos, soundObjectName, matrixProvider)
                    if rules == 0:
                        try:
                            if matrixProvider is not None:
                                mProv = Matrix(matrixProvider)
                                mProvPos = mProv.translation
                                SoundGroups.g_instance.playSoundPos(soundDesc['sound'], mProvPos)
                            elif eventPos is not None:
                                SoundGroups.g_instance.playCameraOriented(soundDesc['sound'], eventPos)
                            else:
                                SoundGroups.g_instance.playSound2D(soundDesc['sound'])
                        except Exception:
                            _logger.exception('play sound exception: %s', soundPath)

                        continue
                    else:
                        lastEnqueuedTime = self.__lastEnqueuedTime.get(soundPath)
                        if lastEnqueuedTime is not None and time - lastEnqueuedTime < minTimeBetweenEvents:
                            continue
                        self.__lastEnqueuedTime[soundPath] = time
                        if rules == 1:
                            clearActiveEvents = True
                            if self.__activeEvents[category] is not None:
                                clearActiveEvents = False
                            self.__clearQueue(category, clearActiveEvents)
                            queues[category].append(queueItem)
                        elif rules == 2:
                            queues[category].insert(0, queueItem)
                        elif rules == 3:
                            queues[category].append(queueItem)
                    if self.__activeEvents[category] is None:
                        self.__playFirstFromQueue(category)

            return

    def enable(self, isEnabled):
        self.__isEnabled = isEnabled
        if not isEnabled:
            for category in ('fx', 'voice'):
                self.__clearQueue(category)

    def clear(self):
        if self.__isEnabled:
            self.enable(False)
            self.enable(True)

    def enableFX(self, isEnabled):
        self.enableCategory('fx', isEnabled)

    def enableVoices(self, isEnabled, clearQueue=True):
        self.enableCategory('voice', isEnabled, clearQueue)

    def enableCategory(self, category, isEnabled, clearQueue=True):
        if isEnabled:
            self.__enabledSoundCategories.add(category)
        else:
            self.__enabledSoundCategories.remove(category)
            if clearQueue:
                self.__clearQueue(category)

    def setRemapping(self, remap):
        self.__remappedNotifications = remap

    def isCategoryEnabled(self, category):
        return True if category in self.__enabledSoundCategories else False

    def isPlaying(self, eventName):
        for category in ('fx', 'voice'):
            eventDesc = self.__events[eventName].get(category, None)
            if eventDesc is not None:
                activeEvent = self.__activeEvents[category]
                soundPath = eventDesc['sound']
                if activeEvent is not None and activeEvent['soundPath'] == soundPath:
                    return activeEvent['sound'].isPlaying

        return False

    def __clearQueue(self, category, clearActiveEvents=True):
        if self.__activeEvents[category] is not None:
            if clearActiveEvents is True:
                self.__activeEvents[category] = None
        self.__soundQueues[category] = []
        return

    def __onSoundEnd(self, category, sound):
        if self.__activeEvents is None:
            return
        else:
            if WWISE.enabled:
                if sound.isPlaying:
                    BigWorld.callback(0.01, lambda : self.__onSoundEnd(category, sound))
                else:
                    self.__activeEvents[category] = None
                    queue = self.__soundQueues[category]
                    if queue:
                        BigWorld.callback(0.01, partial(self.__playFirstFromQueue, category))
            elif sound.state.find('playing') != -1:
                BigWorld.callback(0.01, lambda : self.__onSoundEnd(category, sound))
            else:
                self.__activeEvents[category] = None
                BigWorld.callback(0.01, partial(self.__playFirstFromQueue, category))
            return

    def __playFirstFromQueue(self, category):
        if not self.__isEnabled:
            return
        else:
            queue = self.__soundQueues[category]
            time = BigWorld.time()
            while queue:
                soundPath, timeout, _, vehicleIdToBind, checkFn, sndPos, soundObjectName, matrixProvider = queue[0]
                del queue[0]
                if vehicleIdToBind is not None:
                    vehicles = BigWorld.player().arena.vehicles
                    vehicleInfo = vehicles.get(vehicleIdToBind)
                    if vehicleInfo is None or not vehicleInfo['isAlive']:
                        continue
                if checkFn is not None and not checkFn():
                    continue
                if time > timeout:
                    continue
                if matrixProvider is not None:
                    sound = SoundGroups.g_instance.WWgetSound(soundPath, soundObjectName, matrixProvider)
                elif sndPos is not None:
                    sound = SoundGroups.g_instance.getCameraOriented(soundPath, sndPos)
                else:
                    sound = SoundGroups.g_instance.getSound2D(soundPath)
                if sound is not None:
                    sound.setCallback(partial(self.__onSoundEnd, category))
                    sound.play()
                    self.__activeEvents[category] = {'sound': sound,
                     'soundPath': soundPath}
                return

            return

    def __readConfig(self):
        sec = ResMgr.openSection(self.__CFG_SECTION_PATH)
        events = {}
        for eventSec in sec.values():
            event = events[eventSec.name] = {}
            for category in ('fx', 'voice'):
                soundSec = eventSec[category]
                if soundSec is not None:
                    event[category] = {'sound': soundSec.readString('wwsound'),
                     'playRules': soundSec.readInt('playRules'),
                     'timeout': soundSec.readFloat('timeout', 3.0),
                     'minTimeBetweenEvents': soundSec.readFloat('minTimeBetweenEvents', 0),
                     'shouldBindToPlayer': soundSec.readBool('shouldBindToPlayer', False)}

        self.__events = events
        return


class ComplexSoundConstants(object):
    SPG_DISTANT_THREAT_SOUND = 'wpn_artillery_distant_threat'
    RTPC_EXT_SPG_SIGHT = 'RTPC_ext_artillery_sight'


class ComplexSoundNotifications(object):

    def __init__(self, ingameSoundNotifications):
        self.__isAimingEnded = False
        self.__ingameSoundNotifications = ingameSoundNotifications
        self.__activeSounds = {}

    def destroy(self):
        for sound, hasMatrix in self.__activeSounds.values():
            self.__soundStop(sound, hasMatrix)

        self.__activeSounds.clear()

    def setAimingEnded(self, isEnded, isReloading):
        if not self.__isAimingEnded and isEnded and not isReloading:
            self.__ingameSoundNotifications.play('sight_convergence')
        self.__isAimingEnded = isEnded

    def notifyEnemySpotted(self, isPlural):
        self.__ingameSoundNotifications.cancel('`p`p', True)
        if isPlural:
            self.__ingameSoundNotifications.play('enemies_sighted')
        else:
            self.__ingameSoundNotifications.play('enemy_sighted')

    def notifyEnemySPGShotSound(self, distToTarget, shooterPosition):
        soundMatrix = Math.Matrix()
        soundMatrix.translation = shooterPosition
        try:
            sound = SoundGroups.g_instance.getSound3D(soundMatrix, ComplexSoundConstants.SPG_DISTANT_THREAT_SOUND)
            if sound is not None:
                soundId = id(sound)
                self.__activeSounds[soundId] = (sound, True)
                sound.setRTPC(ComplexSoundConstants.RTPC_EXT_SPG_SIGHT, distToTarget)
                sound.setCallback(lambda s: self.__endSoundCallback(soundId, s, True))
                sound.play()
        except Exception:
            _logger.exception('play wpn_artillery_distant_threat sound exception')

        return

    def __endSoundCallback(self, soundID, sound, hasMatrix=False):
        self.__soundStop(sound, hasMatrix)
        self.__activeSounds.pop(soundID, None)
        return

    def __soundStop(self, sound, hasMatrix=False):
        if sound is not None:
            sound.stop()
            if hasMatrix:
                sound.releaseMatrix()
        return
