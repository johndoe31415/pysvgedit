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

import enum
import logging
import functools
from .SVGTransformation import ChangeVisibilityTransformation
from .Exceptions import SVGInputFileException

_log = logging.getLogger(__spec__.name)

class SVGAnimationMode(enum.Enum):
	Compose = "compose"				# Add new layers on top
	ComposeAll = "compose-all"		# Add new layers on top, but consider all layers from the start
	Replace = "replace"				# New layers replace lower layers

class SVGLayerTag(enum.Enum):
	NoStop = "nostop"				# Do not emit this layer
	Protect = "protect"				# Do not remove this layer on 'reset'
	Reset = "reset"					# Remove all but protected layers

class SVGAnimation():
	def __init__(self, svg_document, animation_mode: SVGAnimationMode = SVGAnimationMode.Compose):
		self._svg_document = svg_document
		self._animation_mode = animation_mode

	@functools.cached_property
	def all_layers(self):
		return list(self._svg_document.get("g", constraint = lambda g: g.is_layer))

	@functools.cached_property
	def considered_layers(self):
		# Determine which layers we consider for the animation in the first place
		if self._animation_mode == SVGAnimationMode.Compose:
			considered_layers = self.visible_layers
		elif self._animation_mode in [ SVGAnimationMode.ComposeAll, SVGAnimationMode.Replace ]:
			considered_layers = self.all_layers
		else:
			raise NotImplementedError(self._animation_mode)
		return considered_layers

	@functools.cached_property
	def layer_tags(self):
		# Get all tags of considered layers
		return { layer.svgid: self._get_layer_tags(layer) for layer in self.considered_layers }

	@property
	def visible_layers(self):
		return [ layer for layer in self.all_layers if layer.style.is_visible ]

	def _get_layer_tags(self, layer):
		layer_tags = set()
		label = layer.label
		if ":" in label:
			(tag_string, _) = label.split(":", maxsplit = 1)
			for tag in tag_string.split(","):
				try:
					tag = SVGLayerTag(tag)
					layer_tags.add(tag)
				except ValueError as e:
					_log.warning("Unknown layer tag in layer %s (label %s): %s", layer.svgid, layer.label, tag)
		return layer_tags

	def _generate_layer_transformations(self):
		# Ensure all layers have unique layer IDs
		layer_ids = [layer.svgid for layer in self.considered_layers]
		if any(layer_id is None for layer_id in layer_ids):
			raise SVGInputFileException(f"{len(layer_ids)} layers found in SVG source, but some layers do not have an ID assigned.")
		if len(layer_ids) != len(set(layer_ids)):
			raise SVGInputFileException(f"{len(layer_ids)} layers found in SVG source, but some layers have duplicate layer IDs.")

		# Store commands to hide all layers first
		shown_unprotected_layers = [ ]
		svg_transforms = [ ChangeVisibilityTransformation(layer, visible = False) for layer in self.considered_layers ]

		# Then go through the layers one-by-one and render then as appropriate
		previous_layer = None
		for layer in self.considered_layers:
			tags = self.layer_tags[layer.svgid]
			_log.debug("Processing layer %s, tags %s", layer.svgid, tags)

			# Determine if slide is causing a reset, i.e. removal of below
			# layers which are unprotected
			if SVGLayerTag.Reset in tags:
				# Hide all below layers but those which are protected
				for below_layer in shown_unprotected_layers:
					svg_transforms.append(ChangeVisibilityTransformation(below_layer, visible = False))
				shown_unprotected_layers = [ ]

			# Then show the current layer
			svg_transforms.append(ChangeVisibilityTransformation(layer, visible = True))

			if SVGLayerTag.Protect not in tags:
				shown_unprotected_layers.append(layer)

			# If we're in a replacing mode, then hide the previous layer
			if (self._animation_mode == SVGAnimationMode.Replace) and (previous_layer is not None):
				svg_transforms.append(ChangeVisibilityTransformation(previous_layer, visible = False))

			# Emit it as a frame if it's not marked as "nostop"
			if SVGLayerTag.NoStop not in tags:
				yield svg_transforms
			previous_layer = layer

	def __iter__(self):
		for transformations in self._generate_layer_transformations():
			for transformation in transformations:
				transformation.apply()
			yield self._svg_document
