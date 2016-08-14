'''
Created on Jun 19, 2015

@author: Joseph Lim
'''
from engine.actions import getMovementRange


class UnitCache(object):

    # Unit modifiers
    softAttackMods = {}    # %SA modifier
    movementMods = {}      # %Move modifier
    hitRatioMods = {}      # +Shift hits (SA - SD)
    initiativeMods = {}    # Determines attack initiative

    # Game optimisation caches
    movementRange = {}      # All cells that the unit can move to
    visionRange = {}        # All cells that the unit can fire upon


class UnitStatisticsCalculator(object):

    """ Every turn or post combat: updates the unit combat stats """

    @classmethod
    def updateStatistics(cls, unitCell, terrainMap=None):
        """ Main method which updates all stats on the given unit """
        if not unitCell.unit.isAlive or not unitCell.refreshCache:
            return

        unitCell.cache = UnitCache()
        unitCell.refreshCache = False

        cls._updateSupressionModifiers(unitCell)
        cls._updateLeadershipModifiers(unitCell)
        cls._updateMovementModifiers(unitCell)
        cls._updateSizeModifiers(unitCell)
        cls._updateVehicleModifier(unitCell)

        if terrainMap:
            [terrainCell] = [
                cell for cell in terrainMap.cells if
                (cell.ordinate == unitCell.ordinate).all()
            ]

            cls._updateMovementModifiers(unitCell, terrainCell)

    @classmethod
    def _updateMovementRange(cls, unitCell, terrainMap):
        """ Cache all cells which the unit can move to as a dict of
        destination: movement cost """
        movement = unitCell.unit.get('movement', 1)
        movementCostType = 'passability_{0}'.format(
            unitCell.unit.get('movementType', 'foot'))

        terrainCells = terrainMap.context.view_terrain.cells
        terrainMovementCosts = {
            c.ordinate: getattr(c, movementCostType) for c in terrainCells}

        movementRangeOrdinates = getMovementRange(
            unitCell.ordinate, movement, terrainMovementCosts)
        movementRangeCells = [
            c for c in terrainCells if c.ordinate in movementRangeOrdinates]
        unitCell.cache.movementRange = movementRangeCells

    @classmethod
    def _updateSupressionModifiers(cls, unitCell):
        """ Cache the effects of enemy fire - fire effectiveness
        is captured by soft defence reduction (HP decrease) """
        combatUnit = unitCell.unit
        cache = unitCell.cache
        manpower = combatUnit.manpower.manpower

        pinnedMsg = 'This unit cannot take any actions due to heavy fire'
        suppresssedMsg = 'This unit is suppressed by enemy fire'

        # Pinned - Less than 0.5 SD per man
        if combatUnit.softDefense * 2 <= manpower:
            cache.softAttackMods['suppression'] = (
                'Pinned', pinnedMsg, 0.25)
            cache.movementMods['suppression'] = ('Pinned', pinnedMsg, 0)
            cache.hitRatioMods['suppression'] = (
                'Taking cover', 'suppresssedMsg', 1)

        # Suppressed - Less than 50% SD left
        elif combatUnit.softDefense * 2 <= combatUnit.softDefenseMax:
            cache.softAttackMods['suppression'] = (
                'Suppressed', suppresssedMsg, 0.5)
            cache.movementMods['suppression'] = (
                'Suppressed', suppresssedMsg, 0.5)
            cache.hitRatioMods['suppression'] = (
                'Taking cover', 'suppresssedMsg', 1)

    @classmethod
    def _updateLeadershipModifiers(cls, unitCell):
        """ Officer and NCO ratio are force multipliers to platoon effectiveness
        poor leadership kills, good leadership allows for tactical exploits """
        combatUnit = unitCell.unit
        cache = unitCell.cache
        manpower = combatUnit.manpower.manpower
        leadership = combatUnit.manpower.leadership
        leadershipRatio = leadership / manpower

        # Elite team - 2 NCO + 2 men recce teams or elite sections
        if leadershipRatio >= 0.5:
            cache.softAttackMods['leadership'] = (
                'Elite',
                'Elite teams easily achieve tactical superiority',
                1.5)
            cache.initiativeMods['leadership'] = (
                'Elite',
                'Elite teams are masters of camouflage and spotting the enemy',
                2)

        # High - 1 PC (3) + 1 PS(1) + 6 Sec Coms/2ICs(6)
        elif leadershipRatio > 1 / 3:
            msg = 'NCO heavy units are cohesive and highly flexible'
            cache.softAttackMods['leadership'] = (
                'Effective leadership', msg, 1.25)
            cache.initiativeMods['leadership'] = (
                'Effective leadership',
                'Officers/NCOs maintain high camouflage and patrol discipline',
                1)

        # Average Leadership - 1 PC (3) + 1 PS(1) + 3 Sec Coms (3) per PL (30)
        elif leadershipRatio > 0.2:
            pass

        # Poor - 1 PC (3) + 1 PS(1), rest enlisted, typical conscript unit
        elif leadershipRatio > 1 / 8:
            msg = 'This unit is almost all enlisted'
            cache.softAttackMods['leadership'] = (
                'Poor leadership', msg, 0.75)

        # Terrible - 1..3 surviving leaders. Depleted or penal unit
        elif leadership >= 1:
            msg = 'This unit has few if any leaders remaining'
            cache.softAttackMods['leadership'] = (
                'Fractured leadership', msg, 0.5)
            cache.movementMods['leadership'] = (
                'Fractured leadership', msg, 0.75)

        else:
            msg = 'This unit is leader-less and has ceased to be effective'
            cache.softAttackMods['leadership'] = ('Broken', msg, 0)
            cache.movementMods['leadership'] = ('Broken', msg, 0.5)

    @classmethod
    def _updateTerrainModifiers(cls, unitCell, terrainCell):
        """ Terrain provides cover and concealment. Cover blocks incoming
        fire while concealment determines attacker/ambush initiative """
        cover = terrainCell.defense_cover
        unitCell.hitRatioMods['terrain'] = (
            terrainCell.terrain_name,
            'Terrain determines how exposed the unit is to enemy fire',
            cover)

        concealment = terrainCell.defense_concealment
        unitCell.initiativeMods['terrain'] = (
            terrainCell.terrain_name,
            'Terrain determines how easy it is to ambush the enemy',
            concealment)

    @classmethod
    def _updateMovementModifiers(cls, unitCell):
        """ The state of the unit determines its tactical position. A stationary
        unit has had time to setup its heavy weapons, lay an ambush and
        entrench itself. A moving unit has greater attack capabilities
        due to concentration of force """
        combatUnit = unitCell.unit
        if combatUnit.hasMoved:
            unitCell.softAttackMods['movement'] = (
                'Combat Advance',
                'Advancing units have greater tactical flexibility',
                0.2)
            if combatUnit.hasFired:
                unitCell.initiativeMods['movement'] = (
                    'Firing',
                    'Firing gives away your position',
                    -3)
            else:
                unitCell.initiativeMods['movement'] = (
                    'Combat Advance',
                    'Moving units are far easier to spot',
                    -1)
        else:
            unitCell.hitRatioMods['movement'] = (
                'Defending',
                'Stationary units have had time to entrench themselves',
                1)
            if combatUnit.hasFired:
                unitCell.initiativeMods['movement'] = (
                    'Firing',
                    'Firing gives away your position',
                    -3)
            else:
                unitCell.initiativeMods['movement'] = (
                    'Ambush',
                    'Stationary units are concealed in ambush positions',
                    1)

    @classmethod
    def _updateSizeModifiers(cls, unitCell):
        """ Small units easily conceal themselves while larger units
        have economy of force - mainly gives bonuses to weapons teams
        and sniper units """
        combatUnit = unitCell.unit
        manpower = sum(man.isAlive for man in combatUnit.internalCriticals)

        if manpower <= 2:
            unitCell.initiativeMods['size'] = (
                'Tiny unit',
                'Lone or pairs of soldiers are almost impossible to detect',
                2)
        elif manpower <= 4:
            unitCell.initiativeMods['size'] = (
                'Small unit',
                'Small teams are not easily spotted',
                1)
        elif manpower >= 40:
            unitCell.initiativeMods['size'] = (
                'Large unit',
                'Large units are easily spotted due to their large footprint',
                -1)

    @classmethod
    def _updateVehicleModifier(cls, unitCell):
        """ Armoured vehicles are protected and mount heavy weapons but are
        loud and noisy due to the horsepower requirements """
        combatUnit = unitCell.unit
        armourScore = round(combatUnit.armourNet ** 0.5)

        if armourScore < 1:
            return

        if combatUnit.hasMoved:
            unitCell.initiativeMods['vehicle'] = (
                'Moving Vehicle',
                'Moving vehicles are loud and noisy',
                -armourScore)
        else:
            unitCell.movementMods['vehicle'] = (
                'Stationary Vehicle',
                'Heavier vehicles take longer to manoeuvre into formation',
                max(1 - 0.25 * armourScore, 0.5))


if __name__ == '__main__':
    pass
    '''from units.infantryunits import getNATOReservePlatoon, getNATOMechanisedPlatoon
    from units.infantrytypes import NATOReservist, NATORegular, NATOElite
    from units.smallarms import RifleNATOEarly, GrenadeLauncherLightNATO
    from units.basetypes import UnitCell
    from numpy import array
    unitA = getNATOReservePlatoon(NATORegular, RifleNATOEarly)
    unitB = getNATOMechanisedPlatoon(NATOElite, RifleNATOEarly)
    unitB.hasMoved = True
    unit = UnitCell(unitB, 1, array([0, 0, 0]), None)

    UnitStatisticsCalculator.updateStatistics(unit)
    print(unit.softAttackMods.items())
    print(unit.movementMods.items())
    print(unit.hitRatioMods.items())
    print(unit.initiativeMods.items())'''
