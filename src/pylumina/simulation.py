from ._core import (
    PhysicsEngine, Particle, RigidBody, Vector3D,
    CollisionSystem, BatchParticleSystem, GravityForce,
)


class Simulation:
    """High-level simulation controller with forces, collisions,
    batch particles, and recording support."""

    def __init__(self):
        self._engine = PhysicsEngine()
        self._collision = CollisionSystem()
        self._batch = None
        self._step_count = 0
        self._particles = {}   # name -> shared_ptr kept alive
        self._recording = False
        self._history = []

    # ── entities ─────────────────────────────────────────────────

    def add_particle(self, name="particle", position=(0, 0, 0),
                     mass=1.0, velocity=(0, 0, 0)):
        p = Particle(name, Vector3D(*position), mass)
        p.velocity = Vector3D(*velocity)
        self._engine.add_particle(p)
        self._particles[name] = p
        return p

    def add_rigid_body(self, name="body", position=(0, 0, 0),
                       mass=1.0, moi=1.0, velocity=(0, 0, 0)):
        rb = RigidBody(name, Vector3D(*position), mass, moi)
        rb.velocity = Vector3D(*velocity)
        self._engine.add_rigid_body(rb)
        self._particles[name] = rb
        return rb

    # ── forces ───────────────────────────────────────────────────

    def add_force(self, force):
        if hasattr(force, 'core'):
            self._engine.add_force(force.core)
        else:
            self._engine.add_force(force)

    def enable_gravity(self, y=-9.81, x=0, z=0):
        self._engine.add_force(GravityForce(Vector3D(x, y, z)))

    # ── collision shapes ─────────────────────────────────────────

    def add_sphere(self, particle, radius=1.0):
        """Attach a sphere collider to a particle."""
        self._collision.add_sphere_collider(particle, radius)

    def add_plane(self, normal=(0, 1, 0), offset=0.0):
        """Add an infinite static collision plane."""
        body = Particle("plane", Vector3D(0, offset, 0), 1.0)
        body.is_static = True
        self._engine.add_particle(body)
        self._particles["__plane__" + str(len(self._particles))] = body
        self._collision.add_plane_collider(body, Vector3D(*normal), offset)
        return body

    def add_box(self, particle, half_extents=(0.5, 0.5, 0.5)):
        """Attach an AABB box collider to a particle."""
        self._collision.add_box_collider(particle, Vector3D(*half_extents))

    def enable_collisions(self, enabled=True, restitution=0.5):
        self._collision.enabled = enabled
        self._collision.restitution = restitution

    # ── batch particles (NumPy) ──────────────────────────────────

    def add_particles(self, positions, velocities=None, masses=None):
        """Add thousands of particles from NumPy arrays."""
        import numpy as np
        positions = np.ascontiguousarray(positions, dtype=np.float64)
        if self._batch is None:
            self._batch = BatchParticleSystem()
        if velocities is not None and masses is not None:
            velocities = np.ascontiguousarray(velocities, dtype=np.float64)
            masses = np.ascontiguousarray(masses, dtype=np.float64)
            self._batch.add_particles_full(positions, velocities, masses)
        else:
            self._batch.add_particles(positions)

    def get_positions(self):
        if self._batch is None:
            return None
        return self._batch.get_positions()

    def get_velocities(self):
        if self._batch is None:
            return None
        return self._batch.get_velocities()

    # ── recording / history ──────────────────────────────────────

    def enable_recording(self):
        """Start recording a snapshot after every step."""
        self._recording = True
        self._history.clear()

    def disable_recording(self):
        self._recording = False

    @property
    def history(self):
        """Return the list of recorded frames."""
        return list(self._history)

    def _snapshot(self):
        """Capture the current state as a dict."""
        entities = self._engine.particles
        frame = {
            "time": self._engine.elapsed_time,
            "step": self._step_count,
            "names": [],
            "positions": [],
            "velocities": [],
            "masses": [],
        }
        for e in entities:
            frame["names"].append(e.name)
            frame["positions"].append((e.position.x, e.position.y, e.position.z))
            frame["velocities"].append((e.velocity.x, e.velocity.y, e.velocity.z))
            frame["masses"].append(e.mass)

        if self._batch is not None:
            frame["batch_positions"] = self._batch.get_positions()
            frame["batch_velocities"] = self._batch.get_velocities()

        return frame

    # ── simulation control ───────────────────────────────────────

    def step(self, dt=1/60):
        self._engine.step(dt)
        self._collision.detect_and_resolve()
        if self._batch is not None:
            self._batch.step(dt, 0, -9.81, 0)
        self._step_count += 1

        if self._recording:
            self._history.append(self._snapshot())

    def run(self, steps=100, dt=1/60):
        for _ in range(steps):
            self.step(dt)

    # ── export helpers ───────────────────────────────────────────

    def export(self, output_dir="output", fmt="hdf5", basename="simulation"):
        """Export recorded history to a file.

        Parameters
        ----------
        output_dir : str
            Directory to write output (created if needed).
        fmt : str
            ``"hdf5"`` or ``"vtk"``.
        basename : str
            File name prefix (without extension).
        """
        if fmt == "vtk":
            from .exporters.vtk_exporter import export_vtk
            return export_vtk(self, output_dir, basename)
        elif fmt in ("hdf5", "h5"):
            from .exporters.hdf5_exporter import export_hdf5
            return export_hdf5(self, output_dir, basename)
        else:
            raise ValueError(f"Unknown format '{fmt}'. Use 'vtk' or 'hdf5'.")

    # ── queries ──────────────────────────────────────────────────

    @property
    def entities(self):
        return self._engine.particles

    @property
    def time(self):
        return self._engine.elapsed_time

    @property
    def step_count(self):
        return self._step_count

    @property
    def batch_count(self):
        return self._batch.count if self._batch else 0
