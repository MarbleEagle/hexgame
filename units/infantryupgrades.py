'''
Created on Jun 9, 2015

@author: Joseph Lim
'''
from units.basetypes import BaseUpgrade

##########################################################################
#    Infantry logistics upgrades
##########################################################################


class UpgradeAmmo(BaseUpgrade):
    name = 'Extra ammo'
    cost = 5

    def upgrade(self, internal):
        for weapon in internal.weapons:
            weapon.ammo = round(weapon.ammo * 1.5)


class UpgradeFuel(BaseUpgrade):
    name = 'Extra Supplies'
    cost = 20

    def upgrade(self, internal):
        internal.fuel = internal.fuel * 1.5


##############################################################################
#    Infantry Defense upgrades
##############################################################################
class UpgradeInfantryArmorLight(BaseUpgrade):
    name = 'Kevlar IIB Vests'
    cost = 50

    def upgrade(self, internal):
        internal.soft_defense_max += 1


class UpgradeInfantryArmorHeavy(BaseUpgrade):
    name = 'Kevlar/Ceramic III Vests'
    cost = 100

    def upgrade(self, internal):
        internal.soft_defense_max += 2
        internal.movement -= 1


class UpgradeInfantryArmorPowered(BaseUpgrade):
    name = 'Light Exoskeleton'
    cost = 200

    def upgrade(self, internal):
        internal.armor += 1
