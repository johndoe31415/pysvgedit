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

class SVGTransformation():
	_IDENTIFIER = None

	def __init__(self, svg_object):
		self._svg_object = svg_object

	@property
	def svg_object(self):
		return self._svg_object

	def apply(self):
		raise NotImplementedError(self.__class__.__name__)


class FormatTextTransformation(SVGTransformation):
	_IDENTIFIER = "format_text"

	def __init__(self, svg_object, template_vars):
		super().__init__(svg_object)
		self._template_vars = template_vars

	def apply(self):
		for tspan in self.svg_object.walk("tspan"):
			tspan.text = tspan.text.format(**self._template_vars)


class ChangeVisibilityTransformation(SVGTransformation):
	_IDENTIFIER = "visibility"

	def __init__(self, svg_object, visible):
		super().__init__(svg_object)
		self._visible = visible

	def apply(self):
		if self._visible:
			self.svg_object.style.show()
		else:
			self.svg_object.style.hide()
