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

import re
import contextlib
import dataclasses
from .SVGObject import SVGObject, SVGStyleObject
from .Vector2D import Vector2D

@dataclasses.dataclass
class SVGPathElementClose():
	def apply(self, pos):
		return pos

@dataclasses.dataclass
class SVGPathElementBasic():
	_IDENTIFIER = None
	pos: Vector2D
	relative: bool

	def serialize(self):
		return f"{self._IDENTIFIER if self.relative else self._IDENTIFIER.upper()} {self.pos.x} {self.pos.y}"

	def apply(self, pos):
		if self.relative:
			return pos + self.pos
		else:
			return self.pos

class SVGPathElementMove(SVGPathElementBasic):
	_IDENTIFIER = "m"

class SVGPathElementLine(SVGPathElementBasic):
	_IDENTIFIER = "l"

@dataclasses.dataclass
class SVGPathElementArc():
	_IDENTIFIER = "a"

	pos: Vector2D
	radius: Vector2D
	xrotation: float
	large_arc: bool
	sweep: bool
	relative: bool

	def serialize(self):
		return f"{self._IDENTIFIER if self.relative else self._IDENTIFIER.upper()} {self.radius.x} {self.radius.y} {self.xrotation} {1 if self.large_arc else 0} {1 if self.sweep else 0} {self.pos.x} {self.pos.y}"

	def apply(self, pos):
		if self.relative:
			return pos + self.pos
		else:
			return self.pos


@dataclasses.dataclass
class SVGPathElementBezier():
	_IDENTIFIER = "c"

	p1: Vector2D
	p2: Vector2D
	p3: Vector2D
	relative: bool

	def serialize(self):
		return f"{self._IDENTIFIER if self.relative else self._IDENTIFIER.upper()} {self.p1.x} {self.p1.y} {self.p2.x} {self.p2.y} {self.p3.x} {self.p3.y}"

	def apply(self, pos):
		if self.relative:
			return pos + self.p3
		else:
			return self.p3


@dataclasses.dataclass
class SVGPathElementHorizontal():
	_IDENTIFIER = "h"

	x: float
	relative: bool

	def serialize(self):
		return f"{self._IDENTIFIER if self.relative else self._IDENTIFIER.upper()} {self.x}"

	def apply(self, pos):
		if self.relative:
			return Vector2D(pos.x + self.x, pos.y)
		else:
			return Vector2D(self.x, pos.y)

@dataclasses.dataclass
class SVGPathElementVertical():
	_IDENTIFIER = "v"

	y: float
	relative: bool

	def serialize(self):
		return f"{self._IDENTIFIER if self.relative else self._IDENTIFIER.upper()} {self.y}"

	def apply(self, pos):
		if self.relative:
			return Vector2D(pos.x, pos.y + self.y)
		else:
			return Vector2D(pos.x, self.y)

