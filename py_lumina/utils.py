"""
Utility helpers for py_lumina simulations.
"""

from __future__ import annotations

import json
import csv
import io
from typing import List

from py_lumina._core import Vector3D


def vec_to_tuple(v: Vector3D) -> tuple:
    """Convert a Vector3D to a plain Python tuple."""
    return (v.x, v.y, v.z)


def tuple_to_vec(t: tuple) -> Vector3D:
    """Convert a 3-element tuple to a Vector3D."""
    return Vector3D(*t)


def history_to_json(history: List[dict], indent: int = 2) -> str:
    """Serialise a simulation history (from Simulation.history) to JSON."""
    return json.dumps(history, indent=indent)


def history_to_csv(history: List[dict], entity_name: str) -> str:
    """Extract one entity's trajectory from the history as CSV.

    Parameters
    ----------
    history : list of dict
        The snapshot list returned by ``Simulation.history``.
    entity_name : str
        Name of the particle or rigid body to extract.

    Returns
    -------
    str
        CSV text with columns: time, x, y, z, vx, vy, vz
    """
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["time", "x", "y", "z", "vx", "vy", "vz"])

    for frame in history:
        t = frame["time"]
        data = (
            frame.get("particles", {}).get(entity_name)
            or frame.get("rigid_bodies", {}).get(entity_name)
        )
        if data is None:
            continue
        px, py_, pz = data["position"]
        vx, vy, vz = data["velocity"]
        writer.writerow([f"{t:.6f}", f"{px:.6f}", f"{py_:.6f}", f"{pz:.6f}",
                         f"{vx:.6f}", f"{vy:.6f}", f"{vz:.6f}"])

    return buf.getvalue()


def print_state(sim) -> None:
    """Pretty-print the current state of every entity in a Simulation."""
    print(f"╔══ {sim.name} ═══════════════════════════════════════════╗")
    print(f"║  Time: {sim.elapsed_time:.4f}s   Steps: {sim.step_count}")
    print(f"║  Total KE: {sim.total_kinetic_energy:.4f} J")
    print(f"╠══ Particles ({'none' if not sim._particle_registry else ''}) ════")
    for name, p in sim._particle_registry.items():
        print(f"║  {name}: pos={vec_to_tuple(p.position)}, "
              f"vel={vec_to_tuple(p.velocity)}, KE={p.kinetic_energy():.4f}")
    print(f"╠══ Rigid Bodies ({'none' if not sim._body_registry else ''}) ════")
    for name, rb in sim._body_registry.items():
        print(f"║  {name}: pos={vec_to_tuple(rb.position)}, "
              f"orient={vec_to_tuple(rb.orientation)}, "
              f"KE={rb.total_kinetic_energy():.4f}")
    print("╚═══════════════════════════════════════════════════════════╝")
