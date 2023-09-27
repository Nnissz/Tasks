import pytest

from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calculator = Calculator

    def test_adding(self):
        assert self.calculator.adding(self, 1, 1) == 2

    def test_subtraction(self):
        assert self.calculator.subtraction(self, 2, 1) == 1

    def test_division(self):
        assert self.calculator.division(self, 2, 1) == 2

    def test_multiply(self):
        assert self.calculator.multiply(self, 2, 1) == 2

    def test_zero_division(self):
        with pytest.raises(ZeroDivisionError):
            self.calculator.division(self, 1, 0)

    def teardown(self):
        print('Выполнение метода Teardown')