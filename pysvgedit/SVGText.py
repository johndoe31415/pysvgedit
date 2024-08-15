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

from .SVGRect import SVGRect
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
	def new(cls, pos = None, rect_extents = None, text = ""):
		svg_text = cls(cls._new_element())
		svg_text.node.setAttribute("xml:space", "preserve")
		if (pos is not None) and (rect_extents is None):
			# Normal text with position
			svg_text.pos = pos
		elif (pos is not None) and (rect_extents is not None):
			# Text within rectangle (as definition)
			def post_add_hook(parent):
				rect = parent.svg_document.defs.add(SVGRect.new(pos = pos, extents = rect_extents))
				rect.style.clear()
				svg_text.style.shape_inside = rect
			svg_text.post_add_hook = post_add_hook

		svg_text.style.default_text()
		svg_text.add_span(SVGTextSpan.new(pos = pos, text = text))
		return svg_text

	def hull_vertices(self, max_interpolation_count = 4):
		inside_shape = self.svg_document.defs.get(self.style.shape_inside)
		if inside_shape is not None:
			# If inside shape is defined, all is well; otherwise we would need
			# to render the actual text/glyphs to determine the extents, which
			# we don't do.
			yield from inside_shape.hull_vertices(max_interpolation_count = max_interpolation_count)

	def add_span(self, svg_text_span: SVGTextSpan):
		self.node.appendChild(svg_text_span.node)
		return svg_text_span

	@property
	def tspans(self):
		return (SVGTextSpan(node) for node in XMLTools.find_all_elements(self.node, "tspan"))

	@property
	def tspan(self):
		return next(self.tspans)
