import string

from hypothesis import given, settings, strategies as st
from income_tax_parser import clean_pan, parse_amount, parse_tax_slab

fuzz_values = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(),
    st.binary(),
    st.lists(st.text()),
)


@settings(max_examples=500)
@given(fuzz_values)
def test_clean_pan_no_crash(s):
    try:
        result = clean_pan(s)
    except Exception as e:
        assert False, f"clean_pan crashed with: {e!r}"
    assert result is None or isinstance(result, str)


@settings(max_examples=500)
@given(fuzz_values)
def test_parse_amount_no_crash(s):
    try:
        result = parse_amount(s)
    except Exception as e:
        assert False, f"parse_amount crashed with: {e!r}"
    assert result is None or isinstance(result, int)


@settings(max_examples=500)
@given(fuzz_values)
def test_parse_tax_slab_no_crash(s):
    try:
        result = parse_tax_slab(s)
    except Exception as e:
        assert False, f"parse_tax_slab crashed with: {e!r}"
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 3
        and all(isinstance(x, int) for x in result)
    )


@st.composite
def pan_with_random_spaces(draw):
    first = draw(st.text(alphabet=string.ascii_letters, min_size=5, max_size=5))
    middle = draw(st.text(alphabet=string.digits, min_size=4, max_size=4))
    last = draw(st.text(alphabet=string.ascii_letters, min_size=1, max_size=1))
    core = first + middle + last
    spaced = [draw(st.text(alphabet=" ", min_size=0, max_size=2))]
    for ch in core:
        if ch.isalpha():
            ch = draw(st.sampled_from((ch.lower(), ch.upper())))
        spaced.append(ch)
        spaced.append(draw(st.text(alphabet=" ", min_size=0, max_size=2)))
    return "".join(spaced), core.upper()


@settings(max_examples=500)
@given(pan_with_random_spaces())
def test_clean_pan_valid(value):
    pan_input, expected = value
    assert clean_pan(pan_input) == expected


@settings(max_examples=500)
@given(st.integers(min_value=0, max_value=10**12))
def test_parse_amount_valid(n):
    text = "Rs " + f"{n:,}"
    assert parse_amount(text) == n


@settings(max_examples=500)
@given(
    st.integers(min_value=0, max_value=10**9),
    st.integers(min_value=0, max_value=10**9),
    st.integers(min_value=0, max_value=100),
)
def test_parse_tax_slab_valid(low, high, rate):
    if low > high:
        low, high = high, low
    text = f"{low}-{high}:{rate}"
    assert parse_tax_slab(text) == (low, high, rate)


def test_clean_pan_rejects_non_ascii_letters():
    # "ı".upper() == "I", so this must be rejected before upper-casing
    assert clean_pan("abcdı1234f") is None
