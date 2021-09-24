# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/battle_results/service.py
import logging
import typing
import BigWorld
import Event
from adisp import async, process
from Account import PlayerAccount
from constants import ARENA_BONUS_TYPE, PREMIUM_TYPE
from arena_bonus_type_caps import ARENA_BONUS_TYPE_CAPS
from debug_utils import LOG_CURRENT_EXCEPTION, LOG_WARNING
from gui import SystemMessages
from gui.Scaleform.locale.BATTLE_RESULTS import BATTLE_RESULTS
from gui.battle_results import composer
from gui.battle_results import emblems
from gui.battle_results import context
from gui.battle_results import reusable
from gui.battle_results import stored_sorting
from gui.battle_results.composer import StatsComposer
from gui.battle_results.presenter.presenter import DataPresenter
from gui.battle_results.br_constants import PremiumState, POSTBATTLE20_ARENAS
from gui.battle_results.reusable.progress import VehicleProgressHelper
from gui.battle_pass.battle_pass_helpers import setInBattleProgress
from gui.shared import event_dispatcher
from gui.shared import g_eventBus, events
from gui.shared.utils import decorators
from gui.shared.gui_items.processors.common import BattleResultsGetter, PremiumBonusApplier
from helpers import dependency
import personal_missions
from skeletons.gui.battle_results import IBattleResultsService
from skeletons.gui.battle_session import IBattleSessionProvider
from skeletons.gui.lobby_context import ILobbyContext
from skeletons.gui.shared import IItemsCache
from skeletons.gui.server_events import IEventsCache
from soft_exception import SoftException
from shared_utils import first
from shared_utils.account_helpers.battle_results_helpers import getEmptyClientPB20UXStats
_logger = logging.getLogger(__name__)

