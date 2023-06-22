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
import json
import tempfile
import subprocess
import datetime
import mako.template
import pysvgedit
from .FriendlyArgumentParser import FriendlyArgumentParser

class HelperClass():
	pass

class MakoRendererApp():
	def __init__(self, args):
		self._args = args
		with open(self._args.datafile_json) as f:
			self._template_data = json.load(f)
		self._update_helper_vars()

	def _update_helper_vars(self):
		if self._args.functions != "none":
			h = HelperClass()
			self._template_data["h"] = h

			if self._args.functions == "default":
				h.now = datetime.datetime.now()

	def _write_svg(self):
		self._doc.writefile(self._args.outfile)

	def _write_pdf(self):
		with tempfile.NamedTemporaryFile(prefix = "pysvgedit_", suffix = ".svg", mode = "w") as f:
			self._doc.write(f)
			f.flush()
			subprocess.check_call([ "inkscape", "-o", self._args.outfile, f.name])

	def _replace_text(self):
		for tspan in self._doc.walk("tspan"):
			text = tspan.text
			if text == "":
				continue
			template = mako.template.Template(text, strict_undefined = True)
			try:
				rendered_text = template.render(**self._template_data)
			except Exception as e:
				if not self._args.ignore_errors:
					raise
				rendered_text = f"{e.__class__.__name__}: {e}"
				if self._args.verbose >= 1:
					print(f"Error rendering {text}: {rendered_text}")
			if text != rendered_text:
				if self._args.verbose >= 2:
					print(f"{text} -> {rendered_text}")
				tspan.text = rendered_text

	def _patch_style(self):
		for (style_id, style_update) in self._template_data.get("svg_style_patches", { }).items():
			node = self._doc.get_element_by_id(style_id)
			if node is None:
				print(f"Style update of '{style_id}' requested, but no such element found.")
				continue
			style = pysvgedit.SVGStyle.from_node(node, auto_sync = True)
			style.update(style_update)

	def run(self):
		self._doc = pysvgedit.SVGDocument.readfile(self._args.infile_svg)
		self._replace_text()
		if self._args.patch_style:
			self._patch_style()

		if self._args.outfile.endswith(".pdf"):
			self._write_pdf()
		else:
			self._write_svg()

	@classmethod
	def main(cls):
		parser = FriendlyArgumentParser(description = "Render text blocks in SVG files using Mako.")
		parser.add_argument("-i", "--ignore-errors", action = "store_true", help = "By default, rendering is refused if there are errors. This will continue rendering and replace tpspans with the encountered issues instead.")
		parser.add_argument("-p", "--patch-style", action = "store_true", help = "Interpret an 'svg_style_patches' dictionary as elements for which style should be updated.")
		parser.add_argument("-f", "--functions", choices = [ "none", "default" ], default = "default", help = "Special functions to supply using the 'h' variable. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("datafile_json", help = "JSON file that contains the data that will be used as template variables.")
		parser.add_argument("infile_svg", help = "Input SVG file.")
		parser.add_argument("outfile", help = "Output file. If the extension is '.pdf', will be directly rendered to PDF using Inkscape. Otherwise, SVG is produced.")
		args = parser.parse_args(sys.argv[1:])

		app = cls(args)
		return app.run()
