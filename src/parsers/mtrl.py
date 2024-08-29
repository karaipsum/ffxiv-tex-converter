# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Mtrl(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.signature = self._io.read_u4le()
        self.file_size = self._io.read_u2le()
        self.color_set_data_size = self._io.read_u2le()
        self.string_table_size = self._io.read_u2le()
        self.shader_name_offset = self._io.read_u2le()
        self.texture_count = self._io.read_u1()
        self.uv_set_count = self._io.read_u1()
        self.color_set_count = self._io.read_u1()
        self.additional_data_size = self._io.read_u1()
        self.textures = []
        for i in range(self.texture_count):
            self.textures.append(Mtrl.Texture(self._io, self, self._root))

        self.uv_sets = []
        for i in range(self.uv_set_count):
            self.uv_sets.append(Mtrl.UvSet(self._io, self, self._root))

        self.color_sets = []
        for i in range(self.color_set_count):
            self.color_sets.append(Mtrl.ColorSet(self._io, self, self._root))

        self.string_table = self._io.read_bytes(self.string_table_size)
        self.additional_data = self._io.read_bytes(self.additional_data_size)
        self.color_set_data = self._io.read_bytes(self.color_set_data_size)
        self.shader_info = Mtrl.ShaderInfo(self._io, self, self._root)
        self.shader_keys = []
        for i in range(self.shader_info.shader_key_count):
            self.shader_keys.append(Mtrl.ShaderKey(self._io, self, self._root))

        self.shader_constants = []
        for i in range(self.shader_info.shader_constants_count):
            self.shader_constants.append(Mtrl.ShaderConstant(self._io, self, self._root))

        self.texture_samplers = []
        for i in range(self.shader_info.texture_sampler_count):
            self.texture_samplers.append(Mtrl.TextureSampler(self._io, self, self._root))

        self._raw_shader_constants_data = self._io.read_bytes(self.shader_info.shader_constants_data_size)
        _io__raw_shader_constants_data = KaitaiStream(BytesIO(self._raw_shader_constants_data))
        self.shader_constants_data = Mtrl.ShaderConstantsData(_io__raw_shader_constants_data, self, self._root)

    class ShaderConstantsData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(self._io.read_u1())
                i += 1



    class TextureSampler(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sampler_id = self._io.read_u4le()
            self.sampler_settings = self._io.read_u4le()
            self.texture_index = self._io.read_u1()
            self.padding = self._io.read_bytes(3)


    class ColorSet(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u2le()
            self.index = self._io.read_u2le()


    class ShaderKey(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.key_id = self._io.read_u4le()
            self.value = self._io.read_u4le()


    class ShaderConstant(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.constant_id = self._io.read_u4le()
            self.offset = self._io.read_u2le()
            self.size = self._io.read_u2le()

        @property
        def value_bytes(self):
            if hasattr(self, '_m_value_bytes'):
                return self._m_value_bytes

            if self.size > 16:
                io = self._root.shader_constants_data._io
                _pos = io.pos()
                io.seek(self.offset)
                self._m_value_bytes = io.read_bytes(self.size)
                io.seek(_pos)

            return getattr(self, '_m_value_bytes', None)

        @property
        def value_f4x4(self):
            if hasattr(self, '_m_value_f4x4'):
                return self._m_value_f4x4

            if self.size == 16:
                io = self._root.shader_constants_data._io
                _pos = io.pos()
                io.seek(self.offset)
                self._m_value_f4x4 = []
                for i in range(4):
                    self._m_value_f4x4.append(io.read_f4le())

                io.seek(_pos)

            return getattr(self, '_m_value_f4x4', None)

        @property
        def value_f4(self):
            if hasattr(self, '_m_value_f4'):
                return self._m_value_f4

            if self.size == 4:
                io = self._root.shader_constants_data._io
                _pos = io.pos()
                io.seek(self.offset)
                self._m_value_f4 = io.read_f4le()
                io.seek(_pos)

            return getattr(self, '_m_value_f4', None)

        @property
        def value_f4x2(self):
            if hasattr(self, '_m_value_f4x2'):
                return self._m_value_f4x2

            if self.size == 8:
                io = self._root.shader_constants_data._io
                _pos = io.pos()
                io.seek(self.offset)
                self._m_value_f4x2 = []
                for i in range(2):
                    self._m_value_f4x2.append(io.read_f4le())

                io.seek(_pos)

            return getattr(self, '_m_value_f4x2', None)

        @property
        def value_f4x3(self):
            if hasattr(self, '_m_value_f4x3'):
                return self._m_value_f4x3

            if self.size == 12:
                io = self._root.shader_constants_data._io
                _pos = io.pos()
                io.seek(self.offset)
                self._m_value_f4x3 = []
                for i in range(3):
                    self._m_value_f4x3.append(io.read_f4le())

                io.seek(_pos)

            return getattr(self, '_m_value_f4x3', None)


    class UvSet(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u2le()
            self.index = self._io.read_u2le()


    class Texture(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u2le()
            self.flags = self._io.read_u2le()


    class ShaderInfo(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.shader_constants_data_size = self._io.read_u2le()
            self.shader_key_count = self._io.read_u2le()
            self.shader_constants_count = self._io.read_u2le()
            self.texture_sampler_count = self._io.read_u2le()
            self.material_flags = self._io.read_u2le()
            self.material_flags2 = self._io.read_u2le()


    @property
    def shader_name(self):
        if hasattr(self, '_m_shader_name'):
            return self._m_shader_name

        _pos = self._io.pos()
        self._io.seek(self.shader_name_offset)
        self._m_shader_name = (self._io.read_bytes_term(0, False, True, True)).decode(u"ASCII")
        self._io.seek(_pos)
        return getattr(self, '_m_shader_name', None)


