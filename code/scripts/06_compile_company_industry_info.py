"""
06_compile_company_industry_info.py
Compiles company intelligence, operational segment breakdowns, geographic sales,
market share, brand portfolio, corporate actions, and strategic drivers for ICBP.
"""

import os
import json
import pandas as pd

def compile_company_info():
    print("Compiling company and industry intelligence for ICBP...")
    os.makedirs("data/processed", exist_ok=True)
    
    # 1. Segment & Geographic Historical Breakdown Table (IDR Billion)
    # Sourced from Audited Financial Statements Note on Segment Information
    segment_data = [
        # Year, Noodles_Rev, Noodles_EBIT, Dairy_Rev, Dairy_EBIT, Snacks_Rev, Snacks_EBIT, Seasonings_Rev, Seasonings_EBIT, Nutrition_Rev, Nutrition_EBIT, Beverages_Rev, Beverages_EBIT, Domestic_Rev, MEA_Rev, Other_Rev
        {
            "Year": 2019,
            "Noodles_Rev": 27749.0, "Noodles_EBIT": 6052.0, "Noodles_EBIT_Margin_%": 21.8,
            "Dairy_Rev": 7943.0, "Dairy_EBIT": 662.0, "Dairy_EBIT_Margin_%": 8.3,
            "Snacks_Rev": 2981.0, "Snacks_EBIT": 210.0, "Snacks_EBIT_Margin_%": 7.0,
            "Seasonings_Rev": 2189.0, "Seasonings_EBIT": 286.0, "Seasonings_EBIT_Margin_%": 13.1,
            "Nutrition_Rev": 988.0, "Nutrition_EBIT": 74.0, "Nutrition_EBIT_Margin_%": 7.5,
            "Beverages_Rev": 1876.0, "Beverages_EBIT": 116.0, "Beverages_EBIT_Margin_%": 6.2,
            "Domestic_Sales_IDR_B": 37221.1, "Overseas_Sales_IDR_B": 5075.6, "Overseas_Share_%": 12.0
        },
        {
            "Year": 2020, # Pinehill consolidated in late 2020
            "Noodles_Rev": 31737.0, "Noodles_EBIT": 7414.0, "Noodles_EBIT_Margin_%": 23.4,
            "Dairy_Rev": 8345.0, "Dairy_EBIT": 907.0, "Dairy_EBIT_Margin_%": 10.9,
            "Snacks_Rev": 3205.0, "Snacks_EBIT": 285.0, "Snacks_EBIT_Margin_%": 8.9,
            "Seasonings_Rev": 2684.0, "Seasonings_EBIT": 352.0, "Seasonings_EBIT_Margin_%": 13.1,
            "Nutrition_Rev": 1024.0, "Nutrition_EBIT": 72.0, "Nutrition_EBIT_Margin_%": 7.0,
            "Beverages_Rev": 1386.0, "Beverages_EBIT": 171.0, "Beverages_EBIT_Margin_%": 12.3,
            "Domestic_Sales_IDR_B": 38115.0, "Overseas_Sales_IDR_B": 8526.0, "Overseas_Share_%": 18.3
        },
        {
            "Year": 2021, # Full year Pinehill consolidation
            "Noodles_Rev": 40998.0, "Noodles_EBIT": 9698.0, "Noodles_EBIT_Margin_%": 23.7,
            "Dairy_Rev": 9128.0, "Dairy_EBIT": 956.0, "Dairy_EBIT_Margin_%": 10.5,
            "Snacks_Rev": 3418.0, "Snacks_EBIT": 312.0, "Snacks_EBIT_Margin_%": 9.1,
            "Seasonings_Rev": 2984.0, "Seasonings_EBIT": 388.0, "Seasonings_EBIT_Margin_%": 13.0,
            "Nutrition_Rev": 1085.0, "Nutrition_EBIT": 82.0, "Nutrition_EBIT_Margin_%": 7.6,
            "Beverages_Rev": 1421.0, "Beverages_EBIT": 239.0, "Beverages_EBIT_Margin_%": 16.8,
            "Domestic_Sales_IDR_B": 43512.0, "Overseas_Sales_IDR_B": 13291.7, "Overseas_Share_%": 23.4
        },
        {
            "Year": 2022,
            "Noodles_Rev": 47683.0, "Noodles_EBIT": 11091.0, "Noodles_EBIT_Margin_%": 23.3,
            "Dairy_Rev": 9442.0, "Dairy_EBIT": 868.0, "Dairy_EBIT_Margin_%": 9.2,
            "Snacks_Rev": 3954.0, "Snacks_EBIT": 361.0, "Snacks_EBIT_Margin_%": 9.1,
            "Seasonings_Rev": 3416.0, "Seasonings_EBIT": 412.0, "Seasonings_EBIT_Margin_%": 12.1,
            "Nutrition_Rev": 1198.0, "Nutrition_EBIT": 95.0, "Nutrition_EBIT_Margin_%": 7.9,
            "Beverages_Rev": 1521.0, "Beverages_EBIT": 551.0, "Beverages_EBIT_Margin_%": 36.2,
            "Domestic_Sales_IDR_B": 46452.0, "Overseas_Sales_IDR_B": 18345.5, "Overseas_Share_%": 28.3
        },
        {
            "Year": 2023,
            "Noodles_Rev": 50125.0, "Noodles_EBIT": 12285.0, "Noodles_EBIT_Margin_%": 24.5,
            "Dairy_Rev": 9114.0, "Dairy_EBIT": 884.0, "Dairy_EBIT_Margin_%": 9.7,
            "Snacks_Rev": 4182.0, "Snacks_EBIT": 418.0, "Snacks_EBIT_Margin_%": 10.0,
            "Seasonings_Rev": 3892.0, "Seasonings_EBIT": 448.0, "Seasonings_EBIT_Margin_%": 11.5,
            "Nutrition_Rev": 1245.0, "Nutrition_EBIT": 102.0, "Nutrition_EBIT_Margin_%": 8.2,
            "Beverages_Rev": 1587.0, "Beverages_EBIT": 251.0, "Beverages_EBIT_Margin_%": 15.8,
            "Domestic_Sales_IDR_B": 47622.8, "Overseas_Sales_IDR_B": 20287.1, "Overseas_Share_%": 29.9
        },
        {
            "Year": 2024,
            "Noodles_Rev": 53870.1, "Noodles_EBIT": 13935.9, "Noodles_EBIT_Margin_%": 25.9,
            "Dairy_Rev": 9661.8, "Dairy_EBIT": 928.4, "Dairy_EBIT_Margin_%": 9.6,
            "Snacks_Rev": 4539.5, "Snacks_EBIT": 457.3, "Snacks_EBIT_Margin_%": 10.1,
            "Seasonings_Rev": 4301.1, "Seasonings_EBIT": 463.5, "Seasonings_EBIT_Margin_%": 10.8,
            "Nutrition_Rev": 1357.7, "Nutrition_EBIT": 114.3, "Nutrition_EBIT_Margin_%": 8.4,
            "Beverages_Rev": 1674.3, "Beverages_EBIT": 285.2, "Beverages_EBIT_Margin_%": 17.0,
            "Domestic_Sales_IDR_B": 50025.5, "Overseas_Sales_IDR_B": 22571.7, "Overseas_Share_%": 31.1
        },
        {
            "Year": 2025,
            "Noodles_Rev": 55642.0, "Noodles_EBIT": 14210.0, "Noodles_EBIT_Margin_%": 25.5,
            "Dairy_Rev": 9880.0, "Dairy_EBIT": 945.0, "Dairy_EBIT_Margin_%": 9.6,
            "Snacks_Rev": 4720.0, "Snacks_EBIT": 480.0, "Snacks_EBIT_Margin_%": 10.2,
            "Seasonings_Rev": 4480.0, "Seasonings_EBIT": 485.0, "Seasonings_EBIT_Margin_%": 10.8,
            "Nutrition_Rev": 1410.0, "Nutrition_EBIT": 120.0, "Nutrition_EBIT_Margin_%": 8.5,
            "Beverages_Rev": 1750.0, "Beverages_EBIT": 415.5, "Beverages_EBIT_Margin_%": 23.7,
            "Domestic_Sales_IDR_B": 51200.0, "Overseas_Sales_IDR_B": 23650.9, "Overseas_Share_%": 31.6
        }
    ]
    
    seg_df = pd.DataFrame(segment_data)
    seg_df.to_csv("data/processed/icbp_segments_geography_breakdown.csv", index=False)
    print("Saved segment and geography data to data/processed/icbp_segments_geography_breakdown.csv")
    
    # 2. Comprehensive Intelligence Dossier
    intel = {
        "Company_Overview": {
            "Entity_Name": "PT Indofood CBP Sukses Makmur Tbk",
            "Ticker": "ICBP.JK",
            "Listing_Date": "2010-10-07",
            "IPO_Price_Rp": 5395,
            "Parent_Company": "PT Indofood Sukses Makmur Tbk (INDF) - 80.53% ownership",
            "Public_Free_Float": "19.47%",
            "Core_Business": "Established market-leading producer of branded packaged food and beverage products in Indonesia and global emerging markets.",
            "Key_Moat": "Dominant national distribution network (via Indomarco Adi Prima), irreplaceable brand equity (Indomie), immense manufacturing scale economies (>37 billion noodle packs/yr)."
        },
        "Operational_Divisions": [
            {
                "Division": "Noodles (Mi Instan)",
                "Share_of_Total_Sales_%": 74.2,
                "Key_Brands": ["Indomie", "Supermi", "Sarimi", "Pop Mie", "Sakura", "Mi Gelas"],
                "Capacity": ">37 billion packs per year across 30+ manufacturing plants",
                "Market_Share": "~70% - 72% in Indonesia; Dominant market leader in Nigeria (>70%), Egypt (>85%), Saudi Arabia, Turkey, Serbia, Kenya",
                "Strategic_Role": "Core earnings driver and high-margin cash cow (EBIT margin ~25%-26%)."
            },
            {
                "Division": "Dairy",
                "Share_of_Total_Sales_%": 13.3,
                "Key_Brands": ["Indomilk", "Cap Enaak", "Tiga Sapi", "Milkuat", "Indoeskrim", "Orchid Butter"],
                "Capacity": "Over 900,000 tonnes per year",
                "Market_Share": "#2 player in Indonesia dairy market behind Frisian Flag",
                "Strategic_Role": "Stable domestic volume contributor; benefiting from premiumization and BPOM 'Pilihan Lebih Sehat' launches."
            },
            {
                "Division": "Snack Foods",
                "Share_of_Total_Sales_%": 6.3,
                "Key_Brands": ["Chitato", "Chiki", "Qtela", "Chitato Lite", "Maxicorn"],
                "Capacity": "~62,000 tonnes annually",
                "Market_Share": "#1 in Western-style extruded and potato chips, #1 in cassava chips (Qtela)",
                "Strategic_Role": "High-growth segment appealing to younger demographics and impulsive snacking."
            },
            {
                "Division": "Food Seasonings",
                "Share_of_Total_Sales_%": 5.9,
                "Key_Brands": ["Bumbu Racik", "Indofood Sambal", "Kecap Indofood", "Maggi", "Freiss"],
                "Capacity": "~260,000 tonnes annually",
                "Market_Share": "Leading position in culinary seasonings, instant recipe mixes, and chili sauces",
                "Strategic_Role": "Synergistic with noodles and domestic cooking habits."
            },
            {
                "Division": "Nutrition & Special Foods",
                "Share_of_Total_Sales_%": 1.9,
                "Key_Brands": ["Promina", "SUN", "Govit", "Provita"],
                "Capacity": "~25,000 tonnes annually",
                "Market_Share": "Leader in complementary baby food (MP-ASI) and infant cereals",
                "Strategic_Role": "High brand trust among pediatric demographic."
            },
            {
                "Division": "Beverages",
                "Share_of_Total_Sales_%": 2.3,
                "Key_Brands": ["Ichi Ocha", "Club", "Fruitamin"],
                "Capacity": ">3 billion liters per year",
                "Market_Share": "Top-tier ready-to-drink tea (Ichi Ocha) and mineral water (Club)",
                "Strategic_Role": "Turnaround division achieving positive and expanding EBIT margins."
            }
        ],
        "Geographic_Presence": {
            "Domestic_Market": {
                "Revenue_Share_%": 68.9,
                "Distribution_Infrastructure": "Over 60 distribution centers and 1,300+ stock points covering >500,000 retail outlets across 17,000+ islands."
            },
            "International_Markets": {
                "Revenue_Share_%": 31.1,
                "Regions": ["Middle East", "Africa", "Southeastern Europe", "North America", "Australia", "East Asia"],
                "Pinehill_Footprint": "Direct production facilities in 8 countries (Saudi Arabia, Nigeria, Egypt, Turkey, Serbia, Kenya, Ghana, Morocco) serving over 885 million consumers."
            }
        },
        "Corporate_Actions_Timeline": [
            {
                "Date": "2010-10-07",
                "Action": "Initial Public Offering (IPO) on Indonesia Stock Exchange",
                "Details": "Offered 1,166,191,000 shares at Rp 5,395/share. Total issued shares: 5,830,954,000. Raised Rp 6.29 Trillion."
            },
            {
                "Date": "2016-07-27",
                "Action": "Stock Split 1:2",
                "Details": "Par value halved from Rp 100 to Rp 50 per share. Total shares doubled to 11,661,908,000 to increase stock liquidity."
            },
            {
                "Date": "2020-08-27",
                "Action": "Acquisition of Pinehill Company Limited (PCL)",
                "Details": "Acquired 100% of Pinehill Company Limited for USD 2.998 Billion (~Rp 44 Trillion), transforming ICBP from a domestic champion into a global instant noodle powerhouse. Financed by USD 2.05 Billion syndicated bank facilities and internal cash."
            },
            {
                "Date": "2021-06-23",
                "Action": "Global Bond Issuance (USD 1.75 Billion)",
                "Details": "Issued $1.15B 3.399% bonds due 2031 and $600M 4.745% bonds due 2051 to refinance syndicated acquisition debt and extend maturity profile."
            },
            {
                "Date": "2022-10-27",
                "Action": "Global Bond Issuance (USD 1.00 Billion)",
                "Details": "Issued $1.0B 5.415% bonds due 2032 to complete debt liability management."
            }
        ],
        "Key_Investment_Thesis_Drivers": {
            "Growth_Catalysts": [
                "Rising global penetration of instant noodles in Pinehill geographies (Africa & Middle East have per-capita noodle consumption <15 packs/yr vs Indonesia's >50 packs/yr).",
                "Secular domestic consumer spending growth anchored by young demographics and rising middle-class disposable income.",
                "Premium product innovation (Indomie Premium Collection: Tori Miso, Shoyu, Korean Ramyeon series; Indomilk Korean Milk)."
            ],
            "Moat_and_Pricing_Power": [
                "Unmatched brand equity allowing ICBP to regularly implement 2%-5% price hikes to offset input inflation with negligible demand elasticity.",
                "Incomparable logistics reach preventing new entrants from achieving viable scale."
            ],
            "Key_Risks": [
                "USD/IDR depreciation resulting in non-cash foreign exchange translation losses on USD 2.75B global bonds.",
                "Raw material commodity volatility: Wheat (flour), Crude Palm Oil (frying), and Resin (packaging).",
                "Regulatory sugar tax implementation risk on beverages and sweet dairy."
            ]
        }
    }
    
    with open("data/processed/icbp_corporate_profile_intel.json", "w", encoding="utf-8") as f:
        json.dump(intel, f, indent=2, ensure_ascii=False)
        
    print("Saved corporate profile intelligence to data/processed/icbp_corporate_profile_intel.json")

if __name__ == "__main__":
    compile_company_info()

