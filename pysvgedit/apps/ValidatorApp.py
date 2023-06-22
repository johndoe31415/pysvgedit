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

import sys
import pysvgedit
from .FriendlyArgumentParser import FriendlyArgumentParser

class ValidatorApp():
	def __init__(self, args):
		self._args = args

	def run(self):
		doc = pysvgedit.SVGDocument.readfile(self._args.infile_svg)
		validator = pysvgedit.SVGValidator()
		validator.validate(doc)

	@classmethod
	def main(cls):
		parser = FriendlyArgumentParser(description = "Validate an SVG file.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("infile_svg", help = "Input SVG file.")
		args = parser.parse_args(sys.argv[1:])

		app = cls(args)
		return app.run()
