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

import os
import sys
import pysvgedit
from .FriendlyArgumentParser import FriendlyArgumentParser

class AnimationRendererApp():
	def __init__(self, args):
		self._args = args

	@property
	def outdir(self):
		if self._args.outdir is None:
			return ""
		else:
			return self._outdir + "/"

	def run(self):
		self._doc = pysvgedit.SVGDocument.readfile(self._args.infile_svg)
		self._anim = pysvgedit.SVGAnimation(self._doc)
		tvars = {
			"prefix": os.path.splitext(self._args.infile_svg)[0],
		}
		for (frameno, frame) in enumerate(self._anim, 1):
			tvars["frameno"] = frameno
			output_filename = f"{self.outdir}{self._args.filename_template.format(**tvars)}"
			if self._args.verbose >= 1:
				print(f"Frame {frameno}: {output_filename}")
			frame.writefile(output_filename)

	@classmethod
	def main(cls):
		parser = FriendlyArgumentParser(description = "Render an animated SVG file.")
		parser.add_argument("-m", "--animation-mode", choices = [ "compose", "compose-all", "replace" ], default = "compose", help = "Specify the animation mode to render in. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-n", "--filename-template", metavar = "template", default = "{prefix}_{frameno:02d}.svg", help = "Can specify a filename template. Defaults to '%(default)s'.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("infile_svg", help = "Input SVG file.")
		parser.add_argument("outdir", nargs = "?", help = "Output directory to render frames in. Defaults to current directory if omitted.")
		args = parser.parse_args(sys.argv[1:])

		app = cls(args)
		return app.run()
