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

from .SVGText import SVGText
from .Vector2D import Vector2D
from .Exceptions import SVGLibUsageException

class Convenience():
	_ALLOWED_HALIGN = set([ "left", "center", "right", "justify" ])

	@classmethod
	def style_set(cls, style, fill, stroke):
		if fill is None:
			style["fill"] = "none"
			style["fill-opacity"] = None
		else:
			style["fill"] = fill
			style["fill-opacity"] = 1

		if stroke is None:
			style["stroke"] = "none"
			style["stroke-opacity"] = None
		else:
			style["stroke"] = stroke
			style["stroke-opacity"] = 1


	@classmethod
	def text(cls, parent, x, y, text, width = None, height = None, halign = "left", font = "sans-serif", font_size = 12, fill = "#000000", stroke = None):
		if halign not in cls._ALLOWED_HALIGN:
			raise SVGLibUsageException(f"halign must be one of {', '.join(sorted(cls._ALLOWED_HALIGN))}, but was: {halign}")

		if (width is None) and (height is not None):
			raise SVGLibUsageException("When 'height' is not none, 'width' must be given as well.")
		if (width is not None) and (height is None):
			height = font_size

		if width is None:
			rect_extents = None
		else:
			rect_extents = Vector2D(width, height)
		text_obj = SVGText.new(pos = Vector2D(x, y), text = text, rect_extents = rect_extents)
		text_obj.style["font-size"] = f"{font_size}px"
		text_obj.style["text-align"] = halign
		text_obj.style["font-family"] = font
		cls.style_set(text_obj.style, fill = fill, stroke = stroke)

		parent.add(text_obj)

	@classmethod
	def autosize(cls, root):
		pass
