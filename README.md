🌧️Rainfall-Pattern-and-Climate-Analysis
📌 Project Overview

Rainfall plays a crucial role in agriculture, water resource management, and disaster preparedness. This project analyzes long-term rainfall data across Indian regions to identify seasonal patterns, variability, and trends. The goal is to derive actionable insights that support better agricultural planning and decision-making.

🎯 Objectives

* Analyze rainfall variability across regions (subdivisions/states)
* Identify seasonal rainfall patterns (monsoon, pre/post-monsoon)
* Study long-term rainfall trends (1901–2015)
* Detect extreme rainfall years (droughts and floods)
* Generate insights useful for agricultural planning

🛠️ Tools & Technologies

* Python
* Pandas
* NumPy
* Matplotlib

📂 Project Structure

```
Rainfall-Pattern-and-Climate-Analysis/
│
├── data/
│   ├── rainfall_cleaned.csv
│   └── rainfall_long.csv
│
├── notebooks/
│   └── rainfall_analysis.ipynb
│
├── outputs/
│   ├── 04_seasonal_analysis.png
│   └── 05_longterm_trends.png
│
└── README.md
```
🔄 Data Processing Pipeline

1. **Data Loading & Inspection**

   * Explored dataset structure, columns, and missing values

2. **Data Cleaning**

   * Handled missing values using subdivision-wise averages
   * Fixed inconsistencies and typos
   * Recalculated annual rainfall
   * Rebuilt seasonal features

3. **Data Transformation**

   * Converted wide format → long format
   * Structured data for analysis (STATE, YEAR, MONTH, RAINFALL)

📊 Key Analyses & Results

🌦️ Seasonal Rainfall Patterns

* Peak rainfall occurs in **July (~347 mm)**
* **~75% of annual rainfall** occurs during **monsoon (Jun–Sep)**
* Winter months (Jan–Feb) receive very low rainfall

📉 Long-Term Trend Analysis (1901–2015)

* Slight decreasing trend: **−0.305 mm/year**
* Total change: ~−35 mm over 115 years
* **No statistically significant trend** (p-value > 0.05)
* Conclusion: Rainfall variability is more important than long-term trend

⚠️ Extreme Years

* **Drought years**: 1972, 2002, 2009
* **High rainfall years**: 1961, 1990, 1988

🌾 Agricultural Insights

* **Monsoon dependency**:
  Kharif crops (Rice, Maize, Cotton) rely heavily on monsoon rainfall

* **Dry season advantage**:
  Rabi crops (Wheat, Mustard) benefit from low rainfall in winter

* **Variability risk**:
  High year-to-year variation highlights the need for irrigation planning

* **Regional cropping strategies**:
  Different rainfall patterns support region-specific crop planning

📈 Outputs

* Seasonal rainfall analysis chart
* Long-term rainfall trend visualization
* Rainfall variability insights

📊 Dataset

* Source: IMD Rainfall Data (via Kaggle)
* Coverage: 1901–2015
* Regions: 36 Indian meteorological subdivisions

🚀 Future Work

* State-wise rainfall comparison
* Rainfall variability (Coefficient of Variation) analysis
* Crop suitability mapping
* Interactive dashboard using Streamlit

⭐ Conclusion

This project demonstrates that Indian agriculture is highly dependent on monsoon rainfall. While no strong long-term trend is observed, rainfall variability plays a critical role in agricultural risk, making adaptive planning essential.
