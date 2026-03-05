#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "vector3d.hpp"
#include "particle.hpp"
#include "rigid_body.hpp"
#include "forces.hpp"
#include "engine.hpp"

namespace py = pybind11;
using namespace pylumina;

PYBIND11_MODULE(_core, m) {
    m.doc() = "py_lumina — High-performance physics simulation engine (C++ core)";

    // ═════════════════════════════════════════════════════════════════
    //  Vector3D
    // ═════════════════════════════════════════════════════════════════
    py::class_<Vector3D>(m, "Vector3D",
        "3-component vector for positions, velocities, and forces.")
        .def(py::init<>())
        .def(py::init<double, double, double>(),
             py::arg("x") = 0.0, py::arg("y") = 0.0, py::arg("z") = 0.0)
        .def_readwrite("x", &Vector3D::x)
        .def_readwrite("y", &Vector3D::y)
        .def_readwrite("z", &Vector3D::z)
        // operators
        .def("__add__",  &Vector3D::operator+)
        .def("__sub__",  static_cast<Vector3D (Vector3D::*)(const Vector3D&) const>(&Vector3D::operator-))
        .def("__mul__",  &Vector3D::operator*)
        .def("__truediv__", &Vector3D::operator/)
        .def("__eq__",   &Vector3D::operator==)
        .def("__ne__",   &Vector3D::operator!=)
        .def("__repr__", &Vector3D::to_string)
        .def("__str__",  &Vector3D::to_string)
        // methods
        .def("dot",        &Vector3D::dot, py::arg("other"))
        .def("cross",      &Vector3D::cross, py::arg("other"))
        .def("magnitude",          &Vector3D::magnitude)
        .def("magnitude_squared",  &Vector3D::magnitude_squared)
        .def("normalized",         &Vector3D::normalized)
        .def("distance_to",       &Vector3D::distance_to, py::arg("other"))
        .def("lerp",              &Vector3D::lerp,
             py::arg("target"), py::arg("t"))
        // static factories
        .def_static("zero",    &Vector3D::zero)
        .def_static("up",      &Vector3D::up)
        .def_static("right",   &Vector3D::right)
        .def_static("forward", &Vector3D::forward);

    // ═════════════════════════════════════════════════════════════════
    //  Particle
    // ═════════════════════════════════════════════════════════════════
    py::class_<Particle, std::shared_ptr<Particle>>(m, "Particle",
        "Point-mass particle with linear dynamics.")
        .def(py::init<>())
        .def(py::init<const std::string&, const Vector3D&, double>(),
             py::arg("name"), py::arg("position"), py::arg("mass"))
        .def_readwrite("name",     &Particle::name)
        .def_readwrite("position", &Particle::position)
        .def_readwrite("velocity", &Particle::velocity)
        .def_readwrite("acceleration", &Particle::acceleration)
        .def_readwrite("mass",     &Particle::mass)
        .def_readwrite("damping",  &Particle::damping)
        .def_readwrite("is_static", &Particle::is_static)
        .def("apply_force",  &Particle::apply_force, py::arg("force"))
        .def("clear_forces", &Particle::clear_forces)
        .def("integrate",    &Particle::integrate, py::arg("dt"))
        .def("kinetic_energy", &Particle::kinetic_energy)
        .def("speed",        &Particle::speed)
        .def("__repr__",     &Particle::to_string)
        .def("__str__",      &Particle::to_string);

    // ═════════════════════════════════════════════════════════════════
    //  RigidBody
    // ═════════════════════════════════════════════════════════════════
    py::class_<RigidBody, Particle, std::shared_ptr<RigidBody>>(m, "RigidBody",
        "Rigid body with linear + rotational dynamics.")
        .def(py::init<>())
        .def(py::init<const std::string&, const Vector3D&, double, double>(),
             py::arg("name"), py::arg("position"),
             py::arg("mass"), py::arg("moment_of_inertia"))
        .def_readwrite("orientation",       &RigidBody::orientation)
        .def_readwrite("angular_velocity",  &RigidBody::angular_velocity)
        .def_readwrite("moment_of_inertia", &RigidBody::moment_of_inertia)
        .def_readwrite("angular_damping",   &RigidBody::angular_damping)
        .def("apply_torque",         &RigidBody::apply_torque, py::arg("torque"))
        .def("apply_force_at_point", &RigidBody::apply_force_at_point,
             py::arg("force"), py::arg("point"))
        .def("clear_torques",        &RigidBody::clear_torques)
        .def("integrate",            &RigidBody::integrate, py::arg("dt"))
        .def("rotational_kinetic_energy", &RigidBody::rotational_kinetic_energy)
        .def("total_kinetic_energy",      &RigidBody::total_kinetic_energy)
        .def("__repr__", &RigidBody::to_string)
        .def("__str__",  &RigidBody::to_string);

    // ═════════════════════════════════════════════════════════════════
    //  Force generators
    // ═════════════════════════════════════════════════════════════════
    py::class_<ForceGenerator, std::shared_ptr<ForceGenerator>>(m, "ForceGenerator",
        "Abstract base class for force generators.")
        .def("type_name", &ForceGenerator::type_name)
        .def("__repr__",  &ForceGenerator::to_string)
        .def("__str__",   &ForceGenerator::to_string);

    py::class_<GravityForce, ForceGenerator, std::shared_ptr<GravityForce>>(
        m, "GravityForce",
        "Uniform gravitational field: F = m * g")
        .def(py::init<>())
        .def(py::init<const Vector3D&>(), py::arg("gravity"))
        .def_readwrite("gravity", &GravityForce::gravity)
        .def("__repr__", &GravityForce::to_string)
        .def("__str__",  &GravityForce::to_string);

    py::class_<WindForce, ForceGenerator, std::shared_ptr<WindForce>>(
        m, "WindForce",
        "Constant directional wind: F = strength * direction_hat")
        .def(py::init<>())
        .def(py::init<const Vector3D&, double>(),
             py::arg("direction"), py::arg("strength"))
        .def_readwrite("direction", &WindForce::direction)
        .def_readwrite("strength",  &WindForce::strength)
        .def("__repr__", &WindForce::to_string)
        .def("__str__",  &WindForce::to_string);

    py::class_<DragForce, ForceGenerator, std::shared_ptr<DragForce>>(
        m, "DragForce",
        "Aerodynamic drag: F = -0.5 * rho * Cd * A * |v|^2 * v_hat")
        .def(py::init<>())
        .def(py::init<double, double, double>(),
             py::arg("drag_coefficient"),
             py::arg("cross_section_area"),
             py::arg("fluid_density") = 1.225)
        .def_readwrite("drag_coefficient",    &DragForce::drag_coefficient)
        .def_readwrite("cross_section_area",  &DragForce::cross_section_area)
        .def_readwrite("fluid_density",       &DragForce::fluid_density)
        .def("__repr__", &DragForce::to_string)
        .def("__str__",  &DragForce::to_string);

    // ═════════════════════════════════════════════════════════════════
    //  PhysicsEngine
    // ═════════════════════════════════════════════════════════════════
    py::class_<PhysicsEngine>(m, "PhysicsEngine",
        "Core simulation engine managing entities and forces.")
        .def(py::init<>())
        .def_readwrite("elapsed_time", &PhysicsEngine::elapsed_time)
        .def_readonly("step_count",    &PhysicsEngine::step_count)
        .def("add_particle",    &PhysicsEngine::add_particle,
             py::arg("name"), py::arg("position"), py::arg("mass"),
             py::return_value_policy::reference_internal)
        .def("add_rigid_body",  &PhysicsEngine::add_rigid_body,
             py::arg("name"), py::arg("position"),
             py::arg("mass"), py::arg("moment_of_inertia"),
             py::return_value_policy::reference_internal)
        .def("add_force",       &PhysicsEngine::add_force,
             py::arg("force_generator"))
        .def("remove_particle",   &PhysicsEngine::remove_particle,
             py::arg("name"))
        .def("remove_rigid_body", &PhysicsEngine::remove_rigid_body,
             py::arg("name"))
        .def("clear_forces", &PhysicsEngine::clear_forces)
        .def("clear_all",    &PhysicsEngine::clear_all)
        .def("step",         &PhysicsEngine::step, py::arg("dt"))
        .def("run",          &PhysicsEngine::run,
             py::arg("dt"), py::arg("num_steps"))
        .def("total_kinetic_energy", &PhysicsEngine::total_kinetic_energy)
        .def("entity_count",         &PhysicsEngine::entity_count)
        .def("__repr__",             &PhysicsEngine::to_string)
        .def("__str__",              &PhysicsEngine::to_string);
}
