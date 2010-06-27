# Copyright (C) 2010 Adam Wagner <awagner83@gmail.com>, 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""ColorLab - Color manipulation library for python."""

from itertools import izip, imap
from functools import partial


def color_range(start, end, n):
    """Generate a range of color from start to end (inclusive).
    
    Example:
    >>> list(color_range(Color(255, 255, 255), Color(0, 0, 0), 3))
    [<Color 255, 255, 255>, <Color 127, 127, 127>, <Color 0, 0, 0>]
    """
    rgbs = izip(*map(partial(_distribute, n=n), start.rgb, end.rgb))
    return (Color(*x) for x in rgbs)


class Color(object):
    """RGB Based Color Object."""

    def __init__(self, r, g, b):
        """Create new color from rgb components.

        Example:
        >>> Color(255, 255, 255).rgb
        [255, 255, 255]
        """
        self.rgb = [int(r), int(g), int(b)]

    def __repr__(self):
        return "<Color %0.0f, %0.0f, %0.0f>" % tuple(self.rgb)

    def ashex(self):
        """Return hex repr of color.

        Example:
        >>> Color(255, 255, 255).ashex()
        'ffffff'
        """
        return ''.join(str(hex(int(x)))[2:].zfill(2) for x in self.rgb)

    @classmethod
    def fromhex(cls, hex):
        """Create new Color object from hex representation.

        Example:
        >>> Color.fromhex("ffffff").rgb
        [255, 255, 255]
        """
        return cls(*(int(''.join(x), 16) for x in izip(*[iter(hex)]*2)))


def _distribute(start, end, n):
    """Generate N number of datapoints from start to end (inclusive)

    Example:
    >>> list(_distribute(0, 10, 6))
    [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
    >>> list(_distribute(10, 0, 6))
    [10.0, 8.0, 6.0, 4.0, 2.0, 0.0]
    >>> len(list(_distribute(0, 10, 10)))
    10
    >>> list(_distribute(0, 10, 1))
    [10.0]
    """
    if n == 1:
        return [float(end)]
    start, end = float(start), float(end)
    step = (end - start) / (n-1)
    return (start+(x*step) for x in xrange(n))
 
