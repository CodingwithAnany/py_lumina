#pragma once

#include <cmath>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>

namespace pylumina {

// ── Vector3D ────────────────────────────────────────────────────────

struct Vector3D {
    double x, y, z;

    Vector3D() : x(0.0), y(0.0), z(0.0) {}
    Vector3D(double x, double y, double z) : x(x), y(y), z(z) {}

    Vector3D operator+(const Vector3D& o) const { return {x+o.x, y+o.y, z+o.z}; }
    Vector3D operator-(const Vector3D& o) const { return {x-o.x, y-o.y, z-o.z}; }
    Vector3D operator*(double s) const { return {x*s, y*s, z*s}; }
    Vector3D operator/(double s) const { return {x/s, y/s, z/s}; }
    
    double dot(const Vector3D& o) const { return x*o.x + y*o.y + z*o.z; }
    Vector3D cross(const Vector3D& o) const {
        return { y*o.z - z*o.y, z*o.x - x*o.z, x*o.y - y*o.x };
    }
    double magnitude() const { return std::sqrt(x*x + y*y + z*z); }
    Vector3D normalized() const {
        double m = magnitude();
        return (m > 0) ? *this / m : *this;
    }
};

// ── Entities ────────────────────────────────────────────────────────

class Particle {
public:
    std::string name;
    Vector3D position;
    Vector3D velocity;
    Vector3D force_accumulator;
    double mass;
    double damping;
    bool is_static;

    Particle(const std::string& n, Vector3D p, double m)
        : name(n), position(p), velocity(0,0,0), force_accumulator(0,0,0), 
          mass(m), damping(0.01), is_static(false) {}
    
    virtual ~Particle() = default;
    void apply_force(const Vector3D& f);
    virtual void integrate(double dt);
};

class RigidBody : public Particle {
public:
    Vector3D orientation;
    Vector3D angular_velocity;
    Vector3D torque_accumulator;
    double moment_of_inertia;
    double angular_damping;

    RigidBody(const std::string& n, Vector3D p, double m, double moi)
        : Particle(n, p, m), orientation(0,0,0), angular_velocity(0,0,0),
          torque_accumulator(0,0,0), moment_of_inertia(moi), angular_damping(0.01) {}

    void apply_torque(const Vector3D& t);
    void integrate(double dt) override;
};

// ── Force Generator Base ────────────────────────────────────────────

class ForceGenerator {
public:
    virtual ~ForceGenerator() = default;
    virtual void apply(Particle& p, double dt) = 0;
};

// ── Engine ──────────────────────────────────────────────────────────

class PhysicsEngine {
public:
    std::vector<std::shared_ptr<Particle>> particles;
    double elapsed_time = 0.0;

    void add_particle(std::shared_ptr<Particle> p) { particles.push_back(p); }
    void step(double dt);
    void add_force(std::shared_ptr<ForceGenerator> f) { forces.push_back(f); }

private:
    std::vector<std::shared_ptr<ForceGenerator>> forces;
};

} // namespace pylumina
