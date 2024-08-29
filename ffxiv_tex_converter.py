import argparse
from pathlib import Path
from src.packageland import handler
from src.converters import dds_to_tex, tex_to_dds

parser = argparse.ArgumentParser(description="ffxiv-tex-converter, FFXIV TEX FILE CONVERTER")
parser.add_argument('--directory', '-d', metavar='-D', type=str, 
                    help='Initial directory to be processed.',
                    required=True)
parser.add_argument('--command', '-c', metavar='-C', type=str, 
                    help='dds-to-tex, tex-to-dds', 
                    required=True)
parser.add_argument('--parallel', '-p', action='store_true',
                    help='Enable multicore processing')
parser.add_argument('--chunk-size', '-cs', metavar='-CS', type=int, default=100,
                    help='Target chunk size in MB for parallel processing. default = 100')

args = parser.parse_args()

folder = Path(args.directory)

def read_command(command):
    if 'dds-to-tex' == command.lower():
        return do_the_thing_dds_to_tex
    if 'tex-to-dds' == command.lower():
        return do_the_thing_tex_to_dds


def do_the_thing_dds_to_tex(path):
    out_folder = Path(str(folder) + '_tex')
    out_path = Path.joinpath(out_folder, Path(
        *path.parts[1:]).with_suffix('.tex'))
    out_path.parent.mkdir(exist_ok=True, parents=True)
    dds_to_tex.write_tex_file(str(path), str(out_path))


def do_the_thing_tex_to_dds(path):
    out_folder = Path(str(folder) + '_dds')
    out_path = Path.joinpath(out_folder, Path(
        *path.parts[1:]).with_suffix('.dds'))
    out_path.parent.mkdir(exist_ok=True, parents=True)
    try:
        tex_to_dds.write_dds_file(str(path), str(out_path))
    except AttributeError:
        print(f"Error processing {path.name}")


if __name__ == '__main__':
    grabber = list(folder.glob('**/*.*'))
    function = read_command(args.command)
    if args.parallel:
        handler.parallel_process(grabber, function, args.chunk_size)
    else:
        handler.solo_process(grabber, function)
