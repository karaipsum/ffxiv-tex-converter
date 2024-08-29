## Required python libraries

    pip install kaitaistruct
    pip install numpy
    pip install tqdm

---
## ffxiv_tex_converter.py
```
ffxiv-tex-converter, FFXIV TEX FILE CONVERTER

options:
  -h, --help            show this help message and exit
  --directory -D, -d -D
                        Initial directory to be processed.
  --command -C, -c -C   dds-to-tex, tex-to-dds
  -p, --parallel        Enable multicore processing
  --chunk-size -CS, -cs -CS
                        Target chunk size in MB for parallel processing. default = 100
```
* Accepts nested directory structures.
* Supports Compressed Types:
   * BC1 (DXT1), BC2 (DXT3), BC3 (DXT5), BC4 (ATI1), BC5 (ATI2), BC7, BGRA4 (limited).

* Supports Uncompressed Types:
  * L8, A8, BGRA, BGRX
* Further support can be added on as need arises. If you need a specific format, open an issue.
### Usage examples:

**given directory "dog" has dds files I want to convert to FFXIV tex files.**

Run this command: `python ffxiv_tex_converter.py -d dog -c dds-to-tex`

I want to run it faster: `python ffxiv_tex_converter.py -d dog -c dds-to-tex -p --chunk-size 200`

It will output to **"dog_tex"** directory.

**given directory "cat" has FFXIV tex files I want to convert to DDS files.**

Run this command: `python ffxiv_tex_converter.py -d cat -c tex-to-dds`

I want to run it faster: `python ffxiv_tex_converter.py -d cat -c tex-to-dds -p --chunk-size 200`

It will output to **"cat_dds"** directory.

### What is this for?
* You want specific fine-grained control of the DDS you are feeding FFXIV.
* You want to convert many DDS or TEX files at once.

### How do I finely control my DDS?
* [Use Microsoft Textools](https://github.com/Microsoft/DirectXTex/wiki/Texconv) (Recommended)
* [Use Cuttlefish](https://github.com/akb825/Cuttlefish)
* Use Nvidia Texture Tools
* Use Intel Texture Tools

### Alternatives
* Penumbra import
* FFXIV TexTools import


# parsers

### dds.ksy

* kaitai struct to read dds header, body. body reading is only rudimentary to reach EOF.
* Read [Microsoft DDS_Header Docs](https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dds-header) for more info.


### tex.ksy

* kaitai struct to read tex header, body. body reading is only rudimentary to reach EOF.
* See Penumbra/TexTools/Lumina source code for more info.


### mtrl.ksy

* Reads ffxiv material files in a rudimentary manner.


# extra

### ffxiv_mtrl_find_mipmap_load_bias.py

* An example of using the mtrl.py (generated from the mtrl.ksy) to modify many FFXIV mtrl files' values in batch. This specifically corrects an issue with the mipmap load bias being too high on hairs.