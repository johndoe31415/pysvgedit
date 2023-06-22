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

from .Vector2D import Vector2D
from .SVGObject import SVGObject, SVGXYObject, SVGWidthHeightObject, SVGStyleObject

@SVGObject.register
class SVGRect(SVGObject, SVGXYObject, SVGWidthHeightObject, SVGStyleObject):
	_TAG_NAME = "rect"

	@property
	def p1(self):
		return self.pos

	@property
	def p2(self):
		return Vector2D(self.pos.x, self.pos.y + self.extents.y)

	@property
	def p3(self):
		return self.pos + self.extents

	@property
	def p4(self):
		return Vector2D(self.pos.x + self.extents.x, self.pos.y)

	@classmethod
	def new(cls, pos, extents):
		path = cls(cls._new_element())
		path.pos = pos
		path.extents = extents
		path.style.default_path()
		return path
