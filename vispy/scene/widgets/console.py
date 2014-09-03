# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
""" Fast and failsafe GL console """

# Code translated from glumpy

import numpy as np

from ..shaders import ModularProgram
from .widget import Widget
from ...gloo import VertexBuffer, set_state, _check_valid
from ...color import Color
from ...ext.six import string_types


# Translated from
# http://www.piclist.com/tecHREF/datafile/charset/
#     extractor/charset_extractor.htm
__font_6x8__ = np.array([
    (0x00, 0x00, 0x00, 0x00, 0x00, 0x00), (0x10, 0xE3, 0x84, 0x10, 0x01, 0x00),
    (0x6D, 0xB4, 0x80, 0x00, 0x00, 0x00), (0x00, 0xA7, 0xCA, 0x29, 0xF2, 0x80),
    (0x20, 0xE4, 0x0C, 0x09, 0xC1, 0x00), (0x65, 0x90, 0x84, 0x21, 0x34, 0xC0),
    (0x21, 0x45, 0x08, 0x55, 0x23, 0x40), (0x30, 0xC2, 0x00, 0x00, 0x00, 0x00),
    (0x10, 0x82, 0x08, 0x20, 0x81, 0x00), (0x20, 0x41, 0x04, 0x10, 0x42, 0x00),
    (0x00, 0xA3, 0x9F, 0x38, 0xA0, 0x00), (0x00, 0x41, 0x1F, 0x10, 0x40, 0x00),
    (0x00, 0x00, 0x00, 0x00, 0xC3, 0x08), (0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    (0x00, 0x00, 0x00, 0x00, 0xC3, 0x00), (0x00, 0x10, 0x84, 0x21, 0x00, 0x00),
    (0x39, 0x14, 0xD5, 0x65, 0x13, 0x80), (0x10, 0xC1, 0x04, 0x10, 0x43, 0x80),
    (0x39, 0x10, 0x46, 0x21, 0x07, 0xC0), (0x39, 0x10, 0x4E, 0x05, 0x13, 0x80),
    (0x08, 0x62, 0x92, 0x7C, 0x20, 0x80), (0x7D, 0x04, 0x1E, 0x05, 0x13, 0x80),
    (0x18, 0x84, 0x1E, 0x45, 0x13, 0x80), (0x7C, 0x10, 0x84, 0x20, 0x82, 0x00),
    (0x39, 0x14, 0x4E, 0x45, 0x13, 0x80), (0x39, 0x14, 0x4F, 0x04, 0x23, 0x00),
    (0x00, 0x03, 0x0C, 0x00, 0xC3, 0x00), (0x00, 0x03, 0x0C, 0x00, 0xC3, 0x08),
    (0x08, 0x42, 0x10, 0x20, 0x40, 0x80), (0x00, 0x07, 0xC0, 0x01, 0xF0, 0x00),
    (0x20, 0x40, 0x81, 0x08, 0x42, 0x00), (0x39, 0x10, 0x46, 0x10, 0x01, 0x00),
    (0x39, 0x15, 0xD5, 0x5D, 0x03, 0x80), (0x39, 0x14, 0x51, 0x7D, 0x14, 0x40),
    (0x79, 0x14, 0x5E, 0x45, 0x17, 0x80), (0x39, 0x14, 0x10, 0x41, 0x13, 0x80),
    (0x79, 0x14, 0x51, 0x45, 0x17, 0x80), (0x7D, 0x04, 0x1E, 0x41, 0x07, 0xC0),
    (0x7D, 0x04, 0x1E, 0x41, 0x04, 0x00), (0x39, 0x14, 0x17, 0x45, 0x13, 0xC0),
    (0x45, 0x14, 0x5F, 0x45, 0x14, 0x40), (0x38, 0x41, 0x04, 0x10, 0x43, 0x80),
    (0x04, 0x10, 0x41, 0x45, 0x13, 0x80), (0x45, 0x25, 0x18, 0x51, 0x24, 0x40),
    (0x41, 0x04, 0x10, 0x41, 0x07, 0xC0), (0x45, 0xB5, 0x51, 0x45, 0x14, 0x40),
    (0x45, 0x95, 0x53, 0x45, 0x14, 0x40), (0x39, 0x14, 0x51, 0x45, 0x13, 0x80),
    (0x79, 0x14, 0x5E, 0x41, 0x04, 0x00), (0x39, 0x14, 0x51, 0x55, 0x23, 0x40),
    (0x79, 0x14, 0x5E, 0x49, 0x14, 0x40), (0x39, 0x14, 0x0E, 0x05, 0x13, 0x80),
    (0x7C, 0x41, 0x04, 0x10, 0x41, 0x00), (0x45, 0x14, 0x51, 0x45, 0x13, 0x80),
    (0x45, 0x14, 0x51, 0x44, 0xA1, 0x00), (0x45, 0x15, 0x55, 0x55, 0x52, 0x80),
    (0x45, 0x12, 0x84, 0x29, 0x14, 0x40), (0x45, 0x14, 0x4A, 0x10, 0x41, 0x00),
    (0x78, 0x21, 0x08, 0x41, 0x07, 0x80), (0x38, 0x82, 0x08, 0x20, 0x83, 0x80),
    (0x01, 0x02, 0x04, 0x08, 0x10, 0x00), (0x38, 0x20, 0x82, 0x08, 0x23, 0x80),
    (0x10, 0xA4, 0x40, 0x00, 0x00, 0x00), (0x00, 0x00, 0x00, 0x00, 0x00, 0x3F),
    (0x30, 0xC1, 0x00, 0x00, 0x00, 0x00), (0x00, 0x03, 0x81, 0x3D, 0x13, 0xC0),
    (0x41, 0x07, 0x91, 0x45, 0x17, 0x80), (0x00, 0x03, 0x91, 0x41, 0x13, 0x80),
    (0x04, 0x13, 0xD1, 0x45, 0x13, 0xC0), (0x00, 0x03, 0x91, 0x79, 0x03, 0x80),
    (0x18, 0x82, 0x1E, 0x20, 0x82, 0x00), (0x00, 0x03, 0xD1, 0x44, 0xF0, 0x4E),
    (0x41, 0x07, 0x12, 0x49, 0x24, 0x80), (0x10, 0x01, 0x04, 0x10, 0x41, 0x80),
    (0x08, 0x01, 0x82, 0x08, 0x24, 0x8C), (0x41, 0x04, 0x94, 0x61, 0x44, 0x80),
    (0x10, 0x41, 0x04, 0x10, 0x41, 0x80), (0x00, 0x06, 0x95, 0x55, 0x14, 0x40),
    (0x00, 0x07, 0x12, 0x49, 0x24, 0x80), (0x00, 0x03, 0x91, 0x45, 0x13, 0x80),
    (0x00, 0x07, 0x91, 0x45, 0x17, 0x90), (0x00, 0x03, 0xD1, 0x45, 0x13, 0xC1),
    (0x00, 0x05, 0x89, 0x20, 0x87, 0x00), (0x00, 0x03, 0x90, 0x38, 0x13, 0x80),
    (0x00, 0x87, 0x88, 0x20, 0xA1, 0x00), (0x00, 0x04, 0x92, 0x49, 0x62, 0x80),
    (0x00, 0x04, 0x51, 0x44, 0xA1, 0x00), (0x00, 0x04, 0x51, 0x55, 0xF2, 0x80),
    (0x00, 0x04, 0x92, 0x31, 0x24, 0x80), (0x00, 0x04, 0x92, 0x48, 0xE1, 0x18),
    (0x00, 0x07, 0x82, 0x31, 0x07, 0x80), (0x18, 0x82, 0x18, 0x20, 0x81, 0x80),
    (0x10, 0x41, 0x00, 0x10, 0x41, 0x00), (0x30, 0x20, 0x83, 0x08, 0x23, 0x00),
    (0x29, 0x40, 0x00, 0x00, 0x00, 0x00), (0x10, 0xE6, 0xD1, 0x45, 0xF0, 0x00)
], dtype=np.float32)

VERTEX_SHADER = """
uniform float u_scale;
uniform vec2 u_px_scale;
uniform vec4 u_color;

attribute vec2 a_position;
attribute vec3 a_bytes_012;
attribute vec3 a_bytes_345;

varying vec4 v_color;
varying vec3 v_bytes_012, v_bytes_345;

void main (void)
{
    vec4 pos = $transform(vec4(0., 0., 0., 1.));
    gl_Position = pos + vec4(a_position * u_px_scale * u_scale, 0., 0.);
    gl_PointSize = 8.0 * u_scale;
    v_color = u_color;
    v_bytes_012 = a_bytes_012;
    v_bytes_345 = a_bytes_345;
}
"""

FRAGMENT_SHADER = """
float segment(float edge0, float edge1, float x)
{
    return step(edge0,x) * (1.0-step(edge1,x));
}

varying vec4 v_color;
varying vec3 v_bytes_012, v_bytes_345;

void main(void)
{
    vec2 uv = floor(gl_PointCoord.xy * 8.0);
    if(uv.x > 5.0) discard;
    if(uv.y > 7.0) discard;
    float index  = floor( (uv.y*6.0+uv.x)/8.0 );
    float offset = floor( mod(uv.y*6.0+uv.x,8.0));
    float byte = segment(0.0,1.0,index) * v_bytes_012.x
               + segment(1.0,2.0,index) * v_bytes_012.y
               + segment(2.0,3.0,index) * v_bytes_012.z
               + segment(3.0,4.0,index) * v_bytes_345.x
               + segment(4.0,5.0,index) * v_bytes_345.y
               + segment(5.0,6.0,index) * v_bytes_345.z;
    if( floor(mod(byte / (128.0/pow(2.0,offset)), 2.0)) > 0.0 )
        gl_FragColor = v_color;
    else
        discard;
}
"""


class Console(Widget):
    """Fast and failsafe text console

    Parameters
    ----------
    text_color : instance of Color
        Color to use.
    font_scale : int
        Scale factor to use for the font. A scale factor of 1 will use
        glyphs that are 6 pixels wide, with larger factors being
        multiplicatively larger.
    orientation : str
        Either "scroll-up" (like a terminal), or "scroll-down".
        In "scroll-up", the most recent message is at the bottom.
    """
    def __init__(self, text_color='black', font_scale=12.,
                 orientation='scroll-up', **kwargs):
        _check_valid('orientation', orientation, ('scroll-up', 'scroll-down'))

        # Harcoded because of font above and shader program
        self.text_color = text_color
        self.font_scale = font_scale
        self._char_width = 6
        self._char_height = 10
        self._program = ModularProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self._ori = orientation
        self._text_lines = []
        self._row = -1
        self._col = -1
        Widget.__init__(self, **kwargs)

    @property
    def text_color(self):
        return self._color

    @property
    def size(self):
        return super(Console, self).size

    @size.setter
    def size(self, *size):
        Widget.size.fset(self, *size)
        # Resize buffers
        self._n_rows = int(max(self.size[1] / (self._char_height *
                                               self.font_scale), 1))
        self._n_cols = int(max(self.size[0] / (self._char_width *
                                               self.font_scale), 1))
        self._bytes_012 = np.zeros((self._n_rows, self._n_cols, 3), np.float32)
        self._bytes_345 = np.zeros((self._n_rows, self._n_cols, 3), np.float32)
        pos = np.empty((self._n_rows, self._n_cols, 2), np.float32)
        C, R = np.meshgrid(np.arange(self._n_cols), np.arange(self._n_rows))
        # We are in left, top orientation
        x_off = 4.
        y_off = 4. - self._char_height * self._n_rows
        pos[..., 0] = x_off + self._char_width * C
        pos[..., 1] = y_off + self._char_height * R
        self._position = VertexBuffer(pos)

        # Restore lines
        sl = slice(None, None, (-1 if self._ori == 'scroll-down' else 1))
        for ii, line in enumerate(self._text_lines[sl][:self._n_rows]):
            self._insert_text_buf(line, ii)

    @text_color.setter
    def text_color(self, color):
        self._color = Color(color)

    @property
    def font_scale(self):
        return self._font_scale

    @font_scale.setter
    def font_scale(self, font_scale):
        self._font_scale = int(max(font_scale, 1))

    def draw(self, event):
        super(Console, self).draw(event)
        if event is not None:
            xform = event.render_transform.shader_map()
            px_scale = event.framebuffer_cs.transform.scale[:2]
        else:
            xform = self.transform.shader_map()
            # Rather arbitrary scale
            px_scale = 0.01, 0.01
        self._program.vert['transform'] = xform
        self._program.prepare()
        self._program['u_px_scale'] = px_scale
        self._program['u_color'] = self.text_color.rgba
        self._program['u_scale'] = self.font_scale
        self._program['a_position'] = self._position
        self._program['a_bytes_012'] = VertexBuffer(self._bytes_012)
        self._program['a_bytes_345'] = VertexBuffer(self._bytes_345)
        set_state(depth_test=False, blend=True,
                  blend_func=('src_alpha', 'one_minus_src_alpha'))
        self._program.draw('points')

    def clear(self):
        """ Clear console """
        self._bytes_012.fill(0)
        self._bytes_345.fill(0)
        self._row = -1
        self._col = 0
        self._text_lines = [] * self._n_rows

    def write(self, text='', wrap=True):
        """Write text and scroll

        Parameters
        ----------
        text : str
            Text to write. ``''`` can be used for a blank line.
        wrap : str
            If True, long messages will be wrapped to span multiple lines.
        """
        # Clear line
        if not isinstance(text, string_types):
            raise TypeError('text must be a string')
        # ensure we only have ASCII chars
        text = text.encode('utf-8').decode('ascii', errors='replace')
        # truncate in case of *really* long messages
        text = text[-self._n_cols*self._n_rows:]
        text = text.split('\n')
        nr, nc = self._n_rows, self._n_cols
        for para in text:
            para = para[:nc] if not wrap else para
            lines = [para[ii:(ii+nc)] for ii in range(0, len(para), nc)]
            for line in lines:
                # Update row and scroll if necessary
                self._row += 1 if self._ori == 'scroll-down' else -1
                self._text_lines.insert(0, line)
                self._text_lines = self._text_lines[:nr]
                if self._row >= nr:
                    self._bytes_012[:-1] = self._bytes_012[1:]
                    self._bytes_345[:-1] = self._bytes_345[1:]
                    self._row = nr - 1
                elif self._row < nr:
                    self._bytes_012[1:] = self._bytes_012[:-1]
                    self._bytes_345[1:] = self._bytes_345[:-1]
                    self._row = 0
                self._insert_text_buf(line, self._row)

    def _insert_text_buf(self, line, idx):
        """Insert text into bytes buffers"""
        self._bytes_012[idx] = 0
        self._bytes_345[idx] = 0
        # Crop text if necessary
        I = np.array([ord(c) - 32 for c in line[:self._n_cols]])
        I = np.clip(I, 0, len(__font_6x8__)-1)
        b = __font_6x8__[I]
        self._bytes_012[idx, :len(I)] = b[:, :3]
        self._bytes_345[idx, :len(I)] = b[:, 3:]
