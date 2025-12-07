# 📱 **iPhone Sales & Ratings Analysis (EDA Project)**  
![Build](https://img.shields.io/badge/Build-Passing-brightgreen)  
![Python](https://img.shields.io/badge/Python-3.10+-blue)

---

# ⭐ **SITUATION**
Imagine walking into a giant toy store full of iPhones—different colors, sizes, and prices.  
Each one has a star rating from kids who tried it before.  
But which one is best? Which one do people buy more? Which one is overpriced?

This project helps answer those questions using **data**.

---

# 🎯 **TASK**
Build a system that:
- Reads iPhone data from Flipkart
- Finds the best-rated models
- Shows which phones get the most ratings/reviews
- Identifies the most and least expensive models
- Discovers relationships between **price**, **ratings**, and **reviews**

Goal → **Turn messy product data into simple, clear insights.**

---

# 🛠️ **ACTION**
We performed Exploratory Data Analysis (EDA) using:
- **Pandas** → data handling  
- **NumPy** → mathematical support  
- **Plotly** → beautiful interactive visualizations  

Used images included:
- `highest-rated.png`
- `highest-rated-reviews.png`
- `relation-sales-price.png`

---

# 📚 **FULL BREAKDOWN OF LIBRARIES, CLASSES & FUNCTIONS (With Contextual Snippets)**

---

## 🧩 1. **Libraries**

---

### **pandas**
A magic Excel-like tool inside Python used for data tables.

#### **Why we used it here**
Our dataset is a CSV table → Pandas helps load, sort, filter, summarize, and clean it.

#### **Code Example**
```python
import pandas as pd

# Load dataset into DataFrame
data = pd.read_csv("apple_products.csv")

# Preview the first few rows
data.head()
```

---

### **numpy**
A fast math and vector library.

#### **Why used**
Pandas relies on NumPy internally; useful for numeric summaries.

#### **Example**
```python
import numpy as np

# Calculate a simple average
np.mean([3, 4, 5])
```

---

### **plotly.express (px)**
High‑level visualization library — easy charts with few lines.

#### **Why used**
To visualize:
- Number of ratings
- Number of reviews
- Price vs ratings relationship

#### **Example**
```python
import plotly.express as px

# Bar chart for highest rated phones
fig = px.bar(highest_rated, x="Product Name", y="Number Of Ratings",
             title="Ratings of Top iPhones")
fig.show()
```

---

### **plotly.graph_objects (go)**
Advanced plotting library for full customization.

#### **Why used**
To create bar charts where more control was needed.

#### **Example**
```python
import plotly.graph_objects as go

fig = go.Figure(data=[
    go.Bar(x=labels, y=counts)
])
fig.update_layout(title="Review Counts for Top iPhones")
fig.show()
```

---

## 🧩 2. **Core Class: DataFrame**

A DataFrame is like a spreadsheet with superpowers:
- Rows = product entries
- Columns = product details (price, rating, reviews)

#### **Example**
```python
# Show column names
data.columns

# Show dataset shape
data.shape
```

---

## 🧩 3. **Data Loading & Cleaning**

### **3.1 Read CSV**
```python
data = pd.read_csv("apple_products.csv")
```

### **3.2 Check data sample**
```python
data.head()
```

### **3.3 Check missing values**
```python
data.isnull().sum()
```

### **3.4 Summary statistics**
```python
data.describe()
```

---

## 🧩 4. **Core DataFrame Operations**

---

### **4.1 Sort values**
Used to get Top 10 highest-rated iPhones.

```python
highest_rated = data.sort_values(by="Star Rating",
                                 ascending=False).head(10)

highest_rated
```

---

### **4.2 Count model occurrences**
Helps identify popular models.

```python
model_counts = data["Product Name"].value_counts()
model_counts.head()
```

---

### **4.3 Find most expensive & cheapest**
```python
# Index of max & min prices
max_idx = data["Sale Price"].idxmax()
min_idx = data["Sale Price"].idxmin()

# Retrieve full rows
most_expensive = data.loc[max_idx]
least_expensive = data.loc[min_idx]

most_expensive, least_expensive
```

---

### **4.4 Access rows with `.loc`**
```python
best_row = data.loc[max_idx]
best_row
```

---

## 🧩 5. **Plotly Visualization Functions**

---

### **5.1 Bar Chart — Ratings**

```python
fig = px.bar(highest_rated, x="Product Name",
             y="Number Of Ratings",
             title="Ratings of Top iPhones")
fig.show()
```

![Ratings](highest-rated.png)

---

### **5.2 Bar Chart — Reviews**

```python
fig = px.bar(highest_rated, x="Product Name",
             y="Number Of Reviews",
             title="Reviews of Top iPhones")
fig.show()
```

![Reviews](highest-rated-reviews.png)

---

### **5.3 Scatter Plot — Price vs Ratings**

```python
fig = px.scatter(data, x="Sale Price",
                 y="Number Of Ratings",
                 title="Relationship Between Price and Ratings")
fig.show()
```

![Relation Price](relation-sales-price.png)

---

# 🧩 **RESULT**
We achieved:

- Identified **Top 10 highest-rated iPhones**
- Found which models get **most ratings & reviews**
- Discovered that **cheaper phones get more ratings**
- Found **most expensive** and **cheapest** iPhones
- Visualized everything with interactive charts

### Explained like you're 5:
> “We checked which iPhones people love most, which they talk about most, and which ones cost too much!”

---

# 📘 **KEY LEARNINGS**
- Data cleaning and inspection  
- Sorting & filtering  
- Creating interactive charts  
- Finding correlations  
- Extracting insights from messy product data  

---

# ▶️ **HOW TO RUN THE PROJECT**

### **1. Clone the project**
```bash
git clone <your-repo>
cd iphone-sales-analysis
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Start Jupyter Notebook**
```bash
jupyter notebook
```

### **4. Open & run:**
```
IPhone-Sales-Analysis.ipynb
```

You will see:
- Tables  
- Visual insights  
- Scatter plots  
- Saved PNG images  

