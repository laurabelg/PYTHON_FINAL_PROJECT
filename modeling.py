"Creating the regression models."

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS, PooledOLS


def regression_models(df:pd.DataFrame):
    """Run the OLS and Fixed Effects regressions and display results in a single table."""

    # Define the dataframe as panel data
    df["year"] = pd.to_numeric(df["year"], errors="coerce")  # Convert year to numeric
    df.set_index(["country", "year"], inplace=True)

    # Model Pooled OLS
    pooled_model = PooledOLS.from_formula("log_gdp_per_capita ~ log_lowcarbon_elec + log_fossil_elec", data=df)
    pooled_results = pooled_model.fit()
    df["residuals_OLS"] = pooled_results.resids.reindex(df.index)

    # Model Fixed Effects (country)
    fe_i_model = PanelOLS.from_formula("log_gdp_per_capita ~ log_lowcarbon_elec + log_fossil_elec + EntityEffects",
                                    data=df)
    fe_i_results = fe_i_model.fit()
    df["residuals_fe_i"] = fe_i_results.resids.reindex(df.index)

    # Model Fixed Effects (year)
    fe_t_model = PanelOLS.from_formula("log_gdp_per_capita ~ log_lowcarbon_elec + log_fossil_elec + TimeEffects",
                                    data=df)
    fe_t_results = fe_t_model.fit()
    df["residuals_fe_t"] = fe_t_results.resids.reindex(df.index)

    # Create a DataFrame with the coefficients, standard errors and p-values
    results_df = pd.DataFrame({
        "Pooled OLS": pooled_results.params,
        "FE Country": fe_i_results.params,
        "FE Year": fe_t_results.params
    }).round(4)

    std_errors = pd.DataFrame({
        "Pooled OLS": pooled_results.std_errors,
        "FE Country": fe_i_results.std_errors,
        "FE Year": fe_t_results.std_errors
    }).round(4)

    p_values = pd.DataFrame({
    "Pooled OLS": pooled_results.pvalues,
    "FE Country": fe_i_results.pvalues,
    "FE Year": fe_t_results.pvalues
    }).round(4)

    # Generate results table with standard errors and p-values in parentheses
    final_table = pd.DataFrame()

    # Create the p-value stars
    def p_value_stars(p_value):
        if p_value < 0.001:
            return "***"
        elif p_value < 0.01:
            return "**"
        elif p_value < 0.05:
            return "*"
        else:
            return ""

    for col in results_df.columns:
        # Applying p-value stars based on the values
        final_table[col] = (
            results_df[col].astype(str) + 
            " (" + std_errors[col].astype(str) + 
            ") [" + p_values[col].apply(p_value_stars).astype(str) + "]"
        )

    # Show results
    print("\nRegression Results - Pooled vs Fixed Effects models") 
    print(final_table)