class SVGPathParser():
	_CMD_BEGIN = re.compile(r"^[,\s]*(?P<cmd>[a-zA-Z])(?P<tail>.*)")
	_FLOAT = re.compile(r"^[,\s]*(?P<float>-?(\d*)?(\.\d*)?)(?P<tail>.*)")
	_INT = re.compile(r"^[,\s]*(?P<int>-?\d+)(?P<tail>.*)")

	def __init__(self):
		self._cmds = [ ]

	@property
	def cmds(self):
		return self._cmds

	def _parse_begin(self, text):
		rematch = self._CMD_BEGIN.fullmatch(text)
		rematch = rematch.groupdict()
		return (rematch["cmd"], rematch["tail"])

	def _parse_float(self, text):
		rematch = self._FLOAT.fullmatch(text)
		rematch = rematch.groupdict()
		return (float(rematch["float"]), rematch["tail"])

	def _parse_int(self, text):
		rematch = self._INT.fullmatch(text)
		rematch = rematch.groupdict()
		return (int(rematch["int"]), rematch["tail"])

	def _parse_bool(self, text):
		(intval, text) = self._parse_int(text)
		return (intval != 0, text)

	def _parse_pos(self, text):
		(x, text) = self._parse_float(text)
		(y, text) = self._parse_float(text)
		return (Vector2D(x, y), text)

	def parse(self, text):
		while len(text) > 0:
			(cmd, text) = self._parse_begin(text)
			if cmd in "mM":
				(pos, text) = self._parse_pos(text)
				self._cmds.append(SVGPathElementMove(pos, relative = cmd.islower()))
			elif cmd in "lL":
				(pos, text) = self._parse_pos(text)
				self._cmds.append(SVGPathElementLine(pos, relative = cmd.islower()))
			elif cmd in "hH":
				(x, text) = self._parse_float(text)
				self._cmds.append(SVGPathElementHorizontal(x, relative = cmd.islower()))
			elif cmd in "vV":
				(y, text) = self._parse_float(text)
				self._cmds.append(SVGPathElementVertical(y, relative = cmd.islower()))
			elif cmd in "aA":
				(radius, text) = self._parse_pos(text)
				(xrotation, text) = self._parse_float(text)
				(large_arc, text) = self._parse_bool(text)
				(sweep, text) = self._parse_bool(text)
				(pos, text) = self._parse_pos(text)
				self._cmds.append(SVGPathElementArc(radius = radius, xrotation = xrotation, large_arc = large_arc, sweep = sweep, pos = pos, relative = cmd.islower()))
			elif cmd in "cC":
				(p1, text) = self._parse_pos(text)
				(p2, text) = self._parse_pos(text)
				(p3, text) = self._parse_pos(text)
				self._cmds.append(SVGPathElementBezier(p1 = p1, p2 = p2, p3 = p3, relative = cmd.islower()))
			elif cmd in "zZ":
				self._cmds.append(SVGPathElementClose())
			else:
				raise NotImplementedError(cmd)


@SVGObject.register
class SVGPath(SVGObject, SVGStyleObject):
	_TAG_NAME = "path"

	def __init__(self, node):
		super().__init__(node)
		self._pos = Vector2D()
		for cmd in self.parsed:
			self._pos = cmd.apply(self._pos)

	@property
	def pos(self):
		return self._pos

	@property
	def parsed(self):
		if self.node.hasAttribute("d"):
			parser = SVGPathParser()
			parser.parse(self.node.getAttribute("d"))
			return parser.cmds
		else:
			return [ ]

	def clear(self, pos):
		self._pos = pos
		self.node.setAttribute("d", f"M {pos.x} {pos.y}")
		return self

	def __append_path(self, cmd):
		self._pos = cmd.apply(self._pos)
		self.node.setAttribute("d", f"{self.node.getAttribute('d')} {cmd.serialize()}")

	def horizontal(self, x, relative = False):
		return self.__append_path(SVGPathElementHorizontal(x = x, relative = relative))

	def vertical(self, y, relative = False):
		return self.__append_path(SVGPathElementVertical(y = y, relative = relative))

	def moveto(self, pos, relative = False):
		return self.__append_path(SVGPathElementMove(pos = pos, relative = relative))

	def lineto(self, pos, relative = False):
		return self.__append_path(SVGPathElementLine(pos = pos, relative = relative))

	def bezierto(self, p1, p2, p3, relative = False):
		return self.__append_path(SVGPathElementBezier(p1 = p1, p2 = p2, p3 = p3, relative = relative))

	def arcto(self, pos, radius, xrotation = 0, large_arc = True, sweep = True, relative = False):
		if isinstance(radius, float) or isinstance(radius, int):
			radius = Vector2D(radius, radius)
		return self.__append_path(SVGPathElementArc(pos = pos, radius = radius, xrotation = xrotation, large_arc = large_arc, sweep = sweep, relative = relative))

	def close(self):
		return self.__append_path(SVGPathElementClose())

	@contextlib.contextmanager
	def returnto(self):
		previous_pos = self.pos
		yield
		self.moveto(previous_pos)

	@classmethod
	def new(cls, pos):
		path = cls(cls._new_element())
		path._pos = pos
		path.node.setAttribute("d", f"M {pos.x} {pos.y}")
		path.style.default_path()
		return path
