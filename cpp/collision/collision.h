#pragma once

#include "../engine/physics_engine.h"
#include <algorithm>
#include <limits>

namespace pylumina {

// ═══════════════════════════════════════════════════════════════════
//  Collision shapes
// ═══════════════════════════════════════════════════════════════════

enum class ShapeType { SPHERE, PLANE, BOX };

struct SphereShape {
    double radius;
    SphereShape(double r = 1.0) : radius(r) {}
};

struct PlaneShape {
    Vector3D normal;
    double   offset;
    PlaneShape(Vector3D n = Vector3D(0,1,0), double d = 0)
        : normal(n.normalized()), offset(d) {}
};

struct BoxShape {
    Vector3D half_extents;
    BoxShape(Vector3D he = Vector3D(0.5,0.5,0.5)) : half_extents(he) {}
};

// ═══════════════════════════════════════════════════════════════════
//  Collider entry — shape + pointer to body + shape type
// ═══════════════════════════════════════════════════════════════════

struct Collider {
    Particle* body;
    ShapeType type;
    SphereShape sphere;
    PlaneShape  plane;
    BoxShape    box;
};

// ═══════════════════════════════════════════════════════════════════
//  Contact
// ═══════════════════════════════════════════════════════════════════

struct Contact {
    Particle* a = nullptr;
    Particle* b = nullptr;
    Vector3D  normal;
    double    penetration = 0;
};

// ═══════════════════════════════════════════════════════════════════
//  Collision System
// ═══════════════════════════════════════════════════════════════════

class CollisionSystem {
public:
    std::vector<Collider> colliders;
    double restitution = 0.5;
    bool   enabled     = false;

    void add_sphere_collider(Particle* body, double radius) {
        Collider c;
        c.body = body;
        c.type = ShapeType::SPHERE;
        c.sphere = SphereShape(radius);
        colliders.push_back(c);
    }

    void add_plane_collider(Particle* body, Vector3D normal, double offset) {
        Collider c;
        c.body = body;
        c.type = ShapeType::PLANE;
        c.plane = PlaneShape(normal, offset);
        colliders.push_back(c);
    }

    void add_box_collider(Particle* body, Vector3D half_extents) {
        Collider c;
        c.body = body;
        c.type = ShapeType::BOX;
        c.box = BoxShape(half_extents);
        colliders.push_back(c);
    }

    void detect_and_resolve();

private:
    bool test_sphere_sphere(const Collider& a, const Collider& b, Contact& ct);
    bool test_sphere_plane (const Collider& sphere, const Collider& plane, Contact& ct);
    bool test_box_box      (const Collider& a, const Collider& b, Contact& ct);

    void resolve(Contact& ct);
};

} // namespace pylumina
