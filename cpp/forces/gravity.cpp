#include "forces_impl.h"

namespace pylumina {
    void GravityForce::apply(Particle& p, double /*dt*/) {
        if (!p.is_static) p.apply_force(g * p.mass);
    }
}
