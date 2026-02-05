
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


os.makedirs("charts", exist_ok=True)
os.makedirs("output", exist_ok=True)


df = pd.read_csv("sales_data.csv")

# Ensure datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.to_period("M")

# Add Age Group
bins = [18, 25, 35, 45, 60, 100]
labels = ["18-25", "26-35", "36-45", "46-60", "60+"]
df['Age_Group'] = pd.cut(df["Age"], bins=bins, labels=labels)

# Add Day Type
df["Day_Type"] = df["Order_Date"].dt.dayofweek.apply(lambda x: "Weekend" if x >=5 else "Weekday")


def plot_bar(x, y, title, xlabel, ylabel, filename=None, colors=None, rotation=0):
    plt.figure(figsize=(10,6))
    if colors is None:
        colors = 'skyblue'
    plt.bar(x, y, color=colors, edgecolor='black')
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation)
    # Add value labels
    for i, val in enumerate(y):
        plt.text(i, val + max(y)*0.01, int(val), ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    if filename:
        plt.savefig(f"charts/{filename}.png", dpi=300)
    plt.show()


total_sales = df['Sales'].sum()
print(f"Total Sales: {total_sales}")
plot_bar(["Total Sales"], [total_sales], "Total Sales", "", "Sales", filename="total_sales")

sales_by_category = df.groupby('Category')['Sales'].sum()
sales_by_category.to_csv("output/sales_by_category.csv")
plot_bar(sales_by_category.index, sales_by_category.values, "Sales by Category", "Category", "Sales",
         filename="sales_by_category")

monthly_sales = df.groupby('Month')['Sales'].sum()
monthly_sales.to_csv("output/monthly_sales.csv")
plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o', color='orange')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=300)
plt.show()


monthly_sales_cat = df.groupby(['Month','Category'])['Sales'].sum().unstack()
monthly_sales_cat.to_csv("output/monthly_sales_by_category.csv")
plt.figure(figsize=(12,6))
bottom = np.zeros(len(monthly_sales_cat))
for cat in monthly_sales_cat.columns:
    plt.bar(monthly_sales_cat.index.astype(str), monthly_sales_cat[cat], bottom=bottom, label=cat)
    bottom += monthly_sales_cat[cat].values
plt.title("Monthly Sales by Category (Stacked)")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.legend(title="Category")
plt.tight_layout()
plt.savefig("charts/monthly_sales_by_category.png", dpi=300)
plt.show()


top_customers = df.groupby('Customer_ID')['Sales'].sum().sort_values(ascending=False).head(10)
top_customers.to_csv("output/top_customers.csv")
plot_bar(top_customers.index.astype(str), top_customers.values, "Top 10 Customers by Sales",
         "Customer ID", "Sales", filename="top_customers", rotation=45, colors='salmon')


age_group_sales = df.groupby('Age_Group')['Sales'].sum()
age_group_sales.to_csv("output/age_group_spending.csv")
plot_bar(age_group_sales.index.astype(str), age_group_sales.values, "Spending by Age Group",
         "Age Group", "Sales", filename="age_group_spending", colors='violet')


city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
city_sales.to_csv("output/city_sales.csv")
plot_bar(city_sales.index.astype(str), city_sales.values, "Sales by City", "City", "Sales",
         filename="city_sales", rotation=45, colors='teal')


best_month = monthly_sales.idxmax()
print(f"Best Month: {best_month}")
colors = ['green' if month == best_month else 'lightblue' for month in monthly_sales.index.astype(str)]
plot_bar(monthly_sales.index.astype(str), monthly_sales.values, "Monthly Sales with Best Month Highlighted",
         "Month", "Sales", filename="best_month", colors=colors, rotation=45)


weekday_weekend = df.groupby('Day_Type')['Sales'].sum()
weekday_weekend.to_csv("output/weekday_vs_weekend.csv")
plot_bar(weekday_weekend.index, weekday_weekend.values, "Weekday vs Weekend Sales",
         "Day Type", "Sales", filename="weekday_vs_weekend", colors=['skyblue','orange'])


with open("output/summary.txt", "w") as f:
    f.write(f"Total Sales: {total_sales}\n")
    f.write(f"Best Month: {best_month}\n")
    f.write(f"City with highest sales: {city_sales.idxmax()}\n")
    f.write(f"Top Customer ID: {top_customers.index[0]}\n")
    f.write(f"Age Group with highest spending: {age_group_sales.idxmax()}\n")

print("Analysis complete! Charts saved in 'charts/' and outputs in 'output/' folder.")
