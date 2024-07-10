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

from .SVGText import SVGText
from .Vector2D import Vector2D, TransformationMatrix, SVGTransform
from .Exceptions import SVGLibUsageException
from .XMLTools import XMLTools
from .SVGObject import SVGObject

class Convenience():
	_ALLOWED_HALIGN = set([ "left", "center", "right", "justify" ])
	_ALLOWED_ATTRIBUTE = set([ "none", "bold", "italics" ])

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
	def text(cls, parent, text, x = None, y = None, pos = None, extents = None, width = None, height = None, halign = "left", font = "sans-serif", font_size = 12, fill = "#000000", stroke = None, attribute = None):
		if halign not in cls._ALLOWED_HALIGN:
			raise SVGLibUsageException(f"halign must be one of {', '.join(sorted(cls._ALLOWED_HALIGN))}, but was: {halign}")
		if (attribute is not None) and (attribute not in cls._ALLOWED_ATTRIBUTE):
			raise SVGLibUsageException(f"attribute must be one of {', '.join(sorted(cls._ALLOWED_ATTRIBUTE))}, but was: {attribute}")
		if (x is None) and (y is None) and (pos is None):
			raise SVGLibUsageException("Either scalars 'x'/'y' or vector 'pos' must be given.")
		if (x is None) != (y is None):
			raise SVGLibUsageException("Either both scalars 'x'/'y' must be given or neither.")
		if (x is not None) and (pos is not None):
			raise SVGLibUsageException("Not all of 'x'/'y'/'pos' may be given simultaneously, 'x'/'y' and 'pos' are mutually exclusive.")
		if (width is None) and (height is None) and (extents is None):
			raise SVGLibUsageException("Either scalars 'width'/'height' or vector 'extents' must be given.")
		if (width is None) and (height is not None):
			raise SVGLibUsageException("When 'height' is not none, 'width' must be given as well.")
		if (width is not None) and (extents is not None):
			raise SVGLibUsageException("Not all of 'width'/'height'/'extents' may be given simultaneously, 'width'/'height' and 'extents' are mutually exclusive.")

		if width is not None:
			extents = Vector2D(width, height or font_size)
		if x is not None:
			pos = Vector2D(x, y)

		text_obj = SVGText.new(pos = pos, text = text, rect_extents = extents)
		text_obj.style["font-size"] = f"{font_size}px"
		text_obj.style["text-align"] = halign
		text_obj.style["font-family"] = font
		cls.style_set(text_obj.style, fill = fill, stroke = stroke)

		if attribute == "bold":
			text_obj.style["font-weight"] = "bold"
		elif attribute == "italics":
			text_obj.style["font-style"] = "italic"

		parent.add(text_obj)
		return text_obj

	@classmethod
	def walk_with_transformation_matrix(cls, root):
		def _transform_context_function(transformation_matrix, parent, child):
			if child.hasAttribute("transform"):
				matrix = SVGTransform.parse(child.getAttribute("transform"))
				if transformation_matrix is None:
					transformation_matrix = matrix
				else:
					transformation_matrix = matrix * transformation_matrix
			return transformation_matrix

		for (node, transformation_matrix) in XMLTools.walk_elements_with_context(root.node, root_context = root.transformation_matrix, transform_context_function = _transform_context_function, exclude = set([ "defs" ])):
			svg_object = SVGObject.attempt_handle(node)
			if svg_object is not None:
				yield (svg_object, transformation_matrix)

	@classmethod
	def interpolate_extents(cls, root, max_interpolation_count = 100):
		for (svg_object, transformation_matrix) in cls.walk_with_transformation_matrix(root):
			if transformation_matrix is None:
				transformation_matrix = TransformationMatrix.identity()
			for vertex in svg_object.hull_vertices(max_interpolation_count = max_interpolation_count):
				transformed = transformation_matrix.apply(vertex)
				yield transformed

	@classmethod
	def autosize(cls, root, max_interpolation_count = 100, slack = 1):
		(minx, miny, maxx, maxy) = (None, None, None, None)
		for transformed in cls.interpolate_extents(root = root, max_interpolation_count = max_interpolation_count):
			if (minx is None) or (transformed.x < minx):
				minx = transformed.x
			if (maxx is None) or (transformed.x > maxx):
				maxx = transformed.x
			if (miny is None) or (transformed.y < miny):
				miny = transformed.y
			if (maxy is None) or (transformed.y > maxy):
				maxy = transformed.y

		if minx is None:
			return

		minx -= slack / 2
		miny -= slack / 2
		maxx += slack / 2
		maxy += slack / 2

		width = maxx - minx
		height = maxy - miny
		root.extents = Vector2D(width, height)
		for svg_object in root.getall():
			if svg_object._TAG_NAME != "defs":
				svg_object.apply_transform(TransformationMatrix.translate(Vector2D(-minx, -miny)))
