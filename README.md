# 🌟 pylumina

> **High-performance physics simulation library** — C++ engine, Pythonic API.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![C++17](https://img.shields.io/badge/C%2B%2B-17-brightgreen.svg)](https://isocpp.org/)

**pylumina** is a physics simulation library that pairs a **C++ numerical engine** with a clean **Python API**, giving you the best of both worlds: blazing-fast computation and expressive scripting.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Collisions & Resolution** | Analytical narrow-phase (Sphere-Sphere, Sphere-Plane, Box-Box) with impulse resolution. |
| **NumPy Batch Processing** | Simulate 100,000+ particles instantly mapping NumPy arrays to C++ SoA layout. |
| **Data Export (VTK/HDF5)** | Auto-export history. Play back simulations directly in ParaView! |
| **CLI Runner** | Run scripts with `pylumina run script.py --output out/ --format vtk`. |
| **Rigid Body Dynamics** | Full motion: linear + angular velocity, moments of inertia. |
| **Forces (Gravity, Wind, Drag)** | Built-in physically accurate forces. |
| **pybind11** | Zero-copy C++ ↔ Python bridge for minimal overhead. |

---

## 🚀 Installation

### Prerequisites
| Tool | Version |
|---|---|
| Python | ≥ 3.8 |
| C++ compiler | C++17 capable (GCC ≥ 7, Clang ≥ 5, MSVC ≥ 2017) |
| CMake | ≥ 3.15 |

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/pylumina.git
cd pylumina

# Install (builds C++ extension automatically)
pip install .

# For HDF5 export support:
pip install .[hdf5]
```

---

## 🎯 Quick Start

Check out the full [Usage Guide](docs/usage.md) for detailed tutorials.

```python
from pylumina import Simulation

sim = Simulation()
sim.enable_gravity(y=-9.81)
sim.enable_collisions(True, restitution=0.8)

# Add Ground
sim.add_plane(normal=(0, 1, 0), offset=0)

# Add Ball
ball = sim.add_particle("tennis_ball", position=(0, 10, 0), mass=1.0)
sim.add_sphere(ball, radius=0.5)

# Simulate for 5 seconds
sim.run(steps=500, dt=0.01)

print(f"Final vertical position: {ball.position.y:.2f} m")
```

---

## 🖥️ Command-Line auto-export

Pylumina has a built in CLI tool that automatically captures simulation history and exports it.

```bash
# In your script, enable recording:
# sim.enable_recording()

# Run the script via the CLI
pylumina run my_script.py --output results/ --format vtk

# It will automatically generate ParaView-compatible VTK files!
```

---

## 📁 Documentation

Read the rest of our dedicated documentation!
- 📖 [**Usage & API Guide**](docs/usage.md): comprehensive tutorial of all features.
- 🏗️ [**Architecture**](docs/architecture.md): learn how the C++ ↔ Python pipeline works.


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
  <b>pylumina</b> — <i>illuminate your physics simulations</i> ✨
</p>
