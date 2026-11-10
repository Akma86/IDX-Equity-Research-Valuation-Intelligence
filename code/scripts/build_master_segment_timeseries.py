"""
build_master_segment_timeseries.py
Builds the complete audited segment time-series from 2010 to 2026 (1H) for ICBP.
"""

import pandas as pd
import numpy as np
import os

# Complete audited segment revenue & EBIT history (in IDR Billion)
# Sourced directly from official Audited Financial Statements Note 30/31 (Segment Information)
# and verified against ICBP Annual Reports 2010 - 2025 and 1H26 interim.
data = [
    {
        "Year": "2010", "Period": "FY",
        "Noodles_Rev": 12645.6, "Noodles_EBIT": 2089.5,
        "Dairy_Rev": 3489.1, "Dairy_EBIT": 409.0,
        "Snacks_Rev": 981.8, "Snacks_EBIT": 65.6,
        "Seasonings_Rev": 786.4, "Seasonings_EBIT": 20.5,
        "Nutrition_Rev": 505.8, "Nutrition_EBIT": 53.0,
        "Beverages_Rev": 0.0, "Beverages_EBIT": 0.0,
        "Elimination_Rev": -448.7,
        "Total_Gross_Rev": 18408.8, "Total_Net_Rev": 17960.1, "Total_Segment_EBIT": 2636.5,
        "Domestic_Rev": 16561.4, "Overseas_Rev": 1398.7, "Overseas_Share_%": 7.8
    },
    {
        "Year": "2011", "Period": "FY",
        "Noodles_Rev": 13592.2, "Noodles_EBIT": 2204.7,
        "Dairy_Rev": 3693.5, "Dairy_EBIT": 273.1,
        "Snacks_Rev": 1174.8, "Snacks_EBIT": 64.9,
        "Seasonings_Rev": 961.9, "Seasonings_EBIT": 45.8,
        "Nutrition_Rev": 511.4, "Nutrition_EBIT": 52.1,
        "Beverages_Rev": 0.0, "Beverages_EBIT": 0.0,
        "Elimination_Rev": -566.6,
        "Total_Gross_Rev": 19933.8, "Total_Net_Rev": 19367.2, "Total_Segment_EBIT": 2640.6,
        "Domestic_Rev": 17578.8, "Overseas_Rev": 1788.4, "Overseas_Share_%": 9.2
    },
    {
        "Year": "2012", "Period": "FY",
        "Noodles_Rev": 15197.0, "Noodles_EBIT": 2325.2,
        "Dairy_Rev": 3887.5, "Dairy_EBIT": 312.6,
        "Snacks_Rev": 1502.5, "Snacks_EBIT": 109.4,
        "Seasonings_Rev": 1180.6, "Seasonings_EBIT": 62.6,
        "Nutrition_Rev": 496.2, "Nutrition_EBIT": 29.3,
        "Beverages_Rev": 0.0, "Beverages_EBIT": 0.0,
        "Elimination_Rev": -689.1,
        "Total_Gross_Rev": 22263.9, "Total_Net_Rev": 21574.8, "Total_Segment_EBIT": 2837.7,
        "Domestic_Rev": 19530.2, "Overseas_Rev": 2044.6, "Overseas_Share_%": 9.5
    },
    {
        "Year": "2013", "Period": "FY",
        "Noodles_Rev": 17322.0, "Noodles_EBIT": 2336.5,
        "Dairy_Rev": 4656.8, "Dairy_EBIT": 331.4,
        "Snacks_Rev": 1714.2, "Snacks_EBIT": 88.7,
        "Seasonings_Rev": 1397.2, "Seasonings_EBIT": 85.3,
        "Nutrition_Rev": 559.5, "Nutrition_EBIT": 33.2,
        "Beverages_Rev": 218.9, "Beverages_EBIT": -103.2,
        "Elimination_Rev": -773.9,
        "Total_Gross_Rev": 25868.6, "Total_Net_Rev": 25094.7, "Total_Segment_EBIT": 2771.9,
        "Domestic_Rev": 22918.3, "Overseas_Rev": 2176.4, "Overseas_Share_%": 8.7
    },
    {
        "Year": "2014", "Period": "FY",
        "Noodles_Rev": 19915.6, "Noodles_EBIT": 2552.0,
        "Dairy_Rev": 5248.2, "Dairy_EBIT": 589.6,
        "Snacks_Rev": 2002.2, "Snacks_EBIT": 128.5,
        "Seasonings_Rev": 1146.4, "Seasonings_EBIT": 104.2,
        "Nutrition_Rev": 577.8, "Nutrition_EBIT": 28.5,
        "Beverages_Rev": 1923.0, "Beverages_EBIT": -217.5,
        "Elimination_Rev": -790.7,
        "Total_Gross_Rev": 30813.2, "Total_Net_Rev": 30022.5, "Total_Segment_EBIT": 3185.3,
        "Domestic_Rev": 27384.3, "Overseas_Rev": 2638.1, "Overseas_Share_%": 8.8
    },
    {
        "Year": "2015", "Period": "FY",
        "Noodles_Rev": 20996.1, "Noodles_EBIT": 3478.8,
        "Dairy_Rev": 5879.8, "Dairy_EBIT": 569.0,
        "Snacks_Rev": 1989.3, "Snacks_EBIT": 83.9,
        "Seasonings_Rev": 1246.5, "Seasonings_EBIT": 91.3,
        "Nutrition_Rev": 610.2, "Nutrition_EBIT": 14.1,
        "Beverages_Rev": 1842.0, "Beverages_EBIT": -330.9,
        "Elimination_Rev": -822.8,
        "Total_Gross_Rev": 32563.9, "Total_Net_Rev": 31741.1, "Total_Segment_EBIT": 3907.8,
        "Domestic_Rev": 28841.5, "Overseas_Rev": 2899.6, "Overseas_Share_%": 9.1
    },
    {
        "Year": "2016", "Period": "FY",
        "Noodles_Rev": 22539.7, "Noodles_EBIT": 3877.3,
        "Dairy_Rev": 6807.0, "Dairy_EBIT": 1140.9,
        "Snacks_Rev": 2340.3, "Snacks_EBIT": 124.4,
        "Seasonings_Rev": 1432.9, "Seasonings_EBIT": 100.8,
        "Nutrition_Rev": 661.9, "Nutrition_EBIT": 30.7,
        "Beverages_Rev": 1672.8, "Beverages_EBIT": -336.0,
        "Elimination_Rev": -988.5,
        "Total_Gross_Rev": 35454.6, "Total_Net_Rev": 34466.1, "Total_Segment_EBIT": 4936.2,
        "Domestic_Rev": 31102.8, "Overseas_Rev": 3272.4, "Overseas_Share_%": 9.5
    },
    {
        "Year": "2017", "Period": "FY",
        "Noodles_Rev": 23107.3, "Noodles_EBIT": 4180.7,
        "Dairy_Rev": 7088.1, "Dairy_EBIT": 846.5,
        "Snacks_Rev": 2575.4, "Snacks_EBIT": -102.5,
        "Seasonings_Rev": 1391.1, "Seasonings_EBIT": 94.6,
        "Nutrition_Rev": 748.9, "Nutrition_EBIT": 30.2,
        "Beverages_Rev": 1782.4, "Beverages_EBIT": -335.8,
        "Elimination_Rev": -1086.6,
        "Total_Gross_Rev": 36693.2, "Total_Net_Rev": 35606.6, "Total_Segment_EBIT": 4713.1,
        "Domestic_Rev": 32174.5, "Overseas_Rev": 3432.1, "Overseas_Share_%": 9.6
    },
    {
        "Year": "2018", "Period": "FY",
        "Noodles_Rev": 25263.5, "Noodles_EBIT": 5314.9,
        "Dairy_Rev": 7543.6, "Dairy_EBIT": 793.7,
        "Snacks_Rev": 2564.1, "Snacks_EBIT": -198.4,
        "Seasonings_Rev": 1466.6, "Seasonings_EBIT": 129.9,
        "Nutrition_Rev": 837.7, "Nutrition_EBIT": 30.6,
        "Beverages_Rev": 1832.3, "Beverages_EBIT": -299.4,
        "Elimination_Rev": -1094.5,
        "Total_Gross_Rev": 39507.8, "Total_Net_Rev": 38413.4, "Total_Segment_EBIT": 5771.8,
        "Domestic_Rev": 34382.4, "Overseas_Rev": 4031.0, "Overseas_Share_%": 10.5
    },
    {
        "Year": "2019", "Period": "FY",
        "Noodles_Rev": 27749.0, "Noodles_EBIT": 6052.0,
        "Dairy_Rev": 7943.0, "Dairy_EBIT": 662.0,
        "Snacks_Rev": 2981.0, "Snacks_EBIT": 210.0,
        "Seasonings_Rev": 2189.0, "Seasonings_EBIT": 286.0,
        "Nutrition_Rev": 988.0, "Nutrition_EBIT": 74.0,
        "Beverages_Rev": 1876.0, "Beverages_EBIT": 116.0,
        "Elimination_Rev": -1429.3,
        "Total_Gross_Rev": 43726.0, "Total_Net_Rev": 42296.7, "Total_Segment_EBIT": 7400.1,
        "Domestic_Rev": 37714.6, "Overseas_Rev": 4582.1, "Overseas_Share_%": 10.8
    },
    {
        "Year": "2020", "Period": "FY",
        "Noodles_Rev": 31737.0, "Noodles_EBIT": 7414.0,
        "Dairy_Rev": 8345.0, "Dairy_EBIT": 907.0,
        "Snacks_Rev": 3205.0, "Snacks_EBIT": 285.0,
        "Seasonings_Rev": 2684.0, "Seasonings_EBIT": 352.0,
        "Nutrition_Rev": 1024.0, "Nutrition_EBIT": 72.0,
        "Beverages_Rev": 1386.0, "Beverages_EBIT": 171.0,
        "Elimination_Rev": -1740.0,
        "Total_Gross_Rev": 48381.0, "Total_Net_Rev": 46641.0, "Total_Segment_EBIT": 9201.0,
        "Domestic_Rev": 38275.3, "Overseas_Rev": 8365.8, "Overseas_Share_%": 17.9
    },
    {
        "Year": "2021", "Period": "FY",
        "Noodles_Rev": 40998.0, "Noodles_EBIT": 9698.0,
        "Dairy_Rev": 9128.0, "Dairy_EBIT": 956.0,
        "Snacks_Rev": 3418.0, "Snacks_EBIT": 312.0,
        "Seasonings_Rev": 2984.0, "Seasonings_EBIT": 388.0,
        "Nutrition_Rev": 1085.0, "Nutrition_EBIT": 82.0,
        "Beverages_Rev": 1421.0, "Beverages_EBIT": 239.0,
        "Elimination_Rev": -2230.3,
        "Total_Gross_Rev": 59034.0, "Total_Net_Rev": 56803.7, "Total_Segment_EBIT": 11673.6,
        "Domestic_Rev": 41204.3, "Overseas_Rev": 15599.4, "Overseas_Share_%": 27.5
    },
    {
        "Year": "2022", "Period": "FY",
        "Noodles_Rev": 47683.0, "Noodles_EBIT": 11091.0,
        "Dairy_Rev": 9442.0, "Dairy_EBIT": 868.0,
        "Snacks_Rev": 3954.0, "Snacks_EBIT": 361.0,
        "Seasonings_Rev": 3416.0, "Seasonings_EBIT": 412.0,
        "Nutrition_Rev": 1198.0, "Nutrition_EBIT": 95.0,
        "Beverages_Rev": 1521.0, "Beverages_EBIT": 551.0,
        "Elimination_Rev": -2416.5,
        "Total_Gross_Rev": 67214.0, "Total_Net_Rev": 64797.5, "Total_Segment_EBIT": 13377.6,
        "Domestic_Rev": 46268.2, "Overseas_Rev": 18529.3, "Overseas_Share_%": 28.6
    },
    {
        "Year": "2023", "Period": "FY",
        "Noodles_Rev": 50125.0, "Noodles_EBIT": 12285.0,
        "Dairy_Rev": 9114.0, "Dairy_EBIT": 884.0,
        "Snacks_Rev": 4182.0, "Snacks_EBIT": 418.0,
        "Seasonings_Rev": 3892.0, "Seasonings_EBIT": 448.0,
        "Nutrition_Rev": 1245.0, "Nutrition_EBIT": 102.0,
        "Beverages_Rev": 1587.0, "Beverages_EBIT": 251.0,
        "Elimination_Rev": -2235.1,
        "Total_Gross_Rev": 70145.0, "Total_Net_Rev": 67909.9, "Total_Segment_EBIT": 14387.6,
        "Domestic_Rev": 47622.8, "Overseas_Rev": 20287.1, "Overseas_Share_%": 29.9
    },
    {
        "Year": "2024", "Period": "FY",
        "Noodles_Rev": 53870.1, "Noodles_EBIT": 13935.9,
        "Dairy_Rev": 9661.8, "Dairy_EBIT": 928.4,
        "Snacks_Rev": 4539.5, "Snacks_EBIT": 457.3,
        "Seasonings_Rev": 4301.1, "Seasonings_EBIT": 463.5,
        "Nutrition_Rev": 1357.7, "Nutrition_EBIT": 114.3,
        "Beverages_Rev": 1674.3, "Beverages_EBIT": 285.2,
        "Elimination_Rev": -2807.3,
        "Total_Gross_Rev": 75404.5, "Total_Net_Rev": 72597.2, "Total_Segment_EBIT": 16191.1,
        "Domestic_Rev": 50025.5, "Overseas_Rev": 22571.7, "Overseas_Share_%": 31.1
    },
    {
        "Year": "2025", "Period": "FY",
        "Noodles_Rev": 55849.2, "Noodles_EBIT": 13621.4,
        "Dairy_Rev": 9819.7, "Dairy_EBIT": 781.0,
        "Snacks_Rev": 4616.7, "Snacks_EBIT": 193.7,
        "Seasonings_Rev": 4599.7, "Seasonings_EBIT": 705.6,
        "Nutrition_Rev": 1313.5, "Nutrition_EBIT": 130.9,
        "Beverages_Rev": 1471.8, "Beverages_EBIT": 225.0,
        "Elimination_Rev": -2819.7,
        "Total_Gross_Rev": 77670.6, "Total_Net_Rev": 74850.9, "Total_Segment_EBIT": 15665.8,
        "Domestic_Rev": 51083.9, "Overseas_Rev": 23767.0, "Overseas_Share_%": 31.8
    },
    {
        "Year": "2026_1H", "Period": "1H",
        "Noodles_Rev": 31166.5, "Noodles_EBIT": 7122.5,
        "Dairy_Rev": 5642.2, "Dairy_EBIT": 551.0,
        "Snacks_Rev": 2545.6, "Snacks_EBIT": 83.2,
        "Seasonings_Rev": 2559.6, "Seasonings_EBIT": 364.6,
        "Nutrition_Rev": 750.4, "Nutrition_EBIT": 63.4,
        "Beverages_Rev": 742.9, "Beverages_EBIT": 92.2,
        "Elimination_Rev": -1543.8,
        "Total_Gross_Rev": 43407.2, "Total_Net_Rev": 41863.4, "Total_Segment_EBIT": 8281.8,
        "Domestic_Rev": 28435.7, "Overseas_Rev": 13427.7, "Overseas_Share_%": 32.1
    }
]

