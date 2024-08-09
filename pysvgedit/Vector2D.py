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

import re
from math import sqrt, sin, cos, tan, isclose, pi, atan2

class Vector2D():
	def __init__(self, x = 0, y = 0):
		self._x = x
		self._y = y

	@property
	def x(self):
		return self._x

	@property
	def y(self):
		return self._y

	@property
	def length(self):
		return sqrt((self.x ** 2) + (self.y ** 2))

	@property
	def norm(self):
		return self / self.length

	@property
	def ortho(self):
		return Vector2D(self.y, self.x)

	@classmethod
	def angled(self, phi):
		return Vector2D(cos(phi), sin(phi))

	@property
	def angle(self):
		return atan2(self.y, self.x)

	def lerp(self, other, t):
		return ((1 - t) * self) + (t * other)

	def rotate(self, phi):
		return Vector2D(cos(phi) * self.x - sin(phi) * self.y, sin(phi) * self.x + cos(phi) * self.y)

	def angle_between(self, other):
		return other.angle - self.angle

	def max_xy(self, other: "Vector2D"):
		return Vector2D(max(self.x, other.x), max(self.y, other.y))

	def cmul(self, other):
		# Component-wise product
		return Vector2D(self.x * other.x, self.y * other.y)

	def cdiv(self, other):
		# Component-wise quotient
		return Vector2D(self.x / other.x, self.y / other.y)

	def xmul(self, other):
		# Cross product
		return self.x * other.y - self.y * other.x

	def __matmul__(self, other):
		# Dot product / scalar product
		return (self.x * other.x) + (self.y * other.y)

	def __add__(self, vector):
		return Vector2D(self.x + vector.x, self.y + vector.y)

	def __sub__(self, vector):
		return Vector2D(self.x - vector.x, self.y - vector.y)

	def __neg__(self):
		return Vector2D(-self.x, -self.y)

	def __mul__(self, scalar):
		return Vector2D(self.x * scalar, self.y * scalar)

	def __rmul__(self, scalar):
		return self * scalar

	def __truediv__(self, divisor):
		return Vector2D(self.x / divisor, self.y / divisor)

	def __repr__(self):
		return f"<{self.x:.1f}, {self.y:.1f}>"


class TransformationMatrix():
	def __init__(self, a, b, c, d, e, f):
		self._a = a
		self._b = b
		self._c = c
		self._d = d
		self._e = e
		self._f = f

	@property
	def a(self):
		return self._a

	@property
	def b(self):
		return self._b

	@property
	def c(self):
		return self._c

	@property
	def d(self):
		return self._d

	@property
	def e(self):
		return self._e

	@property
	def f(self):
		return self._f

	@property
	def aslist(self):
		return [ self.a, self.b, self.c, self.d, self.e, self.f ]

	def apply(self, vec2d):
		return Vector2D(
			self.a * vec2d.x + self.c * vec2d.y + self.e,
			self.b * vec2d.x + self.d * vec2d.y + self.f,
		)

	@property
	def is_identity(self):
		return self == self.identity()

	@classmethod
	def identity(cls):
		return cls.scale(1)

	@classmethod
	def scale(cls, scale_factor):
		return cls(scale_factor, 0, 0, scale_factor, 0, 0)

	@classmethod
	def translate(cls, vec2d):
		return cls(1, 0, 0, 1, vec2d.x, vec2d.y)

	@classmethod
	def rotate(cls, phi, center_of_rotation = None):
		if center_of_rotation is None:
			# No center of rotation given, rotate around origin
			return cls(cos(phi), -sin(phi), sin(phi), cos(phi), 0, 0)
		else:
			return cls.translate(-center_of_rotation) * cls.rotate(phi) * cls.translate(center_of_rotation)

	def __eq__(self, other):
		return all(isclose(x, y) for (x, y) in zip(self.aslist, other.aslist))

	def __neq__(self, other):
		return not (self == other)

	def __mul__(self, other):
		return TransformationMatrix(
			self.a * other.a + self.b * other.c,
			self.a * other.b + self.b * other.d,
			self.c * other.a + self.d * other.c,
			self.c * other.b + self.d * other.d,
			self.e * other.a + self.f * other.c + other.e,
			self.e * other.b + self.f * other.d + other.f,
		)

	def __repr__(self):
		return str(self)

	def __str__(self):
		if self.is_identity:
			values = "identity"
		else:
			values = ", ".join(f"{round(value, 3)}" for value in self.aslist)
		return "Matrix<%s>" % (values)

class SVGTransform():
	_OPERATION_RE = re.compile(r"[ \t\n]*(?P<op>[A-Za-z]+)\(\s*(?P<args>[^\)]+)\)(?P<remainder>.*)", flags = re.MULTILINE | re.DOTALL)
	_ARG_SPLIT_RE = re.compile(r"[, \t\n]+")

	@classmethod
	def parse(cls, transform_string):
		matrices = [ ]
		while True:
			result = cls._OPERATION_RE.fullmatch(transform_string)
			if result is None:
				if transform_string.strip("\t\n ") != "":
					raise ValueError("Unparsable trailing data in SVG transformation string: %s" % (transform_string))
				break
			result = result.groupdict()
			args = cls._ARG_SPLIT_RE.split(result["args"].strip("\n\t "))
			args = [ float(arg) for arg in args ]
			match (result["op"], len(args)):
				case ("matrix", 6):
					matrices.append(TransformationMatrix(*args))

				case ("translate", 2):
					matrices.append(TransformationMatrix.translate(Vector2D(*args)))

				case ("scale", 2):
					(scale_x, scale_y) = args
					matrices.append(TransformationMatrix(scale_x, 0, 0, scale_y, 0, 0))

				case ("rotate", 1):
					phi = args[0] / 180 * pi
					matrices.append(TransformationMatrix.rotate(-phi))

				case ("rotate", 3):
					phi = args[0] / 180 * pi
					center_of_rotation = Vector2D(args[1], args[2])
					matrices.append(TransformationMatrix.rotate(-phi, center_of_rotation = center_of_rotation))

				case ("skewX", 1):
					phi = args[0] / 180 * pi
					matrices.append(TransformationMatrix(1, 0, tan(phi), 1, 0, 0))

				case ("skewY", 1):
					phi = args[0] / 180 * pi
					matrices.append(TransformationMatrix(1, tan(phi), 0, 1, 0, 0))

				case _:
					raise ValueError(f"Unable to find result for: {result}")
			transform_string = result["remainder"]

		matrix = TransformationMatrix.identity()
		for transform in reversed(matrices):
			matrix *= transform
		return matrix

	@classmethod
	def to_svg(cls, matrix):
		return f"matrix({' '.join(str(value) for value in matrix.aslist)})"
