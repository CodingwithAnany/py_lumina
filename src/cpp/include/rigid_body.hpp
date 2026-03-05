#pragma once

#include "particle.hpp"
#include <cmath>

namespace pylumina {

/**
 * @brief Rigid body with both linear and rotational dynamics.
 *
 * Extends the point-mass Particle with orientation, angular velocity,
 * torque accumulation, and a scalar moment of inertia (uniform sphere
 * approximation by default).
 */
class RigidBody : public Particle {
public:
    Vector3D orientation;          // Euler angles (radians) — simplified model
    Vector3D angular_velocity;
    Vector3D torque_accumulator;
    double moment_of_inertia;      // scalar approximation (kg·m²)
    double angular_damping;

    RigidBody()
        : Particle(), orientation(), angular_velocity(),
          torque_accumulator(), moment_of_inertia(1.0), angular_damping(0.01) {}

    RigidBody(const std::string& name, const Vector3D& pos,
              double mass, double moi)
        : Particle(name, pos, mass), orientation(), angular_velocity(),
          torque_accumulator(), moment_of_inertia(moi), angular_damping(0.01) {}

    // ── torque helpers ──────────────────────────────────────────────
    void apply_torque(const Vector3D& torque) {
        if (!is_static)
            torque_accumulator += torque;
    }

    /**
     * @brief Apply a force at an offset from the centre of mass.
     *
     * This simultaneously applies the linear force *and* the torque
     * (r × F) produced by the off-centre application point.
     */
    void apply_force_at_point(const Vector3D& force, const Vector3D& point) {
        apply_force(force);
        Vector3D r = point - position;
        apply_torque(r.cross(force));
    }

    void clear_torques() {
        torque_accumulator = Vector3D::zero();
    }

    // ── integration (linear + angular) ──────────────────────────────
    void integrate(double dt) {
        if (is_static) return;

        // Linear integration (reuse parent)
        Particle::integrate(dt);

        // Angular integration
        if (moment_of_inertia > 0.0) {
            Vector3D angular_accel = torque_accumulator / moment_of_inertia;
            angular_velocity += angular_accel * dt;
            angular_velocity *= (1.0 - angular_damping);
            orientation += angular_velocity * dt;
        }

        clear_torques();
    }

    // ── energy helpers ──────────────────────────────────────────────
    double rotational_kinetic_energy() const {
        return 0.5 * moment_of_inertia * angular_velocity.magnitude_squared();
    }

    double total_kinetic_energy() const {
        return kinetic_energy() + rotational_kinetic_energy();
    }

    std::string to_string() const {
        std::ostringstream oss;
        oss << "RigidBody('" << name << "', pos=" << position.to_string()
            << ", orient=" << orientation.to_string()
            << ", mass=" << mass
            << ", moi=" << moment_of_inertia << ")";
        return oss.str();
    }
};

}  // namespace pylumina
