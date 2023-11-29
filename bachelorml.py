# -*- coding: utf-8 -*-
"""BachelorML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q1DURRcc8Rtc5AMM-GzPGEv5QrTbUg8-
"""

import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

from mlxtend.frequent_patterns import apriori, association_rules
import warnings

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pexpect")
# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="ipykernel")

# Enabelling the LabelEncoder
le = LabelEncoder()

from google.colab import drive # Gets my data stored in the cloud
drive.mount("/content/drive")

# Libraries imported, if imported correctly the below will print
print("Libraries imported.")

# Data set upload
filepath = "/content/drive/MyDrive//Data/online_retail_10_11.csv"

# I needed the below code to figure ut why it wsa not working
"""
# Library called Chardent to detect the encoding
import chardet

# Opens the file in binary
with open(filepath, "rb") as f:
    result = chardet.detect(f.read())

# Prints encoding value
print(result["encoding"])
"""

# First look at the dataset
df = pd.read_csv(filepath, encoding = "ISO-8859-1") # Encoding as would not open
df.head(1)

import pandas as pd

file_path = '/content/drive/My Drive/Data/online_retail_10_11.csv'  # Adjust the path as necessary
df = pd.read_csv(file_path, encoding='utf-8-sig')

# Initial look at the data types
df.info()

# Turns columns to datetime data type
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Seperate date column
df["Date"] = df["InvoiceDate"].dt.date
# Time column
df["InvoiceTime"] = df["InvoiceDate"].dt.time
# df.info()

# convert column from object to string
df["Description"] = df["Description"].astype(str)

# Storing rows with words found thorught the project that are not product sales
remove_words = ["AMAZON FEE", "Manual", "Adjust bad debt", "Bank Charges", "CRUK Commission", "Discount", "SAMPLES"]

# Boolean indexing to drop rows containing specific words
df = df[~df["Description"].str.contains("|".join(remove_words))]

df.isnull().sum()

# Have a total order column by multiplying the quantity by unit price
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

# df.head(2)

# Missing values
df.isnull().sum()

# Checking the df
df.describe()

# Assuming that minus values are refunds
print(df[df["Quantity"] < 0])

# Need to reference/ If quantity is negative, it is a returned or cancelled item
df["Transaction Type"] = np.where(df["Quantity"] < 0, "Cancelled", "Sale")

# Print the resulting dataframe
print(df)

#@title Duplicates
# If row duplicated store here
Duplicates = df[df.duplicated(keep=False)]

# If statement which shows
if len(Duplicates) > 0:
  # Prints the length or count of duplicate rows
    print("Total count of duplicate rows:", len(Duplicates))
# If all duplicates missing or now deleted will show no duplicate found
else:
    print("No duplicate rows found.")


# Droppin doubles
df = df.drop_duplicates()

# DOne again to check if deleted now
Duplicates2 = df[df.duplicated(keep=False)]

# If statement which shows
if len(Duplicates2) > 0:
  # Prints the length or count of duplicate rows
    print("Total count of duplicate rows:", len(Duplicates2))
# If all duplicates missing or now deleted will show no duplicate found
else:
    print("No duplicate rows found, they have now been deleted.")

#@title Start/End Date
# Looking for start and end date in df
StartDate = (df["InvoiceDate"].min())
EndDate = (df["InvoiceDate"].max())
print("Start date of data set: ", StartDate)
print("End date of data set: ", EndDate)

df.describe()

# Locating outliers throuhg a box plot, on colu,n qunatity by price
df.loc[:, ["Quantity", "TotalPrice"]].boxplot(figsize = (10,10));

# Function with some pre argumetns inside
def remove_outliers(data, lower_percentile = 0.25, upper_percentile = 0.75):
  # Defining Q's
    q1 = data.quantile(lower_percentile)
    q3 = data.quantile(upper_percentile)
    # Finding the inter quartile range
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    # Checks if data is in side the quartile range and stored
    filtered_data = data[(data >= lower_bound) & (data <= upper_bound)]
    return filtered_data

