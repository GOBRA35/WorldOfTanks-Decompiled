# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/shared/messages/player_messages.py
import logging
import SoundGroups
from constants import EQUIPMENT_STAGES
from gui.Scaleform.daapi.view.battle.shared.messages import fading_messages
from gui.battle_control import avatar_getter
from items import vehicles
from gui.sounds.epic_sound_constants import EPIC_SOUND
_logger = logging.getLogger(__name__)
_ID_TO_DESTRUCTIBLE_ENTITY_NAME = {1: '1',
 2: '2',
 3: '3',
 4: '4',
 5: '5'}

class PlayerMessages(fading_messages.FadingMessages):

    def __init__(self):
        super(PlayerMessages, self).__init__('PlayerMessagesPanel', 'player_messages_panel.xml')

    def __del__(self):
        _logger.debug('PlayerMessages panel is deleted')

    def _addGameListeners(self):
        super(PlayerMessages, self)._addGameListeners()
        ctrl = self.sessionProvider.shared.messages
        if ctrl is not None:
            ctrl.onShowPlayerMessageByCode += self.__onShowPlayerMessageByCode
            ctrl.onShowPlayerMessageByKey += self.__onShowPlayerMessageByKey
            ctrl.onShowDestructibleEntityMessageByCode += self.__onShowDestructibleEntityMessageByCode
        ctrl = self.sessionProvider.shared.equipments
        if ctrl is not None:
            ctrl.onEquipmentUpdated += self.__onCombatEquipmentUpdated
        arena = avatar_getter.getArena()
        if arena:
            arena.onCombatEquipmentUsed += self.__onCombatEquipmentUsed
        return

    def _removeGameListeners(self):
        ctrl = self.sessionProvider.shared.messages
        if ctrl is not None:
            ctrl.onShowPlayerMessageByCode -= self.__onShowPlayerMessageByCode
            ctrl.onShowPlayerMessageByKey -= self.__onShowPlayerMessageByKey
            ctrl.onShowDestructibleEntityMessageByCode -= self.__onShowDestructibleEntityMessageByCode
        ctrl = self.sessionProvider.shared.equipments
        if ctrl is not None:
            ctrl.onEquipmentUpdated -= self.__onCombatEquipmentUpdated
        arena = avatar_getter.getArena()
        if arena:
            arena.onCombatEquipmentUsed -= self.__onCombatEquipmentUsed
        super(PlayerMessages, self)._removeGameListeners()
        return

    def __onShowDestructibleEntityMessageByCode(self, code, entityID, attackerID):
        _logger.debug('onShowDestructibleEntityMessage %r %r %r', code, entityID, attackerID)
        getFullName = self.sessionProvider.getCtx().getPlayerFullName
        self.showMessage(code, {'target': _ID_TO_DESTRUCTIBLE_ENTITY_NAME[entityID],
         'attacker': getFullName(attackerID, showClan=False)})

    def __onShowPlayerMessageByCode(self, code, postfix, targetID, attackerID, equipmentID):
        _logger.debug('onShowPlayerMessage %r %r %r %r %r', code, postfix, targetID, attackerID, equipmentID)
        getFullName = self.sessionProvider.getCtx().getPlayerFullName
        if equipmentID:
            equipment = vehicles.g_cache.equipments().get(equipmentID)
            if equipment is not None:
                postfix = '_'.join((postfix, equipment.equipmentName))
        self.showMessage(code, {'target': getFullName(targetID, showClan=False),
         'attacker': getFullName(attackerID, showClan=False)}, extra=(('target', targetID), ('attacker', attackerID)), postfix=postfix)
        return

    def __onShowPlayerMessageByKey(self, key, args=None, extra=None):
        self.showMessage(key, args, extra)

    def __onCombatEquipmentUpdated(self, _, item):
        if item.getPrevStage() in (EQUIPMENT_STAGES.DEPLOYING, EQUIPMENT_STAGES.UNAVAILABLE, EQUIPMENT_STAGES.COOLDOWN) and item.getStage() == EQUIPMENT_STAGES.READY:
            postfix = item.getDescriptor().equipmentName
            self.showMessage('COMBAT_EQUIPMENT_READY', {}, postfix=postfix)

    def __onCombatEquipmentUsed(self, shooterID, eqID):
        battleCxt = self.sessionProvider.getCtx()
        if not battleCxt.isCurrentPlayer(shooterID):
            equipment = vehicles.g_cache.equipments().get(eqID)
            getFullName = battleCxt.getPlayerFullName
            if equipment is not None:
                postfix = equipment.equipmentName
                self.showMessage('COMBAT_EQUIPMENT_USED', {'player': getFullName(shooterID, showClan=False)}, extra=(('player', shooterID),), postfix=postfix)
        else:
            equipment = vehicles.g_cache.equipments().get(eqID)
            if equipment is None:
                return
            postfix = equipment.equipmentName
            if postfix in EPIC_SOUND.BF_EB_ABILITY_LIST:
                soundNotifications = avatar_getter.getSoundNotifications()
                if soundNotifications is not None:
                    notification = EPIC_SOUND.BF_EB_ABILITY_USED.get(postfix, None)
                    if notification is not None:
                        soundNotifications.play(notification)
            elif postfix in EPIC_SOUND.BF_EB_EQUIPMENT_SOUND_LIST:
                if getattr(equipment, 'wwsoundEquipmentUsed', None):
                    if SoundGroups.g_instance:
                        SoundGroups.g_instance.playSound2D(equipment.wwsoundEquipmentUsed)
                    else:
                        _logger.warning('Can not play "%s" ability. SoundGroups.g_instance is None', postfix)
        return
