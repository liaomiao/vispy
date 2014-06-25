# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

from __future__ import division
import numpy as np

from ...scene.entity import Entity
from ...scene.visuals import Line as LineVisual
from ...util.event import Event
from ...util.geometry import Rect
from ...scene.viewbox import ViewBox


class Box(Entity):
    """
    Rectangular Entity used as a container for other entities.
    """
    def __init__(self, parents=None, pos=None, size=None, border=None,
                 clip=False):
        super(Box, self).__init__(parents)
        self.events.add(rect_change=Event)

        if border is None:
            border = (0.2, 0.2, 0.2, 0.5)
        self._border = border
        self._visual = LineVisual(color=border, width=1)  # for drawing border
        self._clip = clip
        self._pos = (0, 0)
        self._size = (1, 1)
        self._padding = 0
        self._margin = 0
        self._boxes = set()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, p):
        assert isinstance(p, tuple)
        assert len(p) == 2
        self._pos = p
        self._update_line()
        self.events.rect_change()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        assert isinstance(s, tuple)
        assert len(s) == 2
        self._size = s
        self._update_line()
        self.update()
        self.events.rect_change()

    @property
    def rect(self):
        return Rect(self.pos, self.size)

    @rect.setter
    def rect(self, r):
        with self.events.rect_change.blocker():
            self.pos = r.pos
            self.size = r.size
        self.update()
        self.events.rect_change()

    @property
    def border(self):
        return self._border

    @border.setter
    def border(self, b):
        self._border = b
        self._visual.set_data(color=b)
        self.update()

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, m):
        self._margin = m
        self._update_line()

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, p):
        self._padding = p
        self._update_child_boxes()

    def _update_line(self):
        pad = self.margin
        left = self.pos[0] + pad
        right = self.pos[0] + self.size[0] - pad
        bottom = self.pos[1] + pad
        top = self.pos[1] + self.size[1] - pad

        pos = np.array([
            [left, bottom],
            [right, bottom],
            [right, top],
            [left, top],
            [left, bottom]]).astype(np.float32)
        self._visual.set_data(pos=pos)

    def on_draw(self, event):
        self._visual.transform = event.viewport_transform
        self._visual.draw()

    def on_rect_change(self, ev):
        self._update_child_boxes()

    def _update_child_boxes(self):
        # Set the position and size of child boxes (only those added
        # using add_box)
        for ch in self._boxes:
            ch.rect = self.rect.padded(self.padding + self.margin)

    def add_box(self, box):
        """
        Add a Box as a managed child of this Box. The child will be
        automatically positioned and sized to fill the entire space inside
        this Box.
        """
        self._boxes.add(box)
        box.add_parent(self)
        self._update_child_boxes()
        return box

    def add_grid(self, *args, **kwds):
        """
        Create a new GridBox and add it to the grid.

        All arguments are given to add_box().
        """
        grid = GridBox()
        return self.add_box(grid, *args, **kwds)

    def add_view(self, *args, **kwds):
        """
        Create a new ViewBox and add it to the grid.

        All arguments are given to add_box().
        """
        view = ViewBox()
        return self.add_box(view, *args, **kwds)

    def remove_box(self, box):
        self._boxes.remove(box)
        box.remove_parent(self)


