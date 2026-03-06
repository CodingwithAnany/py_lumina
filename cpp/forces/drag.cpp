#include "forces_impl.h"

namespace pylumina {
    void DragForce::apply(Particle& p, double /*dt*/) {
        if (p.is_static) return;
        double speed = p.velocity.magnitude();
        if (speed < 1e-6) return;
        
        double magnitude = 0.5 * rho * cd * area * speed * speed;
        Vector3D force = p.velocity.normalized() * (-magnitude);
        p.apply_force(force);
    }
}
