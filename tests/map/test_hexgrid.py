'''
Created on Jun 1, 2015

@author: Joseph Lim
'''
import unittest
from numpy import array
from numpy.testing import assert_array_equal
from map.hexgrid import HexCell


class HexCellClassTests(unittest.TestCase):

    def test_equality(self):
        a = HexCell(array([0, 0, 0]))
        b = HexCell(array([0, 0, 0]))

        self.assertFalse(a is b)
        self.assertFalse(a != b)
        self.assertTrue(a == b)


class HexCellFunctionalityTests(unittest.TestCase):

    def test_round(self):
        c1 = HexCell(array([0, 0, 0]))

        assert_array_equal(
            c1.round(array([1, -1, 0]), c1.ordinate), array([1, -1, 0]))
        assert_array_equal(
            c1.round(array([1.8, -1.8, 0]), c1.ordinate), array([2, -2, 0]))

    def test_getDirection(self):
        c1 = HexCell(array([0, 0, 0]))
        c1.getDirection(0)

    def test_getNeighbours(self):
        c1 = HexCell(array([0, 1, -1]))
        self.assertEqual(len(c1.getNeighbours(c1, 0)), 1)
        assert_array_equal(c1.getNeighbours(c1, 0)[0], array([0, 1, -1]))

        c2 = HexCell(array([0, 0, 0]))
        neighbours = c2.getNeighbours(c2, 1)
        expected = [[-1, 1, 0], [1, 0, -1], [0, -1, 1],
                    [1, -1, 0], [-1, 0, 1], [0, 1, -1]]
        self.assertEqual(len(neighbours), 6)
        for neighbour in neighbours:
            self.assertTrue(neighbour.tolist() in expected)
        self.assertEqual(len(c1.getNeighbours(c1, 2)), 12)

    def test_getDistance(self):
        c1 = HexCell(array([0, 0, 0]))
        c2 = HexCell(array([1, 1, 0]))
        c3 = HexCell(array([2, 1, -3]))
        self.assertEqual(c1.getDistance(c1, c2), 1)
        self.assertEqual(c1.getDistance(c1, c3), 3)

    def test_getLine(self):
        c1 = HexCell(array([0, 0, 0]))
        c2 = HexCell(array([4, -2, -2]))
        self.assertEqual(len(c1.getLine(c1, c2)), 5)
        expected = [[0.0, 0.0, 0.0], [1.0, 0.0, -1.0],
                    [2.0, -1.0, -1.0], [3.0, -2.0, -1.0], [4.0, -2.0, -2.0]]
        for cell in c1.getLine(c1, c2):
            self.assertTrue(cell.tolist() in expected)

    def test_cartesianConversion(self):
        c1 = HexCell(array([1, -1, 0]))
        self.assertEqual(c1.cartesianOrdinate, (1.0, 0.0))
        c2 = HexCell(array([-1, -1, 2]))
        self.assertEqual(c2.cartesianOrdinate, (0.0, 1.5))

        c1.cartesianOrdinate = array([-2, 0])
        self.assertEqual(c1.ordinate.tolist(), [-2.0, 2.0, 0.0])
        c2.cartesianOrdinate = array([0, -1.5])
        self.assertEqual(c2.ordinate.tolist(), [1, 1, -2])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
