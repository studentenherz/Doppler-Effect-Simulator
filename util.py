import numpy as np

def convert_to_float32(a : np.ndarray) -> np.ndarray:
	if a.dtype == np.int16:
		return a.astype(np.float32) / 32767
	if a.dtype == np.int32:
		return a.astype(np.float32) / 2147483647
	if a.dtype == np.int8:
		return -1 + 2 * a.astype(np.float32) / 256
	return a