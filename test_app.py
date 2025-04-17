import pytest
from app import CurrencyConverter
import tkinter as tk


class TestCurrencyConverter:
    @pytest.fixture
    def app(self):
        root = tk.Tk()
        root.withdraw()  # Hide GUI window during tests
        yield CurrencyConverter(root)
        root.destroy()

    def test_initial_rates(self, app):
        assert 'USD' in app.rates
        assert isinstance(app.rates['USD'], (int, float))  # Accepts either type
