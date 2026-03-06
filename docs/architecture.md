# Pylumina Architecture

## Overview
Pylumina is a hybrid C++/Python physics engine. The compute-intensive core
(integration, collision detection, batch particle processing) is implemented
in C++17 and exposed to Python via Pybind11.

## C++ Layer (`cpp/`)

### `engine/`
| File | Purpose |
|---|---|
| `physics_engine.h` | Core types: `Vector3D`, `Particle`, `RigidBody`, `ForceGenerator`, `PhysicsEngine` |
| `physics_engine.cpp` | Engine step loop — applies forces, integrates all entities |
| `integrator.cpp` | Semi-implicit Euler integration for linear and angular motion |
| `batch_particles.h` | `BatchParticleSystem` — SoA layout for cache-friendly processing of thousands of particles |

### `forces/`
| File | Purpose |
|---|---|
| `forces_impl.h` | Declarations for `GravityForce`, `WindForce`, `DragForce` |
| `gravity.cpp` | `F = m·g` |
| `wind.cpp` | `F = strength · dir_normalized` |
| `drag.cpp` | `F = -½ρCdA|v|²v̂` |

### `collision/`
| File | Purpose |
|---|---|
| `collision.h` | `SphereShape`, `PlaneShape`, `BoxShape`, `Collider`, `Contact`, `CollisionSystem` |
| `collision.cpp` | Narrow-phase tests (sphere-sphere, sphere-plane, box-box) + impulse-based resolution |

### `bindings/`
| File | Purpose |
|---|---|
| `pybind_module.cpp` | Pybind11 module exposing all C++ types to Python with NumPy integration |

## Python Layer (`src/pylumina/`)

| Module | Purpose |
|---|---|
| `__init__.py` | Public API, global simulation singleton, convenience functions |
| `simulation.py` | `Simulation` class — entities, forces, collisions, batch particles |
| `physics/` | Python wrappers for `Gravity`, `Wind`, `Drag` |
| `renderer.py` | Console visualization of simulation state |
| `environment.py` | Singleton `Environment` for module-level API |
| `utils/` | Math helpers and data conversion |
| `cli.py` | CLI entry point: `pylumina run script.py` |

## Collision Pipeline
```
detect_and_resolve()
    for each pair of colliders:
        ├── narrow-phase test (sphere/plane/box)
        │     → generates Contact {a, b, normal, penetration}
        └── resolve(contact)
              ├── positional correction (with slop)
              └── velocity impulse (restitution-based)
```

## Batch Particle Pipeline
```
Python: np.ndarray (N,3) → C++: flat double arrays
    │
    ├── add_particles_from_arrays()  — positions only
    ├── add_particles_full()         — positions + velocities + masses
    │
    └── step(dt, gx, gy, gz)  — tight C++ loop over SoA arrays
         ├── apply gravity
         └── integrate positions
    │
    └── get_positions() → Python: np.ndarray (N,3)
```

## Data Flow
1. User defines simulation in Python
2. Entities and forces are created in the C++ core
3. Every `step(dt)`:
   - Python calls `PhysicsEngine::step()` (forces + integration)
   - Then `CollisionSystem::detect_and_resolve()` (collision response)
   - Then `BatchParticleSystem::step()` (batch particles, if any)
4. User queries results or calls `render()`
