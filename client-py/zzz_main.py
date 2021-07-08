import struct
import numpy as np

format_str = '>2f'
ret = struct.pack(format_str, *[1., 1.])
print(ret)
print(type(ret))

ret = np.array([1., 1.], dtype='>f').tobytes()
print(ret)
print(type(ret))


format_str = '>2q'
ret = struct.pack(format_str, *[123321, 123123])
print(ret)
print(type(ret))

ret = np.array([123321, 123123], dtype='>q').tobytes()
print(ret)
print(type(ret))

