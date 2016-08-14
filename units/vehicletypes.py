'''
Created on Jun 20, 2015

@author: Joseph Lim
'''
from units.basetypes import BaseUnit, BaseInternal


class Vehicle(BaseUnit):

    """ A vehicle - many vehicles form a platoon"""
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

    @property
    def softDefense(self):
        """ Override - vehicle is completely hard """
        return 100

    @property
    def softDefenseMax(self):
        """ Override - vehicle is completely hard """
        return 100

    @property
    def armour(self):
        """ Override - armour is a vehicle level property """
        return self._armour

    @property
    def armourNet(self):
        """ Override - armour is a vehicle level property """
        return self._armour

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
        """ Override - movement is a vehicle level property """
        return self._movement

    @property
    def movementPassability(self):
        """ The unit movement penalties are the max of each subunit """
        return getattr(self._movementPassability, None) or {}


class Turret(BaseInternal):
    name = 'Turret'

    def onDestruction(self):
        pass
