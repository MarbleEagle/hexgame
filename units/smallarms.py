'''
Created on Jun 7, 2015

@author: Joseph Lim
'''
from units.basetypes import BaseWeapon
# TODO: import this from an csv file

##########################################################################
#    Rifles: Bread and butter
#    NATO - Good range (accuracy), expensive
#    Pact - Poor accuracy (-range, -ammo), cheap
##########################################################################


class RifleNATOBasic(BaseWeapon):
    name = 'M-16'
    cost = 10

    soft_attack = 1
    range = 2
    moving_fire = True

    ammo_max = 7
    ammo_nominal = 28


class RifleWarsawBasic(BaseWeapon):
    name = 'AK-47'
    cost = 5

    soft_attack = 1
    range = 2
    moving_fire = True

    ammo_max = 5
    ammo_nominal = 30


class RifleNATO(BaseWeapon):
    name = 'L1A1 SLR'
    cost = 20

    soft_attack = 1
    range = 3
    moving_fire = True

    ammo_max = 7
    ammo_nominal = 20


class RifleWarsaw(BaseWeapon):
    name = 'AK-74'
    cost = 10

    soft_attack = 1
    range = 2
    moving_fire = True

    ammo_max = 6
    ammo_nominal = 20

##########################################################################
#    Specialised Rifles: Squad or Platoon marksman
#    NATO: Cheap, low ROF
#    PACT: PL weapon, expensive, superior
##########################################################################


class MarksmanWarsaw(BaseWeapon):
    name = 'SVD-63 Dragunov'
    cost = 70

    soft_attack = 4
    range = 4
    moving_fire = True

    ammo_max = 5
    ammo_nominal = 10


class MarksmanNATO(BaseWeapon):
    name = 'M14'
    cost = 40

    soft_attack = 3
    range = 4
    moving_fire = True

    ammo_max = 6
    ammo_nominal = 10


class SniperWarsaw(BaseWeapon):
    name = 'OTs-03 Dragunov'
    cost = 100

    soft_attack = 4
    range = 6
    moving_fire = False

    ammo_max = 5
    ammo_nominal = 10


class SniperNATO(BaseWeapon):
    name = 'H&K PSG1'
    cost = 90

    soft_attack = 4
    range = 4
    moving_fire = False

    ammo_max = 6
    ammo_nominal = 5


class SniperWarsawHeavy(BaseWeapon):
    name = 'KSVK 12.7'
    cost = 200

    soft_attack = 6
    hard_attack = 1
    range = 7
    moving_fire = False

    ammo_max = 10
    ammo_nominal = 5


class SniperNATOHeavy(BaseWeapon):
    name = 'M82 Barrett .50'
    cost = 250

    soft_attack = 6
    hard_attack = 1
    range = 9
    moving_fire = False

    ammo_max = 10
    ammo_nominal = 10


##########################################################################
#    Squad automatic weapons: Lightweight MGs
##########################################################################
class LightSawWarsaw(BaseWeapon):
    name = 'RPK'
    cost = 15

    soft_attack = 2
    range = 2
    moving_fire = True

    ammo_max = 3
    ammo_nominal = 80


class LightSawNATO(BaseWeapon):
    name = 'Ultimax-100'
    cost = 20

    soft_attack = 2
    range = 2
    moving_fire = True

    ammo_max = 4
    ammo_nominal = 50


class SawWarsaw(BaseWeapon):
    name = 'Pecheneg'
    cost = 30

    soft_attack = 3
    range = 5
    moving_fire = True

    ammo_max = 2
    ammo_nominal = 200


class SawNATO(BaseWeapon):
    name = 'M-249 Minimi'
    cost = 30

    soft_attack = 2
    range = 3
    moving_fire = True

    ammo_max = 4
    ammo_nominal = 100


##########################################################################
#    Squad weapons: Grenade launchers
##########################################################################
class GrenadeLauncherLightNATO(BaseWeapon):
    name = 'M203'
    cost = 5

    soft_attack = 1
    range = 3
    moving_fire = True

    ammo_max = 4
    ammo_nominal = 1


class GrenadeLauncherWarsaw(BaseWeapon):
    name = 'RG6'
    cost = 20

    soft_attack = 6
    range = 3
    moving_fire = True

    ammo_max = 2
    ammo_nominal = 6
