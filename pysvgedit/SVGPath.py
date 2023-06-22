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

from .SVGObject import SVGObject, SVGStyleObject
from .Vector2D import Vector2D

@SVGObject.register
class SVGPath(SVGObject, SVGStyleObject):
	_TAG_NAME = "path"

	def clear(self, pos):
		self.node.setAttribute("d", f"M {pos.x} {pos.y}")
		return self

	def __append_path(self, strvalue):
		self.node.setAttribute("d", f"{self.node.getAttribute('d')} {strvalue}")

	def horizontal(self, x, relative = False):
		self.__append_path(f"{'h' if relative else 'H'} {x}")
		return self

	def vertical(self, y, relative = False):
		self.__append_path(f"{'v' if relative else 'V'} {y}")
		return self

	def lineto(self, pos, relative = False):
		self.__append_path(f"{'l' if relative else 'L'} {pos.x} {pos.y}")
		return self

	def bezierto(self, p1, p2, p3, relative = False):
		self.__append_path(f"{'c' if relative else 'C'} {p1.x} {p1.y} {p2.x} {p2.y} {p3.x} {p3.y}")
		return self

	def arcto(self, pos, radius, xrotation = 0, large_arc = True, sweep = True, relative = False):
		if isinstance(radius, float) or isinstance(radius, int):
			radius = Vector2D(radius, radius)
		self.__append_path(f"{'a' if relative else 'A'} {radius.x} {radius.y} {xrotation} {1 if large_arc else 0},{1 if sweep else 0} {pos.x} {pos.y}")
		return self

	def close(self):
		self.__append_path("Z")
		return self

	@classmethod
	def new(cls, pos):
		path = cls(cls._new_element())
		path.node.setAttribute("d", f"M {pos.x} {pos.y}")
		path.style.default_path()
		return path
