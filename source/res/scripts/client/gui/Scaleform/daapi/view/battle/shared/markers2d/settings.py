# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/battle/shared/markers2d/settings.py
from Math import Vector3
from gui.shared import EVENT_BUS_SCOPE
SCOPE = EVENT_BUS_SCOPE.BATTLE
MARKER_POSITION_ADJUSTMENT = Vector3(0.0, 12.0, 0.0)
MARKERS_MANAGER_SWF = 'battleVehicleMarkersApp.swf'
MARKERS_COLOR_SCHEME_PREFIX = 'vm_'

class MARKER_SYMBOL_NAME(object):
    VEHICLE_MARKER = 'VehicleMarker'
    EVENT_VEHICLE_MARKER = 'EventVehicleMarker'
    TARGET_MARKER = 'TargetMarker'
    EQUIPMENT_MARKER = 'FortConsumablesMarker'
    LOCATION_MARKER = 'LocationMarkerUI'
    ATTENTION_MARKER = 'AttentionMarkerUI'
    SHOOTING_MARKER = 'AimMarkerUI'
    NAVIGATION_MARKER = 'NavigationMarkerUI'
    SAFE_ZONE_MARKER = 'SafeZoneIndicatorUI'
    STATIC_OBJECT_MARKER = 'StaticObjectMarker'
    STATIC_ARTY_MARKER = 'StaticArtyMarkerUI'
    SECTOR_BASE_TYPE = 'SectorBaseMarkerUI'
    HEADQUARTER_TYPE = 'HeadquarterMarkerUI'
    STEP_REPAIR_MARKER_TYPE = 'ResupplyMarkerUI'
    WAYPOINT_MARKER = 'SectorWaypointMarkerUI'
    SECTOR_WARNING_MARKER = 'SectorWarningMarkerUI'
    EVENT_VOLOT_MARKER = 'EventVolotMarkerUI'
    EVENT_DEATH_ZONE_MARKER = 'DeathZoneMarkerUI'


class DAMAGE_TYPE(object):
    FROM_UNKNOWN = 0
    FROM_ALLY = 1
    FROM_ENEMY = 2
    FROM_SQUAD = 3
    FROM_PLAYER = 4
