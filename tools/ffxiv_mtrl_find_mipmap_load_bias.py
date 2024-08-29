from pathlib import Path
from kaitaistruct import KaitaiStream, BytesIO
from src.parsers.mtrl import Mtrl
import struct

def process_mtrl_file(input_path: Path, output_path: Path):
    with input_path.open('rb') as f:
        data = f.read()

    io = KaitaiStream(BytesIO(data))
    mtrl = Mtrl(io)

    constant_id = 0x39551220
    target_constant = next((sc for sc in mtrl.shader_constants if sc.constant_id == constant_id), None)

    if target_constant is not None:
        shader_data_start = (mtrl._io.size() - mtrl.shader_info.shader_constants_data_size)
        actual_offset = shader_data_start + target_constant.offset

        current_value = struct.unpack('<f', data[actual_offset:actual_offset + 4])[0]

        if current_value != 0.0:
            new_value = 0.0
            new_bytes = struct.pack('<f', new_value)
            data = (
                    data[:actual_offset] +
                    new_bytes +
                    data[actual_offset + 4:]
            )

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(data)

            return True  # Indicate that the file was modified

    return False  # Indicate that the file was not modified

def process_directory(input_dir: Path, output_dir: Path):
    for input_path in input_dir.rglob('*.mtrl'):
        relative_path = input_path.relative_to(input_dir)
        output_path = output_dir / relative_path

        try:
            was_modified = process_mtrl_file(input_path, output_path)
            if was_modified:
                print(f"Modified: {input_path} -> {output_path}")
            else:
                print(f"Skipped (already 0 or constant not found): {input_path}")
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}")

# Set your input and output directories here
input_directory = Path("material_input")
output_directory = Path("material_output")

process_directory(input_directory, output_directory)