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

class SVGStyle():
	def __init__(self, style_dict: dict | None = None, auto_sync: bool = False, node = None):
		assert((style_dict is None) or isinstance(style_dict, dict))
		self._style = style_dict if (style_dict is not None) else { }
		self._auto_sync = auto_sync
		self._node = node

	@property
	def auto_sync(self):
		return self._auto_sync

	@auto_sync.setter
	def auto_sync(self, value):
		self._auto_sync = value

	@property
	def node(self):
		return self._node

	@node.setter
	def node(self, value):
		self._node = value

	@property
	def shape_inside(self):
		return self["shape-inside"]

	@shape_inside.setter
	def shape_inside(self, obj):
		self["shape-inside"] = f"url(#{obj.svgid})"

	@property
	def is_visible(self):
		if "display" in self._style:
			hidden = (self["display"].lower() == "none")
			return not hidden
		return True

	def clear(self):
		self._style = { }
		self._on_style_changed()

	def hide(self):
		self["display"] = "none"

	def show(self):
		self["display"] = None

	@classmethod
	def from_style_str(cls, style_str: str):
		style_dict = { }
		for style_item in style_str.split(";"):
			style_item = style_item.strip()
			if style_item == "":
				continue
			style_item = style_item.split(":", maxsplit = 1)
			if len(style_item) == 2:
				(key, value) = style_item
				key = key.strip()
				value = value.strip()
				style_dict[key] = value
		return cls(style_dict)

	@classmethod
	def from_node(cls, node, auto_sync: bool = False):
		if node.hasAttribute("style"):
			style = cls.from_style_str(node.getAttribute("style"))
		else:
			style = cls()
		style.node = node
		style.auto_sync = auto_sync
		return style

	def sync_node_style(self):
		if (len(self._style) == 0) and self._node.hasAttribute("style"):
			self._node.removeAttribute("style")
		else:
			self._node.setAttribute("style", self.serialize())

	def serialize(self):
		return ";".join("%s:%s" % (key, value) for (key, value) in self._style.items())

	def _on_style_changed(self):
		if (self._node is not None) and self._auto_sync:
			self.sync_node_style()

	def update(self, style_dict: dict):
		changed = False
		for (key, value) in style_dict.items():
			if self._setitem(key, value):
				changed = True
		if changed:
			self._on_style_changed()

	def default_path(self):
		self.update({
			"fill":				"none",
			"stroke":			"#000000",
			"stroke-width":		"1px",
			"stroke-linecap":	"butt",
			"stroke-linejoin":	"miter",
			"stroke-opacity":	"1",
		})
		return self

	def default_text(self):
		self.update({
			"font-style":		"normal",
			"font-weight":		"normal",
			"font-size":		"12px",
			"line-height":		"1.25",
			"font-family":		"sans-serif",
			"white-space":		"pre",
			"fill":				"#000000",
			"fill-opacity":		"1",
			"stroke":			"none",
		})
		return self

	def _setitem(self, key, value):
		changed = False
		if (value is None) and (key in self._style):
			del self._style[key]
			changed = True
		else:
			changed = self[key] != value
			self._style[key] = value
		return changed

	def __setitem__(self, key: str, value: str):
		if self._setitem(key, value):
			self._on_style_changed()

	def __getitem__(self, key: str):
		return self._style.get(key)

	def get(self, key: str, unstringify = False):
		value = self._style.get(key)
		if unstringify and (value is not None):
			if (value.startswith("'") and value.endswith("'")) or (value.startswith("\"") and value.endswith("\"")):
				value = value[1 : -1]
		return value

	def __str__(self):
		return f"SVGStyle<{self._style}>"
