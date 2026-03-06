import pytest
from pylumina import Simulation

class TestPhysicsEngine:
    def test_no_force_no_motion(self):
        sim = Simulation()
        p = sim.add_particle("P1", position=(0, 0, 0), mass=1.0)
        sim.step(0.1)
        assert p.position.x == 0
        assert p.position.y == 0

    def test_time_advances(self):
        sim = Simulation()
        sim.step(0.5)
        assert abs(sim.time - 0.5) < 0.001
        sim.step(0.5)
        assert abs(sim.time - 1.0) < 0.001

    def test_entity_count(self):
        sim = Simulation()
        sim.add_particle("a", (0, 0, 0), 1.0)
        sim.add_particle("b", (1, 0, 0), 1.0)
        assert len(sim.entities) >= 2
