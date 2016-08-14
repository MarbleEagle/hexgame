'''
Created on Jun 9, 2015

@author: Joseph Lim
'''
from units.basetypes import BaseInternal


class WarsawConscript(BaseInternal):

    """ Basic, low cost unit """
    name = 'Conscript'
    _cost = 50
    movement = 2
    soft_defense_max = 1


class NATOReservist(BaseInternal):

    """ Basic, low cost unit """
    name = 'Reservist'
    _cost = 65
    movement = 2
    soft_defense_max = 1


class WarsawRegular(BaseInternal):

    """ Regular troops """
    name = 'Regular'
    _cost = 100
    movement = 3
    soft_defense_max = 3


class NATORegular(BaseInternal):

    """ Regular troops """
    name = 'Regular'
    _cost = 125
    movement = 3
    soft_defense_max = 3


class WarsawElite(BaseInternal):

    """ Elite, hardened unit """
    name = 'Spetznaz'
    _cost = 300
    movement = 4
    soft_defense_max = 5


class NATOElite(BaseInternal):

    """ Elite, hardened unit """
    name = 'Rangers'
    _cost = 375
    movement = 4
    soft_defense_max = 5


def InfantryEnlisted(unit, title):
    """ Enlisted men with appointment """
    unit.name = '%s %s' % (unit.name, title)
    return unit


def InfantryMedic(unit, title):
    """ Specialist """
    unit.name = '%s %s' % (unit.name, title)
    unit._cost += 25
    unit.medical += 1
    return unit


def InfantryDoctor(unit, title):
    """ Specialist """
    unit.name = '%s %s' % (unit.name, title)
    unit._cost = unit._cost * 2 + 300
    unit.medical += 5
    return unit


def InfantryNCO(unit, title):
    """ NCO with appointment """
    unit.name = '%s %s' % (unit.name, title)
    unit._cost = unit._cost * 2
    unit.leadership += 1
    unit.soft_defense_max += 1
    return unit


def InfantryJuniorOfficer(unit, title):
    """ LT/2LT with appointment """
    unit.name = '%s %s' % (unit.name, title)
    unit._cost = unit._cost * 4
    unit.leadership += 2
    unit.medical += 1
    unit.soft_defense_max += 1
    return unit


def InfantryStaffOfficer(unit, title):
    """ Captain with appointment """
    unit.name = '%s %s' % (unit.name, title)
    unit._cost = unit._cost * 10
    unit.leadership += 4
    unit.soft_defense_max += 1
    return unit


def InfantrySeniorOfficer(unit, title):
    """ Major/LC with appointment """
    unit.name = '%s %s' % (unit.name, title)
    unit._cost = unit._cost * 100
    unit.leadership += 10
    unit.soft_defense_max += 5
    return unit
