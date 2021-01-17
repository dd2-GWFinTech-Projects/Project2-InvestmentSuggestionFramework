from unittest import TestCase

from lib.valuation.ValuationCalculator import ValuationCalculator


class TestValuationCalculator(TestCase):

    def test_compute_value__dcf(self):
        valuation_calculator = ValuationCalculator()
        npv_actual = valuation_calculator.compute_value__dcf(
            ebitda_projection=[-645000.00, 189430.00, 183115.00, 187266.00, 191375.00, 195432.00, 199427.00,
                               203348.00, 207184.00, 210923.00, 214550.00],
            wacc=0.08)
        npv_expected = 621178.98
        self.assertAlmostEqual(npv_expected, npv_actual, 1)


class TestValuationCalculator(TestCase):
    def test_compute_value_list(self):
        self.fail()
