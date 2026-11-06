import pytest

from income_tax import refund_status, tax_due, taxable_income


def test_taxable_income_raises_for_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_taxable_income_new_regime_deduction():
    assert taxable_income(500000, "new", 12345) == 425000


def test_taxable_income_old_regime_caps_investments_above_limit():
    assert taxable_income(700000, "old", 200000) == 500000


def test_taxable_income_old_regime_investments_below_limit_not_capped():
    assert taxable_income(600000, "old", 120000) == 430000


def test_taxable_income_old_regime_investments_exactly_150000_boundary():
    assert taxable_income(700000, "old", 150000) == 500000


def test_taxable_income_unknown_regime_raises():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "legacy", 0)


def test_taxable_income_returns_zero_when_taxable_is_negative():
    assert taxable_income(50000, "new", 0) == 0


def test_taxable_income_returns_zero_when_taxable_is_exactly_zero():
    assert taxable_income(75000, "new", 0) == 0


def test_tax_due_raises_for_negative_taxable():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


def test_tax_due_age_80_boundary_and_above_exemption():
    assert tax_due(600000, 80) == 5000  # (600000 - 500000) * 5% = 100000 * 5% = 5000


def test_tax_due_age_79_boundary_uses_60_to_79_exemption():
    assert tax_due(350000, 79) == 2500  # (350000 - 300000) * 5% = 50000 * 5% = 2500


def test_tax_due_age_60_boundary_uses_60_to_79_exemption():
    assert tax_due(350000, 60) == 2500  # (350000 - 300000) * 5% = 50000 * 5% = 2500


def test_tax_due_age_59_boundary_uses_under_60_exemption():
    assert tax_due(300000, 59) == 2500  # (300000 - 250000) * 5% = 50000 * 5% = 2500


def test_tax_due_taxable_exactly_equal_to_exemption_returns_zero():
    assert tax_due(250000, 30) == 0


def test_tax_due_slab_exactly_250000_boundary():
    assert tax_due(500000, 30) == 12500  # (500000 - 250000) * 5% = 250000 * 5% = 12500


def test_tax_due_slab_above_250000_uses_higher_rate():
    assert tax_due(800000, 30) == 72500  # 12500 + (550000 - 250000) * 20% = 12500 + 60000


def test_refund_status_refund():
    assert refund_status(12000, 10000, True) == "refund"


def test_refund_status_refund_delayed():
    assert refund_status(12000, 10000, False) == "refund delayed"


def test_refund_status_pay_balance():
    assert refund_status(8000, 10000, True) == "pay balance"


def test_refund_status_pay_balance_with_penalty():
    assert refund_status(8000, 10000, False) == "pay balance with penalty"


def test_refund_status_tax_paid_exactly_equals_tax_due():
    assert refund_status(10000, 10000, True) == "settled"
