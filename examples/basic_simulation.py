#!/usr/bin/env python3
"""
py_lumina — Example: projectile with gravity, wind, and drag.

Demonstrates how to set up a simulation, add forces, create particles
and rigid bodies, run the simulation, and inspect results.
"""

import py_lumina as pl


def main():
    # ── create simulation ────────────────────────────────────────────
    sim = pl.Simulation(name="projectile_demo")

    # ── add forces ───────────────────────────────────────────────────
    sim.add_gravity()                          # Earth-surface gravity (-Y)
    sim.add_wind(direction=(1, 0, 0), strength=3.0)  # light crosswind +X
    sim.add_drag(drag_coefficient=0.47,        # sphere drag in air
                 cross_section_area=0.005,
                 fluid_density=1.225)

    # ── add a projectile particle ────────────────────────────────────
    ball = sim.add_particle(
        name="cannonball",
        position=(0, 0, 0),
        mass=5.0,
        velocity=(30, 40, 0),   # launched at ~50 m/s, 53° elevation
        damping=0.001,
    )

    # ── add a spinning rigid body (tumbling box) ─────────────────────
    box = sim.add_rigid_body(
        name="tumbling_box",
        position=(0, 5, 0),
        mass=2.0,
        moment_of_inertia=0.5,
        velocity=(10, 15, 0),
        angular_velocity=(0, 0, 5.0),   # spinning around Z
        damping=0.005,
        angular_damping=0.01,
    )

    # ── enable per-step recording ────────────────────────────────────
    sim.enable_recording()

    # ── run simulation ───────────────────────────────────────────────
    dt = 0.01          # 10 ms time-step
    steps = 800        # 8 seconds of simulation

    print(f"▸ Running '{sim.name}' for {steps * dt:.1f}s "
          f"({steps} steps @ dt={dt}s) …\n")

    sim.run(dt=dt, steps=steps)

    # ── print final state ────────────────────────────────────────────
    print("═══ Final state ═══════════════════════════════════════════")
    print(f"  Elapsed time : {sim.elapsed_time:.2f} s")
    print(f"  Total steps  : {sim.step_count}")
    print(f"  Total KE     : {sim.total_kinetic_energy:.4f} J")
    print()

    print(f"  🏀 {ball.name}")
    print(f"     position : ({ball.position.x:.3f}, "
          f"{ball.position.y:.3f}, {ball.position.z:.3f})")
    print(f"     velocity : ({ball.velocity.x:.3f}, "
          f"{ball.velocity.y:.3f}, {ball.velocity.z:.3f})")
    print(f"     speed    : {ball.speed():.3f} m/s")
    print(f"     KE       : {ball.kinetic_energy():.4f} J")
    print()

    print(f"  📦 {box.name}")
    print(f"     position : ({box.position.x:.3f}, "
          f"{box.position.y:.3f}, {box.position.z:.3f})")
    print(f"     orient.  : ({box.orientation.x:.3f}, "
          f"{box.orientation.y:.3f}, {box.orientation.z:.3f}) rad")
    print(f"     ang. vel : ({box.angular_velocity.x:.3f}, "
          f"{box.angular_velocity.y:.3f}, {box.angular_velocity.z:.3f}) rad/s")
    print(f"     total KE : {box.total_kinetic_energy():.4f} J")
    print()

    # ── history summary ──────────────────────────────────────────────
    history = sim.history
    print(f"  📊 Recorded {len(history)} frames")

    # Show the first and last frame positions of the cannonball
    first = history[0]["particles"]["cannonball"]["position"]
    last  = history[-1]["particles"]["cannonball"]["position"]
    print(f"     cannonball start : {first}")
    print(f"     cannonball end   : {last}")

    # ── optional: export trajectory to CSV ───────────────────────────
    from py_lumina.utils import history_to_csv
    csv_data = history_to_csv(history, "cannonball")
    csv_path = "cannonball_trajectory.csv"
    with open(csv_path, "w") as f:
        f.write(csv_data)
    print(f"\n  💾 Trajectory saved to {csv_path}")


if __name__ == "__main__":
    main()
