import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

def residuals(df:pd.DataFrame):
    """Plot the residuals."""

    # Define the independent variables and dependent variable
    X = df[['log_lowcarbon_elec', 'log_fossil_elec']]  # Independent variables
    X = sm.add_constant(X)  # Add constant to the model (intercept)
    y = df['log_gdp_per_capita']  # Dependent variable

    # Creates a figure with 1 row and 3 columns
    fig, axes = plt.subplots(1, 3, figsize=(12, 5)) 

    # Plot 1: Residuals vs GDP per capita
    sns.scatterplot(x=df['gdp_per_capita'], y=df['residuals_fe_i'], ax=axes[0])
    axes[0].axhline(y=0, color='black', linestyle='--')
    axes[0].set_xlabel('GDP per capita')
    axes[0].set_ylabel('Residuals (Country FE)')
    axes[0].set_title('Residuals vs GDP per capita')

    # Plot 2: Residuals vs Low carbon electricity generation per capita
    sns.scatterplot(x=df['lowcarbon_elec'], y=df['residuals_fe_i'], ax=axes[1])
    axes[1].axhline(y=0, color='black', linestyle='--')
    axes[1].set_xlabel('Low carbon electricity generation per capita')
    axes[1].set_ylabel('Residuals (Country FE)')
    axes[1].set_title('Residuals vs Low carbon electricity generation')

    # Plot 3: Residuals vs Fossil fuels generation per capita
    sns.scatterplot(x=df['fossil_elec'], y=df['residuals_fe_i'], ax=axes[2])
    axes[2].axhline(y=0, color='black', linestyle='--')
    axes[2].set_xlabel('Fossil fuels generation per capita')
    axes[2].set_ylabel('Residuals (Country FE)')
    axes[2].set_title('Residuals vs Fossil fuels generation')

    # Show the plot
    plt.tight_layout()
    plt.show()