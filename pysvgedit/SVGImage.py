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

import base64
import mimetypes
from .Vector2D import Vector2D
from .SVGObject import SVGObject, SVGXYObject, SVGWidthHeightObject
from .Exceptions import SVGLibUsageException

@SVGObject.register
class SVGImage(SVGObject, SVGXYObject, SVGWidthHeightObject):
	_TAG_NAME = "image"

	@property
	def p1(self):
		return self.pos

	@property
	def p2(self):
		return Vector2D(self.pos.x, self.pos.y + self.extents.y)

	@property
	def p3(self):
		return self.pos + self.extents

	@property
	def p4(self):
		return Vector2D(self.pos.x + self.extents.x, self.pos.y)

	def hull_vertices(self, max_interpolation_count = 4):
		yield self.p1
		yield self.p2
		yield self.p3
		yield self.p4

	def set_image_data(self, content, mimetype):
		content_str = f"data:{mimetype};base64,{base64.b64encode(content).decode('ascii')}"
		self.node.setAttribute("xlink:href", content_str)

	def set_image_filename(self, filename):
		self.node.setAttribute("xlink:href", filename)

	@classmethod
	def new(cls, pos, extents, filename = None, embed = True, content = None, mimetype = None):
		if (filename is not None) and (content is not None):
			raise SVGLibUsageException("Either a filename can be provided or raw content, but not both.")
		if (content is not None) and (not embed):
			raise SVGLibUsageException("Content embedding is only possible when a filename is provided that can be used as a reference.")

		image = cls(cls._new_element())
		image.pos = pos
		image.extents = extents

		if filename is not None:
			if mimetype is None:
				mimetype = mimetypes.guess_type(filename)[0]
			if embed:
				with open(filename, "rb") as f:
					content = f.read()

		if content is not None:
			image.set_image_data(content = content, mimetype = mimetype)
		else:
			image.set_image_filename(filename)
		return image
