# 🌟 py_lumina

> **High-performance physics simulation library** — C++ engine, Pythonic API.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![C++17](https://img.shields.io/badge/C%2B%2B-17-brightgreen.svg)](https://isocpp.org/)

**py_lumina** is a physics simulation library that pairs a **C++ numerical engine** with a clean **Python API**, giving you the best of both worlds: blazing-fast computation and expressive scripting.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Gravity** | Configurable uniform gravitational fields (Earth, Moon, Mars, or custom) |
| **Wind Forces** | Constant-direction wind with adjustable strength |
| **Aerodynamic Drag** | Physically accurate drag: `F = -½ ρ Cd A |v|² v̂` |
| **Rigid Body Dynamics** | Full 6-DOF motion: linear + angular velocity, torques, moment of inertia |
| **Particles** | Lightweight point-mass entities for fast simulations |
| **Recording** | Per-step snapshot history — export to JSON or CSV |
| **Force Presets** | One-liner presets for common environments |
| **pybind11** | Zero-copy C++ ↔ Python bridge for minimal overhead |

---

## 📁 Project Structure

```
py_lumina/
├── CMakeLists.txt              # CMake build configuration
├── pyproject.toml              # PEP 517 build config (scikit-build-core)
├── LICENSE                     # MIT license
├── README.md
├── .gitignore
│
├── src/cpp/                    # ── C++ physics engine ──
│   ├── include/
│   │   ├── vector3d.hpp        # 3D vector maths
│   │   ├── particle.hpp        # Point-mass particle
│   │   ├── rigid_body.hpp      # Rigid body (linear + angular)
│   │   ├── forces.hpp          # Gravity, Wind, Drag generators
│   │   └── engine.hpp          # Core simulation engine
│   └── bindings/
│       └── py_lumina_bindings.cpp  # pybind11 module
│
├── py_lumina/                  # ── Python package ──
│   ├── __init__.py             # Public API re-exports
│   ├── simulation.py           # High-level Simulation class
│   ├── forces.py               # Force factories & presets
│   └── utils.py                # Helpers (JSON/CSV export, pretty-print)
│
├── examples/
│   └── basic_simulation.py     # End-to-end demo
│
└── tests/
    └── test_simulation.py      # pytest suite
```

---

## 🚀 Installation

### Prerequisites

| Tool | Version |
|---|---|
| Python | ≥ 3.8 |
| C++ compiler | C++17 capable (GCC ≥ 7, Clang ≥ 5, MSVC ≥ 2017) |
| CMake | ≥ 3.15 |
| pip | latest recommended |

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/py_lumina.git
cd py_lumina

# Install (builds C++ extension automatically)
pip install .

# Or install in development mode
pip install -e .
```

> **Note:** `pip install .` uses **scikit-build-core** to invoke CMake, compile the C++ extension, and install everything in one step.

### Verify installation

```bash
python -c "import py_lumina; print(py_lumina.__version__)"
# 0.1.0
```

---

## 🎯 Quick Start

```python
import py_lumina as pl

# Create a simulation
sim = pl.Simulation(name="free-fall")

# Add forces
sim.add_gravity()                              # Earth gravity (-Y)
sim.add_wind(direction=(1, 0, 0), strength=3)  # Crosswind
sim.add_drag(drag_coefficient=0.47)            # Sphere drag

# Add a particle
ball = sim.add_particle(
    name="ball",
    position=(0, 50, 0),
    mass=2.0,
    velocity=(20, 30, 0),
)

# Run for 5 seconds at 100 Hz
sim.run(dt=0.01, steps=500)

# Inspect results
print(f"Final position: {ball.position}")
print(f"Final speed:    {ball.speed():.2f} m/s")
print(f"Kinetic energy: {ball.kinetic_energy():.2f} J")
```

---

## 🔧 API Reference

### `Simulation`

The main entry point for running physics scenarios.

```python
sim = pl.Simulation(name="my_sim")

# Entities
sim.add_particle(name, position, mass, velocity, damping, is_static)
sim.add_rigid_body(name, position, mass, moment_of_inertia, velocity,
                   angular_velocity, damping, angular_damping, is_static)

# Forces
sim.add_gravity(g=(0, -9.81, 0))
sim.add_wind(direction=(1, 0, 0), strength=5.0)
sim.add_drag(drag_coefficient=0.47, cross_section_area=0.01, fluid_density=1.225)

# Run
sim.step(dt=1/60)
sim.run(dt=0.01, steps=1000)

# Queries
sim.elapsed_time
sim.step_count
sim.total_kinetic_energy
sim.entity_count

# Recording
sim.enable_recording()
sim.run(dt=0.01, steps=100)
history = sim.history  # list of per-step snapshots
```

### `ForcePresets`

One-liner force generators:

```python
from py_lumina import ForcePresets

earth   = ForcePresets.earth_gravity()
moon    = ForcePresets.moon_gravity()
mars    = ForcePresets.mars_gravity()
breeze  = ForcePresets.gentle_breeze()
gale    = ForcePresets.strong_gale()
sphere  = ForcePresets.sphere_drag(radius=0.05)
cube    = ForcePresets.cube_drag(side=0.1)
```

### `Vector3D`

Low-level 3D vector (backed by C++):

```python
v = pl.Vector3D(1, 2, 3)
v.magnitude()        # 3.7416...
v.normalized()       # unit vector
v.dot(other)         # scalar dot product
v.cross(other)       # cross product
v.distance_to(other) # Euclidean distance
v.lerp(target, t)    # linear interpolation
```

### Utilities

```python
from py_lumina.utils import history_to_json, history_to_csv, print_state

json_str = history_to_json(sim.history)
csv_str  = history_to_csv(sim.history, "ball")
print_state(sim)  # pretty-print current state
```

---

## 🧪 Testing

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## 📦 Publishing to PyPI

```bash
# Install build tools
pip install build twine

# Build source distribution and wheel
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## 🗺️ Roadmap

- [ ] Collision detection (AABB, sphere-sphere)
- [ ] Constraint solver (springs, joints)
- [ ] Quaternion-based orientation
- [ ] Spatial partitioning (octree / grid)
- [ ] GPU acceleration (CUDA / OpenCL)
- [ ] Matplotlib / Plotly visualisation helpers
- [ ] WASM build for browser demos

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>py_lumina</b> — <i>illuminate your physics simulations</i> ✨
</p>
