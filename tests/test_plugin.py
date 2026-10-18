"""Packaging-level tests: namespace resolution of both application subpackages.

discopt-apps ships no CLI entry point (the builders are library-only), so there
is nothing in the ``discopt.cli`` group to assert. The packaging contract is
instead that both PEP 420 subpackages merge into the ``discopt`` namespace and
expose their public builders.
"""

import pytest

pytestmark = pytest.mark.smoke


def test_namespace_import():
    import discopt  # noqa: F401
    import discopt.opf
    import discopt.pooling

    # Both plugins merge into the discopt namespace; both must be importable
    # side by side, and the public builder surface must be present.
    assert hasattr(discopt.opf, "build_ac_opf_rectangular")
    assert hasattr(discopt.pooling, "build_pq_formulation")


def test_opf_public_api():
    from discopt.opf import ACOPF, Bus, Line, admittance_matrix, two_bus_example

    assert callable(admittance_matrix)
    assert callable(two_bus_example)
    for cls in (Bus, Line, ACOPF):
        assert isinstance(cls, type)


def test_pooling_public_api():
    from discopt.pooling import (
        Input,
        Output,
        Pool,
        PoolingProblem,
        haverly_hpp1,
    )

    assert callable(haverly_hpp1)
    for cls in (Input, Pool, Output, PoolingProblem):
        assert isinstance(cls, type)


@pytest.mark.parametrize("modname", ["discopt.opf", "discopt.pooling"])
def test_all_names_resolve(modname):
    import importlib

    mod = importlib.import_module(modname)
    missing = [name for name in mod.__all__ if not hasattr(mod, name)]
    assert not missing
