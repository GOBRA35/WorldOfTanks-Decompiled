# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/missions/regular/mission_details_container_view.py
from async import async, await
from gui.Scaleform.daapi import LobbySubView
from gui.Scaleform.daapi.view.lobby.missions import missions_helper
from gui.Scaleform.daapi.view.lobby.missions.regular.group_packers import getGroupPackerByContextID
from gui.Scaleform.daapi.view.meta.MissionDetailsContainerViewMeta import MissionDetailsContainerViewMeta
from gui.Scaleform.genConsts.QUESTS_ALIASES import QUESTS_ALIASES
from gui.impl import backport
from gui.impl.gen import R
from gui.impl.gen.view_models.views.lobby.secret_event.action_menu_model import ActionMenuModel
from gui.server_events.events_helpers import isDailyQuest, isPremium
from gui.server_events.formatters import parseComplexToken
from gui.shared import events, event_bus_handlers, EVENT_BUS_SCOPE, event_dispatcher
from helpers import dependency
from skeletons.gui.server_events import IEventsCache
from gui.prb_control.settings import PREBATTLE_ACTION_NAME
from adisp import process
from gui.prb_control.dispatcher import g_prbLoader
from gui.prb_control.entities.base.ctx import PrbAction

class MissionDetailsContainerView(LobbySubView, MissionDetailsContainerViewMeta):
    eventsCache = dependency.descriptor(IEventsCache)
    __showDQInMissionsTab = False
    __metaclass__ = event_bus_handlers.EventBusListener

    def __init__(self, ctx=None):
        super(MissionDetailsContainerView, self).__init__(ctx)
        self.__ctx = ctx
        self.__groupPacker = None
        self.__quests = {}
        return

    def closeView(self):
        self.destroy()

    def requestMissionData(self, index):
        missionData = self.__datailedList[index]
        self.as_setMissionDataS(missionData)
        self.onChangePage(missionData['eventID'])

    def onTokenBuyClick(self, tokenId, questId):
        self.fireEvent(events.OpenLinkEvent(events.OpenLinkEvent.TOKEN_SHOP, params={'name': parseComplexToken(tokenId).webID}))

    def onToEventClick(self):
        if self._secretEventTabMenuItem:
            self.__doSelectAction(PREBATTLE_ACTION_NAME.EVENT_BATTLE)

    def onChangePage(self, eventID):
        vehicleSelector = self.getComponent(QUESTS_ALIASES.MISSIONS_VEHICLE_SELECTOR_ALIAS)
        if vehicleSelector is None:
            return
        else:
            quest = self.__quests.get(eventID)
            criteria, extraConditions = missions_helper.getDetailedMissionData(quest).getVehicleRequirementsCriteria()
            vehicleSelector.as_closeS()
            if criteria and not quest.isCompleted():
                vehicleSelector.setCriteria(criteria, extraConditions)
            else:
                vehicleSelector.as_hideSelectedVehicleS()
            return

    @classmethod
    def setShowDQInMissionsTab(cls, value):
        cls.__showDQInMissionsTab = value

    def _populate(self):
        super(MissionDetailsContainerView, self)._populate()
        self.eventsCache.onSyncCompleted += self.__setData
        self.__setData(needDemand=True)

    def _invalidate(self, ctx=None):
        self.__ctx = ctx
        self.__setData(needDemand=False)

    def _dispose(self):
        self.eventsCache.onSyncCompleted -= self.__setData
        self.__quests = None
        if self.__groupPacker is not None:
            self.__groupPacker.clear()
            self.__groupPacker = None
        super(MissionDetailsContainerView, self)._dispose()
        return

    @async
    def __setData(self, needDemand=True):
        if needDemand:
            yield await(self.eventsCache.prefetcher.demand())

        def missionsFilter(q):
            checkDaily = True if self.__showDQInMissionsTab else not isDailyQuest(q.getID()) and not isPremium(q.getID())
            return checkDaily and q.getFinishTimeLeft()

        self.__quests = self.eventsCache.getQuests(missionsFilter)
        eventID = self.__ctx.get('eventID')
        groupID = self.__ctx.get('groupID')
        self._secretEventTabMenuItem = self.__ctx.get('secretEventTabMenuItem')
        if self.__groupPacker is not None:
            self.__groupPacker.clear()
        self.__groupPacker = getGroupPackerByContextID(groupID, self.eventsCache)
        self.__datailedList = []
        if self.__groupPacker is not None:
            for quest in self.__groupPacker.findEvents(self.__quests):
                data = missions_helper.getDetailedMissionData(quest).getInfo()
                self.__datailedList.append(data)

        else:
            quest = self.__quests.get(eventID)
            if quest is not None:
                self.__datailedList.append(missions_helper.getDetailedMissionData(quest).getInfo())
        if not self.__datailedList:
            self.closeView()
        else:
            pages = [ {'buttonsGroup': 'MissionDetailsPageGroup',
             'pageIndex': i,
             'label': '%i' % (i + 1),
             'tooltip': mission.get('statusTooltipData'),
             'status': mission.get('status'),
             'selected': eventID == mission.get('eventID')} for i, mission in enumerate(self.__datailedList) ]
            self.as_setInitDataS({'pages': pages})
            backButton = R.strings.quests.backButton
            if self._secretEventTabMenuItem is not None:
                self.as_showBackButtonS(backport.text(backButton.label()), backport.text(backButton.description()))
            else:
                self.as_hideBackButtonS()
        return

    @event_bus_handlers.eventBusHandler(events.HideWindowEvent.HIDE_MISSION_DETAILS_VIEW, EVENT_BUS_SCOPE.LOBBY)
    def __handleDetailsClose(self, _):
        self.destroy()

    @process
    def __doSelectAction(self, actionName):
        result = yield g_prbLoader.getDispatcher().doSelectAction(PrbAction(actionName))
        if self._secretEventTabMenuItem != ActionMenuModel.BASE and result:
            event_dispatcher.loadSecretEventTabMenu(self._secretEventTabMenuItem)
