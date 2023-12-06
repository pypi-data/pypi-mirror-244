import unyt
import pytest

import libtalley.steeldesign as steel


# ===============================================================================
# Material lookups
# ===============================================================================
def test_material_lookup_exact_match():
    """Material is specified exactly."""
    material = steel.SteelMaterial.from_name('A500', grade='C', application='HSS')
    assert unyt.allclose_units(material.E, 29000 * unyt.ksi)
    assert unyt.allclose_units(material.Fy, 50 * unyt.ksi)
    assert unyt.allclose_units(material.Fu, 62 * unyt.ksi)
    assert unyt.allclose_units(material.Ry, 1.3)
    assert unyt.allclose_units(material.Rt, 1.2)


def test_material_lookup_slice_match_1():
    """Material is only partially specified, but sufficiently to match."""
    material = steel.SteelMaterial.from_name('A500', 'C')
    assert unyt.allclose_units(material.E, 29000 * unyt.ksi)
    assert unyt.allclose_units(material.Fy, 50 * unyt.ksi)
    assert unyt.allclose_units(material.Fu, 62 * unyt.ksi)
    assert unyt.allclose_units(material.Ry, 1.3)
    assert unyt.allclose_units(material.Rt, 1.2)


def test_material_lookup_slice_match_2():
    """Material is only partially specified, but sufficiently to match."""
    material = steel.SteelMaterial.from_name('A992')
    assert unyt.allclose_units(material.E, 29000 * unyt.ksi)
    assert unyt.allclose_units(material.Fy, 50 * unyt.ksi)
    assert unyt.allclose_units(material.Fu, 65 * unyt.ksi)
    assert unyt.allclose_units(material.Ry, 1.1)
    assert unyt.allclose_units(material.Rt, 1.1)


def test_material_lookup_too_many_results():
    with pytest.raises(ValueError, match=r'^Multiple materials found:\n'):
        steel.SteelMaterial.from_name('A500')


def test_material_lookup_no_results():
    with pytest.raises(ValueError, match=r'^No materials found$'):
        steel.SteelMaterial.from_name('ThisIsNotAMaterial')
