# Pylumina Usage Guide

Welcome to Pylumina! This document is a comprehensive guide to understanding and using all the features of the Pylumina physics engine.

## Table of Contents
1. [Core Concepts](#1-core-concepts)
2. [Entities: Particles and Rigid Bodies](#2-entities-particles-and-rigid-bodies)
3. [Forces](#3-forces)
4. [Collisions](#4-collisions)
5. [Batch Particle Processing (NumPy)](#5-batch-particle-processing)
6. [Recording & Data Export](#6-recording--data-export)
7. [Command-Line Interface (CLI)](#7-command-line-interface)

---

## 1. Core Concepts
A `Simulation` is the primary wrapper for everything. It holds entities, applies forces, handles collisions, coordinates batch processing, and keeps track of simulation history.

```python
from pylumina import Simulation

sim = Simulation()
sim.step(dt=0.01)       # Advance simulation by 0.01 seconds
sim.run(steps=500, dt=0.01) # Advance simulation by 500 steps
```

`Simulation.step()` internally does:
1. Engine Step: computes physics logic (semi-implicit Euler integration, applying forces).
2. Collision System Step: detects collisions between enabled colliders and resolves them using impulsive responses.
3. Batch Processing Step: updates thousands of raw, stateless CPU particles mapped to C++ arrays.

---

## 2. Entities: Particles and Rigid Bodies

Pylumina uses two core entities:
- **Particle**: A point mass. It has `position`, `velocity`, `mass`, and `damping`.
- **RigidBody**: Inherits from Particle but also has a moment of inertia (`moi`), `orientation`, and `angular_velocity` in 3D. 

### Adding Entities
```python
p = sim.add_particle("Ball", position=(0, 10, 0), mass=2.5, velocity=(5, 0, 0))
rb = sim.add_rigid_body("Box", position=(0, 5, 0), mass=1.0, moi=1.0)
rb.angular_velocity.y = 3.14  # Spin around Y axis
```

Entities have attributes you can read and write directly to:
```python
p.position.y = 5.0
p.velocity.x += 10.0
p.damping = 0.05  # Linear speed damping inside the integrator
```

---

## 3. Forces

Pylumina includes three pre-built forces logic: `Gravity`, `Wind`, and `Drag`.

```python
sim.enable_gravity(y=-9.81) # Adds gravity on the Y-axis (-9.81 by default)

from pylumina.physics import Wind, Drag

# Add wind blowing along the X-axis
sim.add_force(Wind(direction=(1, 0, 0), strength=15.0))

# Add global drag (air resistance)
sim.add_force(Drag(cd=0.47, area=0.1, rho=1.225))
```

---

## 4. Collisions

Pylumina supports analytical narrow-phase collision detection between:
- Sphere vs Sphere
- Sphere vs Plane
- AABB Box vs AABB Box

### Setting up Collisions
Collisions are disabled by default. You need to enable them and define the "restitution" coefficient (how bouncy they are: `0.0` = completely dead, `1.0` = perfectly elastic).

```python
sim.enable_collisions(True, restitution=0.8)

# Add an infinite collision plane (the ground)
ground = sim.add_plane(normal=(0, 1, 0), offset=0.0)

# Add a sphere collider to a particle
ball = sim.add_particle("Ball", position=(0, 5, 0))
sim.add_sphere(ball, radius=1.0)

# Add an AABB box collider tracking a rigid body
crate = sim.add_rigid_body("Crate", position=(0, 10, 0))
sim.add_box(crate, half_extents=(0.5, 0.5, 0.5))
```

---

## 5. Batch Particle Processing

For thousands of particles without heavy collision interactions, Pylumina has a separate **Structure-of-Arrays (SoA)** memory layout in C++. By passing NumPy arrays directly, you can bypass Python loops completely for extreme performance.

```python
import numpy as np

# N points scattered
positions = np.random.uniform(-10, 10, size=(100000, 3))

sim.add_particles(positions)

# Step
sim.run(steps=500, dt=0.01)

# Get states back instantly
final_positions = sim.get_positions()
final_velocities = sim.get_velocities()
```
The batch processing relies strictly on a 3-component `(N, 3)` NumPy `float64` layout.

---

## 6. Recording & Data Export

Pylumina can record the entire entity and batch history for every simulation step.

```python
sim.enable_recording()
sim.run(steps=300, dt=0.01)

# Check recorded history frames
print(len(sim.history)) # 300
```
### Data Conversion
Once history is collected, you can export it explicitly using:
```python
# HDF5 Export: Saves one single structured .h5 file matching your simulation layout
sim.export(output_dir="./exports", fmt="hdf5", basename="my_sim")

# VTK Export: Saves 300 .vtk files (one per frame) readable natively by ParaView
sim.export(output_dir="./exports", fmt="vtk", basename="my_sim")
```

---

## 7. Command-Line Interface

Pylumina features a `run` CLI application, which automatically captures and exports your simulation script natively.
It looks inside your script for any instantiated `Simulation(..)` with a populated history (`enable_recording()`).

```bash
# Basic run with auto-export
pylumina run examples/basic_simulation.py

# Specify output directory and format (hdf5 / vtk)
pylumina run examples/basic_simulation.py --output ./results --format vtk

# Skip the export entirely
pylumina run examples/basic_simulation.py --no-export
```
