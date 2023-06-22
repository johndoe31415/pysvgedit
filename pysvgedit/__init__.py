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

from .Vector2D import Vector2D
from .SVGDocument import SVGDocument
from .SVGDefs import SVGDefs
from .SVGGroup import SVGGroup
from .SVGStyle import SVGStyle
from .SVGText import SVGText
from .SVGPath import SVGPath
from .SVGRect import SVGRect
from .SVGCircle import SVGCircle
from .SVGAnimation import SVGAnimation, SVGAnimationMode
from .SVGValidator import SVGValidator
from .Exceptions import SVGException

VERSION = "0.0.2"
