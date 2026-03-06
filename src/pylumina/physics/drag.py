from .._core import DragForce

class Drag:
    def __init__(self, cd=0.47, area=0.01, rho=1.225):
        self._force = DragForce(cd, area, rho)
    
    @property
    def core(self):
        return self._force
