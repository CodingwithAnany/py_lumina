"""
Example simulation script designed for CLI export.

Run with:
    pylumina run examples/basic_simulation.py
    pylumina run examples/basic_simulation.py --output ./results --format vtk
"""
from pylumina import Simulation, render

sim = Simulation()
sim.enable_gravity()
sim.enable_recording()
sim.enable_collisions(True, restitution=0.7)

sim.add_plane(normal=(0, 1, 0), offset=0)

ball1 = sim.add_particle("ball_1", position=(0, 10, 0), mass=1.0)
sim.add_sphere(ball1, radius=0.5)

ball2 = sim.add_particle("ball_2", position=(3, 15, 0), mass=2.0)
sim.add_sphere(ball2, radius=0.8)

print("🏀 Collision Demo — Bouncing Spheres")
print("=" * 40)

sim.run(steps=500, dt=0.01)

print(f"  Simulated {sim.step_count} steps ({sim.time:.2f}s)")
print(f"  Recorded {len(sim.history)} frames")
render(sim)
