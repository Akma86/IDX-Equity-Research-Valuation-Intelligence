import sys
print("Python:", sys.version)

packages = ['pandas', 'numpy', 'yfinance', 'requests', 'bs4', 'openpyxl', 'matplotlib', 'seaborn', 'lxml']
for pkg in packages:
    try:
        m = __import__(pkg)
        ver = getattr(m, '__version__', 'unknown')
        print(f"{pkg}: OK ({ver})")
    except ImportError:
        print(f"{pkg}: MISSING")
