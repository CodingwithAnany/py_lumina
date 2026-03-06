#include "forces_impl.h"

namespace pylumina {
    void WindForce::apply(Particle& p, double /*dt*/) {
        if (!p.is_static) p.apply_force(direction.normalized() * strength);
    }
}
