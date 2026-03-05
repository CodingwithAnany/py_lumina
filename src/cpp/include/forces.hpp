#pragma once

#include "vector3d.hpp"
#include "particle.hpp"
#include <cmath>
#include <string>
#include <sstream>

namespace pylumina {

// ═══════════════════════════════════════════════════════════════════════
//  Abstract force generator
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Abstract base class for force generators.
 */
class ForceGenerator {
public:
    virtual ~ForceGenerator() = default;
    virtual void apply(Particle& p, double dt) = 0;
    virtual std::string type_name() const = 0;
    virtual std::string to_string() const = 0;
};

// ═══════════════════════════════════════════════════════════════════════
//  Gravity
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Uniform gravitational field  F = m · g
 */
class GravityForce : public ForceGenerator {
public:
    Vector3D gravity;   // acceleration vector (m/s²)

    GravityForce() : gravity(0.0, -9.81, 0.0) {}
    explicit GravityForce(const Vector3D& g) : gravity(g) {}

    void apply(Particle& p, double /*dt*/) override {
        if (p.is_static) return;
        p.apply_force(gravity * p.mass);
    }

    std::string type_name() const override { return "GravityForce"; }

    std::string to_string() const override {
        std::ostringstream oss;
        oss << "GravityForce(g=" << gravity.to_string() << ")";
        return oss.str();
    }
};

// ═══════════════════════════════════════════════════════════════════════
//  Wind
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Constant-direction wind force  F = strength · direction
 *
 * The force magnitude is independent of the particle's state.
 */
class WindForce : public ForceGenerator {
public:
    Vector3D direction;   // unit direction
    double   strength;    // Newton-scale multiplier

    WindForce() : direction(1.0, 0.0, 0.0), strength(0.0) {}
    WindForce(const Vector3D& dir, double str)
        : direction(dir), strength(str) {}

    void apply(Particle& p, double /*dt*/) override {
        if (p.is_static) return;
        double mag = direction.magnitude();
        if (mag > 0.0) {
            Vector3D force = (direction / mag) * strength;
            p.apply_force(force);
        }
    }

    std::string type_name() const override { return "WindForce"; }

    std::string to_string() const override {
        std::ostringstream oss;
        oss << "WindForce(dir=" << direction.to_string()
            << ", strength=" << strength << ")";
        return oss.str();
    }
};

// ═══════════════════════════════════════════════════════════════════════
//  Drag
// ═══════════════════════════════════════════════════════════════════════

/**
 * @brief Aerodynamic drag   F = -½ ρ Cd A |v|² v̂
 *
 * Parameters:
 *   drag_coefficient   –  Cd  (dimensionless, e.g. 0.47 for a sphere)
 *   cross_section_area –  A   (m²)
 *   fluid_density      –  ρ   (kg/m³, air ≈ 1.225)
 */
class DragForce : public ForceGenerator {
public:
    double drag_coefficient;
    double cross_section_area;
    double fluid_density;

    DragForce()
        : drag_coefficient(0.47), cross_section_area(0.01),
          fluid_density(1.225) {}

    DragForce(double cd, double area, double rho)
        : drag_coefficient(cd), cross_section_area(area),
          fluid_density(rho) {}

    void apply(Particle& p, double /*dt*/) override {
        if (p.is_static) return;
        double speed = p.velocity.magnitude();
        if (speed == 0.0) return;

        double drag_mag = 0.5 * fluid_density * drag_coefficient
                        * cross_section_area * speed * speed;

        Vector3D drag_dir = p.velocity.normalized() * (-1.0);
        p.apply_force(drag_dir * drag_mag);
    }

    std::string type_name() const override { return "DragForce"; }

    std::string to_string() const override {
        std::ostringstream oss;
        oss << "DragForce(Cd=" << drag_coefficient
            << ", A=" << cross_section_area
            << ", rho=" << fluid_density << ")";
        return oss.str();
    }
};

}  // namespace pylumina
