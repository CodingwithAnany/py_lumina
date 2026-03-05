"""
Convenience factories and presets for common force configurations.
"""

from __future__ import annotations

from py_lumina._core import (
    DragForce,
    GravityForce,
    Vector3D,
    WindForce,
)


# ═══════════════════════════════════════════════════════════════════════
#  Factory functions
# ═══════════════════════════════════════════════════════════════════════

def create_gravity(
    gx: float = 0.0,
    gy: float = -9.81,
    gz: float = 0.0,
) -> GravityForce:
    """Create a gravity force generator.

    Parameters
    ----------
    gx, gy, gz : float
        Components of the gravitational acceleration vector (m/s²).
        Default is Earth-surface gravity pointing in -Y.
    """
    return GravityForce(Vector3D(gx, gy, gz))


def create_wind(
    direction: tuple = (1.0, 0.0, 0.0),
    strength: float = 5.0,
) -> WindForce:
    """Create a wind force generator.

    Parameters
    ----------
    direction : tuple of float
        Direction vector (will be normalised internally).
    strength : float
        Force magnitude in Newtons.
    """
    return WindForce(Vector3D(*direction), strength)


def create_drag(
    drag_coefficient: float = 0.47,
    cross_section_area: float = 0.01,
    fluid_density: float = 1.225,
) -> DragForce:
    """Create an aerodynamic drag force generator.

    Parameters
    ----------
    drag_coefficient : float
        Dimensionless drag coefficient Cd (0.47 for a sphere).
    cross_section_area : float
        Reference area A in m².
    fluid_density : float
        Fluid density ρ in kg/m³ (1.225 for air at sea level).
    """
    return DragForce(drag_coefficient, cross_section_area, fluid_density)


# ═══════════════════════════════════════════════════════════════════════
#  Presets
# ═══════════════════════════════════════════════════════════════════════

class ForcePresets:
    """Ready-made force generators for common scenarios."""

    @staticmethod
    def earth_gravity() -> GravityForce:
        """Standard Earth surface gravity (9.81 m/s², -Y)."""
        return create_gravity(0, -9.81, 0)

    @staticmethod
    def moon_gravity() -> GravityForce:
        """Lunar surface gravity (1.62 m/s², -Y)."""
        return create_gravity(0, -1.62, 0)

    @staticmethod
    def mars_gravity() -> GravityForce:
        """Mars surface gravity (3.72 m/s², -Y)."""
        return create_gravity(0, -3.72, 0)

    @staticmethod
    def zero_gravity() -> GravityForce:
        """Zero-G environment."""
        return create_gravity(0, 0, 0)

    @staticmethod
    def gentle_breeze() -> WindForce:
        """Light wind (≈ 2 N, +X direction)."""
        return create_wind((1, 0, 0), 2.0)

    @staticmethod
    def strong_gale() -> WindForce:
        """Strong gale-force wind (≈ 50 N, +X direction)."""
        return create_wind((1, 0, 0), 50.0)

    @staticmethod
    def sphere_drag(radius: float = 0.05) -> DragForce:
        """Drag for a smooth sphere of the given radius (m) in air."""
        import math
        area = math.pi * radius ** 2
        return create_drag(0.47, area, 1.225)

    @staticmethod
    def cube_drag(side: float = 0.1) -> DragForce:
        """Drag for a cube of the given side length (m) in air."""
        return create_drag(1.05, side * side, 1.225)
