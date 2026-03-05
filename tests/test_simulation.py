"""
Basic test suite for py_lumina.

Run with:  python -m pytest tests/
"""

import math
import pytest
import py_lumina as pl
from py_lumina._core import Vector3D, Particle, RigidBody, GravityForce


# ═══════════════════════════════════════════════════════════════════════
#  Vector3D
# ═══════════════════════════════════════════════════════════════════════

class TestVector3D:
    def test_construction(self):
        v = Vector3D(1.0, 2.0, 3.0)
        assert v.x == 1.0
        assert v.y == 2.0
        assert v.z == 3.0

    def test_addition(self):
        a = Vector3D(1, 2, 3)
        b = Vector3D(4, 5, 6)
        c = a + b
        assert c.x == 5.0 and c.y == 7.0 and c.z == 9.0

    def test_dot_product(self):
        a = Vector3D(1, 0, 0)
        b = Vector3D(0, 1, 0)
        assert a.dot(b) == 0.0

    def test_cross_product(self):
        a = Vector3D(1, 0, 0)
        b = Vector3D(0, 1, 0)
        c = a.cross(b)
        assert c.z == pytest.approx(1.0)

    def test_magnitude(self):
        v = Vector3D(3, 4, 0)
        assert v.magnitude() == pytest.approx(5.0)

    def test_normalized(self):
        v = Vector3D(0, 0, 5)
        n = v.normalized()
        assert n.z == pytest.approx(1.0)
        assert n.magnitude() == pytest.approx(1.0)


# ═══════════════════════════════════════════════════════════════════════
#  Particle
# ═══════════════════════════════════════════════════════════════════════

class TestParticle:
    def test_free_fall(self):
        """A particle under gravity should accelerate downward."""
        p = Particle("test", Vector3D(0, 100, 0), 1.0)
        p.damping = 0.0
        gravity = Vector3D(0, -9.81, 0)
        dt = 0.01
        for _ in range(100):
            p.apply_force(gravity * p.mass)
            p.integrate(dt)
        # After 1 second: y ≈ 100 - 0.5·9.81·1² ≈ 95.095
        assert p.position.y < 100.0
        assert p.velocity.y < 0.0

    def test_static_ignores_force(self):
        p = Particle("wall", Vector3D(0, 0, 0), 1.0)
        p.is_static = True
        p.apply_force(Vector3D(100, 100, 100))
        p.integrate(0.01)
        assert p.position.x == 0.0 and p.position.y == 0.0


# ═══════════════════════════════════════════════════════════════════════
#  Simulation (high-level)
# ═══════════════════════════════════════════════════════════════════════

class TestSimulation:
    def test_basic_run(self):
        sim = pl.Simulation(name="test")
        sim.add_gravity()
        sim.add_particle("ball", position=(0, 10, 0), mass=1.0)
        sim.run(dt=0.01, steps=100)
        ball = sim.get_particle("ball")
        assert ball.position.y < 10.0

    def test_recording(self):
        sim = pl.Simulation()
        sim.add_gravity()
        sim.add_particle("p", position=(0, 5, 0), mass=1.0)
        sim.enable_recording()
        sim.run(dt=0.01, steps=50)
        assert len(sim.history) == 50

    def test_rigid_body_rotation(self):
        sim = pl.Simulation()
        rb = sim.add_rigid_body(
            "spinner", position=(0, 0, 0),
            mass=1.0, moment_of_inertia=1.0,
            angular_velocity=(0, 0, 10),
            is_static=False,
        )
        sim.run(dt=0.01, steps=100)
        # Angular velocity should still be non-trivial (damped, but present)
        assert abs(rb.angular_velocity.z) > 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
