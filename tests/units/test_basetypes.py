'''
Created on Jun 11, 2015

@author: Joseph Lim
'''
from copy import copy
import unittest
from units.basetypes import (BaseInternal, BaseUnit, BaseUpgrade,
                             BaseUnit, BaseWeapon)


class TestWeapon(BaseWeapon):
    name = 'Test weapon'
    cost = 10
    ammo_max = 5
    ammo_nominal = 20


class TestUpgrade(BaseUpgrade):
    name = 'Test upgrade'
    cost = 3

    def upgrade(self, internals):
        internals.name += ' Upgraded'


class Test(unittest.TestCase):

    def test_baseInternal(self):
        # Test weapon
        weapon = TestWeapon()
        self.assertEqual(weapon.ammo, 5)
        self.assertEqual(weapon.cost, 10)
        self.assertEqual(weapon.name, 'Test weapon')

        # Test upgrade
        upgrade = TestUpgrade()
        self.assertEqual(upgrade.cost, 3)

        # Test internal
        internal = BaseInternal(
            name='Test', soft_defense_max=2, armour=1, fuel_max=3, _cost=10,
            weapons=[weapon], upgrades=[upgrade])

        self.assertTrue(internal.isAlive)
        self.assertEqual(internal.soft_defense, 2)
        self.assertEqual(internal.fuel, 3)
        self.assertEqual(internal._cost, 10)
        self.assertEqual(internal.cost, 23)
        self.assertEqual(internal.name, 'Test Upgraded')

    def test_baseUnit(self):
        internalA = BaseInternal(
            name='Test', soft_defense_max=2, armour=1, fuel_max=3, _cost=10,
            weapons=[TestWeapon()], upgrades=[TestUpgrade()],
            movement_passability={'A': 0.5, 'B': 0.2})

        internalB = BaseInternal(
            name='Test', soft_defense_max=4, armour=0, fuel_max=3, _cost=10,
            weapons=[TestWeapon()], upgrades=[],
            movement_passability={'A': 0.2, 'B': 0.5})

        unit = BaseUnit(name='Test Unit', internals=[internalA, internalB])

        self.assertEqual(unit.name, 'Test Unit')
        self.assertEqual(unit.cost, 43)
        self.assertEqual(len(unit.weapons), 2)
        self.assertEqual(unit.softDefense, 6)
        self.assertEqual(unit.softDefenseMax, 6)
        self.assertEqual(unit.armour, 0)
        self.assertEqual(unit.movementPassability, {'A': 0.5, 'B': 0.5})
        self.assertEqual(unit.internalCriticals, [internalA, internalB])

        platoon = BaseUnit(
            name='Unit of units', internals=[copy(unit), copy(unit)])
        self.assertEqual(platoon.name, 'Unit of units')
        self.assertEqual(platoon.cost, 86)
        self.assertEqual(len(platoon.weapons), 4)
        self.assertEqual(platoon.softDefense, 12)
        self.assertEqual(platoon.softDefenseMax, 12)
        self.assertEqual(platoon.armour, 0)
        self.assertEqual(platoon.movementPassability, {'A': 0.5, 'B': 0.5})
        self.assertEqual(len(platoon.internalCriticals), 4)

if __name__ == "__main__":
    unittest.main()
