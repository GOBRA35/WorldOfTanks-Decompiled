# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/messenger/formatters/collections_by_type.py
from chat_shared import SYS_MESSAGE_TYPE as _SM_TYPE
from messenger.formatters import service_channel as _sc
from messenger.formatters import wot_plus as _wotPlusFormatters
from messenger.formatters import token_quest_subformatters
from messenger.m_constants import SCH_CLIENT_MSG_TYPE
_TOKEN_QUEST_SUB_FORMATTERS = (token_quest_subformatters.LootBoxTokenQuestFormatter(),
 token_quest_subformatters.RecruitQuestsFormatter(),
 token_quest_subformatters.RankedSeasonTokenQuestFormatter(),
 token_quest_subformatters.RankedFinalTokenQuestFormatter(),
 token_quest_subformatters.RankedYearLeaderFormatter(),
 token_quest_subformatters.SeniorityAwardsFormatter(),
 token_quest_subformatters.PersonalMissionsTokenQuestsFormatter(),
 token_quest_subformatters.BattlePassDefaultAwardsFormatter(),
 token_quest_subformatters.WotPlusDirectivesFormatter())
_PERSONAL_MISSIONS_SUB_FORMATTERS = (token_quest_subformatters.PersonalMissionsFormatter(),)
SERVER_FORMATTERS = {_SM_TYPE.serverReboot.index(): _sc.ServerRebootFormatter(),
 _SM_TYPE.serverRebootCancelled.index(): _sc.ServerRebootCancelledFormatter(),
 _SM_TYPE.battleResults.index(): _sc.BattleResultsFormatter(),
 _SM_TYPE.invoiceReceived.index(): _sc.InvoiceReceivedFormatter(),
 _SM_TYPE.adminTextMessage.index(): _sc.AdminMessageFormatter(),
 _SM_TYPE.accountTypeChanged.index(): _sc.AccountTypeChangedFormatter(),
 _SM_TYPE.giftReceived.index(): _sc.GiftReceivedFormatter(),
 _SM_TYPE.autoMaintenance.index(): _sc.AutoMaintenanceFormatter(),
 _SM_TYPE.premiumBought.index(): _sc.PremiumBoughtFormatter(),
 _SM_TYPE.premiumExtended.index(): _sc.PremiumExtendedFormatter(),
 _SM_TYPE.premiumExpired.index(): _sc.PremiumExpiredFormatter(),
 _SM_TYPE.premiumChanged.index(): _sc.PremiumChangedFormatter(),
 _SM_TYPE.prbArenaFinish.index(): _sc.PrebattleArenaFinishFormatter(),
 _SM_TYPE.prbKick.index(): _sc.PrebattleKickFormatter(),
 _SM_TYPE.prbDestruction.index(): _sc.PrebattleDestructionFormatter(),
 _SM_TYPE.vehicleCamouflageTimedOut.index(): _sc.VehCamouflageTimedOutFormatter(),
 _SM_TYPE.vehiclePlayerEmblemTimedOut.index(): _sc.VehEmblemTimedOutFormatter(),
 _SM_TYPE.vehiclePlayerInscriptionTimedOut.index(): _sc.VehInscriptionTimedOutFormatter(),
 _SM_TYPE.vehTypeLockExpired.index(): _sc.VehicleTypeLockExpired(),
 _SM_TYPE.serverDowntimeCompensation.index(): _sc.ServerDowntimeCompensation(),
 _SM_TYPE.achievementReceived.index(): _sc.AchievementFormatter(),
 _SM_TYPE.converter.index(): _sc.ConverterFormatter(),
 _SM_TYPE.tokenQuests.index(): _sc.TokenQuestsFormatter(subFormatters=_TOKEN_QUEST_SUB_FORMATTERS),
 _SM_TYPE.notificationsCenter.index(): _sc.NCMessageFormatter(),
 _SM_TYPE.clanEvent.index(): _sc.ClanMessageFormatter(),
 _SM_TYPE.fortEvent.index(): _sc.StrongholdMessageFormatter(),
 _SM_TYPE.vehicleRented.index(): _sc.VehicleRentedFormatter(),
 _SM_TYPE.rentalsExpired.index(): _sc.RentalsExpiredFormatter(),
 _SM_TYPE.potapovQuestBonus.index(): _sc.TokenQuestsFormatter(subFormatters=_PERSONAL_MISSIONS_SUB_FORMATTERS),
 _SM_TYPE.goodieRemoved.index(): _sc.GoodyRemovedFormatter(),
 _SM_TYPE.goodieDisabled.index(): _sc.GoodyDisabledFormatter(),
 _SM_TYPE.goodieEnabled.index(): _sc.GoodieEnabledFormatter(),
 _SM_TYPE.telecomOrderCreated.index(): _sc.TelecomReceivedInvoiceFormatter(),
 _SM_TYPE.telecomOrderUpdated.index(): _sc.TelecomStatusFormatter(),
 _SM_TYPE.telecomOrderDeleted.index(): _sc.TelecomRemovedInvoiceFormatter(),
 _SM_TYPE.prbVehicleKick.index(): _sc.PrbVehicleKickFormatter(),
 _SM_TYPE.prbVehicleKickFilter.index(): _sc.PrbVehicleKickFilterFormatter(),
 _SM_TYPE.vehicleGroupLocked.index(): _sc.RotationGroupLockFormatter(),
 _SM_TYPE.vehicleGroupUnlocked.index(): _sc.RotationGroupUnlockFormatter(),
 _SM_TYPE.rankedQuests.index(): _sc.RankedQuestFormatter(),
 _SM_TYPE.royaleQuests.index(): _sc.BRQuestsFormatter(),
 _SM_TYPE.bootcamp.index(): _sc.BootcampResultsFormatter(),
 _SM_TYPE.prbVehicleMaxSpgKick.index(): _sc.PrbVehicleMaxSpgKickFormatter(),
 _SM_TYPE.hangarQuests.index(): _sc.TokenQuestsFormatter(),
 _SM_TYPE.currencyUpdate.index(): _sc.CurrencyUpdateFormatter(),
 _SM_TYPE.personalMissionFailed.index(): _sc.PersonalMissionFailedFormatter(),
 _SM_TYPE.customizationChanged.index(): _sc.CustomizationChangedFormatter(),
 _SM_TYPE.lootBoxesAutoOpenReward.index(): _sc.LootBoxAutoOpenFormatter(),
 _SM_TYPE.progressiveReward.index(): _sc.ProgressiveRewardFormatter(),
 _SM_TYPE.piggyBankSmashed.index(): _sc.PiggyBankSmashedFormatter(),
 _SM_TYPE.blackMapRemoved.index(): _sc.BlackMapRemovedFormatter(),
 _SM_TYPE.enhancementRemoved.index(): _sc.EnhancementRemovedFormatter(),
 _SM_TYPE.enhancementsWiped.index(): _sc.EnhancementsWipedFormatter(),
 _SM_TYPE.battlePassReward.index(): _sc.BattlePassRewardFormatter(),
 _SM_TYPE.battlePassReachedCap.index(): _sc.BattlePassReachedCapFormatter(),
 _SM_TYPE.battlePassStyleChoiceAvailable.index(): _sc.BattlePassStyleChoiceAvailableFormatter(),
 _SM_TYPE.battlePassStyleChosen.index(): _sc.BattlePassStyleChosenFormatter(),
 _SM_TYPE.battlePassSeasonEnd.index(): _sc.BattlePassSeasonEndFormatter(),
 _SM_TYPE.badges.index(): _sc.BadgesFormatter(),
 _SM_TYPE.collectibleVehiclesUnlocked.index(): _sc.CollectibleVehiclesUnlockedFormatter(),
 _SM_TYPE.customizationProgress.index(): _sc.CustomizationProgressFormatter(),
 _SM_TYPE.dogTagsUnlockComponent.index(): _sc.DogTagComponentUnlockFormatter(),
 _SM_TYPE.dogTagsGradingChange.index(): _sc.DogTagComponentGradingFormatter(),
 _SM_TYPE.enhancementsWipedOnVehicles.index(): _sc.EnhancementsWipedOnVehiclesFormatter(),
 _SM_TYPE.prbWrongEnqueueDataKick.index(): _sc.PrbEventEnqueueDataFormatter(),
 _SM_TYPE.dedicationReward.index(): _sc.DedicationRewardFormatter(),
 _SM_TYPE.customizationProgressionChanged.index(): _sc.CustomizationProgressionChangedFormatter(),
 _SM_TYPE.wotPlusUnlocked.index(): _wotPlusFormatters.WotPlusUnlockedFormatter(),
 _SM_TYPE.wotPlusRenewed.index(): _wotPlusFormatters.WotPlusRenewedFormatter(),
 _SM_TYPE.wotPlusExpired.index(): _wotPlusFormatters.WotPlusExpiredFormatter(),
 _SM_TYPE.goldReserveIsFull.index(): _wotPlusFormatters.SimpleFormatter('GoldReserveFullMessage'),
 _SM_TYPE.passiveXPNoTank.index(): _wotPlusFormatters.SimpleFormatter('PassiveXPNoTankMessage'),
 _SM_TYPE.passiveXPIncompatibleCrew.index(): _wotPlusFormatters.SimpleFormatter('PassiveXPIncompatibleCrewMessage'),
 _SM_TYPE.wotPlusRentEnd.index(): _wotPlusFormatters.RentEnd(),
 _SM_TYPE.wotPlusNoRentSelected.index(): _wotPlusFormatters.SimpleFormatter('WotPlusRentNoRentSelectedMessage'),
 _SM_TYPE.halloweenVehicleRent.index(): _sc.VehicleRentFormatter(),
 _SM_TYPE.halloweenStyleBought.index(): _sc.StyleBoughtFormatter(),
 _SM_TYPE.halloweenStyleBoughtByGold.index(): _sc.StyleBoughtByGoldFormatter(),
 _SM_TYPE.halloweenStyleBundleBought.index(): _sc.StyleBundleFormatter(),
 _SM_TYPE.halloweenDifficultyLevelReached.index(): _sc.DifficultyLevelReachedFormatter(),
 _SM_TYPE.bestDealBandleBought.index(): _sc.BestDealBandleFormatter(),
 _SM_TYPE.eventVehiclePurchased.index(): _sc.EventVehiclePurchasedFormatter(),
 _SM_TYPE.eventTokenPurchased.index(): _sc.EventTokenPurchasedFormatter(),
 _SM_TYPE.eventC11nItemPurchased.index(): _sc.EventC11nItemPurchasedFormatter()}
