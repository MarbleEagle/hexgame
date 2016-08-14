'''
Created on Jun 7, 2015

@author: Joseph Lim
'''
from map.hexgrid import HexCell
from map.unitmap import UnitMap


class UnitCell(HexCell):

    def __init__(self, unit, owner, position, iconFlags):
        """ Actual board counter object - holds graphical data as well

        :param: unit: BaseUnit: 
           unit object from units.basetypes

        :param: owner: int: 
            The player index of the unit's owner

        :param: position: array: 
            The current hexagonal coordinates of this counter

        :param: iconFlags, list(enum):
            When rendering the unit icon, each flag will cause a specific
            unit type to be rendered (linear combination) """
        self.unit = unit
        self.owner = owner
        self.iconFlags = iconFlags
        self.isActive = True  # Toggle once move/actions is complete
        self.reRender = True  # Trigger graphics re-rendering
        self.ordinate = position


class BaseUnit(object):

    """ A single board token - a collection of constituent units
     (Platoon made of men etc.)"""
    internals = []
    name = 'Unit name'

    # Combat states
    hasMoved = False
    hasFired = False

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        _cache = self.internalCriticals

        for internal in self.internals:
            internal._parent = self

    def __repr__(self):
        return """{0}-(${1}). Attack: {2}, Defence:{3}/{4}, Armour:{5},
        Move:{6}[{9}/{10} l], Special:{7} Leadership, {8} Medical""".format(
            self.name,
            self.cost,
            self.getSoftAttack(2),
            self.softDefense,
            self.softDefenseMax,
            self.armour,
            self.movement,
            self.leadership,
            self.medical,
            self.fuel,
            self.fuelMax
        )

    def _sumNestedProperty(self, criticalAttr, subUnitAttr, initialValue=0):
        result = initialValue
        for internal in self._internalCriticals:
            if internal.isAlive:
                result += getattr(internal, criticalAttr)
        for internal in self._internalSubUnits:
            result += getattr(internal, subUnitAttr)
        return result

    def _minNestedProperty(self, criticalAttr, subUnitAttr):
        result = []
        for internal in self._internalCriticals:
            if internal.isAlive:
                result.append(getattr(internal, criticalAttr))
        for internal in self._internalSubUnits:
            result.append(getattr(internal, subUnitAttr))
        return min(result or [0])

    @property
    def isAlive(self):
        return any(crit for crit in self.internalCriticals if crit.isAlive)

    @property
    def _internalCriticals(self):
        return list(
            filter(lambda x: isinstance(x, BaseInternal), self.internals))

    @property
    def _internalSubUnits(self):
        return list(filter(lambda x: isinstance(x, BaseUnit), self.internals))

    @property
    def internalCriticals(self):
        """ Expensive, cache this """
        if getattr(self, '_allInternals', None):
            return self._allInternals
        else:
            results = self._internalCriticals
            for subUnit in self._internalSubUnits:
                results += subUnit.internalCriticals
            self._allInternals = results
            return results

    @property
    def cost(self):
        """ All weapons """
        return self._sumNestedProperty('cost', 'cost')

    @property
    def weapons(self):
        """ All weapons """
        return self._sumNestedProperty('weapons', 'weapons', [])

    @property
    def softDefense(self):
        """ Total current soft defence """
        return self._sumNestedProperty('soft_defense', 'softDefense')

    @property
    def softDefenseMax(self):
        """ Total maximum soft defence """
        return self._sumNestedProperty('soft_defense_max', 'softDefenseMax')

    @property
    def leadership(self):
        """ Total unit leadership """
        return self._sumNestedProperty('leadership', 'leadership')

    @property
    def medical(self):
        """ Total unit medical capabilities """
        return self._sumNestedProperty('medical', 'medical')

    @property
    def armour(self):
        """ Report lowest armour for focus fire -> Rolls against subunits """
        return self._minNestedProperty('armour', 'armour')

    @property
    def armourNet(self):
        """ Report the total armour """
        return self._sumNestedProperty('armour', 'armour')

    @property
    def fuel(self):
        """ Total fuel reserve """
        return self._sumNestedProperty('fuel', 'fuel')

    @property
    def fuelMax(self):
        """ Total maximum fuel capacity """
        return self._sumNestedProperty('fuel_max', 'fuelMax')

    @property
    def movement(self):
        """ The unit moves at the slowest component's speed """
        return self._minNestedProperty('movement', 'movement')

    @property
    def movementPassability(self):
        """ The unit movement penalties are the max of each subunit """
        result = {}
        for internal in self._internalCriticals:
            if internal.isAlive:
                for k, v in internal.movement_passability.items():
                    result[k] = max(result.get(k, 0), v)
        for internal in self._internalSubUnits:
            for k, v in internal.movementPassability.items():
                result[k] = max(result.get(k, 0), v)
        return result

    def getAvaliableWeapons(self, combatRange, armor=0):
        results = []
        for weapon in self.weapons:
            if (
                weapon.range >= combatRange and
                weapon.ammo > 0 and
                weapon.hard_attack >= armor and
                (not self.hasMoved or (
                    self.hasMoved and weapon.moving_fire))):

                results.append(weapon)
        return results

    def getSoftAttack(self, combatRange):
        """ Unit fires all weapons with ammo """
        softAttack = 0
        for weapon in self.getAvaliableWeapons(combatRange):
            softAttack += weapon.soft_attack
        return softAttack


class BaseWeapon(object):

    """ Each internal can have 0..* weapons """
    name = 'Generic weapon'
    cost = 0

    soft_attack = 1         # Number of attack dice rolls
    hard_attack = 0         # AP score.
    range = 1               # Range in hexes
    moving_fire = False     # Can move and fire on the same turn?

    ammo_max = 0            # Can fire for x turns before running out
    # Display info only. Each firing turn uses these many units
    ammo_nominal = 10

    def __init__(self):
        self.ammo = self.ammo_max


class BaseUpgrade(object):

    """ Each internal can have 0..2 upgrades """
    name = 'Generic upgrade'
    cost = 0

    def upgrade(self, internal):
        """ Increases some statistics of self """


class BaseInternal(object):

    """ A constituent of a unit """
    name = 'Internal'
    _cost = 0

    weapons = []            # Can have 0..* weapons
    upgrades = []
    soft_defense_max = 0    # Depletes, negates this many attack rolls
    leadership = 0          # NCO/Officer bonuses scale of this
    medical = 0     # Medical/Mitigation. Chance of avoiding critical damage.
    armour = 0              # Negates all attacks with AP below this threshold

    movement = 1            # Base movement in cells
    movement_passability = {}  # Terrain modifiers
    fuel_movement_cost = 0  # Each base movement uses this much fuel/rations
    fuel_max = 0            # Max fuel carried by the unit/rations

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        for upgrade in self.upgrades:
            upgrade.upgrade(self)

        self.fuel = self.fuel_max
        self.soft_defense = self.soft_defense_max
        self.isAlive = True

    @property
    def cost(self):
        """ Total cost of all equipment """
        result = self._cost
        for weapon in self.weapons:
            result += weapon.cost
        for upgrade in self.upgrades:
            result += upgrade.cost
        return result