class BattleResultsService(IBattleResultsService):
    itemsCache = dependency.descriptor(IItemsCache)
    sessionProvider = dependency.descriptor(IBattleSessionProvider)
    lobbyContext = dependency.descriptor(ILobbyContext)
    eventsCache = dependency.descriptor(IEventsCache)
    __slots__ = ('__composers', '__buy', '__eventsManager', 'onResultPosted', '__appliedAddXPBonus', '__presenter', '__arenaBonusTypes')

    def __init__(self):
        super(BattleResultsService, self).__init__()
        self.__composers = {}
        self.__presenter = None
        self.__arenaBonusTypes = {}
        self.__buy = set()
        self.__appliedAddXPBonus = set()
        self.__eventsManager = Event.EventManager()
        self.onResultPosted = Event.Event(self.__eventsManager)
        return

    def init(self):
        self.__presenter = DataPresenter()
        g_eventBus.addListener(events.GUICommonEvent.LOBBY_VIEW_LOADED, self.__handleLobbyViewLoaded)
        g_eventBus.addListener(events.LobbySimpleEvent.PREMIUM_BOUGHT, self.__onPremiumBought)

    def fini(self):
        g_eventBus.removeListener(events.GUICommonEvent.LOBBY_VIEW_LOADED, self.__handleLobbyViewLoaded)
        g_eventBus.removeListener(events.LobbySimpleEvent.PREMIUM_BOUGHT, self.__onPremiumBought)
        self.clear()
        self.__presenter.fini()
        self.__presenter = None
        self.__arenaBonusTypes = None
        return

    def clear(self):
        while self.__composers:
            _, item = self.__composers.popitem()
            item.clear()

        self.__eventsManager.clear()
        self.__presenter.clear()

    @async
    @process
    def requestResults(self, ctx, callback=None):
        arenaUniqueID = ctx.getArenaUniqueID()
        if not ctx.resetCache() and arenaUniqueID in self.__composers:
            isSuccess = True
            self.__showBattleResultsImmediatelyIfNeeded(ctx)

            def dummy(callback=None):
                if callback is not None:
                    callback(None)
                return

            yield dummy
            self.__notifyBattleResultsPosted(arenaUniqueID, needToShowUI=ctx.needToShowIfPosted())
        else:
            results = yield BattleResultsGetter(arenaUniqueID).request()
            if not results.success and ctx.getArenaBonusType() == ARENA_BONUS_TYPE.MAPS_TRAINING:
                results = yield self.waitForBattleResults(arenaUniqueID)
            isSuccess = results.success
            if not isSuccess or not self.postResult(results.auxData, ctx.needToShowIfPosted()):
                self.__composers.pop(arenaUniqueID, None)
            else:
                self.__showBattleResultsImmediatelyIfNeeded(ctx)
                self.__notifyBattleResultsPosted(arenaUniqueID)
        if callback is not None:
            callback(isSuccess)
        return

    @async
    def requestEmblem(self, ctx, callback=None):
        fetcher = emblems.createFetcher(ctx)
        if fetcher is not None:
            fetcher.fetch(callback)
        else:
            LOG_WARNING('Icon fetcher is not found', ctx)
            if callback is not None:
                callback(None)
        return

    def postResult(self, result, needToShowUI=True):
        reusableInfo = reusable.createReusableInfo(result)
        if reusableInfo is None:
            SystemMessages.pushI18nMessage(BATTLE_RESULTS.NODATA, type=SystemMessages.SM_TYPE.Warning)
            return False
        else:
            self.__updateReusableInfo(reusableInfo)
            self.__updateBattlePassInfo(reusableInfo)
            arenaUniqueID = reusableInfo.arenaUniqueID
            arenaBonusType = reusableInfo.common.arenaBonusType
            self.__arenaBonusTypes[arenaUniqueID] = arenaBonusType
            composerObj = composer.createComposer(reusableInfo)
            composerObj.setResults(result, reusableInfo)
            self.__presenter.addBattleResult(reusableInfo, result)
            self.__composers[arenaUniqueID] = composerObj
            resultsWindow = self.__notifyBattleResultsPosted(arenaUniqueID, needToShowUI=needToShowUI)
            self.onResultPosted(reusableInfo, composerObj, resultsWindow)
            self.__postStatistics(reusableInfo, result)
            return True

    def areResultsPosted(self, arenaUniqueID):
        return arenaUniqueID in self.__composers

    def getResultsVO(self, arenaUniqueID):
        if arenaUniqueID in self.__composers:
            found = self.__composers[arenaUniqueID]
            vo = found.getVO()
        else:
            vo = None
        return vo

    @property
    def presenter(self):
        return self.__presenter

    def popResultsAnimation(self, arenaUniqueID):
        if arenaUniqueID in self.__composers:
            found = self.__composers[arenaUniqueID]
            vo = found.popAnimation()
        else:
            vo = None
        return vo

    def saveStatsSorting(self, bonusType, iconType, sortDirection):
        stored_sorting.writeStatsSorting(bonusType, iconType, sortDirection)

    @decorators.process('updating')
    def applyAdditionalBonus(self, arenaUniqueID):
        arenaInfo = self.__getAdditionalXPBattles().get(arenaUniqueID)
        if arenaInfo is None:
            return
        else:
            result = yield PremiumBonusApplier(arenaUniqueID, arenaInfo.vehicleID).request()
            if result and result.userMsg:
                SystemMessages.pushMessage(result.userMsg, type=result.sysMsgType)
            if result.success:
                self.__appliedAddXPBonus.add(arenaUniqueID)
                yield self.__updateComposer(arenaUniqueID)
                self.__onAddXPBonusChanged()
            return

    def isAddXPBonusApplied(self, arenaUniqueID):
        return arenaUniqueID in self.__appliedAddXPBonus

    def isAddXPBonusEnabled(self, arenaUniqueID):
        return arenaUniqueID in self.__getAdditionalXPBattles() and self.itemsCache.items.stats.isPremium

    def getAdditionalXPValue(self, arenaUniqueID):
        arenaInfo = self.__getAdditionalXPBattles().get(arenaUniqueID)
        return 0 if arenaInfo is None else arenaInfo.extraXP

    def canApplyAdditionalXPBonus(self, arenaBonusType):
        isBonusEnabled = self.lobbyContext.getServerSettings().getAdditionalBonusConfig().get('enabled', False)
        bonusLeft = self.itemsCache.items.stats.applyAdditionalXPCount
        hasPremium = self.itemsCache.items.stats.isActivePremium(PREMIUM_TYPE.PLUS)
        isProperArena = ARENA_BONUS_TYPE_CAPS.checkAny(arenaBonusType, ARENA_BONUS_TYPE_CAPS.ADDITIONAL_XP_POSTBATTLE)
        return hasPremium and isBonusEnabled and isProperArena and bonusLeft > 0

    def isCrewSameForArena(self, arenaUniqueID):
        arenaInfo = self.__getAdditionalXPBattles().get(arenaUniqueID)
        vehicle = self.getVehicleForArena(arenaUniqueID)
        if arenaInfo is not None and vehicle is not None:
            currentCrew = set((tankman.invID for _, tankman in vehicle.crew if tankman is not None))
            lastCrew = set((tankmanID for tankmanID, _ in arenaInfo.extraTmenXP))
            return currentCrew == lastCrew
        else:
            return False

    def isXPToTManSameForArena(self, arenaUniqueID):
        arenaInfo = self.__getAdditionalXPBattles().get(arenaUniqueID)
        vehicle = self.getVehicleForArena(arenaUniqueID)
        return vehicle.isXPToTman == arenaInfo.isXPToTMan if arenaInfo is not None and vehicle is not None else False

    def getVehicleForArena(self, arenaUniqueID):
        arenaInfo = self.__getAdditionalXPBattles().get(arenaUniqueID)
        return self.itemsCache.items.getItemByCD(arenaInfo.vehicleID) if arenaInfo is not None else None

    def __postStatistics(self, reusableInfo, result):
        playerAccount = BigWorld.player()
        if playerAccount is None or not isinstance(playerAccount, PlayerAccount):
            raise SoftException('Could not post afterbattle statistics, possible not in hangar')
        if reusableInfo.common.arenaBonusType != ARENA_BONUS_TYPE.REGULAR:
            _logger.debug('Only random battles results are logging')
            return
        else:
            statisticsResult = getEmptyClientPB20UXStats()
            vehTypeCompDescr, vData = first(reusableInfo.personal.getVehicleCDsIterator(result['personal']))
            statisticsResult['vehTypeCompDescr'] = vehTypeCompDescr
            if reusableInfo.economics.isPostBattlePremiumPlus:
                statisticsResult['premiumType'] = PREMIUM_TYPE.PLUS
            elif reusableInfo.economics.isPostBattlePremium:
                statisticsResult['premiumType'] = PREMIUM_TYPE.BASIC
            else:
                statisticsResult['premiumType'] = PREMIUM_TYPE.NONE
            statisticsResult['timestamp'] = result['common'].get('arenaCreateTime', 0)
            statisticsResult['arenaTypeID'] = reusableInfo.common.arenaTypeID
            personalMissions = {}
            questsProgress = reusableInfo.progress.getQuestsProgress()
            if questsProgress:
                linkedsetQuests = self.eventsCache.getLinkedSetQuests()
                premiumQuests = self.eventsCache.getPremiumQuests()
                allCommonQuests = self.eventsCache.getQuests()
                allCommonQuests.update(self.eventsCache.getHiddenQuests(lambda q: q.isShowedPostBattle()))
                for qID, qProgress in questsProgress.iteritems():
                    _, pPrev, pCur = qProgress
                    isCompleted = pCur.get('bonusCount', 0) - pPrev.get('bonusCount', 0) > 0
                    if qID in allCommonQuests:
                        if qID in linkedsetQuests:
                            questType = 'linkedset'
                        elif qID in premiumQuests:
                            questType = 'premium'
                        else:
                            questType = 'other'
                        if isCompleted:
                            statisticsResult[questType + 'QuestsCompleted'] += 1
                        else:
                            statisticsResult[questType + 'QuestsInProgress'] += 1
                    if personal_missions.g_cache.isPersonalMission(qID):
                        pqID = personal_missions.g_cache.getPersonalMissionIDByUniqueID(qID)
                        questsCache = self.eventsCache.getPersonalMissions()
                        quest = questsCache.getAllQuests()[pqID]
                        personalMissions.setdefault(quest, {})[qID] = isCompleted

            pm2Progress = reusableInfo.progress.getPM2Progress()
            if pm2Progress:
                quests = self.eventsCache.getPersonalMissions().getAllQuests()
                for qID, data in pm2Progress.iteritems():
                    personalMissions.setdefault(quests[qID], {}).update(data)

            pmCompletedMain = 0
            pmCompletedFull = 0
            for quest, data in personalMissions.items():
                if data.get(quest.getAddQuestID(), False):
                    pmCompletedFull += 1
                if data.get(quest.getMainQuestID(), False):
                    pmCompletedMain += 1

            statisticsResult['personalMissionsInProgress'] = len(personalMissions) - pmCompletedMain - pmCompletedFull
            statisticsResult['personalMissionsCompletedFull'] = pmCompletedFull
            statisticsResult['personalMissionsCompletedMain'] = pmCompletedMain
            vehicleBattleXp = vData.get('xp', 0)
            pureCreditsReceived = vData.get('pureCreditsReceived', 0)
            tmenXps = dict(vData.get('xpByTmen', []))
            helper = VehicleProgressHelper(vehTypeCompDescr)
            ready2UnlockVehicles, ready2UnlockModules = helper.getReady2UnlockItems(vehicleBattleXp)
            ready2BuyVehicles, ready2BuyModules = helper.getReady2BuyItems(pureCreditsReceived)
            tankmen = helper.getNewSkilledTankmen(tmenXps)
            statisticsResult['vehicleProgressReady2UnlockVehicles'] = len(ready2UnlockVehicles)
            statisticsResult['vehicleProgressReady2UnlockModules'] = len(ready2UnlockModules)
            statisticsResult['vehicleProgressReady2BuyVehicles'] = len(ready2BuyVehicles)
            statisticsResult['vehicleProgressReady2BuyModules'] = len(ready2BuyModules)
            statisticsResult['vehicleProgressTankmen'] = len(tankmen)
            playerAccount.logClientPB20UXStats(statisticsResult)
            return

    def __getAdditionalXPBattles(self):
        return self.itemsCache.items.stats.additionalXPCache

    @process
    def __showResults(self, ctx):
        yield self.requestResults(ctx)

    def __notifyBattleResultsPosted(self, arenaUniqueID, needToShowUI=False):
        composerObj = self.__composers[arenaUniqueID]
        window = None
        if needToShowUI:
            isPostbattle20Enabled = self.__isPostbattle20Enabled(arenaUniqueID)
            window = composerObj.onShowResults(arenaUniqueID, isPostbattle20Enabled)
        composerObj.onResultsPosted(arenaUniqueID)
        return window

    def __handleLobbyViewLoaded(self, _):
        battleCtx = self.sessionProvider.getCtx()
        arenaUniqueID = battleCtx.lastArenaUniqueID
        arenaBonusType = battleCtx.lastArenaBonusType or ARENA_BONUS_TYPE.UNKNOWN
        if arenaUniqueID:
            try:
                self.__showResults(context.RequestResultsContext(arenaUniqueID, arenaBonusType))
            except Exception:
                LOG_CURRENT_EXCEPTION()

            battleCtx.lastArenaUniqueID = None
            battleCtx.lastArenaBonusType = None
        return

    @async
    @process
    def __updateComposer(self, arenaUniqueID, callback):
        results = yield BattleResultsGetter(arenaUniqueID).request()
        if results.success:
            result = results.auxData
            reusableInfo = reusable.createReusableInfo(result)
            if reusableInfo is None:
                SystemMessages.pushI18nMessage(BATTLE_RESULTS.NODATA, type=SystemMessages.SM_TYPE.Warning)
                callback(False)
            self.__updateReusableInfo(reusableInfo)
            self.__updateBattlePassInfo(reusableInfo)
            arenaUniqueID = reusableInfo.arenaUniqueID
            composerObj = composer.createComposer(reusableInfo)
            composerObj.setResults(result, reusableInfo)
            self.__composers[arenaUniqueID] = composerObj
            self.__presenter.updateBattleResult(reusableInfo, result)
        callback(True)
        return

    def __updateReusableInfo(self, reusableInfo):
        arenaUniqueID = reusableInfo.arenaUniqueID
        reusableInfo.economics.premiumState = self.__makePremiumState(arenaUniqueID, PREMIUM_TYPE.BASIC)
        reusableInfo.economics.premiumPlusState = self.__makePremiumState(arenaUniqueID, PREMIUM_TYPE.PLUS)
        reusableInfo.economics.isAddXPBonusApplied = self.isAddXPBonusApplied(arenaUniqueID)
        reusableInfo.clientIndex = self.lobbyContext.getClientIDByArenaUniqueID(arenaUniqueID)

    def __updateBattlePassInfo(self, reusableInfo):
        battlePass = reusableInfo.personal.avatar.extensionInfo
        basePoints = battlePass.get('basePointsDiff', 0)
        sumPoints = battlePass.get('sumPoints', 0)
        hasBattlePass = battlePass.get('hasBattlePass', False)
        setIfEmpty = reusableInfo.common.arenaBonusType in ARENA_BONUS_TYPE.BATTLE_ROYALE_RANGE
        setInBattleProgress(reusableInfo.battlePassProgress, basePoints, sumPoints, hasBattlePass, setIfEmpty, reusableInfo.common.arenaBonusType)

    def __onPremiumBought(self, event):
        ctx = event.ctx
        arenaUniqueID = event.ctx['arenaUniqueID']
        becomePremium = event.ctx['becomePremium']
        if becomePremium and arenaUniqueID:
            self.__buy.add(arenaUniqueID)
            event_dispatcher.hideBattleResults()
            self.__showResults(context.RequestResultsContext(arenaUniqueID, resetCache=True))

    def __makePremiumState(self, arenaUniqueID, premType=PREMIUM_TYPE.BASIC):
        state = PremiumState.NONE
        settings = self.lobbyContext.getServerSettings()
        if settings is not None and settings.isPremiumInPostBattleEnabled():
            state |= PremiumState.BUY_ENABLED
        if self.itemsCache.items.stats.isActivePremium(premType):
            state |= PremiumState.HAS_ALREADY
        if arenaUniqueID in self.__buy:
            state |= PremiumState.BOUGHT
        return state

    def __onAddXPBonusChanged(self):
        g_eventBus.handleEvent(events.LobbySimpleEvent(events.LobbySimpleEvent.PREMIUM_XP_BONUS_CHANGED))

    def __showBattleResultsImmediatelyIfNeeded(self, ctx):
        if ctx.needToShowImmediately():
            arenaUniqueID = ctx.getArenaUniqueID()
            isPostbattle20Enabled = self.__isPostbattle20Enabled(arenaUniqueID)
            event_dispatcher.showBattleResultsWindow(arenaUniqueID, isPostbattle20Enabled)

    def __isPostbattle20Enabled(self, arenaUniqueID):
        postbattle20Enabled = self.lobbyContext.getServerSettings().isPostbattle20Enabled()
        arenaBonusType = self.__arenaBonusTypes.get(arenaUniqueID)
        return postbattle20Enabled and arenaBonusType in POSTBATTLE20_ARENAS

    @async
    @process
    def waitForBattleResults(self, arenaUniqueID, callback=None):

        @async
        def wait(t, callback):
            BigWorld.callback(t, lambda : callback(None))

        isSuccess = False
        results = None
        while not isSuccess:
            yield wait(1)
            results = yield BattleResultsGetter(arenaUniqueID).request()
            isSuccess = results.success

        if callback is not None:
            callback(results)
        return
