"""
High-level Simulation wrapper around the C++ PhysicsEngine.

Provides a user-friendly interface for setting up, running, and
inspecting physics simulations without touching the low-level engine
directly.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Union

from py_lumina._core import (
    DragForce,
    GravityForce,
    Particle,
    PhysicsEngine,
    RigidBody,
    Vector3D,
    WindForce,
)


class Simulation:
    """Convenient, Pythonic simulation controller.

    Example
    -------
    >>> sim = Simulation(name="free-fall")
    >>> sim.add_gravity()
    >>> ball = sim.add_particle("ball", position=(0, 10, 0), mass=1.0)
    >>> sim.run(dt=0.01, steps=1000)
    >>> print(ball.position)
    """

    def __init__(self, name: str = "simulation") -> None:
        self.name = name
        self.engine = PhysicsEngine()
        self._particle_registry: Dict[str, Particle] = {}
        self._body_registry: Dict[str, RigidBody] = {}
        self._history: List[dict] = []
        self._record = False

    # ── entity creation ──────────────────────────────────────────────

    def add_particle(
        self,
        name: str,
        position: tuple = (0, 0, 0),
        mass: float = 1.0,
        velocity: tuple = (0, 0, 0),
        damping: float = 0.01,
        is_static: bool = False,
    ) -> Particle:
        """Add a point-mass particle to the simulation."""
        pos = Vector3D(*position)
        p = self.engine.add_particle(name, pos, mass)
        p.velocity = Vector3D(*velocity)
        p.damping = damping
        p.is_static = is_static
        self._particle_registry[name] = p
        return p

    def add_rigid_body(
        self,
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
        """Add a rigid body with rotational dynamics."""
        pos = Vector3D(*position)
        rb = self.engine.add_rigid_body(name, pos, mass, moment_of_inertia)
        rb.velocity = Vector3D(*velocity)
        rb.angular_velocity = Vector3D(*angular_velocity)
        rb.damping = damping
        rb.angular_damping = angular_damping
        rb.is_static = is_static
        self._body_registry[name] = rb
        return rb

    # ── force helpers ────────────────────────────────────────────────

    def add_gravity(self, g: tuple = (0, -9.81, 0)) -> GravityForce:
        """Add uniform gravity (default: Earth surface, -Y)."""
        gf = GravityForce(Vector3D(*g))
        self.engine.add_force(gf)
        return gf

    def add_wind(self, direction: tuple = (1, 0, 0), strength: float = 5.0) -> WindForce:
        """Add a constant wind force."""
        wf = WindForce(Vector3D(*direction), strength)
        self.engine.add_force(wf)
        return wf

    def add_drag(
        self,
        drag_coefficient: float = 0.47,
        cross_section_area: float = 0.01,
        fluid_density: float = 1.225,
    ) -> DragForce:
        """Add aerodynamic drag."""
        df = DragForce(drag_coefficient, cross_section_area, fluid_density)
        self.engine.add_force(df)
        return df

    # ── simulation control ───────────────────────────────────────────

    def step(self, dt: float = 1.0 / 60.0) -> None:
        """Advance the simulation by one time-step."""
        self.engine.step(dt)
        if self._record:
            self._snapshot()

    def run(self, dt: float = 1.0 / 60.0, steps: int = 100) -> None:
        """Run *steps* simulation steps."""
        for _ in range(steps):
            self.step(dt)

    # ── history / recording ──────────────────────────────────────────

    def enable_recording(self) -> None:
        """Start recording a snapshot after every step."""
        self._record = True
        self._history.clear()

    def disable_recording(self) -> None:
        self._record = False

    @property
    def history(self) -> List[dict]:
        """Return the recorded history (list of per-step snapshots)."""
        return list(self._history)

    def _snapshot(self) -> None:
        frame: dict = {
            "time": self.engine.elapsed_time,
            "step": self.engine.step_count,
            "particles": {},
            "rigid_bodies": {},
        }
        for name, p in self._particle_registry.items():
            frame["particles"][name] = {
                "position": (p.position.x, p.position.y, p.position.z),
                "velocity": (p.velocity.x, p.velocity.y, p.velocity.z),
                "speed": p.speed(),
                "kinetic_energy": p.kinetic_energy(),
            }
        for name, rb in self._body_registry.items():
            frame["rigid_bodies"][name] = {
                "position": (rb.position.x, rb.position.y, rb.position.z),
                "velocity": (rb.velocity.x, rb.velocity.y, rb.velocity.z),
                "orientation": (rb.orientation.x, rb.orientation.y, rb.orientation.z),
                "angular_velocity": (
                    rb.angular_velocity.x,
                    rb.angular_velocity.y,
                    rb.angular_velocity.z,
                ),
                "total_ke": rb.total_kinetic_energy(),
            }
        self._history.append(frame)

    # ── queries ──────────────────────────────────────────────────────

    def get_particle(self, name: str) -> Particle:
        return self._particle_registry[name]

    def get_rigid_body(self, name: str) -> RigidBody:
        return self._body_registry[name]

    @property
    def elapsed_time(self) -> float:
        return self.engine.elapsed_time

    @property
    def step_count(self) -> int:
        return self.engine.step_count

    @property
    def total_kinetic_energy(self) -> float:
        return self.engine.total_kinetic_energy()

    @property
    def entity_count(self) -> int:
        return self.engine.entity_count()

    # ── dunder ───────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"Simulation('{self.name}', entities={self.entity_count}, "
            f"elapsed={self.elapsed_time:.4f}s, steps={self.step_count})"
        )
