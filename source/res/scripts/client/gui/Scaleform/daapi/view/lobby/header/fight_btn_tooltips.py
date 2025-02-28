# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/header/fight_btn_tooltips.py
import typing
from gui.impl import backport
from gui.impl.gen import R
from gui.prb_control.formatters.tooltips import getAbsenceCrewList
from gui.prb_control.settings import UNIT_RESTRICTION
from gui.prb_control.settings import PRE_QUEUE_RESTRICTION, PREBATTLE_RESTRICTION
from gui.Scaleform.locale.MENU import MENU
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.shared.formatters import text_styles, icons
from gui.shared.formatters.ranges import toRomanRangeString
from gui.shared.gui_items.Vehicle import getTypeUserName
from gui.shared.utils.functions import makeTooltip
from helpers import i18n
if typing.TYPE_CHECKING:
    from gui.prb_control.items import ValidationResult
_STR_PATH = R.strings.menu.headerButtons.fightBtn.tooltip

def getSquadFightBtnTooltipData(state):
    if state == UNIT_RESTRICTION.COMMANDER_VEHICLE_NOT_SELECTED:
        header = backport.text(R.strings.tooltips.hangar.startBtn.squadNotReady.header())
        body = backport.text(R.strings.tooltips.hangar.startBtn.squadNotReady.body())
    elif state == UNIT_RESTRICTION.VEHICLE_INVALID_LEVEL:
        header = backport.text(R.strings.tooltips.hangar.tankCarusel.wrongSquadVehicle.header())
        body = backport.text(R.strings.tooltips.hangar.tankCarusel.wrongSquadVehicle.body())
    elif state == UNIT_RESTRICTION.SPG_IS_FULL or state == UNIT_RESTRICTION.SPG_IS_FORBIDDEN:
        header = backport.text(R.strings.tooltips.hangar.tankCarusel.wrongSquadSPGVehicle.header())
        body = backport.text(R.strings.tooltips.hangar.tankCarusel.wrongSquadSPGVehicle.body())
    elif state == UNIT_RESTRICTION.SCOUT_IS_FULL or state == UNIT_RESTRICTION.SCOUT_IS_FORBIDDEN:
        header = backport.text(R.strings.tooltips.hangar.tankCarusel.wrongSquadSPGVehicle.header())
        body = backport.text(R.strings.tooltips.hangar.tankCarusel.wrongSquadSPGVehicle.body())
    else:
        return ''
    return makeTooltip(header, body)


def getRankedFightBtnTooltipData(result):
    state = result.restriction
    resShortCut = R.strings.menu.headerButtons.fightBtn.tooltip
    if state == PRE_QUEUE_RESTRICTION.MODE_NOT_SET:
        header = backport.text(resShortCut.rankedNotSet.header())
        body = backport.text(resShortCut.rankedNotSet.body())
    elif state == PRE_QUEUE_RESTRICTION.MODE_NOT_AVAILABLE:
        header = backport.text(resShortCut.rankedDisabled.header())
        body = backport.text(resShortCut.rankedDisabled.body())
    elif state == PRE_QUEUE_RESTRICTION.LIMIT_LEVEL:
        levelStr = toRomanRangeString(result.ctx['levels'])
        levelSubStr = backport.text(resShortCut.rankedVehLevel.levelSubStr(), levels=levelStr)
        header = backport.text(resShortCut.rankedVehLevel.header())
        body = backport.text(resShortCut.rankedVehLevel.body(), levelSubStr=text_styles.neutral(levelSubStr))
    elif state == PRE_QUEUE_RESTRICTION.LIMIT_VEHICLE_TYPE:
        typeSubStr = text_styles.neutral(result.ctx['forbiddenType'])
        header = backport.text(resShortCut.rankedVehType.header())
        body = backport.text(resShortCut.rankedVehType.body(), forbiddenType=typeSubStr)
    elif state == PRE_QUEUE_RESTRICTION.LIMIT_VEHICLE_CLASS:
        classSubStr = text_styles.neutral(getTypeUserName(result.ctx['forbiddenClass'], False))
        header = backport.text(resShortCut.rankedVehClass.header())
        body = backport.text(resShortCut.rankedVehClass.body(), forbiddenClass=classSubStr)
    else:
        return ''
    return makeTooltip(header, body)


