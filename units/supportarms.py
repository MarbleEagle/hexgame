'''
Created on Jun 7, 2015

@author: Joseph Lim
'''
from units.basetypes import BaseWeapon


##########################################################################
#    Single shot rocket launchers
#    NATO - Heavy, anti-tank
#    Pact - Lighter, soft-attack (RPG)
##########################################################################


class RocketNATOBasic(BaseWeapon):
    name = 'M72 LAW'
    cost = 30

    hard_attack = 2
    range = 2
    moving_fire = True

    ammo_max = 1
    ammo_nominal = 1


class RocketWarsawBasic(BaseWeapon):
    name = 'RPG-7'
    cost = 20

    hard_attack = 2
    soft_attack = 6
    range = 2
    moving_fire = True

    ammo_max = 1
    ammo_nominal = 1


class RocketNATO1(BaseWeapon):
    name = 'SMAW - HEDP'
    cost = 60

    soft_attack = 8
    hard_attack = 2
    range = 5
    moving_fire = True

    ammo_max = 1
    ammo_nominal = 1


class RocketNATO2(BaseWeapon):
    name = 'SMAW - HEAT'
    cost = 60

    hard_attack = 3
    range = 5
    moving_fire = True

    ammo_max = 1
    ammo_nominal = 1


class RocketWarsaw1(BaseWeapon):
    name = 'RPG-27'
    cost = 40

    soft_attack = 8
    hard_attack = 3
    range = 2
    moving_fire = True

    ammo_max = 1
    ammo_nominal = 1


class RocketWarsaw2(BaseWeapon):
    name = 'RPO-A Shmel'
    cost = 60

    soft_attack = 16
    range = 6
    moving_fire = True

    ammo_max = 1
    ammo_nominal = 1

##########################################################################
#   Heavy Anti-tank: ATGMS or Recoiless rifles. All need setup
#    NATO: Cheap, low ROF
#    PACT: PL weapon, expensive, superior
##########################################################################


class AntiTankNNATOBasic1(BaseWeapon):
    name = 'M2CG Carl Gustaf - HEAT'
    cost = 200

    hard_attack = 3
    range = 4
    moving_fire = False

    ammo_max = 1
    ammo_nominal = 4


class AntiTankNNATOBasic2(BaseWeapon):
    name = 'M2CG Carl Gustaf - HE'
    cost = 100

    soft_attack = 10
    range = 4
    moving_fire = False

    ammo_max = 1
    ammo_nominal = 2


class AntiTankNNATOAdvanced(BaseWeapon):
    name = 'FGM-148 Javelin'
    cost = 200

    hard_attack = 5
    range = 10
    moving_fire = False

    ammo_max = 1
    ammo_nominal = 1


class AntiTankWarsawAdvanced(BaseWeapon):
    name = '9K111 Fagot'
    cost = 200

    hard_attack = 4
    range = 12
    moving_fire = False

    ammo_max = 4
    ammo_nominal = 1


class AntiTankNATOHeavy(BaseWeapon):
    name = 'BGM-71 TOW'
    cost = 1000

    hard_attack = 5
    range = 20
    moving_fire = False

    ammo_max = 1
    ammo_nominal = 4


class AntiTankWarsawHeavy(BaseWeapon):
    name = '9M133 Kornet'
    cost = 800

    hard_attack = 5
    range = 16
    moving_fire = False

    ammo_max = 1
    ammo_nominal = 1
