import pytest
from pylumina import Simulation
from pylumina.physics import Gravity


class TestSimulation:
    def test_gravity_fall(self):
        sim = Simulation()
        sim.enable_gravity()
        p = sim.add_particle("ball", position=(0, 10, 0), mass=1.0)
        sim.run(steps=100, dt=0.01)
        assert p.position.y < 10
        assert p.velocity.y < 0

    def test_rigid_body_rotation(self):
        sim = Simulation()
        rb = sim.add_rigid_body("box", position=(0, 0, 0), mass=1.0, moi=1.0)
        rb.angular_velocity.z = 2.0
        sim.run(steps=100, dt=0.01)
        assert rb.orientation.z > 0

    def test_step_count(self):
        sim = Simulation()
        sim.run(steps=50, dt=0.01)
        assert sim.step_count == 50

    def test_time(self):
        sim = Simulation()
        sim.run(steps=100, dt=0.01)
        assert abs(sim.time - 1.0) < 0.001

    def test_force_wrapper(self):
        sim = Simulation()
        g = Gravity(y=-9.81)
        sim.add_force(g)
        p = sim.add_particle("p", position=(0, 5, 0), mass=1.0)
        sim.run(steps=50, dt=0.01)
        assert p.position.y < 5
