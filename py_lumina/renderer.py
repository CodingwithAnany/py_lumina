"""
py_lumina.renderer — Console & Matplotlib visualization for simulations.

Provides render() for a rich terminal print-out and render_plot() for
a Matplotlib trajectory chart.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_lumina.simulation import Simulation


def render(sim: "Simulation") -> None:
    """Pretty-print the full simulation state to the console.

    Shows every particle and rigid body with its current position,
    velocity, energy, and orientation (for rigid bodies).
    """

    _BOLD = "\033[1m"
    _CYAN = "\033[96m"
    _GREEN = "\033[92m"
    _YELLOW = "\033[93m"
    _MAGENTA = "\033[95m"
    _RESET = "\033[0m"
    _DIM = "\033[2m"

    w = 62                       # box width
    bar = "═" * w

    print(f"\n{_CYAN}╔{bar}╗{_RESET}")
    print(f"{_CYAN}║{_BOLD}  🌟 py_lumina  ·  {sim.name:<{w - 21}}║{_RESET}")
    print(f"{_CYAN}╠{bar}╣{_RESET}")

    print(f"{_CYAN}║{_RESET}  ⏱  Time elapsed : {_BOLD}{sim.elapsed_time:.4f} s{_RESET}"
          f"{'':>{w - 30}}  {_CYAN}║{_RESET}")
    print(f"{_CYAN}║{_RESET}  🔁 Steps        : {_BOLD}{sim.step_count}{_RESET}"
          f"{'':>{w - 24 - len(str(sim.step_count))}}  {_CYAN}║{_RESET}")
    print(f"{_CYAN}║{_RESET}  ⚡ Total KE     : {_BOLD}{sim.total_kinetic_energy:.4f} J{_RESET}"
          f"{'':>{w - 32}}  {_CYAN}║{_RESET}")
    print(f"{_CYAN}║{_RESET}  📦 Entities     : {_BOLD}{sim.entity_count}{_RESET}"
          f"{'':>{w - 24 - len(str(sim.entity_count))}}  {_CYAN}║{_RESET}")

    # ── Particles ────────────────────────────────────────────────────
    if sim._particle_registry:
        print(f"{_CYAN}╠{bar}╣{_RESET}")
        print(f"{_CYAN}║{_GREEN}{_BOLD}  Particles{_RESET}{'':>{w - 11}}{_CYAN}║{_RESET}")
        print(f"{_CYAN}╠{bar}╣{_RESET}")
        for name, p in sim._particle_registry.items():
            print(f"{_CYAN}║{_RESET}  {_YELLOW}● {name}{_RESET}")
            print(f"{_CYAN}║{_RESET}    pos  = ({p.position.x:+.4f}, {p.position.y:+.4f}, {p.position.z:+.4f})")
            print(f"{_CYAN}║{_RESET}    vel  = ({p.velocity.x:+.4f}, {p.velocity.y:+.4f}, {p.velocity.z:+.4f})")
            print(f"{_CYAN}║{_RESET}    speed = {p.speed():.4f} m/s    KE = {p.kinetic_energy():.4f} J")

    # ── Rigid bodies ─────────────────────────────────────────────────
    if sim._body_registry:
        print(f"{_CYAN}╠{bar}╣{_RESET}")
        print(f"{_CYAN}║{_MAGENTA}{_BOLD}  Rigid Bodies{_RESET}{'':>{w - 14}}{_CYAN}║{_RESET}")
        print(f"{_CYAN}╠{bar}╣{_RESET}")
        for name, rb in sim._body_registry.items():
            print(f"{_CYAN}║{_RESET}  {_YELLOW}■ {name}{_RESET}")
            print(f"{_CYAN}║{_RESET}    pos    = ({rb.position.x:+.4f}, {rb.position.y:+.4f}, {rb.position.z:+.4f})")
            print(f"{_CYAN}║{_RESET}    vel    = ({rb.velocity.x:+.4f}, {rb.velocity.y:+.4f}, {rb.velocity.z:+.4f})")
            print(f"{_CYAN}║{_RESET}    orient = ({rb.orientation.x:+.4f}, {rb.orientation.y:+.4f}, {rb.orientation.z:+.4f}) rad")
            print(f"{_CYAN}║{_RESET}    ω      = ({rb.angular_velocity.x:+.4f}, {rb.angular_velocity.y:+.4f}, {rb.angular_velocity.z:+.4f}) rad/s")
            print(f"{_CYAN}║{_RESET}    KE(total) = {rb.total_kinetic_energy():.4f} J")

    print(f"{_CYAN}╚{bar}╝{_RESET}\n")


def render_plot(sim: "Simulation", entity_name: str, save_path: str | None = None) -> None:
    """Plot the recorded trajectory of a named entity (requires matplotlib).

    Parameters
    ----------
    sim : Simulation
        A simulation that has been run with ``sim.enable_recording()``.
    entity_name : str
        Name of the particle or rigid body to plot.
    save_path : str, optional
        If given, save the figure to this file path instead of showing it.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("⚠  matplotlib is required for render_plot().  pip install matplotlib")
        return

    history = sim.history
    if not history:
        print("⚠  No recorded history. Call sim.enable_recording() before sim.run().")
        return

    times, xs, ys, zs = [], [], [], []

    for frame in history:
        data = (
            frame.get("particles", {}).get(entity_name)
            or frame.get("rigid_bodies", {}).get(entity_name)
        )
        if data is None:
            continue
        times.append(frame["time"])
        px, py_, pz = data["position"]
        xs.append(px)
        ys.append(py_)
        zs.append(pz)

    if not times:
        print(f"⚠  Entity '{entity_name}' not found in recorded history.")
        return

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle(f"py_lumina — trajectory of '{entity_name}'", fontweight="bold")

    for ax, vals, label in zip(axes, [xs, ys, zs], ["X", "Y", "Z"]):
        ax.plot(times, vals, linewidth=1.5)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(f"{label} position (m)")
        ax.set_title(f"{label} vs Time")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"📊 Plot saved to {save_path}")
    else:
        plt.show()
