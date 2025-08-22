# Crypto Price Fetcher from Binance API

Python script that retrieves historical cryptocurrency prices from the Binance API and populates an Excel file with the corresponding values.

## 📋 Description

This script reads an Excel file (`data.xlsx`) containing cryptocurrency transactions and uses the Binance API to:
- Obtain the historical price of each cryptocurrency on the specified date
- Calculate the value in USDT for each transaction
- Generate summaries of quantities and values
- Save the results in a new Excel file

## 🚀 Features

- ✅ Queries the official Binance API
- ✅ Automatically adjusts to California time (PST/PDT)
- ✅ Robust error and exception handling
- ✅ Preserves the original Excel format
- ✅ Generates report with totals and summary

## 📊 Input Excel File Structure

The `data.xlsx` file must have the following columns:
- `crypto`: Cryptocurrency symbol (e.g., ETH, BTC, ADA)
- `Quantity`: Amount of the cryptocurrency
- `Date`: Transaction date (format YYYY-MM-DD HH:MM:SS)
- `Crypto Value (USDT)`: (Empty - will be filled automatically)
- `Quantity Value (USDT)`: (Empty - will be filled automatically)

## 📦 Installation

1. Clone or download the repository
2. Install the dependencies:

```bash
pip install -r requirements.txt
