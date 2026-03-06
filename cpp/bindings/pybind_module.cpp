#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "../engine/physics_engine.h"
#include "../engine/batch_particles.h"
#include "../forces/forces_impl.h"
#include "../collision/collision.h"

namespace py = pybind11;
using namespace pylumina;

PYBIND11_MODULE(_core, m) {
    m.doc() = "pylumina — High-performance physics engine (C++ core)";

    // ═════════════════════════════════════════════════════════════════
    //  Vector3D
    // ═════════════════════════════════════════════════════════════════
    py::class_<Vector3D>(m, "Vector3D")
        .def(py::init<double, double, double>(),
             py::arg("x")=0, py::arg("y")=0, py::arg("z")=0)
        .def_readwrite("x", &Vector3D::x)
        .def_readwrite("y", &Vector3D::y)
        .def_readwrite("z", &Vector3D::z)
        .def("dot",       &Vector3D::dot)
        .def("cross",     &Vector3D::cross)
        .def("magnitude", &Vector3D::magnitude)
        .def("normalized",&Vector3D::normalized)
        .def("__repr__", [](const Vector3D& v) {
            return "Vector3D(" + std::to_string(v.x) + ", "
                               + std::to_string(v.y) + ", "
                               + std::to_string(v.z) + ")";
        });

    // ═════════════════════════════════════════════════════════════════
    //  Particle / RigidBody
    // ═════════════════════════════════════════════════════════════════
    py::class_<Particle, std::shared_ptr<Particle>>(m, "Particle")
        .def(py::init<const std::string&, Vector3D, double>())
        .def_readwrite("name",       &Particle::name)
        .def_readwrite("position",   &Particle::position)
        .def_readwrite("velocity",   &Particle::velocity)
        .def_readwrite("mass",       &Particle::mass)
        .def_readwrite("damping",    &Particle::damping)
        .def_readwrite("is_static",  &Particle::is_static);

    py::class_<RigidBody, Particle, std::shared_ptr<RigidBody>>(m, "RigidBody")
        .def(py::init<const std::string&, Vector3D, double, double>())
        .def_readwrite("orientation",       &RigidBody::orientation)
        .def_readwrite("angular_velocity",  &RigidBody::angular_velocity)
        .def_readwrite("moment_of_inertia", &RigidBody::moment_of_inertia)
        .def_readwrite("angular_damping",   &RigidBody::angular_damping);

    // ═════════════════════════════════════════════════════════════════
    //  Force generators
    // ═════════════════════════════════════════════════════════════════
    py::class_<ForceGenerator, std::shared_ptr<ForceGenerator>>(m, "ForceGenerator");

    py::class_<GravityForce, ForceGenerator, std::shared_ptr<GravityForce>>(
            m, "GravityForce")
        .def(py::init<Vector3D>());

    py::class_<WindForce, ForceGenerator, std::shared_ptr<WindForce>>(
            m, "WindForce")
        .def(py::init<Vector3D, double>());

    py::class_<DragForce, ForceGenerator, std::shared_ptr<DragForce>>(
            m, "DragForce")
        .def(py::init<double, double, double>(),
             py::arg("cd"), py::arg("area"), py::arg("rho")=1.225);

    // ═════════════════════════════════════════════════════════════════
    //  Collision system  (uses raw Particle* from shared_ptr holder)
    // ═════════════════════════════════════════════════════════════════
    py::class_<CollisionSystem>(m, "CollisionSystem")
        .def(py::init<>())
        .def_readwrite("restitution", &CollisionSystem::restitution)
        .def_readwrite("enabled",     &CollisionSystem::enabled)
        .def("add_sphere_collider", [](CollisionSystem& self,
                                       std::shared_ptr<Particle> body,
                                       double radius) {
            self.add_sphere_collider(body.get(), radius);
        }, py::arg("body"), py::arg("radius"))
        .def("add_plane_collider", [](CollisionSystem& self,
                                      std::shared_ptr<Particle> body,
                                      Vector3D normal, double offset) {
            self.add_plane_collider(body.get(), normal, offset);
        }, py::arg("body"), py::arg("normal"), py::arg("offset"))
        .def("add_box_collider", [](CollisionSystem& self,
                                    std::shared_ptr<Particle> body,
                                    Vector3D half_extents) {
            self.add_box_collider(body.get(), half_extents);
        }, py::arg("body"), py::arg("half_extents"))
        .def("detect_and_resolve", &CollisionSystem::detect_and_resolve);

    // ═════════════════════════════════════════════════════════════════
    //  PhysicsEngine
    // ═════════════════════════════════════════════════════════════════
    py::class_<PhysicsEngine>(m, "PhysicsEngine")
        .def(py::init<>())
        .def_readwrite("elapsed_time", &PhysicsEngine::elapsed_time)
        .def_readwrite("particles",    &PhysicsEngine::particles)
        .def("add_particle", [](PhysicsEngine& e, std::shared_ptr<Particle> p) {
            e.particles.push_back(p);
        })
        .def("add_rigid_body", [](PhysicsEngine& e, std::shared_ptr<RigidBody> rb) {
            e.particles.push_back(rb);
        })
        .def("add_force", &PhysicsEngine::add_force)
        .def("step",      &PhysicsEngine::step);

    // ═════════════════════════════════════════════════════════════════
    //  BatchParticleSystem  (NumPy integration)
    // ═════════════════════════════════════════════════════════════════
    py::class_<BatchParticleSystem>(m, "BatchParticleSystem")
        .def(py::init<>())
        .def_readonly("count", &BatchParticleSystem::count)

        .def("add_particles", [](BatchParticleSystem& self,
                                 py::array_t<double> positions) {
            auto buf = positions.request();
            if (buf.ndim != 2 || buf.shape[1] != 3)
                throw std::runtime_error("positions must be (N, 3)");
            size_t n = buf.shape[0];
            self.add_particles_from_arrays(
                static_cast<const double*>(buf.ptr), n);
        }, py::arg("positions"))

        .def("add_particles_full", [](BatchParticleSystem& self,
                                      py::array_t<double> pos,
                                      py::array_t<double> vel,
                                      py::array_t<double> mass) {
            auto pb = pos.request();
            auto vb = vel.request();
            auto mb = mass.request();
            if (pb.ndim != 2 || pb.shape[1] != 3)
                throw std::runtime_error("positions must be (N, 3)");
            size_t n = pb.shape[0];
            self.add_particles_full(
                static_cast<const double*>(pb.ptr),
                static_cast<const double*>(vb.ptr),
                static_cast<const double*>(mb.ptr), n);
        }, py::arg("positions"), py::arg("velocities"), py::arg("masses"))

        .def("step", &BatchParticleSystem::step,
             py::arg("dt"), py::arg("gx")=0, py::arg("gy")=-9.81, py::arg("gz")=0)
        .def("clear", &BatchParticleSystem::clear)

        .def("get_positions", [](const BatchParticleSystem& self) {
            py::array_t<double> out({(int)self.count, 3});
            auto buf = out.mutable_unchecked<2>();
            for (size_t i = 0; i < self.count; ++i) {
                buf(i, 0) = self.px[i];
                buf(i, 1) = self.py[i];
                buf(i, 2) = self.pz[i];
            }
            return out;
        })

        .def("get_velocities", [](const BatchParticleSystem& self) {
            py::array_t<double> out({(int)self.count, 3});
            auto buf = out.mutable_unchecked<2>();
            for (size_t i = 0; i < self.count; ++i) {
                buf(i, 0) = self.vx[i];
                buf(i, 1) = self.vy[i];
                buf(i, 2) = self.vz[i];
            }
            return out;
        });
}