def getEpicFightBtnTooltipData(result):
    state = result.restriction
    if state == PRE_QUEUE_RESTRICTION.MODE_NOT_AVAILABLE:
        header = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.battleRoyaleDisabled.header())
        body = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.battleRoyaleDisabled.body())
    elif state == PRE_QUEUE_RESTRICTION.LIMIT_LEVEL:
        header = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleVehLevel.header())
        body = text_styles.main(backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleVehLevel.body(), requirements=text_styles.neutral(backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleVehLevel.requirements(), level=toRomanRangeString(result.ctx['levels'])))))
    elif state == PRE_QUEUE_RESTRICTION.VEHICLE_WILL_BE_UNLOCKED:
        rStringShort = R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleSituationalVehicle
        header = backport.text(rStringShort.header())
        body = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleSituationalVehicle.body(), forStartBattle=text_styles.neutral(backport.text(rStringShort.levels.forStartBattle(), levels=toRomanRangeString(result.ctx['vehicleLevelsForStartBattle']))), willBeUnlocked=text_styles.neutral(backport.text(rStringShort.levels.willBeUnlocked(), levels=toRomanRangeString(result.ctx['unlockableInBattleVehLevels']))))
    elif state == UNIT_RESTRICTION.UNSUITABLE_VEHICLE:
        header = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyaleSquadNotReady.wrongVehicle.header())
        body = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyaleSquadNotReady.wrongVehicle.body())
    elif state == UNIT_RESTRICTION.UNIT_NOT_FULL:
        header = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyaleSquadNotReady.wrongPlayers.header())
        body = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyaleSquadNotReady.wrongPlayers.body())
    elif state == UNIT_RESTRICTION.NOT_READY_IN_SLOTS:
        header = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyaleSquadNotReady.notReady.header())
        body = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyaleSquadNotReady.notReady.body())
    elif state == UNIT_RESTRICTION.CURFEW:
        header = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.battleRoyaleDisabled.header())
        body = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.battleRoyaleDisabled.body())
    elif state == PREBATTLE_RESTRICTION.VEHICLE_NOT_SUPPORTED:
        header = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.unsutableToBattleRoyale.header())
        body = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.unsutableToBattleRoyale.body())
    elif state == UNIT_RESTRICTION.COMMANDER_VEHICLE_NOT_SELECTED:
        header = backport.text(R.strings.tooltips.hangar.startBtn.squadNotReady.header())
        body = backport.text(R.strings.tooltips.hangar.startBtn.squadNotReady.body())
    elif state == PREBATTLE_RESTRICTION.VEHICLE_RENTALS_IS_OVER:
        header = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyale.notRented.header())
        body = backport.text(R.strings.tooltips.hangar.startBtn.battleRoyale.notRented.body())
    else:
        return ''
    return makeTooltip(header, body)


def getMapsTrainingTooltipData():
    header = backport.text(R.strings.tooltips.hangar.startBtn.mapsTraining.notReady.header())
    body = backport.text(R.strings.tooltips.hangar.startBtn.mapsTraining.notReady.body())
    return makeTooltip(header, body)


def getUnsuitableToQueueTooltipData(result):
    state = result.restriction
    if state in (PREBATTLE_RESTRICTION.VEHICLE_NOT_SUPPORTED, UNIT_RESTRICTION.VEHICLE_WRONG_MODE, PREBATTLE_RESTRICTION.VEHICLE_RENTALS_IS_OVER):
        header = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleOnly.header())
        body = backport.text(R.strings.menu.headerButtons.fightBtn.tooltip.epicBattleOnly.body())
        return makeTooltip(header, body)


def getSandboxTooltipData(result):
    state = result.restriction
    return makeTooltip(i18n.makeString(MENU.HEADERBUTTONS_FIGHTBTN_TOOLTIP_SANDBOX_INVALID_HEADER), i18n.makeString(MENU.HEADERBUTTONS_FIGHTBTN_TOOLTIP_SANDBOX_INVALID_LEVEL_BODY, levels=toRomanRangeString(result.ctx['levels'], 1))) if state == PRE_QUEUE_RESTRICTION.LIMIT_LEVEL else ''