# Outliers removed for quantity
df.Quantity = remove_outliers(df.Quantity)
# Outliers removed for price
df.Revenue = remove_outliers(df.TotalPrice)
df.dropna(inplace=True)
df.loc[:, ["Quantity", "TotalPrice"]].describe()

"""# Weather API connected"""

# The weather API to link the histprical weather data
Base_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_Key = "1e81f8cce84f885d279386c4a8f53d23"
CITY = "London"

# Created URL to call
url = Base_URL + "appid=" + API_Key + "&q=" + CITY
# Data stored in JSON
APIjson = requests.get(url).json()

print(APIjson)

# Function the turns weather to calsius
def kelvin2celsius(kelvin):
  celsius = kelvin - 273.15
  return celsius

# Temp is in kelvin so turned it into celsius
temp_kelvin = APIjson ["main"]["temp"]
temp_celsius = kelvin2celsius(temp_kelvin)
feels_like_kelvin = APIjson ["main"]["feels_like"]
feels_like_celsius = kelvin2celsius(feels_like_kelvin)
# Description is the weather description which could be important
description = APIjson["weather"][0]["description"]

# Prints results
print(f"Current temperature in {CITY}: {temp_celsius:.2f} C")
print(f"Current temperature in {CITY} feels like: {feels_like_celsius:.2f} C")
print(f"General Weather in {CITY}: {description}")

# Shows available API keys
APIjson.keys()

# The two I will use look at type to convert to df
print("Data type for main is: ", type(APIjson["main"]))
print("Data type for weather is: ", type(APIjson["weather"]))
print("Data type for dt is: ", type(APIjson["dt"]))

# Convert to df
TestDf = pd.DataFrame(APIjson["main"], index = [0])
TestDf

"""
 # Getting the wanted weather data from he Json data
weather_data = {"Temperature": kelvin2celsius(APIjson["main"]["temp"]),
  "Feels Like": kelvin2celsius(APIjson["main"]["feels_like"]),
  "Min Temperature": kelvin2celsius(APIjson["main"]["temp_min"]),
  "Max Temperature": kelvin2celsius(APIjson["main"]["temp_max"])}

# Adds the weather data to the df
WeatherDF = df.append(weather_data, ignore_index=True)
WeatherDF
"""

# Would not work no matter what, tired batch processing, found out after that there is a max number of reuqests.

"""# Data analysis"""

#@title Country Sales
import plotly.express as px

# New Country df with columns for the graph
CountryDF = df[["Country", "Quantity", "TotalPrice"]]

# Grouping all countries to see the biggest buyers with.sum()
CountryDFgrouped = CountryDF.groupby("Country").sum()

# Top 20 countries based on Quantity
CountryDFquantity = CountryDFgrouped.sort_values("Quantity", ascending = False).head(20)

# Bar chart for Quantity on x and country on y axis using Plotly made horizontal
fig_quantity = px.bar(CountryDFquantity, x = "Quantity", y = CountryDFquantity.index,
                      orientation = "h", labels={"Quantity": "Quantity Sold", "y": "Country"}, title = "Top 20 Countries by Quantity Sold")

# Adding in colour code for graph
fig_quantity.update_traces(marker = dict(color = px.colors.sequential.Oranges))

fig_quantity.show()

# top 20 countries based on Total Price
CountryDFprice = CountryDFgrouped.sort_values("TotalPrice", ascending = False).head(20)

# Bar chart for Total Price on x and country on y axis using Plotly made horizontal
fig_price = px.bar(CountryDFprice, x = "TotalPrice", y = CountryDFprice.index, orientation="h",
                   labels={"TotalPrice": "Total Price", "y": "Country"}, title = "Top 20 Countries by Total Price")

# Adding in colour code for graph
fig_price.update_traces(marker = dict(color = px.colors.sequential.Oranges))

fig_price.show()

#@title Best/Worst selling products (Attempt 1)
# Group the data by product and sum the total sales, quantity, and calculate the unit price for each product
ProductSummary = df.groupby("Description").agg({"TotalPrice": "sum", "Quantity": "sum"})
ProductSummary["UnitPrice"] = ProductSummary["TotalPrice"] / ProductSummary["Quantity"]

