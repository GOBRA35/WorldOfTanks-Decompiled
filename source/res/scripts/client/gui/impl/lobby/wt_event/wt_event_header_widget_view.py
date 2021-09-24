# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/lobby/wt_event/wt_event_header_widget_view.py
from account_helpers import AccountSettings
from account_helpers.AccountSettings import EVENT_LAST_COLLECTION_SEEN
from frameworks.wulf import ViewFlags, ViewSettings
from gui.Scaleform.daapi.view.meta.WhiteTigerWidgetMeta import WhiteTigerWidgetMeta
from gui.shared.event_dispatcher import showEventCollectionWindow
from gui.impl.gen import R
from gui.impl.gen.view_models.views.lobby.wt_event.wt_event_header_widget_view_model import WtEventHeaderWidgetViewModel
from gui.impl.lobby.wt_event.tooltips.wt_event_header_widget_tooltip_view import WtEventHeaderWidgetTooltipView
from gui.impl.pub import ViewImpl
from helpers import dependency
from skeletons.gui.game_control import IGameEventController
from skeletons.gui.shared import IItemsCache

class WTEventHeaderWidgetComponent(WhiteTigerWidgetMeta):

    def __init__(self):
        super(WTEventHeaderWidgetComponent, self).__init__()
        self.__isSmall = False
        self.__view = None
        return

    def setIsSmall(self, value):
        self.__isSmall = value
        if self.__view is not None:
            self.__view.setIsSmall(self.__isSmall)
        return

    def _dispose(self):
        self.__view = None
        super(WTEventHeaderWidgetComponent, self)._dispose()
        return

    def _makeInjectView(self):
        self.__view = WTEventHeaderWidgetView(self.as_setIsMouseEnabledS, flags=ViewFlags.COMPONENT)
        self.__view.setIsSmall(self.__isSmall)
        return self.__view


class WTEventHeaderWidgetView(ViewImpl):
    __gameEventCtrl = dependency.descriptor(IGameEventController)
    __itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self, setIsMouseEnabled, flags=ViewFlags.VIEW):
        settings = ViewSettings(R.views.lobby.wt_event.WTEventHeaderWidget())
        settings.flags = flags
        settings.model = WtEventHeaderWidgetViewModel()
        self.__setIsMouseEnabled = setIsMouseEnabled
        self.__isSmall = False
        super(WTEventHeaderWidgetView, self).__init__(settings)

    @property
    def viewModel(self):
        return self.getViewModel()

    def setIsSmall(self, value):
        if self.viewModel.proxy:
            self.viewModel.setIsSmall(value)
        self.__isSmall = value

    def createToolTipContent(self, event, contentID):
        return WtEventHeaderWidgetTooltipView()

    def _onLoading(self, *args, **kwargs):
        super(WTEventHeaderWidgetView, self)._onLoading(*args, **kwargs)
        self.__addListeners()
        self.__updateViewModel()

    def _finalize(self):
        self.__removeListeners()
        self.__setIsMouseEnabled = None
        super(WTEventHeaderWidgetView, self)._finalize()
        return

    def __addListeners(self):
        self.viewModel.onClick += self.__onClick
        AccountSettings.onSettingsChanging += self.__onAccountSettingsChanging
        self.__itemsCache.onSyncCompleted += self.__onSyncCompleted

    def __removeListeners(self):
        self.viewModel.onClick -= self.__onClick
        AccountSettings.onSettingsChanging -= self.__onAccountSettingsChanging
        self.__itemsCache.onSyncCompleted -= self.__onSyncCompleted

    def __onSyncCompleted(self, _, __):
        self.__updateViewModel()

    def __onAccountSettingsChanging(self, key, _):
        if key == EVENT_LAST_COLLECTION_SEEN:
            self.__updateIsNewItems()

    def __onClick(self):
        showEventCollectionWindow()

    def __updateViewModel(self):
        self.__setIsMouseEnabled(True)
        totalProgress = self.__gameEventCtrl.getCollectionSize()
        currentProgress = self.__gameEventCtrl.getCollectionProgress()
        tooltip = R.views.lobby.wt_event.tooltips.WtEventHeaderWidgetTooltipView()
        with self.viewModel.transaction() as model:
            model.setIsSmall(self.__isSmall)
            model.setTooltipID(tooltip)
            model.setAllCollected(currentProgress == totalProgress)
            self.__updateIsNewItems()

    def __updateIsNewItems(self):
        with self.viewModel.transaction() as model:
            previous = AccountSettings.getSettings(EVENT_LAST_COLLECTION_SEEN)
            current = self.__gameEventCtrl.getCollectionProgress()
            model.setIsNewItem(current > previous)
