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
from .XMLTools import XMLTools

@SVGObject.register
class SVGGroup(SVGObject, SVGStyleObject):
	_TAG_NAME = "g"

	@property
	def is_layer(self):
		return self.node.getAttribute("inkscape:groupmode") == "layer"

	@is_layer.setter
	def is_layer(self, value: bool):
		if value:
			self.node.setAttribute("inkscape:groupmode", "layer")
		else:
			XMLTools.try_remove_attribute(self.node, "inkscape:groupmode")

	@classmethod
	def new(cls, is_layer = False):
		group = cls(cls._new_element())
		group.is_layer = is_layer
		return group
