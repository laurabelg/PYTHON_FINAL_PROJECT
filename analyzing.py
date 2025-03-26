"""Describing the dataset."""

import pandas as pd
import matplotlib.pyplot as plt

def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize the main descriptive statistics."""

    # Define variables of interest for the modelling
    variables = ["gdp_per_capita", "fossil_elec_per_capita", "low_carbon_elec_per_capita"]

    # Define an empty dataframe
    columns = ['Variable', 'Unit', 'Min', 'Max', 'Mean', 'Median', 'SD']
    descriptive_table = pd.DataFrame(columns=columns)

    for var in variables:
        # Check the unit condition for each variable
        if var == "gdp_per_capita":
            unit = "USD - 2011 prices"
        else:
            unit = "kilowatt-hours per person"

        new_data = pd.DataFrame({
                    "Variable": [var],
                    "Unit": [unit],
                    "Min": [round(df[var].min(), 2)],
                    "Max": [round(df[var].max(), 2)],
                    "Mean": [round(df[var].mean(), 2)],
                    "Median": [round(df[var].median(), 2)],
                    "SD": [df[var].std()]
                })
        descriptive_table = pd.concat([descriptive_table, new_data], ignore_index=True)

    return descriptive_table


def plot_histograms(df: pd.DataFrame):
    """Plot histograms for GDP per capita, low-carbon electricity, and fossil fuels electricity."""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Creates a figure with 1 row and 3 columns
    
    # Histogram for GDP per capita
    axes[0].hist(df["gdp_per_capita"], bins=20, color='skyblue', edgecolor='black')
    axes[0].set_xlabel("GDP per capita")
    axes[0].set_title("GDP per capita")
    
    # Histogram for Low-carbon electricity
    axes[1].hist(df["low_carbon_elec_per_capita"], bins=20, color='lightgreen', edgecolor='black')
    axes[1].set_xlabel("Low-carbon electricity generation")
    axes[1].set_title("Low-carbon electricity sources")
    
    # Histogram for Fossil fuels electricity
    axes[2].hist(df["fossil_elec_per_capita"], bins=20, color='salmon', edgecolor='black')
    axes[2].set_xlabel("Fossil fuels electricity generation")
    axes[2].set_title("Fossil fuels electricity sources")
    
    plt.tight_layout()  # Adjust automatically the spaces between the graphs
    plt.show()