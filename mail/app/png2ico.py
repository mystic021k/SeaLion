#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function

import ctypes
import struct
import sys
import zlib

# ref: http://msdn.microsoft.com/en-us/library/ms997538
class ICONDIR(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("idReserved", ctypes.c_ushort),
                ("idType", ctypes.c_ushort),
                ("idCount", ctypes.c_ushort)]

class ICONDIRENTRY(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("bWidth", ctypes.c_byte),
                ("bHeight", ctypes.c_byte),
                ("bColorCount", ctypes.c_byte),
                ("bReserved", ctypes.c_byte),
                ("wPlanes", ctypes.c_ushort),
                ("wBitCount", ctypes.c_ushort),
                ("dwBytesInRes", ctypes.c_ulong),
                ("dwImageOffset", ctypes.c_ulong)]

CHANNELS = {0: 1, 2: 3, 4: 2, 6: 4}


def _paeth(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png(path):
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    pos = 8
    width = height = bitdepth = colortype = None
    idat = []
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bitdepth, colortype = struct.unpack(">IIBB", chunk[:10])
        elif ctype == b"IDAT":
            idat.append(chunk)
        elif ctype == b"IEND":
            break
    if bitdepth != 8 or colortype not in CHANNELS:
        raise ValueError("unsupported PNG (%s-bit color type %s)" % (bitdepth, colortype))
    channels = CHANNELS[colortype]
    stride = width * channels
    raw = zlib.decompress(b"".join(idat))
    rows = []
    prev = bytearray(stride)
    i = 0
    for _ in range(height):
        filter_type = raw[i]
        i += 1
        row = bytearray(raw[i:i + stride])
        i += stride
        if filter_type == 1:
            for x in range(stride):
                left = row[x - channels] if x >= channels else 0
                row[x] = (row[x] + left) & 255
        elif filter_type == 2:
            for x in range(stride):
                row[x] = (row[x] + prev[x]) & 255
        elif filter_type == 3:
            for x in range(stride):
                left = row[x - channels] if x >= channels else 0
                row[x] = (row[x] + ((left + prev[x]) // 2)) & 255
        elif filter_type == 4:
            for x in range(stride):
                a = row[x - channels] if x >= channels else 0
                b = prev[x]
                c = prev[x - channels] if x >= channels else 0
                row[x] = (row[x] + _paeth(a, b, c)) & 255
        elif filter_type != 0:
            raise ValueError("unsupported PNG filter %s" % filter_type)
        prev = row
        rows.append(row)
    return width, height, channels, rows


def _rgba_pixel(row, channels, x):
    base = x * channels
    if channels == 4:
        return row[base:base + 4]
    if channels == 3:
        return bytes(row[base:base + 3]) + b"\xff"
    if channels == 2:
        return bytes([row[base], row[base], row[base], row[base + 1]])
    value = row[base]
    return bytes([value, value, value, 255])


def write_png(width, height, rgba_rows):
    raw = bytearray()
    stride = width * 4
    for row in rgba_rows:
        raw.append(0)
        raw.extend(row[:stride])
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, payload):
        body = tag + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xffffffff)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"".join([
        b"\x89PNG\r\n\x1a\n",
        chunk(b"IHDR", ihdr),
        chunk(b"IDAT", compressed),
        chunk(b"IEND", b""),
    ])


def struct_bytes(value):
    return ctypes.string_at(ctypes.addressof(value), ctypes.sizeof(value))


def main(infile, left, top, size, outfile):
    _width, _height, channels, rows = read_png(infile)
    cropped = []
    for y in range(size):
        src = rows[top + y]
        row = bytearray()
        for x in range(size):
            row.extend(_rgba_pixel(src, channels, left + x))
        cropped.append(row)
    outpngbuf = write_png(size, size, cropped)

    icondir = ICONDIR()
    icondir.idReserved = 0
    icondir.idType = 1
    icondir.idCount = 1

    iconentry = ICONDIRENTRY()
    iconentry.bWidth = size
    iconentry.bHeight = size
    iconentry.bColorCount = 0
    iconentry.bReserved = 0
    iconentry.wPlanes = 1
    iconentry.wBitCount = 32
    iconentry.dwBytesInRes = len(outpngbuf)
    iconentry.dwImageOffset = ctypes.sizeof(icondir) + ctypes.sizeof(iconentry)

    with open(outfile, "wb") as out:
        out.write(struct_bytes(icondir))
        out.write(struct_bytes(iconentry))
        out.write(outpngbuf)


if __name__ == "__main__":
    main(*([sys.argv[1]] + [int(val) for val in sys.argv[2:5]] + [sys.argv[5]]))
