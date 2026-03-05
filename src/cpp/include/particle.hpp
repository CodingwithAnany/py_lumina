#pragma once

#include "vector3d.hpp"
#include <string>
#include <sstream>

namespace pylumina {

/**
 * @brief A point-mass particle with position, velocity, and accumulated forces.
 *
 * This is the fundamental simulated entity.  External forces are accumulated
 * each frame and integrated via semi-implicit Euler in the engine step.
 */
class Particle {
public:
    std::string name;
    Vector3D position;
    Vector3D velocity;
    Vector3D acceleration;
    Vector3D force_accumulator;
    double mass;
    double damping;          // linear damping factor  (0 = no damping, 1 = full)
    bool is_static;          // if true, particle ignores forces / integration

    Particle()
        : name("particle"), position(), velocity(), acceleration(),
          force_accumulator(), mass(1.0), damping(0.01), is_static(false) {}

    Particle(const std::string& name, const Vector3D& pos, double mass)
        : name(name), position(pos), velocity(), acceleration(),
          force_accumulator(), mass(mass), damping(0.01), is_static(false) {}

    // ── force helpers ───────────────────────────────────────────────
    void apply_force(const Vector3D& force) {
        if (!is_static)
            force_accumulator += force;
    }

    void clear_forces() {
        force_accumulator = Vector3D::zero();
    }

    // ── integration (semi-implicit Euler) ───────────────────────────
    void integrate(double dt) {
        if (is_static || mass <= 0.0) return;

        acceleration = force_accumulator / mass;
        velocity += acceleration * dt;
        velocity *= (1.0 - damping);      // simple linear damping
        position += velocity * dt;

        clear_forces();
    }

    // ── kinetic energy ──────────────────────────────────────────────
    double kinetic_energy() const {
        return 0.5 * mass * velocity.magnitude_squared();
    }

    double speed() const {
        return velocity.magnitude();
    }

    std::string to_string() const {
        std::ostringstream oss;
        oss << "Particle('" << name << "', pos=" << position.to_string()
            << ", vel=" << velocity.to_string()
            << ", mass=" << mass << ")";
        return oss.str();
    }
};

}  // namespace pylumina
