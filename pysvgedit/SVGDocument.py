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

import functools
import xml.dom.minidom
from .SVGObject import SVGObject, SVGWidthHeightObject
from .SVGDefs import SVGDefs
from .XMLTools import XMLTools

class SVGDocument(SVGObject, SVGWidthHeightObject):
	_TAG_NAME = "svg"
	_DEFAULT_WIDTH = 300
	_DEFAULT_HEIGHT = 150
	_NAMESPACES = {
		"inkscape":	"http://www.inkscape.org/namespaces/inkscape",
		"sodipodi":	"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
		"svg":		"http://www.w3.org/2000/svg",
		"rdf":		"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
		"cc":		"http://creativecommons.org/ns#",
		"dc":		"http://purl.org/dc/elements/1.1/",
		"xlink":	"http://www.w3.org/1999/xlink",
	}

	def __init__(self, svg_node):
		super().__init__(svg_node)
		svg_node.ownerDocument._pysvgedit = self
		self._used_ids = set(node.getAttribute("id") for node in XMLTools.walk_elements(svg_node) if node.hasAttribute("id"))

	def get_unused_id(self):
		ctr = len(self._used_ids) + 1
		while True:
			attempt_id = f"id{ctr}"
			if attempt_id not in self._used_ids:
				self._used_ids.add(attempt_id)
				return attempt_id

	@functools.cached_property
	def defs(self):
		try:
			return self.get_first("defs")
		except StopIteration:
			return self.add(SVGDefs.new())

	@classmethod
	def new(cls):
		doc = xml.dom.minidom.Document()
		root = doc.createElement("svg")
		root.setAttribute("xmlns", cls._NAMESPACES["svg"])
		for (nsname, nsvalue) in cls._NAMESPACES.items():
			root.setAttribute(f"xmlns:{nsname}", nsvalue)
		doc.appendChild(root)
		return cls(svg_node = root)

	@classmethod
	def frombytes(cls, bytes_data):
		doc = xml.dom.minidom.parseString(bytes_data)
		root = XMLTools.find_first_element(doc, "svg")
		return cls(root)

	@classmethod
	def read(cls, f):
		doc = xml.dom.minidom.parse(f)
		root = XMLTools.find_first_element(doc, "svg")
		return cls(root)

	@classmethod
	def readfile(cls, filename):
		with open(filename, "rb") as f:
			return cls.read(f)

	def asbytes(self):
		return self.node.ownerDocument.toxml(encoding = "utf-8")

	def write(self, f):
		self.node.ownerDocument.writexml(f)

	def writefile(self, filename):
		with open(filename, "w") as f:
			self.write(f)

	def get_element_by_id(self, element_id):
		constraint = lambda node: node.getAttribute("id") == element_id
		try:
			return next(XMLTools.walk_elements(self.node, constraint = constraint))
		except StopIteration:
			return None

	def __str__(self):
		return f"SVGDocument<{self.extents.x:.0f} x {self.extents.y:.0f}>"
