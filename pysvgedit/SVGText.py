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

from .SVGObject import SVGObject, SVGXYObject, SVGStyleObject
from .XMLTools import XMLTools

@SVGObject.register
class SVGTextSpan(SVGObject, SVGXYObject, SVGStyleObject):
	_TAG_NAME = "tspan"

	def __init__(self, tspan_node):
		super().__init__(tspan_node)
		try:
			self._text_node = next(child for child in tspan_node.childNodes if (child.nodeType == child.TEXT_NODE))
		except StopIteration:
			# No text node, create one (with empty text)
			self._text_node = tspan_node.appendChild(tspan_node.ownerDocument.createTextNode(""))

	@classmethod
	def new(cls, pos = None, text = ""):
		tspan_node = cls._new_element()
		tspan_node.appendChild(tspan_node.ownerDocument.createTextNode(text))

		svg_textspan = cls(tspan_node)
		if pos is not None:
			svg_textspan.pos = pos
		return svg_textspan

	@property
	def text(self):
		return self._text_node.wholeText

	@text.setter
	def text(self, value):
		# If text is replaced, we need to remove the X/Y coordinates
		XMLTools.try_remove_attribute(self.node, "x")
		XMLTools.try_remove_attribute(self.node, "y")
		return self._text_node.replaceWholeText(value)

	def __repr__(self):
		return f"tspan<{self.text}>"

@SVGObject.register
class SVGText(SVGObject, SVGStyleObject):
	_TAG_NAME = "text"

	@classmethod
	def new(cls, pos = None, text = ""):
		svg_text = cls(cls._new_element())
		svg_text.node.setAttribute("xml:space", "preserve")
		if pos is not None:
			svg_text.pos = pos
		svg_text.style.default_text()
		svg_text.node.appendChild(SVGTextSpan.new(pos = pos, text = text).node)
		return svg_text

	@property
	def tspans(self):
		return (SVGTextSpan(node) for node in XMLTools.find_all_elements(self.node, "tspan"))

	@property
	def tspan(self):
		return next(self.tspans)