# Sort the products by total sales in descending order and select the top 25
BestProduct = ProductSummary.sort_values(by="TotalPrice", ascending=False).head(25)

# Print the top 25 products
print("Top 25 best-selling products:")
print(BestProduct)

# Plot the top 25 products and their sales
sns.barplot(x = BestProduct.index, y = "TotalPrice", data = BestProduct)
plt.title("Top 25 best-selling products")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=90)
plt.show()

# Sort the products by total sales in ascending order and select the worst 25
WorstProduct = ProductSummary.sort_values(by="TotalPrice").head(25)

# Print the worst 25 products
print("Worst 25 products:")
# Prints in list format
print(WorstProduct)

# Plot the worst 25 products and their sales
sns.barplot(x = WorstProduct.index, y  ="TotalPrice", data = WorstProduct)
# Addint titles to the graoh
plt.title("Worst 25 products by sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=90)
plt.show

#@title Best/ Worst selling products (Attemtpt 2)
import plotly.graph_objects as go
import plotly.express as px

# Sort the products by total sales in descending order and select the top 25
BestProduct = ProductSummary.sort_values(by = "TotalPrice", ascending = False).head(25)

# Plot the top 25 products and their sales
fig = px.bar(BestProduct, x=BestProduct.index, y = "TotalPrice", hover_data = ["Quantity", "UnitPrice"])
fig.update_layout(
    title="Top 25 best-selling products",
    xaxis_title="Product",
    yaxis_title="Total Sales")

# Adding in colour code for graoh
fig.update_traces(marker=dict(color=px.colors.sequential.Greens))

fig.show()

# Sort the products by total sales in ascending order and select the worst 25
WorstProduct = ProductSummary.sort_values(by = "TotalPrice").head(45)

# Plot the worst 25 products and their sales
fig = px.bar(WorstProduct, x = WorstProduct.index, y="TotalPrice", hover_data=["Quantity", "UnitPrice"])
fig.update_layout(title = "Worst 25 products by sales", xaxis_title = "Product", yaxis_title = "Total Sales")

# Adding in colour code for graoh
fig.update_traces(marker = dict(color = px.colors.sequential.Reds))

fig.show()

# Create own month and year column with pandas to see if month has any correlation with the data set
df["Year"] = pd.to_datetime(df["InvoiceDate"]).dt.year
df["Quarter"] = df.InvoiceDate.dt.quarter
df["Month"] = pd.to_datetime(df["InvoiceDate"]).dt.month
df["Week"] = pd.to_datetime(df["InvoiceDate"]).dt.isocalendar().week

# Convert InvoiceDate to datetime type
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create a new column IsWeekend based on the day of the week
df["IsWeekend"] = (df["InvoiceDate"].dt.dayofweek >= 5).astype(int)

# To check it worked, uses bool to check if 1 which means yes it is weekend
weekend = df[df["IsWeekend"] == True]

# Check it worked
print(weekend)

#@title Duplicates
# If row duplicated store here
Duplicates = df[df.duplicated(keep=False)]

# There were over 10,000 duplicates, if statement
if len(Duplicates) > 0:
  # Prints the length or count of duplicate rows
  print("Current count of duplicate rows:", len(Duplicates))
  # Droppin doubles
  df = df.drop_duplicates()
# If all duplicates missing or now deleted will show no duplicate found
else:
  print("No duplicate rows found to begin with.")

# If there are still duplicated rows
Duplicates2 = df[df.duplicated(keep=False)]

# There were over 10,000 duplicates, if statement
if len(Duplicates2) > 0:
  # Prints the length or count of duplicate rows
  print("Total count of duplicate rows after current count:", len(Duplicates2))
# If all duplicates missing or now deleted will show no duplicate found
else:
  print("No duplicate rows found, all have been deleted successfully.")

"""Encoding Data"""

df.info()
PreDf = df.copy()
PreDf.info()

# apply label encoding to the columns
df["StockCode"] = le.fit_transform(df["StockCode"])
df["Description"] = le.fit_transform(df["Description"])
df["Country"] = le.fit_transform(df["Country"])
df["Transaction Type"] = le.fit_transform(df["Transaction Type"])

# Sorting data types
df["Year"] = df["InvoiceDate"].dt.year
df["Date"] = df["InvoiceDate"].dt.day
df["Week"] = df["InvoiceDate"].dt.week
df["InvoiceTime"] = df["InvoiceDate"].dt.hour * 60 + df["InvoiceDate"].dt.minute

# Make Range between Max and min
AllDates = pd.date_range(start = StartDate, end = EndDate, freq = "D").date

# Dates between max and min
IncludedDates = df["InvoiceDate"].dt.date.unique()

# Dates not included in df
MissingDates = np.setdiff1d(AllDates, IncludedDates)

# All Missing Dates
print("Dates where there were no invoices sold:\n\n", MissingDates)

"""# Heatmap"""

# Heatmap, df.correlation anlaysis on whole df
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df.corr(), vmin = -1, vmax = 1, annot = True)

