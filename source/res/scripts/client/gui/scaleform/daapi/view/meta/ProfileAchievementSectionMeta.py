# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/ProfileAchievementSectionMeta.py
from gui.Scaleform.daapi.view.meta.ProfileSectionWithTabsMeta import ProfileSectionWithTabsMeta

class ProfileAchievementSectionMeta(ProfileSectionWithTabsMeta):

    def as_setRareAchievementDataS(self, rareID, rareIconId):
        return self.flashObject.as_setRareAchievementData(rareID, rareIconId) if self._isDAAPIInited() else None
