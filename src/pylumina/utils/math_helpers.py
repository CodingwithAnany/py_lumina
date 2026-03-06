from .._core import Vector3D

def to_vector3d(val):
    if isinstance(val, (list, tuple)):
        return Vector3D(*val)
    return val