# Grouping columns and adding them based on the columns in brackets
grouped_df = df.groupby(["StockCode", "IsWeekend", "Date", "Year", "Month", "Week", "Country"]).agg({"TotalPrice": "sum", "Quantity": "sum"})

# Resets index
grouped_df = grouped_df.reset_index()

grouped_df.isnull().sum()

"""# Data analysis (Sales)"""

# Compute the total monthly sales
WeeklySales = df.groupby(["Year", "Week"])["Quantity"].sum().reset_index()

# Plot the historical monthly sales with year hue
plt.figure(figsize=(10, 5))
sns.lineplot(x="Week", y="Quantity", hue="Year", data=WeeklySales)
plt.xlabel("Week")
plt.ylabel("Total Sales")
plt.title("Historical Weekly Sales")
plt.legend(title="Year")
plt.show()

# Compute the total monthly sales
MonthlySales = df.groupby(["Year", "Month"])["Quantity"].sum().reset_index()

# Plot the historical monthly sales with year hue
plt.figure(figsize=(10, 5))
sns.lineplot(x="Month", y="Quantity", hue ="Year", data=MonthlySales)
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Historical Monthly Sales")
plt.legend(title="Year")
plt.show()

# Heatmap, df.correlation anlaysis on whole df
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(grouped_df.corr(), vmin = -1, vmax = 1, annot = True)

FullDf = df.copy()
df= df.drop(["CustomerID"], axis=1)
df= df.drop(["InvoiceNo"], axis=1)
df.info()

"""# Train test split"""

from sklearn.model_selection import train_test_split

# Dropping as no needed
X = df.drop(["InvoiceDate"],axis=1)

# Target Variable, predict sales
y = df.TotalPrice
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25, shuffle=False)
print(X_train)
X_test.info()

"""# Machine Learning Algorithm 1 (Inventory Sales Forecasting)"""

df.isnull().sum()

# Import necessary libraries
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Trained and evaluated different regression models
models = [LinearRegression(), DecisionTreeRegressor(), XGBRegressor()]

# For loop to print over each model
for model in models:
    # Train
    model.fit(X_train, y_train)
    # Predict
    y_pred = model.predict(X_test)
    # Check accuracy RMSE and R^2 scores
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)
    print(f"{type(model).__name__}: RMSE={rmse}, R^2={r2}")

    # Calculate the forecasted values
    if isinstance(model, LinearRegression):
        forecast = model.predict(X_test)

    # Plot predicted vs actual valuess
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual values")
    plt.ylabel("Predicted values")
    # Title wiht model name
    plt.title(f"{type(model).__name__} Predicted vs Actual Values")

    # Add a line diagonally to aid visulisation
    min_value = min(y_test.min(), y_pred.min())
    max_value = max(y_test.max(), y_pred.max())
    plt.plot([min_value, max_value], [min_value, max_value], "r--")
    plt.show()

# library needed
from plotly.subplots import make_subplots

