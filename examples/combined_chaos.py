"""
Combined Chaos

This scripts tests NumPy batches, Sphere-Plane collisions,
and Wind forces all running concurrently in the same physics engine loop.

Run with:
    pylumina run examples/combined_chaos.py --format vtk --output ./demo_chaos
"""
import numpy as np
from pylumina import Simulation
from pylumina.physics import Wind, Drag

sim = Simulation()
sim.enable_recording()

print("🌪️ Pylumina Combined Chaos Demonstration")
print("========================================")

# 1) Natural Environment
sim.enable_gravity(y=-9.8)
sim.add_force(Wind(direction=(-1, 0, 0), strength=5.0)) # Side wind
sim.add_force(Drag(cd=0.47, area=0.1, rho=1.0))     # Friction

# 2) Standard Primitives (Bouncing balls!)
sim.enable_collisions(True, restitution=0.85)
sim.add_plane(normal=(0, 1, 0), offset=0)

for x in range(-5, 5, 2):
    ball = sim.add_particle(f"ball_{x}", position=(x, 15, 0), mass=2.0)
    sim.add_sphere(ball, radius=1.0)
print("  ✅ Added 5 bouncing boulders")

# 3) High-performance Batch (15,000 rain droplets!)
rain_n = 15000
# Generate 15k positions scattered within a volume (X: -10 to 10, Y: 20 to 50, Z: -5 to 5)
positions = np.random.uniform(-1, 1, size=(rain_n, 3))
positions[:, 0] *= 10.0   # Span X
positions[:, 1] *= 15.0   # Span Y
positions[:, 1] += 35.0   # Offset Y to the sky
positions[:, 2] *= 5.0    # Span Z

# Optional velocities
velocities = np.random.randn(rain_n, 3) * 0.5

# Standard masses
masses = np.ones(rain_n) * 0.05

sim.add_particles(positions, velocities=velocities, masses=masses)
print(f"  ✅ Batched {rain_n} rain particles into NumPy SoA layout")

# 4) Run the engine
print("\nRunning engine at 100hz for 3 seconds...")
sim.run(steps=300, dt=0.01)

print(f"✅ Success. Try rendering the VTK frames in ParaView!")
