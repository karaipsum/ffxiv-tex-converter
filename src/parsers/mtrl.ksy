meta:
  id: mtrl
  file-extension: mtrl
  endian: le

seq:
  - id: signature
    type: u4
    doc: Should be 0x00000301 (16973824)
  - id: file_size
    type: u2
  - id: color_set_data_size
    type: u2
  - id: string_table_size
    type: u2
  - id: shader_name_offset
    type: u2
  - id: texture_count
    type: u1
  - id: uv_set_count
    type: u1
  - id: color_set_count
    type: u1
  - id: additional_data_size
    type: u1
  - id: textures
    type: texture
    repeat: expr
    repeat-expr: texture_count
  - id: uv_sets
    type: uv_set
    repeat: expr
    repeat-expr: uv_set_count
  - id: color_sets
    type: color_set
    repeat: expr
    repeat-expr: color_set_count
  - id: string_table
    size: string_table_size
  - id: additional_data
    size: additional_data_size
  - id: color_set_data
    size: color_set_data_size
  - id: shader_info
    type: shader_info
  - id: shader_keys
    type: shader_key
    repeat: expr
    repeat-expr: shader_info.shader_key_count
  - id: shader_constants
    type: shader_constant
    repeat: expr
    repeat-expr: shader_info.shader_constants_count
  - id: texture_samplers
    type: texture_sampler
    repeat: expr
    repeat-expr: shader_info.texture_sampler_count
  - id: shader_constants_data
    size: shader_info.shader_constants_data_size
    type: shader_constants_data

types:
  texture:
    seq:
      - id: offset
        type: u2
      - id: flags
        type: u2
  uv_set:
    seq:
      - id: offset
        type: u2
      - id: index
        type: u2
  color_set:
    seq:
      - id: offset
        type: u2
      - id: index
        type: u2
  shader_info:
    seq:
      - id: shader_constants_data_size
        type: u2
      - id: shader_key_count
        type: u2
      - id: shader_constants_count
        type: u2
      - id: texture_sampler_count
        type: u2
      - id: material_flags
        type: u2
      - id: material_flags2
        type: u2
  shader_key:
    seq:
      - id: key_id
        type: u4
      - id: value
        type: u4
  shader_constant:
    seq:
      - id: constant_id
        type: u4
      - id: offset
        type: u2
      - id: size
        type: u2
    instances:
      value_f4:
        io: _root.shader_constants_data._io
        pos: offset
        type: f4
        if: size == 4
      value_f4x2:
        io: _root.shader_constants_data._io
        pos: offset
        type: f4
        repeat: expr
        repeat-expr: 2
        if: size == 8
      value_f4x3:
        io: _root.shader_constants_data._io
        pos: offset
        type: f4
        repeat: expr
        repeat-expr: 3
        if: size == 12
      value_f4x4:
        io: _root.shader_constants_data._io
        pos: offset
        type: f4
        repeat: expr
        repeat-expr: 4
        if: size == 16
      value_bytes:
        io: _root.shader_constants_data._io
        pos: offset
        size: size
        if: size > 16
  texture_sampler:
    seq:
      - id: sampler_id
        type: u4
      - id: sampler_settings
        type: u4
      - id: texture_index
        type: u1
      - id: padding
        size: 3
  shader_constants_data:
    seq:
      - id: data
        type: u1
        repeat: eos

instances:
  shader_name:
    pos: shader_name_offset
    type: str
    terminator: 0
    encoding: ASCII