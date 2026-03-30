# spice-streamlit-app
# ☀️ SPICE Solar Analytics Dashboard

## 📌 Overview

The **SPICE Solar Analytics Dashboard** is an interactive Streamlit application designed to support data-driven decision-making for community solar projects.

It helps stakeholders understand how **system design choices (tilt, azimuth, and system size)** impact solar energy production, financial returns, and environmental benefits.

This project combines **data analysis, simulation modeling, and visualization** into a unified tool for planning and evaluating solar installations.

---

## 🎯 Objectives

* Provide clear insights into solar system performance
* Enable comparison between different design configurations
* Support investment and planning decisions for SPICE projects
* Translate complex data into **business-friendly insights**

---

## ⚙️ Key Features

### 🔋 Solar Simulation

* Dynamic simulation based on:

  * Tilt
  * Azimuth
  * System size
* Monthly, quarterly, and annual production insights
* Comparison against a reference system

---

### 📊 Production Analysis

* Monthly energy trends
* Selected vs reference design comparison
* Annual output comparison
* Weather-based production variability

---

### 📈 Design Insights

* Tilt and azimuth sensitivity analysis
* Heatmap visualization of design performance
* Identification of optimal system configurations

---

### 💰 Financial Impact

* Estimated revenue from solar production
* Investment insights for stakeholders
* Comparison of financial performance across designs

---

### 🌱 Environmental Impact

* Carbon emission reduction estimates
* Sustainability contribution of solar systems

---

### 🏙️ Scalability Insights

* Understanding how solar solutions can scale across communities
* Evaluating broader impact of solar adoption

---

### 🧠 Decision Support (Planned / Added)

* Recommended system configurations
* Performance improvement analysis
* Clear business-focused conclusions

---

### 🤖 AI Assistant (RAG Chatbot - Planned / Added)

* Ask questions about the dashboard and results
* Get explanations of solar concepts and insights
* Translate technical results into simple language

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Pandas / NumPy**
* **Plotly**
* **Joblib (ML Models)**
* **Scikit-learn**
* **PVGIS (data source for solar simulation)**

---

## 📂 Project Structure

```bash
spice-streamlit-app/
│
├── app.py                     # Main entry point
├── pages/                    # Multi-page Streamlit app
├── data/                     # Datasets used in the project
├── models/                   # Trained ML models
├── images/                   # UI assets (logos, banners)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 How to Run the App

### 1. Clone the repository

```bash
git clone https://github.com/your-username/spice-streamlit-app.git
cd spice-streamlit-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python -m streamlit run app.py
```

---

## 📊 Data Sources

* PVGIS solar simulation data
* SPICE project datasets
* Weather and irradiance datasets
* Energy and emissions benchmarks

---

## 📌 Key Insights

* Solar output is highly influenced by **seasonality and weather patterns**
* Optimal performance occurs within specific **tilt and azimuth ranges**
* Design choices significantly impact **annual energy production and returns**
* Data-driven planning improves both **financial and environmental outcomes**

---

## ⚠️ Limitations

* Simulations are based on historical weather averages
* Financial estimates are simplified assumptions
* Model accuracy depends on input data quality

---

## 👨‍💻 Contributors

* Crystal Blackburn
* Harasis Singh
* Jagjiwan Singh
* SPICE Project Team
---

## 📢 Acknowledgments

* SPICE (Solar Power Investment Cooperative of Edmonton)
* NorQuest College
* PVGIS for solar data modeling

---

## 📬 Contact

For questions or feedback, feel free to reach out or open an issue in this repository.

---

⭐ If you found this project useful, consider giving it a star!
