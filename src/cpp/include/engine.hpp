#pragma once

#include "vector3d.hpp"
#include "particle.hpp"
#include "rigid_body.hpp"
#include "forces.hpp"

#include <vector>
#include <memory>
#include <string>
#include <stdexcept>

namespace pylumina {

/**
 * @brief Core physics simulation engine.
 *
 * Manages a collection of particles / rigid bodies and force generators.
 * Each call to step(dt) applies all registered forces to every tracked
 * entity and then integrates their motion.
 */
class PhysicsEngine {
public:
    // ── entity storage ──────────────────────────────────────────────
    std::vector<std::shared_ptr<Particle>>   particles;
    std::vector<std::shared_ptr<RigidBody>>  rigid_bodies;

    // ── force generators (applied to ALL entities each step) ────────
    std::vector<std::shared_ptr<ForceGenerator>> forces;

    double elapsed_time = 0.0;
    size_t step_count   = 0;

    PhysicsEngine() = default;

    // ── add helpers ─────────────────────────────────────────────────
    std::shared_ptr<Particle> add_particle(
            const std::string& name, const Vector3D& pos, double mass) {
        auto p = std::make_shared<Particle>(name, pos, mass);
        particles.push_back(p);
        return p;
    }

    std::shared_ptr<RigidBody> add_rigid_body(
            const std::string& name, const Vector3D& pos,
            double mass, double moi) {
        auto rb = std::make_shared<RigidBody>(name, pos, mass, moi);
        rigid_bodies.push_back(rb);
        return rb;
    }

    void add_force(std::shared_ptr<ForceGenerator> fg) {
        forces.push_back(std::move(fg));
    }

    // ── remove helpers ──────────────────────────────────────────────
    void remove_particle(const std::string& name) {
        particles.erase(
            std::remove_if(particles.begin(), particles.end(),
                [&](const std::shared_ptr<Particle>& p) {
                    return p->name == name;
                }),
            particles.end());
    }

    void remove_rigid_body(const std::string& name) {
        rigid_bodies.erase(
            std::remove_if(rigid_bodies.begin(), rigid_bodies.end(),
                [&](const std::shared_ptr<RigidBody>& rb) {
                    return rb->name == name;
                }),
            rigid_bodies.end());
    }

    void clear_forces() { forces.clear(); }

    void clear_all() {
        particles.clear();
        rigid_bodies.clear();
        forces.clear();
        elapsed_time = 0.0;
        step_count   = 0;
    }

    // ── main simulation step ────────────────────────────────────────
    void step(double dt) {
        if (dt <= 0.0)
            throw std::runtime_error("PhysicsEngine::step: dt must be > 0");

        // Apply global forces to particles
        for (auto& fg : forces)
            for (auto& p : particles)
                fg->apply(*p, dt);

        // Apply global forces to rigid bodies (they inherit from Particle)
        for (auto& fg : forces)
            for (auto& rb : rigid_bodies)
                fg->apply(*rb, dt);

        // Integrate particles
        for (auto& p : particles)
            p->integrate(dt);

        // Integrate rigid bodies (includes angular integration)
        for (auto& rb : rigid_bodies)
            rb->integrate(dt);

        elapsed_time += dt;
        ++step_count;
    }

    /**
     * @brief Run multiple steps at once (useful for batch simulation).
     */
    void run(double dt, size_t num_steps) {
        for (size_t i = 0; i < num_steps; ++i)
            step(dt);
    }

    // ── queries ─────────────────────────────────────────────────────
    double total_kinetic_energy() const {
        double ke = 0.0;
        for (const auto& p : particles)
            ke += p->kinetic_energy();
        for (const auto& rb : rigid_bodies)
            ke += rb->total_kinetic_energy();
        return ke;
    }

    size_t entity_count() const {
        return particles.size() + rigid_bodies.size();
    }

    std::string to_string() const {
        std::ostringstream oss;
        oss << "PhysicsEngine(particles=" << particles.size()
            << ", rigid_bodies=" << rigid_bodies.size()
            << ", forces=" << forces.size()
            << ", elapsed=" << elapsed_time << "s"
            << ", steps=" << step_count << ")";
        return oss.str();
    }
};

}  // namespace pylumina
