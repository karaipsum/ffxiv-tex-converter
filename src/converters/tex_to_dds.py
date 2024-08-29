import io
from struct import pack
from kaitaistruct import KaitaiStream
import numpy
from src.parsers.dds import Dds
from src.parsers.tex import Tex

# if we have a Dds.* put it up here
Dds_fourcc = Dds.DdsPixelformat.PixelFormats
Dds_ddspf_ff = Dds.DdsPixelformat.FormatFlags
Dds_ff = Dds.Header.FormatFlags
Dds_dxgi = Dds.HeaderDxt10.DxgiFormats
Dds_cf = Dds.Header.CapsFlags

# if we have a Tex.* put it here
Tex_format = Tex.Header.TextureFormat


def get_dds_height(tex):
    return int(tex.hdr.height)


def get_dds_width(tex):
    return int(tex.hdr.width)


def get_dds_mipmapCount(tex):
    return int(tex.hdr.mip_levels)


def get_tex_format(tex):
    return tex.hdr.format


def get_dds_fourcc(format):
    if format == Tex_format.dxt1:
        return Dds_fourcc.dxt1
    if format == Tex_format.dxt5:
        return Dds_fourcc.dxt5
    if format == Tex_format.dxt3:
        return Dds_fourcc.dxt3
    if format == Tex_format.ati1:
        return Dds_fourcc.dx10
    if format == Tex_format.ati2:
        return Dds_fourcc.dx10
    if format == Tex_format.bc7:
        return Dds_fourcc.dx10
    if format == Tex_format.b8g8r8a8:
        return Dds_fourcc.none
    if format == Tex_format.a8:
        return Dds_fourcc.none
    if format == Tex_format.l8:
        return Dds_fourcc.none
    if format == Tex_format.b4g4r4a4:
        return Dds_fourcc.none


def get_dds_dxt10_header(tex):
    dxgi = get_dds_dxt10_dxgi(tex.hdr.format)
    resource_dimension = get_dds_dxt10_resource_dimension()
    misc_flag = get_dds_dxt10_misc_flag()
    array_size = get_dds_dxt10_array_size()
    misc_flag2 = get_dds_dxt10_misc_flags2()
    dxt10_header = pack('<IIIII', dxgi.value, resource_dimension,
                        misc_flag, array_size, misc_flag2)
    return dxt10_header


def get_dds_dxt10_dxgi(tex_format):
    # todo theoretically should have support for more options but w/e
    # todo could also be rolled into the fourcc
    if tex_format == Tex_format.ati1:
        return Dds_dxgi.dxgi_format_bc4_unorm
    if tex_format == Tex_format.ati2:
        return Dds_dxgi.dxgi_format_bc5_unorm
    if tex_format == Tex_format.bc7:
        return Dds_dxgi.dxgi_format_bc7_unorm
    if tex_format == Tex_format.a8:
        return Dds_dxgi.dxgi_format_a8_unorm
    if tex_format == Tex_format.l8:
        return Dds_dxgi.dxgi_format_r8_unorm
    if tex_format == Tex_format.b4g4r4a4:
        return Dds_dxgi.dxgi_format_b4g4r4a4_unorm


def get_dds_dxt10_resource_dimension():
    # todo for sure
    return 3


def get_dds_dxt10_misc_flag():
    # todo for sure
    return 0


def get_dds_dxt10_array_size():
    return 1


def get_dds_dxt10_misc_flags2():
    # todo for sure
    return 1


def get_pitch(tex):
    format = tex.hdr.format
    height = get_dds_height(tex)
    width = get_dds_width(tex)
    # these don't seem to break for L8 or A8 so :shrug:
    # doc: https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide#dds-file-layout
    if format == Tex_format.b8g8r8a8 or format == Tex_format.b8g8r8x8:
        bits_per_pixel = 32
        pitch = (width * bits_per_pixel + 7) / 8
    elif format == Tex_format.b4g4r4a4:
        bits_per_pixel = 16
        pitch = (width * bits_per_pixel + 3) / 8
    elif format == Tex_format.a8 or format == Tex_format.l8:
        bits_per_pixel = 8
        pitch = (width * bits_per_pixel + 7) / 8
    else:
        if format == Tex_format.dxt1:
            block_size = 8
        elif format == Tex_format.bc7 or format == Tex_format.dxt5 or format == Tex_format.dxt3 or format == Tex_format.ati2 or format == Tex_format.ati1:
            block_size = 16
        # microsoft recommends width+3 and height+3, but I just set mine to match nvidia texture tools
        else:
            print(format)
        # needs to break if no block_size.
        pitch = max(1, (width / 4)) * max(1, (height / 4)) * block_size
    return int(pitch)


