# Campus Energy Dashboard Capstone Project
# This script builds a complete dashboard pipeline for analyzing campus electricity usage.
# Assumes CSV files are in a /data/ directory, each with columns: Date, Building, KWH (adjust if needed).
# If /data/ doesn't exist, create it and add sample CSVs or use the provided sample data generation.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
from datetime import datetime

# Task 1: Data Ingestion and Validation
def ingest_data(data_dir='data'):
    """
    Reads multiple CSV files from the data directory, combines them into one DataFrame,
    handles missing files and corrupt data.
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"Warning: {data_dir} directory not found. Creating sample data for demonstration.")
        # Generate sample data if no directory exists
        generate_sample_data(data_dir)
    
    df_combined = pd.DataFrame()
    for csv_file in data_path.glob('*.csv'):
        try:
            df = pd.read_csv(csv_file, on_bad_lines='skip')  # Skip bad lines
            # Add metadata if not present
            if 'Building' not in df.columns:
                df['Building'] = csv_file.stem  # Use filename as building name
            if 'Month' not in df.columns:
                df['Month'] = pd.to_datetime(df['Date']).dt.month
            df_combined = pd.concat([df_combined, df], ignore_index=True)
            print(f"Successfully loaded: {csv_file.name}")
        except FileNotFoundError:
            print(f"File not found: {csv_file.name}")
        except Exception as e:
            print(f"Error loading {csv_file.name}: {e}")
    
    # Validate and clean
    df_combined['Date'] = pd.to_datetime(df_combined['Date'], errors='coerce')
    df_combined.dropna(subset=['Date', 'KWH'], inplace=True)
    df_combined.set_index('Date', inplace=True)
    return df_combined

def generate_sample_data(data_dir):
    """
    Generates sample CSV files for demonstration if no data directory exists.
    """
    os.makedirs(data_dir, exist_ok=True)
    buildings = ['Library', 'Dormitory', 'Cafeteria']
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    for building in buildings:
        data = {
            'Date': dates,
            'Building': [building] * len(dates),
            'KWH': np.random.randint(100, 500, len(dates))
        }
        df = pd.DataFrame(data)
        df.to_csv(f'{data_dir}/{building}.csv', index=False)

# Task 2: Core Aggregation Logic
def calculate_daily_totals(df):
    """Calculate daily totals across all buildings."""
    return df.resample('D')['KWH'].sum()

def calculate_weekly_aggregates(df):
    """Calculate weekly aggregates."""
    return df.resample('W')['KWH'].sum()

def building_wise_summary(df):
    """Generate summary per building: mean, min, max, total."""
    return df.groupby('Building')['KWH'].agg(['mean', 'min', 'max', 'sum'])

# Task 3: Object-Oriented Modeling
class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []
    
    def add_reading(self, timestamp, kwh):
        self.meter_readings.append(MeterReading(timestamp, kwh))
    
    def calculate_total_consumption(self):
        return sum(reading.kwh for reading in self.meter_readings)
    
    def generate_report(self):
        total = self.calculate_total_consumption()
        avg = total / len(self.meter_readings) if self.meter_readings else 0
        return f"Building: {self.name}, Total KWH: {total}, Average KWH: {avg:.2f}"

class BuildingManager:
    def __init__(self):
        self.buildings = {}
    
    def add_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
    
    def add_reading_to_building(self, building_name, timestamp, kwh):
        self.add_building(building_name)
        self.buildings[building_name].add_reading(timestamp, kwh)
    
    def get_all_reports(self):
        return [building.generate_report() for building in self.buildings.values()]

# Task 4: Visual Output with Matplotlib
def create_dashboard(df):
    """Create a dashboard with trend line, bar chart, and scatter plot."""
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    
    # Trend Line: Daily consumption over time for all buildings
    daily_totals = calculate_daily_totals(df)
    axs[0, 0].plot(daily_totals.index, daily_totals.values)
    axs[0, 0].set_title('Daily Consumption Trend')
    axs[0, 0].set_xlabel('Date')
    axs[0, 0].set_ylabel('Total KWH')
    
    # Bar Chart: Average weekly usage across buildings
    weekly_building = df.groupby('Building').resample('W')['KWH'].mean().unstack(level=0)
    weekly_building.mean().plot(kind='bar', ax=axs[0, 1])
    axs[0, 1].set_title('Average Weekly Usage by Building')
    axs[0, 1].set_xlabel('Building')
    axs[0, 1].set_ylabel('Average KWH')
    
    # Scatter Plot: Peak-hour consumption (assuming random for demo; adjust for real peak hours)
    # For simplicity, scatter KWH vs. day of week
    df['DayOfWeek'] = df.index.dayofweek
    axs[1, 0].scatter(df['DayOfWeek'], df['KWH'])
    axs[1, 0].set_title('Consumption vs. Day of Week')
    axs[1, 0].set_xlabel('Day of Week')
    axs[1, 0].set_ylabel('KWH')
    
    # Empty subplot or additional plot (e.g., histogram)
    axs[1, 1].hist(df['KWH'], bins=20)
    axs[1, 1].set_title('KWH Distribution')
    axs[1, 1].set_xlabel('KWH')
    axs[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('dashboard.png')
    plt.show()

# Task 5: Persistence and Executive Summary
def export_data(df, building_summary):
    """Export cleaned data and summary."""
    df.to_csv('cleaned_energy_data.csv')
    building_summary.to_csv('building_summary.csv')

def generate_summary(df, building_summary):
    """Generate a text summary."""
    total_campus = df['KWH'].sum()
    highest_building = building_summary['sum'].idxmax()
    peak_load_time = df['KWH'].idxmax()  # Assuming max KWH as peak
    weekly_trends = calculate_weekly_aggregates(df).describe()
    
    summary = f"""
Campus Energy Usage Summary
===========================
Total Campus Consumption: {total_campus} KWH
Highest-Consuming Building: {highest_building}
Peak Load Time: {peak_load_time}
Weekly Trends (Mean: {weekly_trends['mean']:.2f}, Max: {weekly_trends['max']:.2f})
Daily Trends: See dashboard for visualizations.
"""
    with open('summary.txt', 'w') as f:
        f.write(summary)
    print(summary)

# Main Execution
if __name__ == "__main__":
    # Task 1
    df_combined = ingest_data()
    
    # Task 2
    daily_totals = calculate_daily_totals(df_combined)
    weekly_aggregates = calculate_weekly_aggregates(df_combined)
    building_summary = building_wise_summary(df_combined)
    
    # Task 3
    manager = BuildingManager()
    for _, row in df_combined.iterrows():
        manager.add_reading_to_building(row['Building'], row.name, row['KWH'])
    reports = manager.get_all_reports()
    for report in reports:
        print(report)
    
    # Task 4
    create_dashboard(df_combined)
    
    # Task 5
    export_data(df_combined, building_summary)
    generate_summary(df_combined, building_summary)
    
    print("Dashboard pipeline complete. Files exported: cleaned_energy_data.csv, building_summary.csv, summary.txt, dashboard.png")
