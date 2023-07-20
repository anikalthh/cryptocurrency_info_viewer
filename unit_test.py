import unittest
import tkinter as tk
from main import CryptocurrencyInfoViewer 
import datetime as dt
import pandas as pd

class TestCryptocurrencyInfoViewer(unittest.TestCase):

    def setUp(self):
        # Create a test root window and initialize the CryptocurrencyInfoViewer
        self.root = tk.Tk()
        self.app = CryptocurrencyInfoViewer(self.root)

    def tearDown(self):
        # Destroy the test root window after each test
        self.root.destroy()

    def test_get_info(self):
        # Test if get_info returns a DataFrame when valid crypto currency is selected
        for i in range(4):
            self.app.crypto_entry.selection_set(i)  # Select the first item
            df = self.app.get_info()
            self.assertIsInstance(df, pd.DataFrame)

        # Test if get_info returns None when no crypto currency is selected
        self.app.crypto_entry.selection_clear(0, tk.END)  # Deselect all items
        df = self.app.get_info()
        self.assertIsNone(df)

    def test_validate_dates(self):
        # Test if validate_dates returns True for valid dates
        start = pd.Timestamp("2023-07-01").timestamp()
        end = pd.Timestamp("2023-07-10").timestamp()
        self.assertTrue(self.app.validate_dates(start, end))

        # Test if validate_dates returns False for end date earlier than start date
        start = pd.Timestamp("2023-07-10").timestamp()
        end = pd.Timestamp("2023-07-01").timestamp()
        self.assertFalse(self.app.validate_dates(start, end))

        # Test if validate_dates returns False for end date in the future
        start = pd.Timestamp("2023-07-01").timestamp()
        end = pd.Timestamp("2025-07-01").timestamp()
        self.assertFalse(self.app.validate_dates(start, end))

if __name__ == "__main__":
    unittest.main()
