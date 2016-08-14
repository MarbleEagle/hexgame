'''
Created on Jun 9, 2015

@author: Joseph Lim
'''
from units.basetypes import BaseUnit
from units.infantrytypes import InfantryNCO, InfantryEnlisted, InfantryJuniorOfficer, InfantryMedic
from units.infantryupgrades import *
from units.smallarms import *


def getNATOReservePlatoon(BaseSoldier, BaseSmallArm, name=None):
    """ Light Infantry - Low support arms, no armour/anti-armour. Used for guard duty/patrols """

    def _getRifleSection(name='Rifle section'):
        """ 8 men with few supporting arms """
        section = BaseUnit(name=name)
        section.internals = [
            InfantryNCO(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Section Leader (3SG)'),
            InfantryEnlisted(BaseSoldier(
                weapons=[BaseSmallArm(), GrenadeLauncherLightNATO()]), 'Section 2IC (CPL)'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Rifleman'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Rifleman'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Rifleman'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Rifleman'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Rifleman'),
            InfantryEnlisted(
                BaseSoldier(weapons=[LightSawNATO()]), 'SAW Gunner'),
        ]
        return section

    def _getHQSection():
        """ Minimalist HQ section """
        section = BaseUnit(name='HQ section')
        section.internals = [
            InfantryJuniorOfficer(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Platoon Commander (2LT)'),
            InfantryNCO(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Platoon Sergeant (2SG)'),
            InfantryMedic(BaseSoldier(weapons=[BaseSmallArm()]), 'Medic'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Signaller'),
        ]
        return section

    platoon = BaseUnit(name=name or 'Light Infantry')
    platoon.internals = [
        _getHQSection(), _getRifleSection('Rifle Section A'), _getRifleSection('Rifle Section B'), _getRifleSection('Rifle Section C')]
    return platoon


def getNATOMechanisedPlatoon(BaseSoldier, BaseSmallArm, name=None):
    """ Vehicle mounted infantry - Small squad, Heavy firepower. Used for combined arms attack """

    def _getRifleSection(name='Mechanised Section'):
        section = BaseUnit(name=name)
        section.internals = [
            InfantryNCO(BaseSoldier(weapons=[BaseSmallArm()], upgrades=[
                        UpgradeInfantryArmorLight()]), 'Section Leader (3SG)'),
            InfantryEnlisted(BaseSoldier(weapons=[BaseSmallArm(), GrenadeLauncherLightNATO(
            )], upgrades=[UpgradeInfantryArmorLight()]), 'Section 2IC (CPL)'),
            InfantryEnlisted(BaseSoldier(weapons=[BaseSmallArm(), GrenadeLauncherLightNATO(
            )], upgrades=[UpgradeInfantryArmorLight()]), 'Grenadier'),
            InfantryEnlisted(BaseSoldier(weapons=[BaseSmallArm()], upgrades=[
                             UpgradeInfantryArmorLight()]), 'AT-Rifleman'),
            InfantryEnlisted(BaseSoldier(weapons=[BaseSmallArm()], upgrades=[
                             UpgradeInfantryArmorLight()]), 'AT-Rifleman'),
            InfantryEnlisted(BaseSoldier(
                weapons=[LightSawNATO()], upgrades=[UpgradeInfantryArmorLight()]), 'SAW Gunner'),
            InfantryEnlisted(BaseSoldier(
                weapons=[LightSawNATO()], upgrades=[UpgradeInfantryArmorLight()]), 'SAW Gunner'),
        ]
        return section

    def _getHQSection():
        section = BaseUnit(name='HQ section')
        section.internals = [
            InfantryJuniorOfficer(BaseSoldier(weapons=[BaseSmallArm()], upgrades=[
                                  UpgradeInfantryArmorLight()]), 'Platoon Commander (2LT)'),
            InfantryNCO(BaseSoldier(weapons=[BaseSmallArm()], upgrades=[
                        UpgradeInfantryArmorLight()]), 'Platoon Sergeant (2SG)'),
            InfantryMedic(BaseSoldier(weapons=[BaseSmallArm()]), 'Medic'),
            InfantryEnlisted(
                BaseSoldier(weapons=[BaseSmallArm()]), 'Signaller'),
        ]
        return section

    platoon = BaseUnit(name=name or 'Mechanised Platoon')
    platoon.internals = [
        _getHQSection(), _getRifleSection('Section A'), _getRifleSection('Section B'), _getRifleSection('Section C')]
    return platoon


if __name__ == '__main__':
    # TODO: Movement sspeed bug
    print(getNATOReservePlatoon(NATOReservist, RifleNATOEarly))
    print(getNATOReservePlatoon(NATORegular, RifleNATOEarly))
    print(getNATOReservePlatoon(NATOElite, RifleNATOEarly))

    # TODO: Movement sspeed bug
    print(getNATOMechanisedPlatoon(NATOReservist, RifleNATOEarly))
    print(getNATOMechanisedPlatoon(NATORegular, RifleNATOEarly))
    print(getNATOMechanisedPlatoon(NATOElite, RifleNATOEarly))
    print(InfantryNCO(NATORegular(), 'SAW Gunner').cost)
