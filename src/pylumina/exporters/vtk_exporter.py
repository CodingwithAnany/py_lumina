"""
VTK exporter — writes simulation history to Legacy VTK PolyData files.

No external dependencies required.  Produces ASCII .vtk files readable
by ParaView, VisIt, and any VTK-compatible viewer.

Output structure (one file per time-step):
    output_dir/
        simulation_0000.vtk
        simulation_0001.vtk
        ...

Or a single combined file when ``per_step=False``.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pylumina.simulation import Simulation


def _vtk_header(n_points: int, title: str = "pylumina") -> str:
    return (
        f"# vtk DataFile Version 3.0\n"
        f"{title}\n"
        f"ASCII\n"
        f"DATASET POLYDATA\n"
        f"POINTS {n_points} double\n"
    )


def export_vtk(
    sim: "Simulation",
    output_dir: str = "output",
    basename: str = "simulation",
    per_step: bool = True,
) -> list[str]:
    """Export the simulation's recorded history to VTK files.

    Parameters
    ----------
    sim : Simulation
        Must have recording enabled (``sim.enable_recording()``).
    output_dir : str
        Directory to write files into (created if needed).
    basename : str
        File name prefix.
    per_step : bool
        If True, write one .vtk file per recorded frame.
        If False, write a single file with the final state only.

    Returns
    -------
    list[str]
        Paths of all written files.
    """
    os.makedirs(output_dir, exist_ok=True)
    history = sim.history
    written: list[str] = []

    if not history:
        # No recording — export current state as a single snapshot
        history = [sim._snapshot()]

    frames = history if per_step else [history[-1]]

    for idx, frame in enumerate(frames):
        positions = frame.get("positions", [])
        velocities = frame.get("velocities", [])
        n = len(positions)

        if per_step:
            path = os.path.join(output_dir, f"{basename}_{idx:04d}.vtk")
        else:
            path = os.path.join(output_dir, f"{basename}.vtk")

        with open(path, "w") as f:
            f.write(_vtk_header(n, f"pylumina t={frame.get('time', 0):.4f}"))

            # Points
            for px, py, pz in positions:
                f.write(f"{px} {py} {pz}\n")

            # Vertices (each point is its own vertex)
            f.write(f"\nVERTICES {n} {n * 2}\n")
            for i in range(n):
                f.write(f"1 {i}\n")

            # Point data — velocity as vector field
            if velocities:
                f.write(f"\nPOINT_DATA {n}\n")
                f.write(f"VECTORS velocity double\n")
                for vx, vy, vz in velocities:
                    f.write(f"{vx} {vy} {vz}\n")

                # Mass as scalar
                masses = frame.get("masses", [])
                if masses:
                    f.write(f"SCALARS mass double 1\n")
                    f.write(f"LOOKUP_TABLE default\n")
                    for m in masses:
                        f.write(f"{m}\n")

                # Names as field data
                names = frame.get("names", [])
                if names:
                    f.write(f"FIELD FieldData 1\n")
                    f.write(f"name 1 {n} string\n")
                    for nm in names:
                        f.write(f"{nm}\n")

        written.append(path)

    return written
