"""Tests for the high-level entry layer (``msentropy.api``).

For valid inputs, the high-level API resolves the method name, validates
common mistakes, normalizes input orientation, and forwards parameters to the
compatibility function without changing the calculation. These tests check:

- structural facts about the registry (20 multiscale methods and parameter
  lists that match the numerical signatures by introspection, so the two
  layers cannot drift apart silently);
- bit-for-bit agreement with the compatibility API on valid inputs;
- readable rejection of invalid high-level inputs.

One deliberate difference from the compatibility API — a ``(N, 1)`` column
input is normalized to the row convention instead of taking the MATLAB
column path — is pinned explicitly in
``test_column_is_normalized_where_the_compatibility_api_differs``.
"""

import inspect

import numpy as np
import pytest

import msentropy
from msentropy import api
from msentropy.core.cmefude import cmefude
from msentropy.core.cmfude import cmfude
from msentropy.core.mde import mde
from msentropy.core.mefude import mefude
from msentropy.core.mfude import mfude
from msentropy.core.mfe_mu import mfe_mu
from msentropy.core.mpe import mpe
from msentropy.core.mslopen import mslopen
from msentropy.core.mse_mu import mse_mu
from msentropy.core.multiscale_attention_entropy import multiscale_attention_entropy
from msentropy.core.rcmde import rcmde
from msentropy.core.rcmefude import rcmefude
from msentropy.core.rcmfude import rcmfude
from msentropy.core.rcmpe import rcmpe
from msentropy.core.rcmslopen import rcmslopen
from msentropy.core.tsmde import tsmde
from msentropy.core.tsmefude import tsmefude
from msentropy.core.tsmfude import tsmfude
from msentropy.core.tsmpe import tsmpe
from msentropy.core.tsmslopen import tsmslopen

# Deterministic signal: no RNG draws inside the assertions, so the file is
# reproducible and the comparison is exact.
SIGNAL = np.random.default_rng(20260911).standard_normal(64)

PAPER_METHODS = (
    "MPE",
    "MSlopEn",
    "MDE",
    "MFuDE",
    "CMFuDE",
    "RCMFuDE",
    "MEFuDE",
    "CMEFuDE",
    "RCMEFuDE",
    "RCMDE",
    "TSMPE",
    "TSMSlopEn",
    "TSMDE",
    "TSMFuDE",
    "TSMEFuDE",
)

ADDITIONAL_METHODS = (
    "MSE",
    "MFE",
    "MAttEn",
    "RCMPE",
    "RCMSlopEn",
)

ALL_METHODS = PAPER_METHODS + ADDITIONAL_METHODS

#: Method -> (API keywords, positional arguments, direct numerical function).
#: Small parameters keep the suite in the millisecond range; the wrapper's
#: arithmetic is independent of the parameter values.
CASE_SPECS = {
    "MPE": (dict(m=3, tau=2, scale=3), (3, 2, 3), mpe),
    "MSlopEn": (dict(m=3, delta=0.1, gamma=1.0, scale=3), (3, 0.1, 1.0, 3), mslopen),
    "MDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3), mde),
    "MFuDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3, 0), mfude),
    "CMFuDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3, 0), cmfude),
    "RCMFuDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3, 0), rcmfude),
    "MEFuDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3, 0), mefude),
    "CMEFuDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3, 0), cmefude),
    "RCMEFuDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3, 0), rcmefude),
    "RCMDE": (dict(m=3, nc=6, tau=2, scale=3), (3, 6, 2, 3), rcmde),
    "TSMPE": (dict(m=3, tau=2, kmax=3), (3, 2, 3), tsmpe),
    "TSMSlopEn": (dict(m=3, delta=0.1, gamma=1.0, kmax=3), (3, 0.1, 1.0, 3), tsmslopen),
    "TSMDE": (dict(m=3, nc=6, tau=2, kmax=3), (3, 6, 2, 3), tsmde),
    "TSMFuDE": (dict(m=3, nc=6, tau=2, kmax=3), (3, 6, 2, 3), tsmfude),
    "TSMEFuDE": (dict(m=3, nc=6, tau=2, kmax=3), (3, 6, 2, 3), tsmefude),
    "MSE": (dict(m=2, r=0.2, tau=1, scale=3), (2, 0.2, 1, 3), mse_mu),
    "MFE": (dict(m=2, r=0.2, n=2.0, tau=1, scale=3), (2, 0.2, 2.0, 1, 3), mfe_mu),
    "MAttEn": (dict(scale=3), (3,), multiscale_attention_entropy),
    "RCMPE": (dict(m=3, tau=2, scale=3), (3, 2, 3), rcmpe),
    "RCMSlopEn": (dict(m=3, delta=0.1, gamma=1.0, scale=3), (3, 0.1, 1.0, 3), rcmslopen),
}

