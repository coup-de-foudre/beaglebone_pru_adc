import io
import numpy as np

def ndarray_to_bytes(array: np.ndarray) -> bytes:
    """
    Encode a np array to bytes in .npy format
    """
    bio = io.BytesIO()
	np.save(bio, array, allow_pickle=False)
    return bio.getvalue()

def bytes_to_ndarray(b: bytes) -> np.ndarray:
    return np.load(b)
