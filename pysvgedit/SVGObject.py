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

from .XMLTools import XMLTools
from .SVGStyle import SVGStyle
from .Vector2D import Vector2D

class SVGXYObject():
	_X_ATTRIBUTE_NAME = "x"
	_Y_ATTRIBUTE_NAME = "y"

	@property
	def pos(self):
		return Vector2D(x = self._get_float_attribute(self._X_ATTRIBUTE_NAME), y = self._get_float_attribute(self._Y_ATTRIBUTE_NAME))

	@pos.setter
	def pos(self, value: Vector2D):
		self.node.setAttribute(self._X_ATTRIBUTE_NAME, str(value.x))
		self.node.setAttribute(self._Y_ATTRIBUTE_NAME, str(value.y))

class SVGWidthHeightObject():
	@property
	def extents(self):
		return Vector2D(x = self._get_float_attribute("width"), y = self._get_float_attribute("height"))

	@extents.setter
	def extents(self, value: Vector2D):
		self.node.setAttribute("width", str(value.x))
		self.node.setAttribute("height", str(value.y))


class SVGStyleObject():
	@property
	def style(self):
		return SVGStyle.from_node(self.node, auto_sync = True)


class SVGObject():
	_TAG_NAME = None
	_REGISTERED_CLASSES = { }

	def __init__(self, node):
		self._node = node

	@property
	def svg_document(self):
		doc = self.node.ownerDocument
		svg_doc = getattr(doc, "_pysvgedit", None)
		return svg_doc

	@property
	def node(self):
		return self._node

	@property
	def svgid(self):
		return self._default_get_attribute("id")

	@svgid.setter
	def svgid(self, value):
		self.node.setAttribute("id", value)

	@property
	def label(self):
		return self._default_get_attribute("inkscape:label")

	@label.setter
	def label(self, value: str):
		self.node.setAttribute("inkscape:label", value)

	def _default_get_attribute(self, name, default_value = None):
		return XMLTools.default_get_attribute(self.node, name, default_value = default_value)

	def _get_float_attribute(self, name):
		return float(self._default_get_attribute(name, default_value = 0))

	@classmethod
	def _new_element(cls):
		return XMLTools.new_element(cls.get_tagname())

	def add(self, svg_object):
		self.node.appendChild(svg_object.node)
		svg_object.node.ownerDocument = self.node.ownerDocument
		if svg_object.svgid is None:
			svg_object.svgid = self.svg_document.get_unused_id()
		return svg_object

	@classmethod
	def get_tagname(cls):
		assert(cls._TAG_NAME is not None)
		return cls._TAG_NAME

	def get(self, object_class, constraint = None):
		object_class = self._resolve_object_class(object_class)
		for child in XMLTools.find_all_elements(self.node, object_class.get_tagname()):
			child = object_class(child)
			if (constraint is None) or constraint(child):
				yield child

	def get_first(self, object_class, constraint = None):
		return next(self.get(object_class, constraint = constraint))

	def walk(self, object_class, constraint = None):
		object_class = self._resolve_object_class(object_class)
		for node in XMLTools.walk_elements(self.node, object_class.get_tagname()):
			node = object_class(node)
			if (constraint is None) or constraint(node):
				yield node

	def _resolve_object_class(self, object_class):
		if isinstance(object_class, str):
			if object_class in self._REGISTERED_CLASSES:
				return self._REGISTERED_CLASSES[object_class]
			else:
				raise ValueError(f"Class named '{object_class}' does not have a registered handler.")
		else:
			return object_class

	@classmethod
	def register(cls, svg_object_class):
		if svg_object_class._TAG_NAME in cls._REGISTERED_CLASSES:
			raise ValueError(f"{svg_object_class._TAG_NAME} of {svg_object_class} already registered.")
		cls._REGISTERED_CLASSES[svg_object_class._TAG_NAME] = svg_object_class
		return svg_object_class
