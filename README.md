# ⚡ RetailIQ AI — AI-Powered Retail Business Intelligence Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-8E44AD.svg)](https://deepmind.google/technologies/gemini/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3399CC.svg)](https://plotly.com/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-00758F.svg)](https://www.mysql.com/)

**RetailIQ AI** is an executive-grade Business Intelligence platform and AI Copilot designed for retail analytics, automated SQL generation, inventory monitoring, and strategic business insight synthesis. 

---

## 🌟 Key Features

### 1. 🏠 Executive Command Center (`home.py`)
- **Real-Time KPI Cards**: Live tracking of Gross Sales, Total Profit, Profit Margin %, Total Orders, Average Order Value (AOV), and Active Customer Base.
- **Revenue & Profit Growth Trend**: Interactive Plotly line/area chart showing monthly performance trends with hover tooltips.
- **Inventory Warning Alert Banner**: Automatic monitoring flagging SKUs where current stock falls below reorder thresholds (`current_stock < reorder_level`).
- **Quick Action Launchpad**: Instant navigation to AI Copilot and Power BI embedded reports.

### 2. 🤖 AI Intelligence Copilot (`ai_assistant.py`)
- **Natural Language to SQL**: Powered by **Google Gemini 2.5 Flash**, converting plain-English questions into optimized SQL queries.
- **Multi-Chart Type Switcher**: Dynamically toggle query outputs between **Bar Chart**, **Line Chart**, **Donut/Pie Chart**, **Scatter Plot**, or **Data Table**.
- **Formatted SQL Inspector**: High-contrast, large-font SQL code block with query execution timer metrics (`⏱ Execution Time`).
- **Executive Insight Generator**: AI-synthesized key findings, strategic observations, and 2-3 actionable business recommendations.
- **CSV Data Export**: One-click download for all executed query result sets.
- **Query History Drawer**: Session history preserving past questions, SQL queries, and insights.

### 3. 📈 Interactive Analytics Hub (`analytics.py`)
- **Global Interactive Filter Bar**: Filter dataset dynamically by **Region**, **Category**, and **Customer Segment**.
- **4 Deep BI Suites**:
  1. 💰 **Sales & Financials**: Regional sales & profit bars, Category revenue donut charts, State-by-state financial performance matrix.
  2. 🏷️ **Product & Category Intelligence**: Top 10 most profitable products vs bottom loss-making products, Sub-category performance breakdown.
  3. 🚚 **Customer & Operations**: Customer segment revenue contribution, Shipping mode analysis, Payment preference distribution.
  4. 📦 **Inventory & Warehouse Health**: Low stock reorder priority monitor, Warehouse stock distribution, Lead time analysis.

### 4. ⚡ Resilient Dual-Engine Database Layer (`db_connection.py`)
- **MySQL Primary Connection**: Connects to local MySQL database (`ai_retail_bi`).
- **Zero-Downtime SQLite/CSV Fallback**: Automatically loads `data/SuperStore_Sales_Enhanced.csv`, `customer_master.csv`, and `product_master.csv` into an in-memory SQLite database if MySQL server is unreachable, ensuring **100% uninterrupted app operation**.
- **Live System Status Pill**: Visual health badge displaying active database mode in the sidebar (`🟢 MySQL Engine Active` or `⚡ SQLite / CSV Fallback Engine`).

### 5. 📊 Power BI Cloud Integration (`dashboard.py`)
- Embedded launchpad and report summary for published Power BI Cloud Service dashboards.

---

## 🛠️ Technology Stack

| Component | Technology / Library |
| :--- | :--- |
| **Frontend Framework** | Streamlit (Dark Cyber Glassmorphic Design System) |
| **Data Visualization** | Plotly Express & Plotly Graph Objects |
| **AI LLM Engine** | Google Gemini 2.5 Flash via `google-generativeai` |
| **Data Engine & ORM** | MySQL, SQLite, SQLAlchemy, PyMySQL |
| **Data Manipulation** | Pandas, NumPy |
| **Environment Configuration** | `python-dotenv` |

---

## 📁 Project Architecture

```text
AI_Retail_Business_Intelligence_Assistant/
├── .env                       # Environment variables (Google API Key)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── .streamlit/
│   └── config.toml            # Global Streamlit dark theme configuration
├── ai_engine/
│   ├── db_connection.py       # Dual-engine database connection (MySQL + SQLite fallback)
│   ├── sql_agent.py           # Gemini AI SQL generator & business insight agent
│   ├── prompt_template.py     # Prompt engineering templates
│   └── gemini_test.py         # AI engine unit test script
├── app/
│   ├── app.py                 # Main Streamlit application entry point
│   └── modules/
│       ├── custom_css.py      # Glassmorphic CSS design system & white radio styles
│       ├── home.py            # Executive Command Center dashboard
│       ├── ai_assistant.py    # AI Intelligence Copilot module
│       ├── analytics.py       # 4-Tab Interactive Analytics Hub
│       ├── dashboard.py       # Power BI embedded dashboard page
│       └── about.py           # Diagnostic & System Specs page
├── data/
│   ├── SuperStore_Sales_Enhanced.csv
│   ├── customer_master.csv
│   ├── product_master (1).csv
│   └── returns.csv
├── database/
│   ├── import_orders.py       # Script to import orders CSV into MySQL
│   └── import_products.py     # Script to import products CSV into MySQL
└── powerbi/                   # Power BI report files & documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- **Google Gemini API Key** (Obtain from [Google AI Studio](https://aistudio.google.com/)).
- *(Optional)* MySQL Server running locally if using MySQL storage mode.

### 2. Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/AI_Retail_Business_Intelligence_Assistant.git
   cd AI_Retail_Business_Intelligence_Assistant
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

   *(Optional MySQL Credentials)*:
   ```env
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ai_retail_bi
   ```

5. *(Optional)* **Import Datasets into MySQL**:
   If using MySQL mode, run the database import scripts:
   ```bash
   python database/import_orders.py
   python database/import_products.py
   ```
   *(Note: If MySQL is not running, the application will automatically fall back to SQLite using the CSV files in `data/` seamlessly!)*

### 3. Launch the Application

Run Streamlit from the root directory:

```bash
streamlit run app/app.py
```

The app will open automatically in your default browser at `http://localhost:8501`.

---

## 💡 Example AI Questions to Try

- `"Show top 5 selling products by total profit"`
- `"What is the monthly sales and profit trend?"`
- `"Which products currently have stock lower than reorder level?"`
- `"Break down sales by customer segment and region"`
- `"Show total sales by payment mode"`

---

## 📜 License & Credits

Developed with using **Python, Streamlit, Plotly, Google Gemini AI, MySQL, and Power BI**.
