#	pysvgedit - SVG manipulation toolkit
#	Copyright (C) 2023-2024 Johannes Bauer
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

from .SVGObject import SVGObject
from .XMLTools import XMLTools

@SVGObject.register
class SVGDefs(SVGObject):
	_TAG_NAME = "defs"

	@classmethod
	def new(cls):
		return cls(cls._new_element())

	def get(self, shape_spec):
		if (shape_spec is not None) and shape_spec.startswith("url(#") and shape_spec.endswith(")"):
			shape_id = shape_spec[5 : -1]
			try:
				node = XMLTools.find_first_element(self.node, constraint = lambda node: node.getAttribute("id") == shape_id)
			except StopIteration:
				return None
			return SVGObject.attempt_handle(node)
		return None
