# if type is skin.shpk
# does: add shader constant 0x38A64362, size should be of valueF4x3, with values 0=0.5, 1=0.5, 2=0.5
# does: adjust shader info to account for the new shader constant
# does: replace shader key:value from [0x380CAED0: [whatever] to [0x380CAED0: 0x72E697CD]. if not key not exist, add key:value




# example:
# if ShaderKey.key_id = 0x380CAED0 and Shaderkey.key_value = 0x2BDB45F1 or Shaderkey.key_value = 0xF5673524:
#     replace ShaderKey.key_value with 0x72E697CD

# if not "0x38A64362" in shaderConstants' constant_id:
#         create new ShaderConstant:
#             constant_id = 0x38A64362
#             offset = previous shaderConstant's offset + 0xC
#             size = 0xC
#         append to the end of the shaderConstant's list
#         finally at the end of the file append
#             0x0000003F0000003F0000003F

from pathlib import Path
from kaitaistruct import KaitaiStream, BytesIO
from src.parsers.mtrl import Mtrl
import struct

def process_mtrl_file(input_path: Path, output_path: Path):
    try:
        with input_path.open('rb') as f:
            original_data = f.read()

        if b"skin.shpk" not in original_data:
            print(f"Skipped (not a skin shader): {input_path}")
            return False

        io = KaitaiStream(BytesIO(original_data))
        mtrl = Mtrl(io)

        shader_key_exists = False
        for key in mtrl.shader_keys:
            if key.key_id == 0x380CAED0:
                shader_key_exists = True
                if key.value == 0x72E697CD:
                    print(f"Skipped (already processed): {input_path}")
                    return False
                break

        new_data = bytearray()

        # Header
        new_data.extend(struct.pack('<I', mtrl.signature))
        file_size_offset = len(new_data)
        new_data.extend(struct.pack('<H', 0))  # Placeholder for file size
        new_data.extend(struct.pack('<H', mtrl.color_set_data_size))
        new_data.extend(struct.pack('<H', mtrl.string_table_size))
        new_data.extend(struct.pack('<H', mtrl.shader_name_offset))
        new_data.extend(struct.pack('<BBB', mtrl.texture_count, mtrl.uv_set_count, mtrl.color_set_count))
        new_data.extend(struct.pack('<B', mtrl.additional_data_size))

        # Textures, UV sets, Color sets
        for texture in mtrl.textures:
            new_data.extend(struct.pack('<HH', texture.offset, texture.flags))
        for uv_set in mtrl.uv_sets:
            new_data.extend(struct.pack('<HH', uv_set.offset, uv_set.index))
        for color_set in mtrl.color_sets:
            new_data.extend(struct.pack('<HH', color_set.offset, color_set.index))

        # String table, additional data, color set data
        new_data.extend(mtrl.string_table)
        new_data.extend(mtrl.additional_data)
        new_data.extend(mtrl.color_set_data)

        # Shader info
        shader_info_offset = len(new_data)
        new_shader_key_count = mtrl.shader_info.shader_key_count + (0 if shader_key_exists else 1)
        new_data.extend(struct.pack('<HHHHHH', 
            mtrl.shader_info.shader_constants_data_size + 12,  # Increase by 12 (0x4C to 0x58)
            new_shader_key_count,
            mtrl.shader_info.shader_constants_count + 1,  # Increase by 1 (0x10 to 0x11)
            mtrl.shader_info.texture_sampler_count,
            mtrl.shader_info.material_flags,
            mtrl.shader_info.material_flags2
        ))

        # Shader keys
        key_0x380CAED0_added = False
        for key in mtrl.shader_keys:
            if key.key_id == 0x380CAED0:
                new_data.extend(struct.pack('<II', key.key_id, 0x72E697CD))
                key_0x380CAED0_added = True
            else:
                new_data.extend(struct.pack('<II', key.key_id, key.value))

        if not key_0x380CAED0_added:
            new_data.extend(struct.pack('<II', 0x380CAED0, 0x72E697CD))

        # Shader constants
        last_offset = 0
        for constant in mtrl.shader_constants:
            new_data.extend(struct.pack('<IHH', constant.constant_id, constant.offset, constant.size))
            last_offset = constant.offset + constant.size

        # Add new shader constant
        new_data.extend(struct.pack('<IHH', 0x38A64362, last_offset, 12))

        # Texture samplers (copy verbatim from original data)
        texture_sampler_offset = shader_info_offset + 12 + (8 * mtrl.shader_info.shader_key_count) + (8 * mtrl.shader_info.shader_constants_count)
        texture_sampler_size = 12 * mtrl.shader_info.texture_sampler_count
        new_data.extend(original_data[texture_sampler_offset:texture_sampler_offset + texture_sampler_size])

        # Shader constants data (preserve original data)
        constants_data_offset = texture_sampler_offset + texture_sampler_size
        new_data.extend(original_data[constants_data_offset:constants_data_offset + mtrl.shader_info.shader_constants_data_size])

        # Add new constant data
        new_data.extend(struct.pack('<fff', 0.5, 0.5, 0.5))

        # Update file size
        struct.pack_into('<H', new_data, file_size_offset, len(new_data))

        # Write the modified data back to the file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('wb') as f:
            f.write(new_data)

        print(f"Modified: {input_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return False
    

def process_directory(input_dir: Path, output_dir: Path):
    for input_path in input_dir.rglob('*.mtrl'):
        relative_path = input_path.relative_to(input_dir)
        output_path = output_dir / relative_path

        try:
            was_modified = process_mtrl_file(input_path, output_path)
            if not was_modified:
                print(f"No modifications needed: {input_path}")
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}")

# Set your input and output directories here
input_directory = Path("material_input")
output_directory = Path("material_output")

process_directory(input_directory, output_directory)