#: The five parameters of the paper's parameter sweep, used by the smoke test.
SWEEP_PARAMS = {
    "MPE": dict(m=3, tau=1, scale=5),
    "MSlopEn": dict(m=3, delta=0.1, gamma=1.0, scale=5),
    "MDE": dict(m=3, nc=6, tau=1, scale=5),
    "MFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "CMFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "RCMFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "MEFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "CMEFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "RCMEFuDE": dict(m=3, nc=6, tau=1, scale=5),
    "RCMDE": dict(m=3, nc=6, tau=1, scale=5),
    "TSMPE": dict(m=3, tau=1, kmax=5),
    "TSMSlopEn": dict(m=3, delta=0.1, gamma=1.0, kmax=5),
    "TSMDE": dict(m=3, nc=6, tau=1, kmax=5),
    "TSMFuDE": dict(m=3, nc=6, tau=1, kmax=5),
    "TSMEFuDE": dict(m=3, nc=6, tau=1, kmax=5),
    "MSE": dict(m=2, r=0.2, tau=1, scale=5),
    "MFE": dict(m=2, r=0.2, n=2.0, tau=1, scale=5),
    "MAttEn": dict(scale=5),
    "RCMPE": dict(m=3, tau=1, scale=5),
    "RCMSlopEn": dict(m=3, delta=0.1, gamma=1.0, scale=5),
}


def _bit_equal(actual: np.ndarray, expected: np.ndarray) -> bool:
    """Exact equality including the sign bit of zeros and NaN positions."""
    return (
        actual.shape == expected.shape
        and np.array_equal(actual, expected, equal_nan=True)
        and np.array_equal(np.signbit(actual), np.signbit(expected))
    )


# --------------------------------------------------------------------------
# Registry structure
# --------------------------------------------------------------------------


def test_registry_holds_all_supported_multiscale_methods():
    assert msentropy.list_methods() == ALL_METHODS
    assert len(msentropy.list_methods()) == 20
    assert set(api.PARAMETERS) == set(ALL_METHODS)


def test_existing_order_is_preserved_and_toolbox_methods_are_appended():
    assert msentropy.list_methods()[:15] == PAPER_METHODS
    assert msentropy.list_methods()[15:] == ADDITIONAL_METHODS


@pytest.mark.parametrize("name", ALL_METHODS)
def test_parameters_match_the_numerical_signature(name):
    """Keep registry parameters aligned with the numerical signature.

    Built by introspection, minus the arguments the API pins (the inert
    ``type_``), with the MATLAB spelling of an aliased argument replaced by
    its canonical API name.
    """
    spec = msentropy.get_method(name)
    direct_names = list(inspect.signature(spec.function).parameters)[1:]
    expected = tuple(
        spec.aliases.get(direct_name, direct_name)
        for direct_name in direct_names
        if direct_name not in spec.fixed
    )
    assert spec.parameters == expected
    assert api.PARAMETERS[name] == expected


@pytest.mark.parametrize("name", ALL_METHODS)
def test_signature_property_documents_the_call(name):
    spec = msentropy.get_method(name)
    text = spec.signature
    assert text.startswith(f"{name}(x, ")
    for parameter in spec.parameters:
        assert parameter in text
    for value in spec.defaults.values():
        assert repr(value) in text


# --------------------------------------------------------------------------
# The wrapper must not change any number
# --------------------------------------------------------------------------


