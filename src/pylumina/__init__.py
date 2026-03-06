from .simulation import Simulation
from .renderer import render
from .environment import env
from .physics import Gravity, Wind, Drag

__version__ = "0.2.0"

# ── module-level convenience API ─────────────────────────────────

def gravity(y=-9.81, x=0, z=0):
    g = Gravity(y, x, z)
    env.sim.add_force(g)
    return g

def particle(name="particle", position=(0, 0, 0), mass=1.0, velocity=(0, 0, 0)):
    return env.sim.add_particle(name, position, mass, velocity)

def rigid_body(name="body", position=(0, 0, 0), mass=1.0, moi=1.0):
    return env.sim.add_rigid_body(name, position, mass, moi)

def step(dt=1/60):
    env.sim.step(dt)

def run(steps=100, dt=1/60):
    env.sim.run(steps, dt)

def enable_collisions(enabled=True, restitution=0.5):
    env.sim.enable_collisions(enabled, restitution)

def new_simulation():
    env.sim = Simulation()
    return env.sim

__all__ = [
    "Simulation", "render", "gravity", "particle", "rigid_body",
    "step", "run", "enable_collisions", "new_simulation", "env",
    "Gravity", "Wind", "Drag", "__version__",
]
