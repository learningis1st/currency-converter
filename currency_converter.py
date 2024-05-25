import tkinter as tk
from tkinter import ttk
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.minsize(250, 150)
        self.root.resizable(False, False)

        # Initial conversion rates placeholder
        self.conversion_rates = {}

        self.setup_ui()
        self.update_conversion_rates()

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

        currency_options = ["USD", "EUR", "JPY", "GBP", "CHF", "CAD", "AUD", "CNY"]

        ttk.Label(self.root, text="From").grid(column=0, row=0, padx=5, pady=5)
        self.from_currency_var = tk.StringVar(value="USD")
        ttk.OptionMenu(self.root, self.from_currency_var, "USD", *currency_options, command=self.update_rate_label).grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(self.root, text="To").grid(column=0, row=1, padx=5, pady=5)
        self.to_currency_var = tk.StringVar(value="CNY")
        ttk.OptionMenu(self.root, self.to_currency_var, "CNY", *currency_options, command=self.update_rate_label).grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(self.root, text="Amount").grid(column=0, row=2, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_var.trace_add("write", self.convert_currency)
        ttk.Entry(self.root, textvariable=self.amount_var).grid(column=1, row=2, padx=5, pady=5)

        ttk.Label(self.root, text="Result").grid(column=0, row=3, padx=5, pady=5)
        self.result_var = tk.StringVar(value="")
        ttk.Label(self.root, textvariable=self.result_var).grid(column=1, row=3, padx=5, pady=5)

        self.rate_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.rate_var).grid(column=0, row=4, columnspan=2, pady=10)
        self.rate_var.set("Fetching conversion rates...")

    def get_conversion_rates(self):
        api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            return data["rates"]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching conversion rates: {e}")
            return None

    def update_conversion_rates(self):
        rates = self.get_conversion_rates()
        if rates:
            self.conversion_rates = rates
            self.update_rate_label()
        else:
            self.rate_var.set("Failed to fetch rates")

    def update_rate_label(self, *args):
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()
        if from_currency and to_currency and from_currency in self.conversion_rates and to_currency in self.conversion_rates:
            rate = self.conversion_rates[to_currency] / self.conversion_rates[from_currency]
            self.rate_var.set(f"1 {from_currency} = {rate:.2f} {to_currency}")
        else:
            self.rate_var.set("Invalid currency selection")
        self.convert_currency()

    def convert_currency(self, *args):
        try:
            from_currency = self.from_currency_var.get()
            to_currency = self.to_currency_var.get()
            amount = self.amount_var.get()
            if from_currency and to_currency and from_currency in self.conversion_rates and to_currency in self.conversion_rates:
                if amount:
                    rate = self.conversion_rates[to_currency] / self.conversion_rates[from_currency]
                    amount_float = float(amount)
                    converted_amount = amount_float * rate
                    self.result_var.set(f"{converted_amount:.2f} {to_currency}")
                else:
                    self.result_var.set("")
            else:
                self.result_var.set("Invalid currency selection")
        except ValueError:
            self.result_var.set("Invalid Input")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
