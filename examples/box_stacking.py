"""
Box Stacking Demo

Watch a pyramid of boxes collapse under gravity, illustrating
the C++ engine's AABB collision detection and impulse resolution!

Run with:
    pylumina run examples/box_stacking.py --format vtk --output ./box_demo
"""
from pylumina import Simulation

sim = Simulation()
sim.enable_recording()

# Standard earths gravity (-9.81 m/s^2)
sim.enable_gravity()

# We enable collisions. Bouncy = 0.3 means they absorb 70% of impact energy.
sim.enable_collisions(True, restitution=0.3)

# Add the floor
sim.add_plane(normal=(0, 1, 0), offset=0)

# Build a pyramid of boxes!
rows = 5
box_size = 1.0
half_extent = box_size / 2.0

start_y = half_extent
for row in range(rows):
    boxes_in_row = rows - row
    start_x = -boxes_in_row * half_extent
    y = start_y + row * (box_size + 0.05) # slight vertical gap for stability

    for i in range(boxes_in_row):
        x = start_x + (i * box_size * 1.05) + (half_extent if row % 2 == 1 else 0)
        
        # Give them subtle initial velocities or offsets to make them tumble!
        vel_x = (x * 0.1) 
        
        box = sim.add_rigid_body(f"box_{row}_{i}", position=(x, y, 0), mass=2.0)
        box.velocity.x = vel_x
        # Add the physical hit-box
        sim.add_box(box, half_extents=(half_extent, half_extent, half_extent))

print("🧱 Box Stacking Demonstration")
print("===========================")
print("Running 3 seconds of simulation...")

sim.run(steps=300, dt=0.01)

print(f"✅ Finished! {len(sim.history)} steps recorded.")
