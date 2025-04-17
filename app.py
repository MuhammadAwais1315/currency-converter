# app.py (Enhanced Version)
import os
import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
import ssl
import certifi
from datetime import datetime

class CurrencyConverter:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.rates = self.fetch_rates()
        
    def setup_ui(self):
        self.root.title("💰 Ultra Currency Converter")
        self.root.geometry("500x450")
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f5')
        
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with icon
        ttk.Label(main_frame, 
                 text="💱 Currency Converter Pro",
                 font=('Helvetica', 16, 'bold'),
                 foreground='#2c3e50').pack(pady=10)
        
        # Conversion UI elements
        self.create_conversion_widgets(main_frame)
        
    def create_conversion_widgets(self, parent):
        # Amount entry
        ttk.Label(parent, text="Amount:").pack(anchor=tk.W)
        self.amount_entry = ttk.Entry(parent, font=('Arial', 12))
        self.amount_entry.pack(fill=tk.X, pady=5)
        
        # Currency selection
        currency_frame = ttk.Frame(parent)
        currency_frame.pack(fill=tk.X, pady=10)
        
        # From currency
        from_frame = ttk.Frame(currency_frame)
        from_frame.pack(side=tk.LEFT, expand=True)
        ttk.Label(from_frame, text="From:").pack(anchor=tk.W)
        self.from_currency = ttk.Combobox(from_frame, state="readonly")
        self.from_currency.pack(fill=tk.X)
        
        # Swap button
        swap_btn = ttk.Button(currency_frame, text="⇄", width=3, 
                             command=self.swap_currencies)
        swap_btn.pack(side=tk.LEFT, padx=10, pady=15)
        
        # To currency
        to_frame = ttk.Frame(currency_frame)
        to_frame.pack(side=tk.LEFT, expand=True)
        ttk.Label(to_frame, text="To:").pack(anchor=tk.W)
        self.to_currency = ttk.Combobox(to_frame, state="readonly")
        self.to_currency.pack(fill=tk.X)
        
        # Convert button
        ttk.Button(parent, text="CONVERT", 
                  command=self.convert).pack(pady=20, ipadx=20, ipady=5)
        
        # Result display
        self.result_label = ttk.Label(parent, 
                                    font=('Helvetica', 14, 'bold'),
                                    foreground='#27ae60')
        self.result_label.pack()
        
    def fetch_rates(self):
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(
                "https://v6.exchangerate-api.com/v6/" + 
                os.getenv("API_KEY", "82706646934f3fc39c5f6415") + 
                "/latest/USD", 
                context=context
            ) as response:
                data = json.loads(response.read().decode())
                rates = data.get('conversion_rates', {'USD': 1.0})
                currencies = sorted(rates.keys())
                self.from_currency['values'] = currencies
                self.to_currency['values'] = currencies
                self.from_currency.current(currencies.index('USD'))
                self.to_currency.current(currencies.index('EUR') if 'EUR' in currencies else 0)
                return rates
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch rates: {str(e)}")
            return {'USD': 1.0}

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
            from_cur = self.from_currency.get()
            to_cur = self.to_currency.get()
            
            if from_cur == to_cur:
                messagebox.showwarning("Warning", "Select different currencies!")
                return
                
            rate = self.rates[to_cur] / self.rates[from_cur]
            result = amount * rate
            self.result_label.config(
                text=f"➤ {amount:.2f} {from_cur} = {result:.2f} {to_cur}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Invalid conversion: {str(e)}")

    def swap_currencies(self):
        from_idx = self.from_currency.current()
        to_idx = self.to_currency.current()
        self.from_currency.current(to_idx)
        self.to_currency.current(from_idx)

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverter(root)
    root.mainloop()