#pragma once
#include "../engine/physics_engine.h"

namespace pylumina {

class GravityForce : public ForceGenerator {
public:
    Vector3D g;
    GravityForce(Vector3D gravity) : g(gravity) {}
    void apply(Particle& p, double dt) override;
};

class WindForce : public ForceGenerator {
public:
    Vector3D direction;
    double strength;
    WindForce(Vector3D dir, double s) : direction(dir), strength(s) {}
    void apply(Particle& p, double dt) override;
};

class DragForce : public ForceGenerator {
public:
    double cd; // drag coefficient
    double area;
    double rho; // fluid density
    DragForce(double c, double a, double r = 1.225) : cd(c), area(a), rho(r) {}
    void apply(Particle& p, double dt) override;
};

} // namespace pylumina