@pytest.mark.parametrize("name", ALL_METHODS)
def test_compute_is_bit_identical_to_the_numerical_function(name):
    """Same value, same shape, same -0 sign bit, same NaN positions."""
    kwargs, args, direct_fn = CASE_SPECS[name]
    api_result = msentropy.compute(name, SIGNAL, **kwargs)
    direct = direct_fn(SIGNAL, *args)
    assert _bit_equal(api_result, direct)


@pytest.mark.parametrize("name", ALL_METHODS)
def test_all_methods_run_on_one_signal(name):
    """Integration smoke test: every method returns a finite curve here."""
    x = np.random.default_rng(7).standard_normal(512)
    out = msentropy.compute(name, x, **SWEEP_PARAMS[name])
    assert out.ndim == 1
    assert out.size == 5
    assert np.all(np.isfinite(out))


@pytest.mark.parametrize("name", ["MFuDE", "CMFuDE", "RCMFuDE"])
def test_type_defaults_to_zero_where_the_reference_reads_it(name):
    kwargs, args, direct_fn = CASE_SPECS[name]
    assert msentropy.get_method(name).defaults == {"type_": 0}
    assert _bit_equal(
        msentropy.compute(name, SIGNAL, **kwargs),
        direct_fn(SIGNAL, *args),  # args end with the explicit type_ = 0
    )


@pytest.mark.parametrize("name", ["MEFuDE", "CMEFuDE", "RCMEFuDE"])
def test_inert_type_parameter_is_fixed_and_explained(name):
    """The ZCJ modification made ``type`` inert; the API pins it at 0."""
    spec = msentropy.get_method(name)
    assert spec.fixed == {"type_": 0}
    assert "type_" not in spec.parameters
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute(name, SIGNAL, **CASE_SPECS[name][0], type_=1)
    message = str(excinfo.value)
    assert "never reads it" in message
    assert "drop the argument" in message


# --------------------------------------------------------------------------
# Method lookup
# --------------------------------------------------------------------------


@pytest.mark.parametrize("spelling", ["mde", "MDE", "Mde", "  mde  "])
def test_lookup_ignores_case_and_surrounding_space(spelling):
    assert msentropy.get_method(spelling).name == "MDE"


def test_compatibility_file_name_resolves_to_the_paper_abbreviation():
    """TSMDisE.m implements the method the paper calls TSMDE (naming ruling)."""
    assert msentropy.get_method("TSMDisE").name == "TSMDE"
    kwargs = CASE_SPECS["TSMDE"][0]
    assert _bit_equal(
        msentropy.compute("TSMDisE", SIGNAL, **kwargs),
        msentropy.compute("TSMDE", SIGNAL, **kwargs),
    )


def test_unknown_method_lists_the_valid_names():
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute("MDA", SIGNAL, m=3, nc=6, tau=1, scale=3)
    message = str(excinfo.value)
    assert "'MDA'" in message
    for name in ALL_METHODS:
        assert name in message


def test_non_string_method_is_rejected():
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute(mde, SIGNAL, m=3, nc=6, tau=1, scale=3)
    assert "must be a string" in str(excinfo.value)


# --------------------------------------------------------------------------
# Parameter validation
# --------------------------------------------------------------------------


def test_unexpected_parameter_is_rejected_with_the_accepted_list():
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute("MDE", SIGNAL, m=3, nc=6, tau=1, scales=3)
    message = str(excinfo.value)
    assert "'scales'" in message
    assert "accepted parameters: m, nc, tau, scale" in message


def test_missing_parameter_is_rejected_with_the_signature():
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute("MDE", SIGNAL, m=3, nc=6, scale=3)
    message = str(excinfo.value)
    assert "missing required parameter(s): tau" in message
    assert "MDE(x, m, nc, tau, scale)" in message


def test_matlab_spelling_of_the_delay_is_accepted_for_mpe():
    """MPE.m names the delay ``t``; the API canonicalizes it to ``tau``."""
    spec = msentropy.get_method("MPE")
    assert spec.aliases == {"t": "tau"}
    assert _bit_equal(
        msentropy.compute("MPE", SIGNAL, m=3, t=2, scale=3),
        msentropy.compute("MPE", SIGNAL, m=3, tau=2, scale=3),
    )


