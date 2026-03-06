"""
HDF5 exporter — writes simulation history to a structured .h5 file.

Requires ``h5py``.  Install with:

    pip install pylumina[hdf5]

Output structure inside the .h5 file::

    /metadata
        steps          (int)
        dt             (float)
        total_time     (float)
        entity_count   (int)
    /entities/<name>
        positions      (N_steps, 3)   float64
        velocities     (N_steps, 3)   float64
        mass           ()             float64
    /batch
        positions      (N_steps, N_particles, 3)  float64   [if batch particles used]
        velocities     (N_steps, N_particles, 3)  float64
    /timeline
        time           (N_steps,)     float64
        step           (N_steps,)     int
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pylumina.simulation import Simulation


def export_hdf5(
    sim: "Simulation",
    output_dir: str = "output",
    basename: str = "simulation",
) -> str:
    """Export the simulation's recorded history to an HDF5 file.

    Parameters
    ----------
    sim : Simulation
        Must have recording enabled (``sim.enable_recording()``).
    output_dir : str
        Directory to write the file into.
    basename : str
        File name (without extension).

    Returns
    -------
    str
        Path to the written .h5 file.
    """
    try:
        import h5py
        import numpy as np
    except ImportError:
        raise ImportError(
            "HDF5 export requires h5py and numpy.\n"
            "Install with:  pip install pylumina[hdf5]"
        )

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{basename}.h5")

    history = sim.history
    if not history:
        history = [sim._snapshot()]

    with h5py.File(path, "w") as f:
        # ── metadata ─────────────────────────────────────────────
        meta = f.create_group("metadata")
        meta.attrs["steps"] = len(history)
        meta.attrs["total_time"] = history[-1].get("time", 0)
        meta.attrs["entity_count"] = len(history[0].get("names", []))
        meta.attrs["engine"] = "pylumina"

        # ── timeline ─────────────────────────────────────────────
        tl = f.create_group("timeline")
        tl.create_dataset("time", data=[fr["time"] for fr in history])
        tl.create_dataset("step", data=[fr["step"] for fr in history])

        # ── per-entity trajectories ──────────────────────────────
        names = history[0].get("names", [])
        if names:
            entities_grp = f.create_group("entities")

            for eidx, name in enumerate(names):
                egrp = entities_grp.create_group(name)

                pos_data = []
                vel_data = []
                for fr in history:
                    positions = fr.get("positions", [])
                    velocities = fr.get("velocities", [])
                    if eidx < len(positions):
                        pos_data.append(positions[eidx])
                        vel_data.append(velocities[eidx] if eidx < len(velocities) else (0, 0, 0))

                if pos_data:
                    egrp.create_dataset("positions", data=np.array(pos_data, dtype=np.float64))
                    egrp.create_dataset("velocities", data=np.array(vel_data, dtype=np.float64))

                masses = history[0].get("masses", [])
                if eidx < len(masses):
                    egrp.attrs["mass"] = masses[eidx]

        # ── batch particles ──────────────────────────────────────
        batch_pos = [fr.get("batch_positions") for fr in history]
        if any(bp is not None for bp in batch_pos):
            batch_grp = f.create_group("batch")
            bp_arr = np.array([bp for bp in batch_pos if bp is not None])
            batch_grp.create_dataset("positions", data=bp_arr)

            batch_vel = [fr.get("batch_velocities") for fr in history]
            bv_arr = np.array([bv for bv in batch_vel if bv is not None])
            if len(bv_arr):
                batch_grp.create_dataset("velocities", data=bv_arr)

    return path
