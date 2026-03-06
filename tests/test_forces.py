import pytest
from pylumina.physics import Gravity, Wind, Drag
from pylumina._core import Vector3D

def test_gravity_creation():
    g = Gravity(y=-9.8)
    assert g.core is not None

def test_wind_creation():
    w = Wind(direction=(0, 1, 0), strength=2.0)
    assert w.core is not None

def test_drag_creation():
    d = Drag(cd=0.1)
    assert d.core is not None
