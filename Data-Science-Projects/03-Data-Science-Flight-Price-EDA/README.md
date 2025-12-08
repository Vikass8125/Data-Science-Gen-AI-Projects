# ✈️ **Flight Price Analysis – Understanding Key Factors Behind Airfare Variations**

A comprehensive exploratory data analysis of flight prices to understand how **airline**, **stops**, **duration**, **route**, and **timing** influence airfare.

---

# 📌 **The Problem (Situation)**

Flight ticket prices fluctuate heavily even for the same route. Travelers often struggle to answer:

* Why is one airline more expensive than another?
* Do non-stop flights always cost more?
* Does flight duration affect the price?
* Do travel month and departure times impact fares?

Without structured analysis, both **travelers** and **airline platforms** lack clarity on what truly drives price changes.

---

# 💡 **The Solution (Task & Action)**

### 🎯 **Task**

Analyze the flight price dataset to uncover trends and features that influence airfare variability.

### 🛠 **Actions Taken**

Using Python & Pandas, we:

* Loaded flight data from `flight_price.xlsx`
* Cleaned and transformed columns (date, time, duration)
* Extracted key features such as:

  * `day`, `month` from journey date
  * `dep_hour`, `arr_hour` from time columns
* Converted duration into total hours/minutes
* Explored:

  * Price differences across airlines
  * Impact of stops on airfare
  * Duration–price relationships
  * Source/destination influence
  * Route patterns
* Compiled insights based on statistical analysis

---

# 📊 **Key Results (Business-Friendly)**

* ✈️ **Airlines vary significantly in pricing** — premium carriers consistently charge more.
* 🛑 **Non-stop flights are the most expensive**, while 1-stop/2-stop flights offer cost savings.
* ⏳ **Longer durations generally cost more**, especially for connecting flights.
* 🌍 **Source and destination cities strongly impact price**, with major metros showing a wide range.
* ⏰ **Departure time influences cost** — evening flights tend to be more expensive than morning flights.
* 🗓 **Seasonal trends cause price spikes**, especially during holidays and month-ends.

These insights help travelers make informed booking decisions and support pricing teams in understanding fare patterns.

---

# 🔍 **Findings**

* Dataset required significant preprocessing for date & duration fields.
* Airline pricing is uneven — some airlines charge a premium for similar routes.
* Number of stops is one of the **strongest predictors** of airfare.
* Duration affects cost but interacts with stop count.
* Popular routes tend to have more stable pricing.
* Timing (month/day/hour) affects price trends.
* Cleaned dataset is ready for future ML models.

---

# 🛠 **Tech Stack**

* **Python**
* **Pandas**, **NumPy** — for data cleaning & manipulation
* **Jupyter Notebook** — for analysis
* **Excel Dataset** — `flight_price.xlsx`

---

# 🚀 **How to Run This Project**

### **1. Clone the repository**

```bash
git clone <repo-link>
cd flight-price-analysis
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. Open the notebook**

```bash
jupyter notebook Flight-Price-EDA.ipynb
```

### **4. Run the analysis**

Use **Kernel → Restart & Run All**.

---

# 🧠 **Technical Breakdown (Line-by-Line Explanation)**

Below is a technical walk-through of the notebook to help data scientists and for your revision.

---

## **1. Importing Libraries**

```python
import pandas as pd
import numpy as np
```

These libraries are essential for loading, cleaning, and manipulating tabular data.

---

## **2. Loading the Dataset**

```python
df = pd.read_excel("flight_price.xlsx")
df.head()
```

Loads the dataset into a DataFrame and previews its structure.

---

## **3. Checking Dataset Structure**

```python
df.info()
df.describe()
```

* `info()` reveals data types and missing values.
* `describe()` provides summary statistics for numerical columns.

---

## **4. Handling Missing Values**

```python
df.isnull().sum()
```

Used to determine where filling or dropping is required.

---

## **5. Parsing Date and Time Columns*

```python
df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'])
df['Dep_hour'] = pd.to_datetime(df['Dep_Time']).dt.hour
df['Arr_hour'] = pd.to_datetime(df['Arrival_Time']).dt.hour
```

### 🔎 **What This Does**

* Converts `Date_of_Journey` from string → datetime format.
* Extracts **departure hour** and **arrival hour**, creating time-based numerical features.
* Enables grouping by:

  * Day of month
  * Month of journey
  * Departure time slots (morning/evening/night)

### 💡 **Why This Matters**

* Evening flights are often more expensive due to business travel.
* Early morning flights are typically cheaper.
* Seasonal spikes (festivals, holidays) impact fare patterns.

This step transforms messy timestamps into **model-friendly and insight-rich temporal features**.

---

## **6. Converting Duration**

Duration examples in the dataset:

* `'2h 33m'`
* `'15h'`
* `'1h 50m'`

```python
def convert_duration(x):
    h = int(x.split('h')[0])
    m = x.split(' ')
    if len(m) > 1:
        m = int(m[1].replace('m',''))
    else:
        m = 0
    return h * 60 + m