# Function to show graph
def ShowMe(date, true, preds):
    # Plots
    fig = make_subplots(rows=1, cols=1)

    # Adding the true values to the graph
    fig.add_trace(go.Scatter(x = date, y = true.iloc[:, 0], mode = "lines", marker = dict(color = "#783242"), name = "True"))
    # Addes forcasted values to the graph
    fig.add_trace(go.Scatter(x = date, y = preds.iloc[:, 0], mode="lines", name = "Preds"))

    # Tidying up the graph
    fig.update_layout(
        xaxis = dict(title = "Date"),
        yaxis = dict(title = "TotalPrice"),
        title = "Forecasted Values vs True Values"
    )

    fig.show()

# If else codnition for graph with forcasted values ontop of actual
if isinstance(model, LinearRegression):
    forecast = model.predict(X_test.drop("forecast", axis=1))
else:
    forecast = model.predict(X_test)

# Created a new DataFrame for the forecasted values
ForecastDF = pd.DataFrame({"Date": X_test["Date"], "forecast": forecast})

# Combine the forecasted values with the historical data
CombinedDF = pd.concat([df, ForecastDF], ignore_index=True)

# Split the combined DataFrame into true and predicted values based on the splitter index
splitter = round(len(df) * 0.75)
true = CombinedDF.loc[splitter:, ["Date", "TotalPrice"]].groupby("Date").mean()
preds = CombinedDF.loc[splitter:, ["Date", "forecast"]].groupby("Date").mean()

# Plot the true and predicted values
ShowMe(true.index, true, preds)

PreDf.info()

"""# Market basket analysis"""

#@title Checking if there are orders with multiple products
# Stores dublicate InvoiceNo
DuplicateInvoices = PreDf[PreDf.duplicated(["InvoiceNo"], keep=False)]

# If duplicated prints count in pDuplicateInvoice
if len(DuplicateInvoices) > 0:
    print("Total count of duplicate InvoiceNo:", len(DuplicateInvoices["InvoiceNo"].unique()))
    # If non print non
else:
    print("No duplicate InvoiceNo found.")

# Same but for InvoiceNo and Description, shos if potetioal for analysis
DuplicateInvoices = PreDf[PreDf.duplicated(["InvoiceNo", "Description"], keep=False)]

if len(DuplicateInvoices) > 0:
    duplicate_counts = DuplicateInvoices["InvoiceNo"].value_counts()
    # Counts total Invoices with different description
    count = sum(duplicate_counts >= 2)
    print("Count of invoices with 2 or more products based on different descriptions:", count)
else:
    print("No duplicate InvoiceNo found.")

DuplicateRows = PreDf[PreDf.duplicated(keep=False)]

if len(DuplicateRows) > 0:
    print("Total count of duplicate rows:", len(DuplicateRows))
else:
    print("No duplicate rows found.")

DuplicateInvoices = PreDf[PreDf.duplicated(["Description"], keep=False)]

if len(DuplicateInvoices) > 0:
    duplicate_counts = DuplicateInvoices["Description"].value_counts()
    count = sum(duplicate_counts >= 2)
    print("Count of invoices with the same description but different InvoiceNo:", count)
else:
    print("No duplicate invoices with the same description found.")

#@title Aprori Algorithm (Recommended products result)

# basket or group
basket = (PreDf.groupby(["InvoiceNo", "Description"])["Quantity"]
          .sum().unstack().reset_index().fillna(0)
          .set_index("InvoiceNo"))

# Convert the quantity values to 0 or 1
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)

# Apriori algorithm finds frequent itemsets, low min support as only a small % of sales can come here
frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Sort by descending order
rules = rules.sort_values(by = "confidence", ascending=False)

# Print the top 10 association rules
top_rules = rules.head(10)
print("Top 10 association rules:")
print(top_rules[["antecedents", "consequents", "support", "confidence", "lift"]])

# Gets the top items frequently together
top_items = top_rules["antecedents"].tolist() + top_rules["consequents"].tolist()
top_items = list(set(top_items))  # Remove duplicates

# Print the top items frequently together
print("\nTop items frequently paired together:\n")
if len(top_items) >= 2:
    for itemset in top_items:
        if len(itemset) >= 2:
            print(", ".join(itemset))
else:
    print("\nNo frequent itemsets with 2 or more items found.")