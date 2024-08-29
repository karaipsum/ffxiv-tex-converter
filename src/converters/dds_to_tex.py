import io
from struct import pack
from kaitaistruct import KaitaiStream
import numpy
from numpy import ushort
from src.parsers.tex import Tex
from src.parsers.dds import Dds

lod_offset = numpy.array([0, 1, 2], dtype=numpy.int32)

# if we have a Dds.* put it up here
Dds_fourcc = Dds.DdsPixelformat.PixelFormats
Dds_dxgi = Dds.HeaderDxt10.DxgiFormats

# if we have a Tex.* put it here
Tex_format = Tex.Header.TextureFormat


def get_tex_mipmap_length_format(dds):
    height = dds.hdr.height
    width = dds.hdr.width
    fourcc = dds.hdr.ddspf.fourcc

    if fourcc == Dds_fourcc.dxt1:
        return int(height * width // 2)
    if fourcc == Dds_fourcc.dxt3 or fourcc == Dds_fourcc.dxt5 or fourcc == Dds_fourcc.bc5u:
        return int(height * width * 2)
    if fourcc == Dds_fourcc.none:
        if dds.hdr.ddspf.r_bit_mask == b'\x00\x00\xff\x00':
            return int(height * width * 4)
        else:
            # support for A8 and L8 (r8)
            return int(height * width)
    if fourcc == Dds_fourcc.dx10:
        dxgi = dds.hdr_dxt10.dxgi_format
        if dxgi == Dds_dxgi.dxgi_format_bc7_unorm \
                or dxgi == Dds_dxgi.dxgi_format_bc3_unorm \
                or dxgi == Dds_dxgi.dxgi_format_bc2_unorm \
                or dxgi == Dds_dxgi.dxgi_format_b4g4r4a4_unorm \
                or dxgi == Dds_dxgi.dxgi_format_bc5_unorm \
                or dxgi == Dds_dxgi.dxgi_format_bc4_unorm:
            return int(height * width * 2)
        if dxgi == Dds_dxgi.dxgi_format_bc1_unorm:
            return int(height * width // 2)
        if dxgi == Dds_dxgi.dxgi_format_b8g8r8a8_unorm:
            return int(height * width * 4)
        if dxgi == Dds_dxgi.dxgi_format_r8_unorm:
            return int(height * width)
    else:
        return None


def get_mipmap_offsets(mipmap_length, mipmap_count):
    offset_array = numpy.zeros(13, dtype=numpy.int32)
    offset = 80
    j = 0
    try:
        for i in range(mipmap_count):
            offset_array[j] = offset
            offset += mipmap_length
            mipmap_length = max(16, mipmap_length >> 2)
            j += 1
        return offset_array
    except IndexError as e:
        raise SystemExit(
            'Image has too many mipmaps. Mipmap amount: ' +
            str(mipmap_count) + '. Check last \'given\' image.\nToo '
            'many mipmaps can be caused by:\n1) '
            'Having too large an image. '
            'TEX supports up to 4096x4096 '
            'resolution *only* if you are using '
            'mipmaps.\n2) A broken cubemap. Check '
            'if image ends in \'_e\' or \'_f\'. '
            'You cannot import cubemaps anyway, '
            'so get rid of it.\n 3) I don\'t '
            'know.') from e


def get_tex_offset_array(dds):
    tex_mipmap_length = get_tex_mipmap_length_format(dds)
    tex_offset_array = get_mipmap_offsets(
        tex_mipmap_length, dds.hdr.mipmap_count)
    return tex_offset_array


def get_tex_attribute():
    return Tex.Header.Attribute.texture_type_2d.value


def get_tex_format(dds):
    fourcc = dds.hdr.ddspf.fourcc
    if fourcc == Dds_fourcc.dxt1:
        return Tex_format.dxt1.value
    if fourcc == Dds_fourcc.dxt3:
        return Tex_format.dxt3.value
    if fourcc == Dds_fourcc.dxt5:
        return Tex_format.dxt5.value
    if fourcc == Dds_fourcc.bc5u:
        return Tex_format.ati2.value
    if fourcc == Dds_fourcc.dx10:
        dxgi = dds.hdr_dxt10.dxgi_format
        if dxgi == Dds_dxgi.dxgi_format_bc7_unorm:
            return Tex_format.bc7.value
        if dxgi == Dds_dxgi.dxgi_format_bc3_unorm:
            return Tex_format.dxt5.value
        if dxgi == Dds_dxgi.dxgi_format_bc2_unorm:
            return Tex_format.dxt3.value
        if dxgi == Dds_dxgi.dxgi_format_bc1_unorm:
            return Tex_format.dxt1.value
        if dxgi == Dds_dxgi.dxgi_format_b8g8r8a8_unorm:
            return Tex_format.b8g8r8a8.value
        if dxgi == Dds_dxgi.dxgi_format_r8_unorm:
            return Tex_format.l8
        if dxgi == Dds_dxgi.dxgi_format_a8_unorm:
            return Tex_format.a8
        if dxgi == Dds_dxgi.dxgi_format_bc5_unorm:
            return Tex_format.ati2
        if dxgi == Dds_dxgi.dxgi_format_bc4_unorm:
            return Tex_format.ati1
    if fourcc == Dds_fourcc.none:
        if dds.hdr.ddspf.r_bit_mask == b'\x00\x00\xff\x00':
            # basically asking if format is in *.*.R.*, which would be BGRA or BGR
            return Tex_format.b8g8r8a8.value
        elif dds.hdr.ddspf.r_bit_mask == b'\xff\x00\x00\x00':
            return Tex_format.l8.value
        elif dds.hdr.ddspf.a_bit_mask == b'\xff\x00\x00\x00':
            return Tex_format.a8.value
        elif dds.hdr.ddspf.rgb_bit_count == 16:
            return Tex_format.b4g4r4a4


def get_tex_height(dds):
    return ushort(dds.hdr.height)


def get_tex_width(dds):
    return ushort(dds.hdr.width)


def get_tex_mip_levels(dds):
    return ushort(dds.hdr.mipmap_count)


def get_tex_depth(dds):
    return ushort(dds.hdr.depth)


def get_tex_binary(path):
    with open(path, 'rb') as file:
        dds_data = file.read()

    dds_io = KaitaiStream(io.BytesIO(dds_data))
    dds_binary = Dds(dds_io)

    header_info = pack('<IIHHHH', get_tex_attribute(), get_tex_format(dds_binary), get_tex_width(dds_binary),
                       get_tex_height(dds_binary), get_tex_depth(dds_binary), get_tex_mip_levels(dds_binary))
    header = (header_info + lod_offset.tobytes() +
              get_tex_offset_array(dds_binary).tobytes())

    return header + dds_binary.bd.data


def write_tex_file(input_path, output_path):
    tex_binary = get_tex_binary(input_path)
    with open(output_path, 'wb') as file:
        file.write(tex_binary)
