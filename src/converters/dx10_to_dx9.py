# converts supported DX10 files to DX9, is there a better way? oh my god, yes, but it just works^tm.
import numpy

from src.converters.tex_to_dds import get_ddspf_header
from src.parsers.dds import Dds
from struct import pack


def get_dds_fourcc(dds):
    fourcc = dds.hdr.ddspf.fourcc
    dxgi_format = dds.hdr_dxt10.dxgi_format
    ddspf_pf = Dds.DdsPixelformat.PixelFormats
    dds_dxgi = Dds.HeaderDxt10.DxgiFormats
    if fourcc == ddspf_pf.dx10:
        if dxgi_format == dds_dxgi.dxgi_format_bc3_unorm:
            return ddspf_pf.dxt5
        if dxgi_format == dds_dxgi.dxgi_format_bc2_unorm:
            return ddspf_pf.dxt3
        if dxgi_format == dds_dxgi.dxgi_format_bc1_unorm:
            return ddspf_pf.dxt1
        if dxgi_format == dds_dxgi.dxgi_format_b8g8r8a8_unorm:
            return ddspf_pf.none
    else:
        raise NotImplementedError


def get_dds_binary(path):
    dx10_binary = Dds.from_file(path)
    fourcc = get_dds_fourcc(dx10_binary)
    magic = b'DDS '
    size = 124
    flags = dx10_binary.hdr.flags
    height = dx10_binary.hdr.height
    width = dx10_binary.hdr.width
    pitch = dx10_binary.hdr.pitch_or_linear_size
    mipmapCount = dx10_binary.hdr.mipmap_count
    depth = 1
    reserved1_array = numpy.zeros(11, dtype=numpy.int32)
    ddspf_header = get_ddspf_header(fourcc)
    caps1 = dx10_binary.hdr.caps
    caps2 = 0
    caps3 = 0
    caps4 = 0
    reserved2 = 0
    header = magic + pack('<IIIIIII', size, flags, height, width, pitch, depth,
                          mipmapCount) + reserved1_array.tobytes() + ddspf_header + pack('<IIIII', caps1, caps2, caps3,
                                                                                         caps4, reserved2)

    body = (b''.join(dx10_binary.bd.data))
    dx9_binary = header + body

    del dx10_binary

    return dx9_binary
