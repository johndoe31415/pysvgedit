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

import xml.dom.minidom

class XMLTools():
	@classmethod
	def find_all_elements(cls, node, tagname = None, constraint = None):
		return (child for child in node.childNodes if (child.nodeType == child.ELEMENT_NODE) and ((tagname is None) or (child.tagName == tagname)) and ((constraint is None) or constraint(child)))

	@classmethod
	def find_first_element(cls, node, tagname = None, constraint = None):
		return next(cls.find_all_elements(node, tagname, constraint))

	@classmethod
	def walk_elements(cls, node, tagname = None, constraint = None):
		if node.nodeType == node.ELEMENT_NODE:
			if ((constraint is None) or (constraint(node))) and ((tagname is None) or (node.tagName == tagname)):
				yield node
			for child in node.childNodes:
				yield from cls.walk_elements(child, tagname = tagname, constraint = constraint)

	@classmethod
	def _walk_elements_with_context(cls, node, context, transform_context_function, exclude, parent = None):
		yield (node, context)
		for child in node.childNodes:
			if (child.nodeType == child.ELEMENT_NODE) and (child.tagName not in exclude):
				child_context = transform_context_function(context, parent, child)
				yield from cls._walk_elements_with_context(child, child_context, transform_context_function, exclude, parent = node)

	@classmethod
	def walk_elements_with_context(cls, node, root_context, transform_context_function, exclude = None):
		assert(node.nodeType == node.ELEMENT_NODE)
		if exclude is None:
			exclude = tuple()
		yield from cls._walk_elements_with_context(node = node, context = root_context, transform_context_function = transform_context_function, exclude = exclude)

	@classmethod
	def default_get_attribute(cls, node, name, default_value = None):
		if node.hasAttribute(name):
			return node.getAttribute(name)
		else:
			return default_value

	@classmethod
	def new_element(cls, tagname):
		doc = xml.dom.minidom.Document()
		element = doc.createElement(tagname)
		return element

	@classmethod
	def try_remove_attribute(cls, node, name):
		if node.hasAttribute(name):
			node.removeAttribute(name)

	@classmethod
	def all_parent_elements(cls, node):
		while node is not None:
			if node.nodeType == node.ELEMENT_NODE:
				yield node
			node = node.parentNode
