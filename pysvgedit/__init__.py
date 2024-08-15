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

"""\
pysvgedit: SVG manipulation toolkit

The root element is a SVGDocument, which you can easily write to a file. To
each SVGObject, elements can be appended. For example, this writes a SVG file
with a single rectangle:

	import pysvgedit
	doc = pysvgedit.SVGDocument.new()
	doc.add(pysvgedit.SVGRect.new(pos = pysvgedit.Vector2D(10, 20), extents = pysvgedit.Vector2D(100, 150)))
	doc.writefile("output.svg")

pysvgedit also supports layers. Here is a new layer that is added and a red
circle (color #ff0000) and blue (color #0000ff) text is added inside that
layer:

	import pysvgedit
	doc = pysvgedit.SVGDocument.new()
	layer = doc.add(pysvgedit.SVGGroup.new(is_layer = True))
	layer.name = "My layer"

	circle = layer.add(pysvgedit.SVGCircle.new(pos = pysvgedit.Vector2D(30, 20), radius = 5))
	circle.style["stroke"] = "#ff0000"

	text = layer.add(pysvgedit.SVGText.new(pos = pysvgedit.Vector2D(50, 50), text = "My text"))
	text.style["fill"] = "#0000ff"

	doc.writefile("output.svg")
"""

from .Vector2D import Vector2D, TransformationMatrix, SVGTransform
from .SVGDefs import SVGDefs
from .SVGDocument import SVGDocument
from .SVGGroup import SVGGroup
from .SVGStyle import SVGStyle
from .SVGRect import SVGRect
from .SVGCircle import SVGCircle
from .SVGText import SVGTextSpan, SVGText
from .SVGPath import SVGPath
from .SVGImage import SVGImage
from .SVGAnimation import SVGAnimation, SVGAnimationMode
from .SVGValidator import SVGValidator, SVGValidatorErrorClass
from .SVGTransformation import FormatTextTransformation, ChangeVisibilityTransformation
from .Convenience import Convenience
from .Exceptions import SVGException

VERSION = "0.0.5"
