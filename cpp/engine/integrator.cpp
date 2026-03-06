#include "physics_engine.h"

namespace pylumina {

void Particle::integrate(double dt) {
    if (is_static || mass <= 0) {
        force_accumulator = Vector3D(0,0,0);
        return;
    }

    Vector3D acceleration = force_accumulator / mass;
    velocity = velocity + acceleration * dt;
    velocity = velocity * (1.0 - damping);
    position = position + velocity * dt;

    force_accumulator = Vector3D(0,0,0);
}

void RigidBody::integrate(double dt) {
    if (is_static) return;

    // Linear
    Particle::integrate(dt);

    // Angular
    if (moment_of_inertia > 0) {
        Vector3D angular_accel = torque_accumulator / moment_of_inertia;
        angular_velocity = angular_velocity + angular_accel * dt;
        angular_velocity = angular_velocity * (1.0 - angular_damping);
        orientation = orientation + angular_velocity * dt;
    }

    torque_accumulator = Vector3D(0,0,0);
}

} // namespace pylumina
