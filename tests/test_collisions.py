import pytest
from pylumina import Simulation


class TestCollisions:
    def test_sphere_plane_bounce(self):
        """A sphere dropped onto a plane should not go below the plane."""
        sim = Simulation()
        sim.enable_gravity()
        sim.enable_collisions(True, restitution=0.5)

        sim.add_plane(normal=(0, 1, 0), offset=0)
        ball = sim.add_particle("ball", position=(0, 5, 0), mass=1.0)
        ball.damping = 0.0   # no damping for clean test
        sim.add_sphere(ball, radius=0.5)

        # Short simulation — just until first bounce
        for _ in range(150):
            sim.step(0.005)

        # Ball should remain above the plane surface (y >= -radius)
        assert ball.position.y >= -0.6, f"Ball fell through plane at y={ball.position.y}"

    def test_sphere_sphere(self):
        """Two spheres approaching should collide and change velocities."""
        sim = Simulation()
        sim.enable_collisions(True, restitution=1.0)

        a = sim.add_particle("a", position=(-2, 0, 0), mass=1.0,
                             velocity=(5, 0, 0))
        a.damping = 0.0
        sim.add_sphere(a, radius=1.0)

        b = sim.add_particle("b", position=(2, 0, 0), mass=1.0,
                             velocity=(-5, 0, 0))
        b.damping = 0.0
        sim.add_sphere(b, radius=1.0)

        # They start 4 units apart, closing at 10 units/s = meet in 0.2s
        sim.run(steps=50, dt=0.005)

        # After elastic collision of equal masses, velocities swap
        assert a.velocity.x < 1.0, f"a.vx should be negative, got {a.velocity.x}"
        assert b.velocity.x > -1.0, f"b.vx should be positive, got {b.velocity.x}"

    def test_collisions_disabled(self):
        """With collisions disabled, objects pass through each other."""
        sim = Simulation()
        sim.enable_collisions(False)

        a = sim.add_particle("a", position=(-1, 0, 0), mass=1.0,
                             velocity=(10, 0, 0))
        a.damping = 0.0
        sim.add_sphere(a, radius=1.0)

        b = sim.add_particle("b", position=(1, 0, 0), mass=1.0,
                             velocity=(-10, 0, 0))
        b.damping = 0.0
        sim.add_sphere(b, radius=1.0)

        sim.run(steps=50, dt=0.01)

        # They should have passed through each other
        assert a.position.x > 0
        assert b.position.x < 0

    def test_box_box(self):
        """Two boxes approaching should collide."""
        sim = Simulation()
        sim.enable_collisions(True, restitution=0.5)

        a = sim.add_particle("box_a", position=(-1, 0, 0), mass=1.0,
                             velocity=(3, 0, 0))
        a.damping = 0.0
        sim.add_box(a, half_extents=(0.5, 0.5, 0.5))

        b = sim.add_particle("box_b", position=(1, 0, 0), mass=1.0,
                             velocity=(-3, 0, 0))
        b.damping = 0.0
        sim.add_box(b, half_extents=(0.5, 0.5, 0.5))

        sim.run(steps=60, dt=0.005)

        # After collision, they should be separating
        assert a.velocity.x <= b.velocity.x
