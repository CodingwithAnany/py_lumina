"""
py_lumina — High-performance physics simulation library.

A C++ backed physics engine with a clean Pythonic API for simulating
gravity, wind forces, drag, and rigid body motion.

Quick-start (module-level API)
------------------------------
>>> import py_lumina
>>>
>>> py_lumina.gravity()                              # add Earth gravity
>>> py_lumina.wind(direction=(1,0,0), strength=5)    # add crosswind
>>> py_lumina.drag()                                 # add air drag
>>>
>>> ball = py_lumina.particle("ball", position=(0,50,0), mass=2, velocity=(20,30,0))
>>> py_lumina.run(dt=0.01, steps=500)
>>> py_lumina.render()
"""

__version__ = "0.1.0"

# ── re-export every public symbol from the C++ core ──────────────────
from py_lumina._core import (
    Vector3D,
    Particle,
    RigidBody,
    ForceGenerator,
    GravityForce,
    WindForce,
    DragForce,
    PhysicsEngine,
)

# ── high-level Python wrappers (class-based API) ─────────────────────
from py_lumina.simulation import Simulation
from py_lumina.forces import create_gravity, create_wind, create_drag, ForcePresets
from py_lumina.renderer import render as _render_sim, render_plot

# ═════════════════════════════════════════════════════════════════════
#  Global simulation singleton  —  simple module-level API
# ═════════════════════════════════════════════════════════════════════
_active_sim: Simulation = Simulation(name="default")


def get_simulation() -> Simulation:
    """Return the current global simulation instance."""
    return _active_sim


def new_simulation(name: str = "simulation") -> Simulation:
    """Reset the global simulation and return a fresh instance."""
    global _active_sim
    _active_sim = Simulation(name=name)
    return _active_sim


# ── top-level force helpers ──────────────────────────────────────────

def gravity(gy: float = -9.81, gx: float = 0.0, gz: float = 0.0) -> GravityForce:
    """Add gravity to the active simulation.

    Parameters
    ----------
    gy : float
        Vertical acceleration (default -9.81 m/s²).
        Pass ``0`` for zero-g, ``-1.62`` for the Moon, etc.
    gx, gz : float
        Horizontal gravity components (usually 0).

    Examples
    --------
    >>> py_lumina.gravity()        # Earth gravity
    >>> py_lumina.gravity(0)       # zero-g
    >>> py_lumina.gravity(-1.62)   # Moon gravity
    """
    return _active_sim.add_gravity(g=(gx, gy, gz))


def wind(direction: tuple = (1, 0, 0), strength: float = 5.0) -> WindForce:
    """Add wind to the active simulation.

    Parameters
    ----------
    direction : tuple
        Wind direction vector.
    strength : float
        Force magnitude in Newtons.
    """
    return _active_sim.add_wind(direction=direction, strength=strength)


def drag(
    drag_coefficient: float = 0.47,
    cross_section_area: float = 0.01,
    fluid_density: float = 1.225,
) -> DragForce:
    """Add aerodynamic drag to the active simulation."""
    return _active_sim.add_drag(
        drag_coefficient=drag_coefficient,
        cross_section_area=cross_section_area,
        fluid_density=fluid_density,
    )


# ── top-level entity helpers ─────────────────────────────────────────

def particle(
    name: str,
    position: tuple = (0, 0, 0),
    mass: float = 1.0,
    velocity: tuple = (0, 0, 0),
    damping: float = 0.01,
    is_static: bool = False,
) -> Particle:
    """Add a particle to the active simulation."""
    return _active_sim.add_particle(
        name=name, position=position, mass=mass,
        velocity=velocity, damping=damping, is_static=is_static,
    )


def rigid_body(
    name: str,
    position: tuple = (0, 0, 0),
    mass: float = 1.0,
    moment_of_inertia: float = 1.0,
    velocity: tuple = (0, 0, 0),
    angular_velocity: tuple = (0, 0, 0),
    damping: float = 0.01,
    angular_damping: float = 0.01,
    is_static: bool = False,
) -> RigidBody:
    """Add a rigid body to the active simulation."""
    return _active_sim.add_rigid_body(
        name=name, position=position, mass=mass,
        moment_of_inertia=moment_of_inertia,
        velocity=velocity, angular_velocity=angular_velocity,
        damping=damping, angular_damping=angular_damping,
        is_static=is_static,
    )


# ── top-level simulation control ─────────────────────────────────────

def step(dt: float = 1.0 / 60.0) -> None:
    """Advance the active simulation by one time-step."""
    _active_sim.step(dt)


def run(dt: float = 1.0 / 60.0, steps: int = 100) -> None:
    """Run the active simulation for *steps* time-steps."""
    _active_sim.run(dt=dt, steps=steps)


def render() -> None:
    """Pretty-print the current state of the active simulation."""
    _render_sim(_active_sim)


def record() -> None:
    """Enable per-step recording on the active simulation."""
    _active_sim.enable_recording()


def plot(entity_name: str, save_path: str | None = None) -> None:
    """Plot the trajectory of a named entity (requires matplotlib)."""
    render_plot(_active_sim, entity_name, save_path)


# ═════════════════════════════════════════════════════════════════════


__all__ = [
    # core types
    "Vector3D",
    "Particle",
    "RigidBody",
    # force generators
    "ForceGenerator",
    "GravityForce",
    "WindForce",
    "DragForce",
    # engine
    "PhysicsEngine",
    # class-based API
    "Simulation",
    "create_gravity",
    "create_wind",
    "create_drag",
    "ForcePresets",
    # module-level API
    "get_simulation",
    "new_simulation",
    "gravity",
    "wind",
    "drag",
    "particle",
    "rigid_body",
    "step",
    "run",
    "render",
    "record",
    "plot",
    "render_plot",
]
