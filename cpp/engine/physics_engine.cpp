#include "physics_engine.h"
#include <algorithm>

namespace pylumina {

void Particle::apply_force(const Vector3D& f) {
    if (!is_static) force_accumulator = force_accumulator + f;
}

void RigidBody::apply_torque(const Vector3D& t) {
    if (!is_static) torque_accumulator = torque_accumulator + t;
}

void PhysicsEngine::step(double dt) {
    if (dt <= 0) return;

    for (auto& f : forces) {
        for (auto& p : particles) {
            f->apply(*p, dt);
        }
    }

    for (auto& p : particles) {
        p->integrate(dt);
    }

    elapsed_time += dt;
}

} // namespace pylumina
