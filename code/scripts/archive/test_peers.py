import yfinance as yf
import pandas as pd

peers = ["ICBP.JK", "MYOR.JK", "UNVR.JK", "INDF.JK", "CMRY.JK"]

peer_stats = []
for ticker_sym in peers:
    t = yf.Ticker(ticker_sym)
    info = t.info
    print(f"\n--- {ticker_sym} ---")
    print("Short name:", info.get("shortName"))
    print("Market Cap:", info.get("marketCap"))
    print("Trailing PE:", info.get("trailingPE"))
    print("Price to Book:", info.get("priceToBook"))
    print("EV/EBITDA:", info.get("enterpriseToEbitda"))
    print("EV/Revenue:", info.get("enterpriseToRevenue"))
    print("Dividend Yield:", info.get("dividendYield"))
    print("Total Revenue:", info.get("totalRevenue"))
    print("Gross Margins:", info.get("grossMargins"))
    print("Operating Margins:", info.get("operatingMargins"))
    print("Profit Margins:", info.get("profitMargins"))
    print("ROE:", info.get("returnOnEquity"))
    print("Debt to Equity:", info.get("debtToEquity"))
