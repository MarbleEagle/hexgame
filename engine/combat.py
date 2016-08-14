'''
Created on Jun 11, 2015

@author: Joseph Lim
'''
from copy import copy
import functools
import itertools
import random

from engine.unitstats import UnitStatisticsCalculator


class CombatEngine(object):

    """ Handles intern unit combat and resolution """

    def __init__(self, context):
        self.context = context
        self.logs = []

    def _getSoftInternals(self, unit):
        """ Hard vehicle shell stops soft attack. Return all exposed internals,
        and unarmoured subunit internals

        :return:list: [ (internal, subunit), ... ] """
        isValidUnarmoured = lambda x: x.armour < 1 and x.isAlive
        validTargets = [(internal, unit) for internal in filter(
            isValidUnarmoured, unit._internalCriticals)]

        for subUnit in filter(isValidUnarmoured, unit._internalSubUnits):
            validTargets += [
                (internal, subUnit) for internal in
                filter(isValidUnarmoured, subUnit._internalCriticals)]
        return validTargets

    def _executeCombatRound(self, attackerUnitCell, defenderUnitCell, combatRange):
        """ One round of combat """
        aLog = []
        dLog = []

        # 1. Initiative - whether one side shoots first or simultaneously
        aInitiativeModifiers = getattr(
            attackerUnitCell, 'initiativeMods', {}).values()
        dInitiativeModifiers = getattr(
            defenderUnitCell, 'initiativeMods', {}).values()

        aInitiative = sum(v for _, _, v in aInitiativeModifiers)
        dInitiative = sum(v for _, _, v in dInitiativeModifiers)
        initiative = aInitiative - dInitiative
        log = [
            'Initiative: Attacker {0} versus Defender {1} - '.format(aInitiative, dInitiative)]

        if initiative > 1:
            aLog += self._combatRound(attackerUnitCell, defenderUnitCell)
            dLog += self._combatRound(defenderUnitCell, attackerUnitCell)
            log[0] += 'Attacker Assault'
            log += aLog + dLog
        elif initiative < -1:
            dLog += self._combatRound(defenderUnitCell, attackerUnitCell)
            aLog += self._combatRound(attackerUnitCell, defenderUnitCell)
            log[0] += 'Defender Ambush'
            log += dLog + aLog
        else:
            attackerUnitCellSnapshot = copy(attackerUnitCell)
            defenderUnitCellSnapshot = copy(defenderUnitCell)
            aLog += self._combatRound(attackerUnitCellSnapshot,
                                      defenderUnitCell)
            dLog += self._combatRound(defenderUnitCellSnapshot,
                                      attackerUnitCell)
            UnitStatisticsCalculator.updateStatistics(attackerUnitCell)
            UnitStatisticsCalculator.updateStatistics(defenderUnitCell)

            log[0] += 'Meeting Engagement'
            log += aLog + dLog
        return log

    def _combatRound(self, attackerUnitCell, defenderUnitCell):
        log = ['\n{0} attacks {1}'.format(attackerUnitCell.unit.name,
                                          defenderUnitCell.unit.name)]
        # H. Hard attack phase
        '''if defender.armourNet > 0: # At least one armoured
            _hardCombat(attackerUnitCell, defenderUnitCell)'''

        # S. Soft attack phase
        if defenderUnitCell.unit.armour == 0:  # Exposed unarmoured element
            log += self._softCombat(attackerUnitCell, defenderUnitCell)

        # 2. Recalculate unit statistics
        UnitStatisticsCalculator.updateStatistics(defenderUnitCell)

        return log

    def _softCombat(self, attackerUnitCell, defenderUnitCell):
        """ Attacker does soft damage, returns combatLog """
        attacker = attackerUnitCell.unit
        defender = defenderUnitCell.unit
        dDSnapshot = copy(defender.softDefense)
        combatRange = attackerUnitCell.getDistance(defenderUnitCell)

        # S1. Calculate modified attack
        attackModifiers = getattr(
            attackerUnitCell, 'softAttackMods', {}).values()
        attack = attacker.getSoftAttack(combatRange) * functools.reduce(
            lambda x, y: x * y, (v for _, _, v in attackModifiers), 1)

        # S2. Calculate hit shift
        hitModifiers = getattr(
            defenderUnitCell, 'hitRatioMods', {}).values()
        hit = sum(v for _, _, v in hitModifiers)

        # S3. Calculate damage
        damage = max(attack - defender.softDefense, 0)
        suppression = attack - damage
        damage = damage * max((1 - 0.2 * hit), 0.1)
        suppression = suppression * max((1 - 0.2 * hit), 0.1)

        # S4. Inflict damage
        destroyedCriticals = []
        validTargets = self._getSoftInternals(defender)
        if validTargets:
            for _i in range(0, round(damage)):
                destroyedCriticals.append(random.choice(validTargets))

        for critical, _parent in destroyedCriticals:
            critical.isAlive = False
            critical.weapons = []

        # S5. Inflict suppression on remaining live targets
        validTargets = self._getSoftInternals(defender)
        suppressionRemaining = copy(suppression)
        for critical, _parent in validTargets:
            suppressionRemaining -= critical.soft_defense
            critical.soft_defense = 0
            if suppressionRemaining < 1:
                break

        # S6. Reduce ammunition counts and set state flag
        for weapon in filter(lambda x: x.soft_attack > 0,
                             attacker.getAvaliableWeapons(combatRange)):
            weapon.ammo -= 1
        attacker.hasFired = True

        # S7. Compile combat log
        log = ['** Soft Attack **']

        log.append(
            '{0} Attack versus {1} Defence'.format(
                attack, dDSnapshot))

        for name, _, v in attackModifiers:
            log.append('{0}: {1}%'.format(name, round((v - 1) * 100)))

        log.append('\n{0} Hits, {1} Suppression'.format(
            round(damage), round(suppression)))

        for name, _, v in hitModifiers:
            log.append('Defender {0}: {1}'.format(name, -v))

        destroyedCriticals = sorted(
            set(destroyedCriticals), key=lambda x: str(x[1]))
        for parent, men in itertools.groupby(
                destroyedCriticals, lambda x: x[1]):
            men = list(men)
            log.append('\n{0} - {1} destroyed'.format(
                parent.name, len(men)))
            log += ['**{0}** destroyed'.format(i.name)
                    for i, _parent in men]
        return log


if __name__ == '__main__':
    engine = CombatEngine([])
    from units.infantryunits import getNATOReservePlatoon, getNATOMechanisedPlatoon
    from units.infantryinternals import NATOReservist, NATORegular, NATOElite
    from units.smallarms import RifleNATOEarly, GrenadeLauncherLightNATO
    from units.basetypes import UnitCell
    from numpy import array
    plA = getNATOReservePlatoon(NATOReservist, RifleNATOEarly)
    unitA = UnitCell(plA, 1, array([0, 0, 0]), None)

    plB = getNATOMechanisedPlatoon(NATOReservist, RifleNATOEarly)
    unitB = UnitCell(plB, 1, array([0, 0, 0]), None)

    def _oneRound(unitA, unitB):
        print(unitA.unit)
        print(unitB.unit)
        print('=' * 100)
        logs = engine._executeCombatRound(unitA, unitB, 1)
        for log in logs:
            print(log)
        print('=' * 100)

    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
    _oneRound(unitA, unitB)