@pytest.mark.parametrize("name", ["MSlopEn", "TSMSlopEn", "RCMSlopEn"])
def test_gamma_is_canonical_and_gama_remains_an_alias(name):
    spec = msentropy.get_method(name)
    assert "gamma" in spec.parameters
    assert "gama" not in spec.parameters
    assert spec.aliases["gama"] == "gamma"

    kwargs = dict(m=3, delta=0.1, scale=3)
    if name == "TSMSlopEn":
        kwargs = dict(m=3, delta=0.1, kmax=3)
    canonical = msentropy.compute(name, SIGNAL, **kwargs, gamma=1.0)
    historical = msentropy.compute(name, SIGNAL, **kwargs, gama=1.0)
    assert _bit_equal(canonical, historical)


def test_gamma_and_gama_cannot_be_passed_together():
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute(
            "MSlopEn",
            SIGNAL,
            m=3,
            delta=0.1,
            gamma=1.0,
            gama=1.0,
            scale=3,
        )
    assert "'gamma' was passed twice" in str(excinfo.value)


def test_parameter_passed_twice_is_rejected():
    """``t`` and ``tau`` are the same parameter for MPE; do not let one win."""
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute("MPE", SIGNAL, m=3, t=2, tau=3, scale=3)
    message = str(excinfo.value)
    assert "'tau' was passed twice" in message
    assert "'t'" in message and "'tau'" in message


def test_input_array_is_not_mutated():
    """The wrapper forwards the caller's array; nothing may write to it."""
    original = SIGNAL.copy()
    msentropy.compute("MDE", SIGNAL, m=3, nc=6, tau=1, scale=3)
    assert np.array_equal(SIGNAL, original)


def test_unknown_parameter_message_mentions_aliases_when_present():
    with pytest.raises(TypeError) as excinfo:
        msentropy.compute("MPE", SIGNAL, m=3, delay=2, scale=3)
    assert "aliases: t" in str(excinfo.value)


# --------------------------------------------------------------------------
# Input normalization
# --------------------------------------------------------------------------


@pytest.mark.parametrize("name", ALL_METHODS)
def test_1d_row_and_column_inputs_agree_through_the_api(name):
    kwargs = CASE_SPECS[name][0]
    flat = msentropy.compute(name, SIGNAL, **kwargs)
    row = msentropy.compute(name, SIGNAL.reshape(1, -1), **kwargs)
    column = msentropy.compute(name, SIGNAL.reshape(-1, 1), **kwargs)
    assert _bit_equal(row, flat)
    assert _bit_equal(column, flat)


@pytest.mark.parametrize("name", ["MEFuDE", "RCMEFuDE"])
def test_column_is_normalized_where_the_compatibility_api_differs(name):
    """The deliberate orientation difference between the two APIs.

    ``mefude``/``rcmefude`` compute a DIFFERENT scale-1 value for a genuine
    (N, 1) input. The high-level API always takes the row-vector path, so it
    must not reproduce that column value; the compatibility API retains it.
    """
    kwargs, args, direct_fn = CASE_SPECS[name]
    column = SIGNAL.reshape(-1, 1)
    assert not _bit_equal(direct_fn(column, *args), direct_fn(SIGNAL, *args))
    assert _bit_equal(
        msentropy.compute(name, column, **kwargs), direct_fn(SIGNAL, *args)
    )


def test_matrix_input_is_rejected():
    matrix = np.arange(6, dtype=float).reshape(2, 3)
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute("MDE", matrix, m=3, nc=6, tau=1, scale=3)
    message = str(excinfo.value)
    assert "vector-shaped 2-D array" in message
    assert "(2, 3)" in message


def test_scalar_input_is_rejected():
    with pytest.raises(ValueError) as excinfo:
        api.as_signal(1.0)
    assert "got a scalar" in str(excinfo.value)


def test_non_real_input_is_rejected():
    with pytest.raises(TypeError) as excinfo:
        api.as_signal(np.array([1.0 + 2.0j, 3.0 + 0.0j]))
    assert "must be real numbers" in str(excinfo.value)


def test_as_signal_returns_a_contiguous_float64_1d_array():
    out = api.as_signal([[1, 2, 3, 4]])
    assert out.dtype == np.float64
    assert out.ndim == 1
    assert out.flags["C_CONTIGUOUS"]
    assert out.tolist() == [1.0, 2.0, 3.0, 4.0]
    assert api.as_signal([1, 2, 3]).tolist() == [1.0, 2.0, 3.0]  # lists accepted


