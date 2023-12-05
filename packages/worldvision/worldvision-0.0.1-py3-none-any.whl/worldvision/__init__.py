"""
Calculate real world coordinates, distances, angles, etc. from 2D image.

BUG:
- get_2d_coords() does not work for special angles (90, -90, etc.)
- Some negative and positive values are not handled correctly.
- ZeroDivisionError is not handled in some cases.

TODO:
- Fix known issues.
- Add support for roll and yaw.
- Add support for other units.
- Add support for speed, velocity, acceleration, angular velocity, direction.
"""

from .calculations import *
from .camera import Camera