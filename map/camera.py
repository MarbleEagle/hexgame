'''
Created on Jun 7, 2015

@author: Joseph Lim
'''
from numpy import array
import numpy


class Camera(object):

    """ Handles camera related translation and rotation options """

    scroll_x = 0
    scroll_y = 0

    def __init__(self, context):
        self.context = context

    @property
    def scrollSpeed(self):
        xVelocity = self.scroll_x * \
            self.context.display_scroll_speed / self.context.hex_width
        yVelocity = self.scroll_y * \
            self.context.display_scroll_speed / self.context.hex_height
        return array([xVelocity, yVelocity])

    def updateCamera(self):
        """ Moves the camera by touching its vector, for scrolling """
        self.context.display_camera = numpy.add(
            self.scrollSpeed, self.context.display_camera)
        self.context.display_camera = numpy.maximum(
            self.context.display_camera,
            array([0, 0]))
        self.context.display_camera = numpy.minimum(
            self.context.display_camera,
            array([self.context.display_camera_bounds[0],
                   self.context.display_camera_bounds[1]]))