def test_as_signal_does_not_silently_clean_nan():
    """Normalization itself never changes a sample value."""
    assert np.isnan(api.as_signal([1.0, np.nan, 3.0])[1])


# --------------------------------------------------------------------------
# High-level safety checks
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "kwargs", "parameter"),
    [
        ("MPE", dict(m=True, tau=1, scale=3), "m"),
        ("MPE", dict(m=3.0, tau=1, scale=3), "m"),
        ("MPE", dict(m=1, tau=1, scale=3), "m"),
        ("MDE", dict(m=3, nc=1, tau=1, scale=3), "nc"),
        ("MDE", dict(m=3, nc=6, tau=0, scale=3), "tau"),
        ("MDE", dict(m=3, nc=6, tau=1, scale=0), "scale"),
        ("TSMDE", dict(m=3, nc=6, tau=1, kmax=0), "kmax"),
        ("MSlopEn", dict(m=3, delta=-0.1, gamma=1.0, scale=3), "delta"),
        ("MSlopEn", dict(m=3, delta=0.2, gamma=0.1, scale=3), "gamma"),
        ("RCMSlopEn", dict(m=6, delta=0.1, gamma=1.0, scale=3), "m"),
        ("MSE", dict(m=2, r=0.0, tau=1, scale=3), "r"),
        ("MFE", dict(m=2, r=0.2, n=0.0, tau=1, scale=3), "n"),
    ],
)
def test_invalid_parameter_values_are_rejected(name, kwargs, parameter):
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute(name, SIGNAL, **kwargs)
    assert parameter in str(excinfo.value)


@pytest.mark.parametrize("bad_sample", [np.nan, np.inf, -np.inf])
def test_nonfinite_samples_are_rejected_by_compute(bad_sample):
    signal = SIGNAL.copy()
    signal[5] = bad_sample
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute("MDE", signal, m=3, nc=6, tau=1, scale=3)
    assert "NaN or infinite" in str(excinfo.value)


def test_empty_signal_is_rejected_by_compute():
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute("MDE", [], m=3, nc=6, tau=1, scale=3)
    assert "at least one sample" in str(excinfo.value)


def test_largest_scale_must_leave_a_complete_embedding_window():
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute("MDE", SIGNAL, m=3, nc=6, tau=2, scale=16)
    message = str(excinfo.value)
    assert "scale=16" in message
    assert "longer signal" in message


def test_attention_entropy_scale_must_leave_three_samples():
    with pytest.raises(ValueError) as excinfo:
        msentropy.compute("MAttEn", SIGNAL, scale=32)
    assert "at least 3 samples" in str(excinfo.value)


def test_compatibility_functions_retain_degenerate_scale_behavior():
    assert mpe(SIGNAL, 3, 1, 0).shape == (0,)
    direct = mefude(SIGNAL, 3, 6, 1, 0, 0)
    assert direct.shape == (1,)
    assert np.isfinite(direct[0])


def test_output_is_always_a_1d_float64_ndarray():
    for name in ("MDE", "TSMEFuDE", "MSE", "MAttEn"):
        out = msentropy.compute(name, SIGNAL, **CASE_SPECS[name][0])
        assert isinstance(out, np.ndarray)
        assert out.ndim == 1
        assert out.dtype == np.float64


# --------------------------------------------------------------------------
# The package-level re-exports
# --------------------------------------------------------------------------


def test_package_exports_both_layers():
    """Top level exports registry helpers plus direct compatibility functions."""
    for name in ("compute", "list_methods", "get_method", "as_signal", "PARAMETERS"):
        assert name in msentropy.__all__
    for method_name in ALL_METHODS:
        spec = msentropy.get_method(method_name)
        function_name = spec.function.__name__
        assert function_name in msentropy.__all__
        assert getattr(msentropy, function_name) is spec.function


def test_numerical_functions_are_re_exported_unchanged():
    """``msentropy.mde`` is the numerical function, not an API wrapper."""
    assert msentropy.mde is mde
    assert msentropy.tsmslopen is tsmslopen