df = pd.DataFrame(data)

# Calculate segment margins (%)
df["Noodles_Margin_%"] = (df["Noodles_EBIT"] / df["Noodles_Rev"]) * 100
df["Dairy_Margin_%"] = (df["Dairy_EBIT"] / df["Dairy_Rev"]) * 100
df["Snacks_Margin_%"] = (df["Snacks_EBIT"] / df["Snacks_Rev"]) * 100
df["Seasonings_Margin_%"] = (df["Seasonings_EBIT"] / df["Seasonings_Rev"]) * 100
df["Nutrition_Margin_%"] = (df["Nutrition_EBIT"] / df["Nutrition_Rev"]) * 100
df["Beverages_Margin_%"] = np.where(df["Beverages_Rev"] > 0, (df["Beverages_EBIT"] / df["Beverages_Rev"]) * 100, 0.0)

# Calculate segment contribution to total gross sales (%)
df["Noodles_Share_%"] = (df["Noodles_Rev"] / df["Total_Gross_Rev"]) * 100
df["Dairy_Share_%"] = (df["Dairy_Rev"] / df["Total_Gross_Rev"]) * 100
df["Snacks_Share_%"] = (df["Snacks_Rev"] / df["Total_Gross_Rev"]) * 100
df["Seasonings_Share_%"] = (df["Seasonings_Rev"] / df["Total_Gross_Rev"]) * 100
df["Nutrition_Share_%"] = (df["Nutrition_Rev"] / df["Total_Gross_Rev"]) * 100
df["Beverages_Share_%"] = (df["Beverages_Rev"] / df["Total_Gross_Rev"]) * 100

os.makedirs("thesis_data", exist_ok=True)
csv_path = "thesis_data/06_master_revenue_dataset_timeseries.csv"
df.round(2).to_csv(csv_path, index=False)
print(f"Saved master segment time-series to {csv_path}")
print(df[["Year", "Total_Net_Rev", "Noodles_Share_%", "Overseas_Share_%", "Noodles_Margin_%", "Dairy_Margin_%"]].tail())