df['Duration_mins'] = df['Duration'].apply(convert_duration)
```

### 🔎 **What This Does**

* Extracts the hours and minutes from string format.
* Converts duration → **total minutes**.
* Creates a numerical variable suitable for correlation analysis.

### 💡 **Why This Matters**

* Longer flights generally cost more.
* Duration combined with stops reveals inefficient or premium flight options.
* Numeric duration is essential for modeling and deeper analysis.

---

## **7. Analyzing Categorical Variables**

```python
df['Airline'].value_counts()
df['Source'].value_counts()
df['Destination'].value_counts()
```

### 🔎 **What This Does**

* Shows distribution of flights by airline, source city, and destination city.
* Identifies major carriers, busiest routes, and travel hubs.

### 💡 **Why This Matters**

* Airline type significantly impacts fare.
* Major metropolitan hubs have wide price variance.
* Understanding distribution helps contextualize pricing patterns.

---

## **8. Price Relationship Insights**

### ✈️ **Airlines**

Premium airlines (e.g., Jet Airways, Air India) consistently charge more due to service quality and brand.

Budget airlines show:

* Lower fares
* Higher volatility due to dynamic pricing

### 🛑 **Number of Stops**

* Non-stop flights = **highest-priced category**
* 1-stop or 2-stop flights = significantly more affordable

Stops introduce:

* Longer total travel time
* Reduced convenience, hence lower average ticket price

### ⏳ **Duration**

* Long duration flights often cost more.
* A *non-stop long flight* may cost more than a *shorter multi-stop* flight.

### 🌍 **Source & Destination**

* Delhi, Mumbai, Bangalore exhibit large price ranges.
* Some routes show consistent premium pricing due to high demand.

### 🔁 **Routes**

Route analysis helps detect:

* Price patterns for busy travel paths
* Airlines charging extra on specific sectors
* High-demand corridors

---

## **9. Outlier Exploration**

```python
df['Price'].describe()
```

### 🔎 **What You Found**

* Several flights cost **5× more** than the median.
* Outliers may represent:

  * Holiday spikes
  * Last-minute fares
  * Business-class or premium routes
  * Airline-specific anomalies

### 💡 **Why This Matters**

* Outliers distort averages and correlations.
* Helps refine data before modeling.
* Indicates real-world pricing anomalies worth exploring.

---

## **10. Insight Synthesis**

After exploration, you consolidated the findings:

### 🧠 **Key Insight Patterns**

* Non-stop flights are the priciest.
* Evening departure flights cost more.
* Duration affects fares but interacts with stop count.
* Certain airlines systematically charge higher.
* City pairs show consistent demand-based pricing.

### 🎯 **Business Implications**

* **Travelers:** Can avoid high fare windows and choose optimal routes.
* **Airlines:** Can adjust competitiveness for key sectors.
* **Analysts:** Dataset is ready for ML-based fare prediction.

---

# 🎯 **Conclusion**

This EDA demonstrates that flight prices depend heavily on airline choice, stops, duration, route popularity, and journey timing. These insights support:

* **Travelers** — in choosing affordable and efficient flights
* **Airline businesses** — in understanding competitive pricing patterns
* **Data analysts** — in building future forecasting or ML models