def get_ddspf_header(format, fourcc):
    # these don't seem to break for L8 or A8 so :shrug:
    size = 32
    if format == Tex_format.b8g8r8a8:
        # basically just BGRA (B,G,R,A) w/ 8bit per channel, eg rbitmask = [0,0,255,0], could write as array but w/e.
        flags = Dds_ddspf_ff.ddpf_alpha.value + Dds_ddspf_ff.ddpf_rgb.value
        rgbBitCount = 32
        rBitMask = 16711680
        gBitMask = 65280
        bBitmask = 255
        aBitmask = 4278190080
    elif format == Tex_format.a8:
        flags = Dds_ddspf_ff.ddpf_alpha.value
        rgbBitCount = 32
        rBitMask = 0
        gBitMask = 0
        bBitmask = 0
        aBitmask = 255
    elif format == Tex_format.l8:
        flags = Dds_ddspf_ff.ddpf_luminance.value
        rgbBitCount = 32
        rBitMask = 255
        gBitMask = 0
        bBitmask = 0
        aBitmask = 0
    elif format == Tex_format.b4g4r4a4:
        flags = Dds_ddspf_ff.ddpf_alphapixels.value + Dds_ddspf_ff.ddpf_rgb.value
        rgbBitCount = 16
        rBitMask = 0
        gBitMask = 0
        bBitmask = 0
        aBitmask = 0
    else:
        flags = Dds_ddspf_ff.ddpf_fourcc.value
        rgbBitCount = 0
        rBitMask = 0
        gBitMask = 0
        bBitmask = 0
        aBitmask = 0

        # no error catching I want this to break if it's fucked up.
    ddspf_header = pack('<IIIIIIII', size, flags, fourcc.value,
                        rgbBitCount, rBitMask, gBitMask, bBitmask, aBitmask)

    return ddspf_header


def get_dds_flags(format, mipmapCount):
    flags = (Dds_ff.ddsd_caps.value + Dds_ff.ddsd_width.value +
             Dds_ff.ddsd_height.value + Dds_ff.ddsd_pixelformat)
    if format == Tex_format.a8 or Tex_format.l8 or Tex_format.b8g8r8a8:
        flags += Dds_ff.ddsd_pitch.value
    else:
        flags += Dds_ff.ddsd_linearsize.value
    if mipmapCount > 1:
        flags += Dds_ff.ddsd_mipmapcount.value
    return flags


def get_dds_caps1(tex):
    # todo i don't remember how the flags+= works so go look at it again
    flags = Dds_cf.ddscaps_texture.value
    if tex.hdr.mip_levels > 1:
        flags += (Dds_cf.ddscaps_complex.value + Dds_cf.ddscaps_mipmap.value)
    return flags


def get_dds_binary(path):
    with open(path, 'rb') as file:
        tex_data = file.read()

    tex_io = KaitaiStream(io.BytesIO(tex_data))
    tex_binary = Tex(tex_io)

    magic = b'DDS '
    size = 124
    flags = get_dds_flags(tex_binary.hdr.format, tex_binary.hdr.mip_levels)
    height = get_dds_height(tex_binary)
    width = get_dds_width(tex_binary)
    pitch = get_pitch(tex_binary)
    depth = 1
    mipmapCount = get_dds_mipmapCount(tex_binary)
    reserved1_array = numpy.zeros(11, dtype=numpy.int32)
    ddspf_header = get_ddspf_header(
        tex_binary.hdr.format, get_dds_fourcc(tex_binary.hdr.format))
    caps1 = get_dds_caps1(tex_binary)
    caps2 = 0
    caps3 = 0
    caps4 = 0
    reserved2 = 0

    header = magic + pack('<IIIIIII', size, flags, height, width, pitch, depth, mipmapCount) + \
        reserved1_array.tobytes() + ddspf_header + pack('<IIIII',
                                                        caps1, caps2, caps3, caps4, reserved2)

    if get_dds_fourcc(tex_binary.hdr.format) == Dds_fourcc.dx10:
        header += get_dds_dxt10_header(tex_binary)

    return header + tex_binary.bdy.data


def write_dds_file(input_path, output_path):
    dds_binary = get_dds_binary(input_path)
    with open(output_path, 'wb') as file:
        file.write(dds_binary)
