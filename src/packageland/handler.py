import gc
import os
from multiprocessing import Pool
from tqdm import tqdm


# Switching to a chunk based approach

def get_file_size(file_path):
    return os.path.getsize(file_path)

def create_intelligent_chunks(items, target_chunk_size_mb=100):
    chunks = []
    current_chunk = []
    current_chunk_size = 0
    target_chunk_size = target_chunk_size_mb * 1024 * 1024  # Convert MB to bytes

    for item in items:
        file_size = get_file_size(item)
        if current_chunk_size + file_size > target_chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_chunk_size = 0
        
        current_chunk.append(item)
        current_chunk_size += file_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def parallel_process(items, function, target_chunk_size_mb=100):
    core_count = os.cpu_count()
    chunks = create_intelligent_chunks(items, target_chunk_size_mb)
    
    with tqdm(total=len(items)) as pb:
        for chunk in chunks:
            with Pool(core_count) as p:
                p.map(function, chunk)
                gc.collect()
            pb.update(len(chunk))

def solo_process(items, function):
    list(map(function, tqdm(items)))