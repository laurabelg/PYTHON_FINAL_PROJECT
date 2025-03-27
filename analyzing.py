"""Describing and analyzing the dataset."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats

# Define variables of interest for the modelling
variables = ["gdp_per_capita", "fossil_elec", "lowcarbon_elec"]

def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize the main descriptive statistics."""

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
                    "SD": [round(df[var].std(), 2)]
                })
        descriptive_table = pd.concat([descriptive_table, new_data], ignore_index=True)

    return descriptive_table


def plot_histograms(df: pd.DataFrame):
    """Plot histograms for GDP per capita, low-carbon electricity, and fossil fuels electricity."""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Creates a figure with 1 row and 3 columns

    # Define variables to iterate
    colors = ["skyblue", "lightgreen", "salmon"]
    xlabels = ["GDP per capita", "Low-carbon electricity generation", "Fossil fuels electricity generation"]
    titles = ["GDP per capita", "Low-carbon electricity sources", "Fossil fuels electricity sources"]

    for var, color, label, title, ax in zip(variables, colors, xlabels, titles, axes):

        # Histogram
        ax.hist(df[var], bins=20, color = color, edgecolor='black')
        ax.set_xlabel(label)
        ax.set_title(title)
    
    # Show graphics
    plt.tight_layout()  # Adjust automatically the spaces between the graphs
    plt.show()


def plot_scatterplots(df: pd.DataFrame):
    """Plot scatterplots for low-carbon electricity and fossil fuels electricity over GDP per capita."""

    # Define the style of the graph
    sns.set_style("whitegrid")

    # Creates a figure with 1 row and 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(12, 5)) 

    # Graph 1: Fossil fuels vs GDP per capita
    sns.scatterplot(
        data=df,
        x="log_fossil_elec",
        y="log_gdp_per_capita",
        hue="region",
        ax=axes[0],
        palette="tab10",
        legend=True  
    )
    axes[0].set_xlabel("Fossil fuels electricity generation (log)")
    axes[0].set_ylabel("GDP per capita (log)")
    axes[0].set_title("Fossil Fuels vs GDP")

    # Graph 2: Low-carbon electricity vs GDP per capita
    sns.scatterplot(
        data=df,
        x="log_lowcarbon_elec",
        y="log_gdp_per_capita",
        hue="region",
        ax=axes[1],
        palette="tab10",
        legend=True 
    )
    axes[1].set_xlabel("Low-carbon electricity generation (log)")
    axes[1].set_ylabel("GDP per capita (log)")
    axes[1].set_title("Low-Carbon Electricity vs GDP")

    # Show graphics
    plt.tight_layout()
    plt.show()


def calculate_p_values(df: pd.DataFrame):
    """Compute the p-value matrix for correlation significance testing."""
    df_cols = df.columns
    p_matrix = pd.DataFrame(np.ones((len(df_cols), len(df_cols))), columns=df_cols, index=df_cols)
    
    for i in range(len(df_cols)):
        for j in range(i+1, len(df_cols)):  # Avoid redundant calculations
            _, p = stats.pearsonr(df.iloc[:, i], df.iloc[:, j])
            p_matrix.iloc[i, j] = p
            p_matrix.iloc[j, i] = p  # Symmetric matrix
    
    return p_matrix


def correlation_matrix(df: pd.DataFrame):
    """Calculate and visualize the correlation matrix with significance levels."""

    # Select variables of interest for the correlation matrix - excluding category variables
    numeric_variables = ["gdp_per_capita",
                        "fossil_elec",
                        "lowcarbon_elec",
                        "per_capita_electricity",
                        "greenhouse_gas_emissions_per_capita",
                        "carbon_intensity_elec",
                        "electricity_demand_per_capita",
                        "nuclear_elec_per_capita",
                        "renewables_elec_per_capita",
                        "other_renewables_elec_per_capita"]
    
    df_num_var = df[numeric_variables].copy()
    
    # Calculate the correlation matrix
    cor_matrix = df_num_var.corr(method="pearson")

    # Calculate the p-value matrix with the 99% confidence level
    p_matrix = calculate_p_values(df_num_var)

    # Setting the figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Agregate the asterisk for the significant variables (p > 0.01)
    for i in range(cor_matrix.shape[0]):
        for j in range(i):
            if p_matrix.iloc[i, j] < 0.01:  # Show "*" if p < 0.01
                plt.text(j + 0.5, i + 0.5, "*", ha='left', va='bottom', color='white', fontsize=12, fontweight='bold')

    # Create the heatmap
    mask = np.triu(np.ones_like(cor_matrix, dtype=bool))  # Hide the upper triangle
    sns.heatmap(
        cor_matrix,
        mask=mask,
        cmap="RdBu_r",
        annot=True, 
        center=0,
        linewidths=0.5, 
        cbar_kws={"shrink": 0.7}, 
        ax=ax,
        annot_kws={"size": 10, "weight": "bold"},
        fmt=".2f",
        vmin=-1, vmax=1
    )

    # Labels
    plt.xticks(rotation=45, ha="right", fontsize=10, color="black")
    plt.yticks(rotation=0)
    plt.title("Correlation Matrix", fontsize=14, fontweight="bold")

    # Show graphics
    plt.show()

def balance_panel(df:pd.DataFrame):
    """Exclude countries with no data for the variables of interest."""

    # Identified countries which have at least one year without data or 0 on the variables of interest
    countries_to_remove = df.groupby("country")[variables].apply(lambda x: (x == 0).any()).any(axis=1)

    # Filtrer only by the countries with complete data
    cleaned_df = df[~df["country"].isin(countries_to_remove[countries_to_remove].index)]

    print(f"It was removed {countries_to_remove.sum()} countries with at least one year with missing data or 0 on the variables of interest.")

    return cleaned_df