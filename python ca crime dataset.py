import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------- Load Dataset ------------------------
DATA_PATH = "C:\\Users\\hp\\Downloads\\Crime_Data_from_2020_to_Present.csv"  # Replace with actual path if needed

print("Loading CSV file...")
df = pd.read_csv(DATA_PATH)
print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns")

# ---------------------- Basic Overview ----------------------
print("\nBasic Info:")
print(df.info())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# ---------------------- Data Cleaning -----------------------
print("\nCleaning Data...")
df_cleaned = df.dropna(subset=["Date Rptd", "TIME OCC", "Crm Cd Desc", "AREA NAME"])
df_cleaned["Date Rptd"] = pd.to_datetime(df_cleaned["Date Rptd"], errors="coerce")
df_cleaned["TIME OCC"] = df_cleaned["TIME OCC"].astype(str).str.zfill(4)

# ---------------------- Set Plot Style -----------------------
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ---------------------- Visualization Functions -----------------------

def plot_top_crimes():
    print("\nTop 10 Reported Crimes...")
    top_crimes = df_cleaned["Crm Cd Desc"].value_counts().head(10)
    sns.barplot(x=top_crimes.values, y=top_crimes.index, color="salmon")
    plt.title("Top 10 Most Reported Crimes")
    plt.xlabel("Number of Reports")
    plt.ylabel("Crime Type")
    plt.show()

def plot_crimes_over_time():
    print("\nCrime Trend Over Time...")
    crime_trend = df_cleaned.groupby(df_cleaned["Date Rptd"].dt.to_period("M")).size()
    crime_trend.index = crime_trend.index.to_timestamp()
    plt.plot(crime_trend.index, crime_trend.values, color="steelblue", marker="o")
    plt.title("Monthly Crime Trend")
    plt.ylabel("Crime Count")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_crimes_by_area():
    print("\nCrime Count by Area...")
    area_counts = df_cleaned["AREA NAME"].value_counts().head(10)
    sns.barplot(x=area_counts.values, y=area_counts.index, color="skyblue")
    plt.title("Top 10 Crime-Prone Areas")
    plt.xlabel("Number of Crimes")
    plt.ylabel("Area")
    plt.show()

def plot_hourly_distribution():
    print("\nCrimes by Hour of Day...")
    df_cleaned["Hour"] = df_cleaned["TIME OCC"].str[:2].astype(int)
    hourly = df_cleaned["Hour"].value_counts().sort_index()
    plt.plot(hourly.index, hourly.values, color="green", marker="o")
    plt.xticks(range(0, 24))
    plt.title("Crimes by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Crime Count")
    plt.grid(True)
    plt.show()

def plot_heatmap_area_vs_crime():
    print("\nHeatmap of Area vs Crime Type...")
    
    # Get top 10 areas and top 15 crime types
    top_areas = df_cleaned["AREA NAME"].value_counts().head(10).index
    top_crimes = df_cleaned["Crm Cd Desc"].value_counts().head(15).index

    df_filtered = df_cleaned[df_cleaned["AREA NAME"].isin(top_areas) & df_cleaned["Crm Cd Desc"].isin(top_crimes)]

    pivot = df_filtered.pivot_table(index="AREA NAME", columns="Crm Cd Desc", aggfunc="size", fill_value=0)

    print("Pivot shape:", pivot.shape)  # Debug print to confirm data is present

    sns.heatmap(pivot, cmap="coolwarm", linewidths=0.5, annot=True, fmt="d")
    plt.title("Crime Types by Area (Heatmap)")
    plt.xlabel("Crime Type")
    plt.ylabel("Area Name")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# ------------------ Interactive Menu -----------------------

def run_interactive_analysis():
    while True:
        print("\n" + "="*50)
        print("LAPD CRIME DATA ANALYSIS MENU")
        print("="*50)
        print("1. Basic Statistics")
        print("2. Top Crimes")
        print("3. Crime Trend Over Time")
        print("4. Crimes by Area")
        print("5. Hourly Crime Distribution")
        print("6. Area vs Crime Heatmap")
        print("7. Run All")
        print("0. Exit")

        choice = input("\nEnter your choice (0-7): ")
        if choice == '1':
            print(df_cleaned.describe(include='all'))
        elif choice == '2':
            plot_top_crimes()
        elif choice == '3':
            plot_crimes_over_time()
        elif choice == '4':
            plot_crimes_by_area()
        elif choice == '5':
            plot_hourly_distribution()
        elif choice == '6':
            plot_heatmap_area_vs_crime()
        elif choice == '7':
            plot_top_crimes()
            plot_crimes_over_time()
            plot_crimes_by_area()
            plot_hourly_distribution()
            plot_heatmap_area_vs_crime()
        elif choice == '0':
            print("\nThank you for using the LAPD Crime Data Analysis Tool!")
            break
        else:
            print("Invalid choice. Try again!")

# ---------------------- MAIN ----------------------------

run_interactive = input("\nDo you want to run interactive analysis? (y/n): ")
if run_interactive.lower() == 'y':
    run_interactive_analysis()
else:
    print("You Entered Wrong Input , Now You Have To Face So Many Graphs And All")
    plot_top_crimes()
    plot_crimes_over_time()
    plot_crimes_by_area()
    plot_hourly_distribution()
    plot_heatmap_area_vs_crime()
    print("\nAll analysis complete!")
