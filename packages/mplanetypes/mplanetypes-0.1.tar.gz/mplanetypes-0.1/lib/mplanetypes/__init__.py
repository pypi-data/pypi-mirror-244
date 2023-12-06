import numpy as np
import pathlib

__all__ = [
    'is_signed_int',
    'is_int',
    'check_type',
    'check_return_type_None_default',
    'check_return_int',
    'check_return_int_None_default',
    'check_return_Path',
    'check_return_Path_None_default'
]

def is_signed_int(num):
    return isinstance(num, (int, np.int8, np.int16, np.int32, np.int64))

def is_int(num):
    return isinstance(num, (int, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64))

def check_type(obj, name, expected_type):

    if not isinstance(obj, expected_type):
        raise TypeError(f"`{name}` must be of type `{expected_type.__name__}`, not `{type(obj).__name__}`.")

def check_return_type_None_default(obj, name, expected_type, default):

    if obj is not None and not isinstance(obj, expected_type):
        raise TypeError(f"`{name}` must be of type `{expected_type.__name__}`, not `{type(obj).__name__}`.")

    elif obj is not None:
        return obj

    else:
        return default

def check_return_int(obj, name):

    if not is_int(obj):
        raise TypeError(f"`{name}` must be of type `int`, not `{type(obj).__name__}`.")

    else:
        return int(obj)

def check_return_int_None_default(obj, name, default):

    if obj is not None and not is_int(obj):
        raise TypeError(f"`{name}` must be of type `int`, not `{type(obj).__name__}`.")

    elif obj is not None:
        return int(obj)

    else:
        return default

def check_return_Path(obj, name):

    if not isinstance(obj, (str, pathlib.Path)):
        raise TypeError(f"`{name}` must be either of type `str` or `pathlib.Path`, not `{type(obj).__name__}`.")

    else:
        return pathlib.Path(obj)

def check_return_Path_None_default(obj, name, default):

    if obj is None:
        return default

    elif not isinstance(obj, (str, pathlib.Path)):
        raise TypeError(f"`{name}` must be either of type `str` or `pathlib.Path`, not `{type(obj).__name__}`.")

    else:
        return pathlib.Path(obj)