import pytest
from app import CurrencyConverter
import tkinter as tk
import os


class TestCurrencyConverter:
    @pytest.fixture
    def app(self):
        os.environ['DISPLAY'] = ':99'  # Critical for CI environments
        root = tk.Tk()
        root.withdraw()  # Prevent GUI window from appearing
        app = CurrencyConverter(root)
        yield app
        root.destroy()

    def test_initial_rates(self, app):
        """Test that rates are loaded and USD exists"""
        assert isinstance(app.rates, dict)
        assert 'USD' in app.rates
        assert isinstance(app.rates['USD'], (int, float))
        assert app.rates['USD'] > 0

    def test_mock_rates(self, monkeypatch):
        """Test with mocked API response"""
        def mock_fetch_rates(self):
            return {'USD': 1.0, 'EUR': 0.85}

        monkeypatch.setattr(CurrencyConverter, 'fetch_rates', mock_fetch_rates)

        root = tk.Tk()
        root.withdraw()
        app = CurrencyConverter(root)
        assert app.rates['EUR'] == 0.85
        root.destroy()
