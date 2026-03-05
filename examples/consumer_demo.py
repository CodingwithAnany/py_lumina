#!/usr/bin/env python3
"""
Consumer test — Simulates how a user who did `pip install py_lumina`
would actually use the library.  This is the simplest possible API.
"""

import py_lumina

# ── 1. Set up forces ─────────────────────────────────────────────────
py_lumina.gravity()                                  # Earth gravity
py_lumina.wind(direction=(1, 0, 0), strength=3.0)    # light crosswind
py_lumina.drag()                                     # default air drag

# ── 2. Add objects ───────────────────────────────────────────────────
ball = py_lumina.particle(
    "ball",
    position=(0, 50, 0),
    mass=2.0,
    velocity=(20, 30, 0),
)

box = py_lumina.rigid_body(
    "box",
    position=(0, 5, 0),
    mass=1.5,
    moment_of_inertia=0.3,
    velocity=(5, 10, 0),
    angular_velocity=(0, 0, 3),
)

# ── 3. Run the simulation ───────────────────────────────────────────
py_lumina.run(dt=0.01, steps=500)

# ── 4. Render results ───────────────────────────────────────────────
py_lumina.render()

# ── 5. Direct object inspection ─────────────────────────────────────
print(f"Ball final position : {ball.position}")
print(f"Ball speed          : {ball.speed():.2f} m/s")
print(f"Box orientation     : {box.orientation}")
print(f"Box angular vel     : {box.angular_velocity}")


# ═══════════════════════════════════════════════════════════════════════
#  Bonus: zero-gravity demo
# ═══════════════════════════════════════════════════════════════════════
print("\n── Zero-G demo ─────────────────────────────────────────────")

py_lumina.new_simulation("zero-g-demo")    # start fresh

py_lumina.gravity(0)                       # zero gravity!
py_lumina.particle("astronaut", position=(0, 0, 0), velocity=(1, 2, 0), mass=80)

py_lumina.run(dt=0.01, steps=200)
py_lumina.render()
