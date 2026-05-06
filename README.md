# 🌍 Global Climate Indicators Dashboard

An interactive Streamlit dashboard that analyzes the relationship between **CO₂ emissions** and **global temperature anomalies** over time. The project explores how industrialization has influenced climate change using real-world datasets and interactive visualizations.

---

## 📊 Project Overview

This dashboard allows users to explore climate data from 1880 to the present through multiple interactive views:

- 📈 Temperature trends over time  
- 🌫️ CO₂ emissions per capita over time  
- 🔗 Relationship between CO₂ and temperature  
- 📊 Dual-axis comparison of both variables  
- 📉 Pre vs Post industrialization comparison  
- 🎛️ Interactive filtering and smoothing options  

---

## 🎯 Research Question

**How do CO₂ emissions relate to global temperature changes over time, and how has this relationship evolved across different historical periods?**

---

## 🔍 Key Features

- Interactive time range selector:
  - 1880-Present
  - 1880–1949
  - 1950–1999
  - 2000–Present
- Toggle between:
  - Raw data
  - Smoothed trends (5-year rolling average)
- Multiple Plotly visualizations:
  - Line charts
  - Scatter plots with regression line
  - Dual-axis comparison chart
  - Bar comparison (pre vs post industrialization)
- Insight and limitation summaries

---

## 🧠 Key Findings

- CO₂ emissions and temperature anomalies show a strong positive correlation  
- Post-1950 period shows a sharp acceleration in both emissions and warming  
- Recent decades show the most rapid climate change trends in the dataset  
- Smoothed trends reveal long-term patterns more clearly than raw data  

---

## ⚠️ Limitations

- CO₂ data is averaged and not fully country-specific  
- Temperature data represents anomalies, not absolute temperatures  
- Correlation does not imply causation  
- Some early historical data may be incomplete or estimated  

---

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Da125673/Project.git
cd Project

pip install -r requirements.txt

streamlit run app.py