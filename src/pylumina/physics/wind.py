from .._core import WindForce, Vector3D

class Wind:
    def __init__(self, direction=(1, 0, 0), strength=5.0):
        self._force = WindForce(Vector3D(*direction), strength)
    
    @property
    def core(self):
        return self._force