def getEventTooltipData():
    header = i18n.makeString(TOOLTIPS.EVENT_SQUAD_DISABLE_HEADER)
    body = i18n.makeString(TOOLTIPS.EVENT_SQUAD_DISABLE_BODY, tankName='')
    return makeTooltip(header, body)


def getPreviewTooltipData():
    body = i18n.makeString(TOOLTIPS.HANGAR_STARTBTN_PREVIEW_BODY)
    return makeTooltip(None, body)


def getRandomTooltipData(result):
    state = result.restriction
    if state == PREBATTLE_RESTRICTION.VEHICLE_BROKEN:
        header = backport.text(_STR_PATH.vehicleIsBroken.header())
        body = backport.text(_STR_PATH.vehicleIsBroken.body())
    elif state == PREBATTLE_RESTRICTION.CREW_NOT_FULL:
        header = backport.text(_STR_PATH.crewNotFull.header())
        body = backport.text(_STR_PATH.crewNotFull.body(), crewList=getAbsenceCrewList())
    elif state == PREBATTLE_RESTRICTION.VEHICLE_NOT_SUPPORTED:
        header = backport.text(_STR_PATH.notSupported.header())
        body = backport.text(_STR_PATH.notSupported.body())
    elif state == PREBATTLE_RESTRICTION.VEHICLE_IN_PREMIUM_IGR_ONLY:
        header = backport.text(_STR_PATH.inPremiumIgrOnly.header(), icon=icons.premiumIgrSmall())
        body = backport.text(_STR_PATH.inPremiumIgrOnly.body())
    elif state == PREBATTLE_RESTRICTION.VEHICLE_NOT_PRESENT:
        header = backport.text(_STR_PATH.noVehicle.header())
        body = backport.text(_STR_PATH.noVehicle.body())
    elif state == PREBATTLE_RESTRICTION.VEHICLE_RENTALS_IS_OVER:
        header = backport.text(_STR_PATH.rentalIsOver.header())
        body = backport.text(_STR_PATH.rentalIsOver.body())
    else:
        return ''
    return makeTooltip(header, body)


def getMapboxFightBtnTooltipData(result):
    strPath = R.strings.mapbox.headerButtons.fightBtn.tooltip
    strAddPath = R.strings.tooltips.hangar
    restriction = result.restriction
    if restriction == PRE_QUEUE_RESTRICTION.MODE_NOT_AVAILABLE or restriction == UNIT_RESTRICTION.CURFEW:
        header = backport.text(strPath.disabled.header())
        body = backport.text(strPath.disabled.text())
    elif restriction == PRE_QUEUE_RESTRICTION.LIMIT_LEVEL:
        levels = backport.text(strPath.mapboxVehLevel.levelSubStr(), levels=toRomanRangeString(result.ctx['levels']))
        header = backport.text(strPath.mapboxVehLevel.header())
        body = backport.text(strPath.mapboxVehLevel.body(), levelSubStr=levels)
    elif restriction == UNIT_RESTRICTION.COMMANDER_VEHICLE_NOT_SELECTED:
        header = backport.text(strAddPath.startBtn.squadNotReady.header())
        body = backport.text(strAddPath.startBtn.squadNotReady.body())
    elif restriction == UNIT_RESTRICTION.VEHICLE_INVALID_LEVEL:
        header = backport.text(strAddPath.tankCarusel.wrongSquadVehicle.header())
        body = backport.text(strAddPath.tankCarusel.wrongSquadVehicle.body())
    elif restriction == UNIT_RESTRICTION.SPG_IS_FULL or restriction == UNIT_RESTRICTION.SPG_IS_FORBIDDEN:
        header = backport.text(strAddPath.tankCarusel.wrongSquadSPGVehicle.header())
        body = backport.text(strAddPath.tankCarusel.wrongSquadSPGVehicle.body())
    else:
        return getRandomTooltipData(result)
    return makeTooltip(header, body)