CLIENT_FORMATTERS = {SCH_CLIENT_MSG_TYPE.SYS_MSG_TYPE: _sc.ClientSysMessageFormatter(),
 SCH_CLIENT_MSG_TYPE.PREMIUM_ACCOUNT_EXPIRY_MSG: _sc.PremiumAccountExpiryFormatter(),
 SCH_CLIENT_MSG_TYPE.AOGAS_NOTIFY_TYPE: _sc.AOGASNotifyFormatter(),
 SCH_CLIENT_MSG_TYPE.ACTION_NOTIFY_TYPE: _sc.ActionNotificationFormatter(),
 SCH_CLIENT_MSG_TYPE.BATTLE_TUTORIAL_RESULTS_TYPE: _sc.BattleTutorialResultsFormatter(),
 SCH_CLIENT_MSG_TYPE.KOREA_PARENTAL_CONTROL_TYPE: _sc.KoreaParentalControlFormatter(),
 SCH_CLIENT_MSG_TYPE.TECH_TREE_ACTION_DISCOUNT: _sc.TechTreeActionDiscountFormatter(),
 SCH_CLIENT_MSG_TYPE.BLUEPRINTS_CONVERT_SALE: _sc.BlueprintsConvertSaleFormatter(),
 SCH_CLIENT_MSG_TYPE.MAPBOX_PROGRESSION_REWARD: _sc.MapboxRewardReceivedFormatter(),
 SCH_CLIENT_MSG_TYPE.MAPBOX_EVENT_ENDED: _sc.MapboxEndedFormatter(),
 SCH_CLIENT_MSG_TYPE.MAPBOX_EVENT_STARTED: _sc.MapboxStartedFormatter(),
 SCH_CLIENT_MSG_TYPE.MAPBOX_SURVEY_AVAILABLE: _sc.MapboxSurveyAvailableFormatter(),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_GOLDRESERVE_ENABLED: _wotPlusFormatters.SimpleFormatter('GoldReserveEnabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_GOLDRESERVE_DISABLED: _wotPlusFormatters.SimpleFormatter('GoldReserveDisabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_PASSIVEXP_ENABLED: _wotPlusFormatters.SimpleFormatter('PassiveXpEnabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_PASSIVEXP_DISABLED: _wotPlusFormatters.SimpleFormatter('PassiveXpDisabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_TANKRENTAL_ENABLED: _wotPlusFormatters.SimpleFormatter('TankRentalEnabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_TANKRENTAL_DISABLED: _wotPlusFormatters.SimpleFormatter('TankRentalDisabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_FREEDIRECTIVES_ENABLED: _wotPlusFormatters.SimpleFormatter('FreeDirectivesEnabledMessage'),
 SCH_CLIENT_MSG_TYPE.WOTPLUS_FREEDIRECTIVES_DISABLED: _wotPlusFormatters.SimpleFormatter('FreeDirectivesDisabledMessage')}
