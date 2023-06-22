#	pyradium - HTML presentation/slide show generator
#	Copyright (C) 2015-2023 Johannes Bauer
#
#	This file is part of pyradium.
#
#	pyradium is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pyradium is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pyradium; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import enum
import logging
import functools
import subprocess
from .Exceptions import SVGValidationException

_log = logging.getLogger(__spec__.name)

class SVGValidatorErrorClass(enum.IntEnum):
	CheckDisabled = 0
	EmitWarning = 1
	ThrowException = 2

class SVGValidator():
	def __init__(self, check_missing_fonts: SVGValidatorErrorClass = SVGValidatorErrorClass.EmitWarning):
		self._check_missing_fonts = check_missing_fonts

	@functools.lru_cache(maxsize = 1000)
	def _have_font(self, font_family):
		return len(subprocess.check_output([ "fc-list", font_family ])) > 0

	def _check_font(self, font_name, missing_fonts):
		if font_name is None:
			return
		if font_name in missing_fonts:
			# Report only once.
			return
		if not self._have_font(font_name):
			missing_fonts.add(font_name)
			if self._check_missing_fonts == SVGValidatorErrorClass.EmitWarning:
				_log.warning("SVG document is referencing missing font: %s", font_name)
			elif self._check_missing_fonts == SVGValidatorErrorClass.ThrowException:
				raise SVGValidationException(f"SVG document is referencing missing font: {font_name}")

	def _validate_fonts(self, svg_document):
		missing_fonts = set()
		for svg_text in svg_document.walk("text"):
			self._check_font(svg_text.style.get("font-family", unstringify = True), missing_fonts)
			for tspan in svg_text.tspans:
				self._check_font(tspan.style.get("font-family", unstringify = True), missing_fonts)

	def validate(self, svg_document):
		if self._check_missing_fonts != SVGValidatorErrorClass.CheckDisabled:
			self._validate_fonts(svg_document)
