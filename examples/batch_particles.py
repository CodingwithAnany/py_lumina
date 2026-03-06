"""
Batch particles demo — simulate 1000 particles with NumPy.
"""
import numpy as np
from pylumina import Simulation

sim = Simulation()
sim.enable_recording()

# Create 1000 random particles in a 10x10x10 cube
positions = np.random.uniform(-5, 5, size=(1000, 3))
positions[:, 1] = np.abs(positions[:, 1]) + 5   # start above ground

sim.add_particles(positions)

print(f"🔬 Batch Particles Demo — {sim.batch_count} particles")
print("=" * 50)

# Simulate 100 steps
sim.run(steps=100, dt=0.01)

# Get final positions
final = sim.get_positions()
print(f"  After 1.0s:")
print(f"    Mean Y: {final[:, 1].mean():.3f}")
print(f"    Min  Y: {final[:, 1].min():.3f}")
print(f"    Max  Y: {final[:, 1].max():.3f}")

# More steps
sim.run(steps=400, dt=0.01)
final2 = sim.get_positions()
print(f"\n  After 5.0s:")
print(f"    Mean Y: {final2[:, 1].mean():.3f}")
print(f"    Min  Y: {final2[:, 1].min():.3f}")
print(f"    Max  Y: {final2[:, 1].max():.3f}")
print(f"\n  ✅ All {sim.batch_count} particles simulated in C++!")
