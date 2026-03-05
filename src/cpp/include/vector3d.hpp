#pragma once

#include <cmath>
#include <string>
#include <sstream>
#include <stdexcept>

namespace pylumina {

/**
 * @brief High-performance 3D vector class for physics computations.
 *
 * Provides arithmetic operators, dot/cross products, normalization,
 * magnitude, and distance utilities used across all physics models.
 */
class Vector3D {
public:
    double x, y, z;

    // ── constructors ────────────────────────────────────────────────
    Vector3D() : x(0.0), y(0.0), z(0.0) {}
    Vector3D(double x, double y, double z) : x(x), y(y), z(z) {}

    // ── arithmetic operators ────────────────────────────────────────
    Vector3D operator+(const Vector3D& other) const {
        return {x + other.x, y + other.y, z + other.z};
    }

    Vector3D operator-(const Vector3D& other) const {
        return {x - other.x, y - other.y, z - other.z};
    }

    Vector3D operator*(double scalar) const {
        return {x * scalar, y * scalar, z * scalar};
    }

    Vector3D operator/(double scalar) const {
        if (scalar == 0.0)
            throw std::runtime_error("Vector3D: division by zero");
        return {x / scalar, y / scalar, z / scalar};
    }

    // ── compound assignment ─────────────────────────────────────────
    Vector3D& operator+=(const Vector3D& other) {
        x += other.x; y += other.y; z += other.z;
        return *this;
    }

    Vector3D& operator-=(const Vector3D& other) {
        x -= other.x; y -= other.y; z -= other.z;
        return *this;
    }

    Vector3D& operator*=(double scalar) {
        x *= scalar; y *= scalar; z *= scalar;
        return *this;
    }

    // ── comparison ──────────────────────────────────────────────────
    bool operator==(const Vector3D& other) const {
        return x == other.x && y == other.y && z == other.z;
    }

    bool operator!=(const Vector3D& other) const {
        return !(*this == other);
    }

    // ── vector products ─────────────────────────────────────────────
    double dot(const Vector3D& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    Vector3D cross(const Vector3D& other) const {
        return {
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        };
    }

    // ── magnitude & normalization ───────────────────────────────────
    double magnitude() const {
        return std::sqrt(x * x + y * y + z * z);
    }

    double magnitude_squared() const {
        return x * x + y * y + z * z;
    }

    Vector3D normalized() const {
        double mag = magnitude();
        if (mag == 0.0)
            throw std::runtime_error("Vector3D: cannot normalize zero vector");
        return *this / mag;
    }

    // ── utilities ───────────────────────────────────────────────────
    double distance_to(const Vector3D& other) const {
        return (*this - other).magnitude();
    }

    Vector3D lerp(const Vector3D& target, double t) const {
        return *this * (1.0 - t) + target * t;
    }

    std::string to_string() const {
        std::ostringstream oss;
        oss << "Vector3D(" << x << ", " << y << ", " << z << ")";
        return oss.str();
    }

    // ── static factories ────────────────────────────────────────────
    static Vector3D zero()  { return {0.0, 0.0, 0.0}; }
    static Vector3D up()    { return {0.0, 1.0, 0.0}; }
    static Vector3D right() { return {1.0, 0.0, 0.0}; }
    static Vector3D forward() { return {0.0, 0.0, 1.0}; }
};

// Free-function: scalar * vector
inline Vector3D operator*(double scalar, const Vector3D& v) {
    return v * scalar;
}

}  // namespace pylumina
