#	pysvgedit - SVG manipulation toolkit
#	Copyright (C) 2023-2023 Johannes Bauer
#
#	This file is part of pysvgedit.
#
#	pysvgedit is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pysvgedit is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pysvgedit; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import math

class Vector2D():
	def __init__(self, x = 0, y = 0):
		self._x = x
		self._y = y

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def length(self):
		return math.sqrt((self.x ** 2) + (self.y ** 2))

	@property
	def norm(self):
		return self / self.length

	@property
	def ortho(self):
		return Vector2D(self.y, self.x)

	def __matmul__(self, other):
		# Scalar product
		return (self.x * other.y) - (other.x * self.y)

	def __add__(self, vector):
		return Vector2D(self.x + vector.x, self.y + vector.y)

	def __mul__(self, scalar):
		return Vector2D(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		return self * scalar

	def __truediv__(self, divisor):
		return Vector2D(self.x / divisor, self.y / divisor)

	def __repr__(self):
		return f"<{self.x:.1f}, {self.y:.1f}>"
