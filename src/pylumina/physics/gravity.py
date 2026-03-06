from .._core import GravityForce, Vector3D

class Gravity:
    def __init__(self, y=-9.81, x=0, z=0):
        self._force = GravityForce(Vector3D(x, y, z))
    
    @property
    def core(self):
        return self._force
