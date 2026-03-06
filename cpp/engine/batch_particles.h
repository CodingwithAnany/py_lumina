#pragma once

#include "../engine/physics_engine.h"
#include <vector>
#include <cstring>

namespace pylumina {

/**
 * @brief Manages thousands of particles stored as flat arrays for cache-
 *        friendly, vectorised processing.  Positions, velocities, and
 *        masses are kept in separate contiguous buffers.
 */
class BatchParticleSystem {
public:
    // SoA layout — each vector has `count` elements
    std::vector<double> px, py, pz;     // positions
    std::vector<double> vx, vy, vz;     // velocities
    std::vector<double> masses;
    size_t count = 0;

    // ── batch creation ──────────────────────────────────────────
    void add_particles_from_arrays(const double* positions, size_t n) {
        // `positions` has layout [x0,y0,z0, x1,y1,z1, ...]
        for (size_t i = 0; i < n; ++i) {
            px.push_back(positions[i * 3 + 0]);
            py.push_back(positions[i * 3 + 1]);
            pz.push_back(positions[i * 3 + 2]);
            vx.push_back(0); vy.push_back(0); vz.push_back(0);
            masses.push_back(1.0);
        }
        count += n;
    }

    void add_particles_full(const double* positions,
                            const double* velocities,
                            const double* mass_arr,
                            size_t n) {
        for (size_t i = 0; i < n; ++i) {
            px.push_back(positions[i * 3 + 0]);
            py.push_back(positions[i * 3 + 1]);
            pz.push_back(positions[i * 3 + 2]);
            vx.push_back(velocities ? velocities[i * 3 + 0] : 0);
            vy.push_back(velocities ? velocities[i * 3 + 1] : 0);
            vz.push_back(velocities ? velocities[i * 3 + 2] : 0);
            masses.push_back(mass_arr ? mass_arr[i] : 1.0);
        }
        count += n;
    }

    // ── per-step integration with uniform gravity ───────────────
    void step(double dt, double gx, double gy, double gz) {
        for (size_t i = 0; i < count; ++i) {
            // apply gravity
            vx[i] += gx * dt;
            vy[i] += gy * dt;
            vz[i] += gz * dt;
            // integrate position
            px[i] += vx[i] * dt;
            py[i] += vy[i] * dt;
            pz[i] += vz[i] * dt;
        }
    }

    void clear() {
        px.clear(); py.clear(); pz.clear();
        vx.clear(); vy.clear(); vz.clear();
        masses.clear();
        count = 0;
    }
};

} // namespace pylumina
