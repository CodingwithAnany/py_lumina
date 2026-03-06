#include "collision.h"

namespace pylumina {

void CollisionSystem::detect_and_resolve() {
    if (!enabled) return;

    for (size_t i = 0; i < colliders.size(); ++i) {
        for (size_t j = i + 1; j < colliders.size(); ++j) {
            Contact ct;
            bool hit = false;

            auto ti = colliders[i].type;
            auto tj = colliders[j].type;

            if (ti == ShapeType::SPHERE && tj == ShapeType::SPHERE) {
                hit = test_sphere_sphere(colliders[i], colliders[j], ct);
            }
            else if (ti == ShapeType::SPHERE && tj == ShapeType::PLANE) {
                hit = test_sphere_plane(colliders[i], colliders[j], ct);
            }
            else if (ti == ShapeType::PLANE && tj == ShapeType::SPHERE) {
                hit = test_sphere_plane(colliders[j], colliders[i], ct);
            }
            else if (ti == ShapeType::BOX && tj == ShapeType::BOX) {
                hit = test_box_box(colliders[i], colliders[j], ct);
            }

            if (hit) resolve(ct);
        }
    }
}

// ── Sphere vs Sphere ────────────────────────────────────────────
// Normal points from a → b

bool CollisionSystem::test_sphere_sphere(const Collider& ca,
                                         const Collider& cb,
                                         Contact& ct) {
    Vector3D diff = cb.body->position - ca.body->position;
    double dist = diff.magnitude();
    double sum_r = ca.sphere.radius + cb.sphere.radius;

    if (dist >= sum_r || dist < 1e-12) return false;

    ct.a = ca.body;
    ct.b = cb.body;
    ct.normal = diff / dist * -1.0;    // b→a = direction to push a away
    ct.penetration = sum_r - dist;
    return true;
}

// ── Sphere vs Plane ─────────────────────────────────────────────
// Normal = plane normal (direction to push sphere OUT)

bool CollisionSystem::test_sphere_plane(const Collider& csphere,
                                        const Collider& cplane,
                                        Contact& ct) {
    double dist = csphere.body->position.dot(cplane.plane.normal)
                - cplane.plane.offset;

    if (dist >= csphere.sphere.radius) return false;

    ct.a = csphere.body;
    ct.b = cplane.body;
    ct.normal = cplane.plane.normal;  // push sphere along this
    ct.penetration = csphere.sphere.radius - dist;
    return true;
}

// ── AABB Box vs Box ─────────────────────────────────────────────
// Normal points from a → b

bool CollisionSystem::test_box_box(const Collider& ca,
                                   const Collider& cb,
                                   Contact& ct) {
    Vector3D diff = cb.body->position - ca.body->position;

    double ox = (ca.box.half_extents.x + cb.box.half_extents.x) - std::abs(diff.x);
    double oy = (ca.box.half_extents.y + cb.box.half_extents.y) - std::abs(diff.y);
    double oz = (ca.box.half_extents.z + cb.box.half_extents.z) - std::abs(diff.z);

    if (ox <= 0 || oy <= 0 || oz <= 0) return false;

    ct.a = ca.body;
    ct.b = cb.body;

    // Normal points in direction to push a away from b
    if (ox <= oy && ox <= oz) {
        ct.normal = Vector3D(diff.x > 0 ? -1 : 1, 0, 0);
        ct.penetration = ox;
    } else if (oy <= ox && oy <= oz) {
        ct.normal = Vector3D(0, diff.y > 0 ? -1 : 1, 0);
        ct.penetration = oy;
    } else {
        ct.normal = Vector3D(0, 0, diff.z > 0 ? -1 : 1);
        ct.penetration = oz;
    }
    return true;
}

// ═══════════════════════════════════════════════════════════════════
//  Resolve — uses consistent convention:
//    normal = direction to separate a from the collision
//    For sphere-sphere: normal = a → b  => push a backwards (-n), push b forwards (+n)
//    For sphere-plane:  normal = plane up => push sphere along +n
//
//  We unify by always pushing a along +normal and b along -normal:
//    - sphere-sphere: a should go -normal (away from b), b should go +normal
//    - sphere-plane:  a should go +normal (up), b is static
//
//  To handle both: for sphere-sphere, normal = a→b, so pushing a along
//    -normal is correct.  For sphere-plane, normal = up, so pushing a 
//    along +normal is correct.  These are OPPOSITE conventions...
//
//  FIX: Negate the sphere-sphere normal so it always points "push a direction".
//  Instead, let's standardize: normal = the direction to push a.
//    sphere-sphere: -(a→b) = b→a  (push a away from b)  
//    sphere-plane:  plane.normal (push sphere up/away)
//    box-box:       -(a→b)
// ═══════════════════════════════════════════════════════════════════

void CollisionSystem::resolve(Contact& c) {
    if (!c.a) return;

    bool a_static = c.a->is_static;
    bool b_static = (!c.b) || c.b->is_static;

    double inv_ma = a_static ? 0.0 : 1.0 / c.a->mass;
    double inv_mb = b_static ? 0.0 : 1.0 / c.b->mass;
    double inv_total = inv_ma + inv_mb;
    if (inv_total < 1e-12) return;

    // ── Positional correction ───────────────────────────────────
    //    Push a along +normal, push b along -normal
    const double slop = 0.001;
    const double percent = 0.8;
    double corr = std::max(c.penetration - slop, 0.0) * percent / inv_total;
    Vector3D correction = c.normal * corr;

    if (!a_static)
        c.a->position = c.a->position + correction * inv_ma;
    if (!b_static && c.b)
        c.b->position = c.b->position - correction * inv_mb;

    // ── Velocity impulse ────────────────────────────────────────
    //    rel_vel along normal: negative = approaching (a moving toward b)
    //    normal points "push a away", so a's velocity along normal should be
    //    positive or zero after resolution.
    Vector3D rel_vel = c.a->velocity - (c.b ? c.b->velocity : Vector3D());
    double vn = rel_vel.dot(c.normal);

    // If vn >= 0, a is already moving away along normal => no impulse needed
    if (vn >= 0) return;

    double j = -(1.0 + restitution) * vn / inv_total;
    Vector3D impulse = c.normal * j;

    if (!a_static)
        c.a->velocity = c.a->velocity + impulse * inv_ma;
    if (!b_static && c.b)
        c.b->velocity = c.b->velocity - impulse * inv_mb;
}

} // namespace pylumina
