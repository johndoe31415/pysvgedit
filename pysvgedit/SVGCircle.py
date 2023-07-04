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
from .SVGObject import SVGObject, SVGXYObject, SVGStyleObject
from .Vector2D import Vector2D

@SVGObject.register
class SVGCircle(SVGObject, SVGXYObject, SVGStyleObject):
	_TAG_NAME = "circle"
	_X_ATTRIBUTE_NAME = "cx"
	_Y_ATTRIBUTE_NAME = "cy"

	@property
	def radius(self):
		return self._get_float_attribute("r")

	@radius.setter
	def radius(self, value):
		self.node.setAttribute("r", str(float(value)))

	def hull_vertices(self, max_interpolation_count = 100):
		pos = self.pos
		r = self.radius
		for i in range(max_interpolation_count):
			yield pos + (r * Vector2D.angled((i / max_interpolation_count) * 2 * math.pi))

	@classmethod
	def new(cls, pos, radius):
		path = cls(cls._new_element())
		path.pos = pos
		path.radius = radius
		path.style.default_path()
		return path
