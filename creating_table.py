"""Cleaning the energy and country database to create the main database to analyze."""

import pandas as pd

def table_energy(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the energy dataset."""

    # Define the list with the variables of interest
    selected_columns = [
        "country", "iso_code", "year", "population", "gdp", "carbon_intensity_elec",
        "electricity_demand", "fossil_elec_per_capita", "greenhouse_gas_emissions",
        "low_carbon_elec_per_capita", "nuclear_elec_per_capita",
        "other_renewables_elec_per_capita", "per_capita_electricity",
        "renewables_elec_per_capita"
    ]
    energy_df = df[selected_columns].copy()

    # Filter by countries with completed data from 2000 to 2022
    energy_df = energy_df[
        (energy_df["year"] >= 2000) & 
        (energy_df["iso_code"] != "") &
        (~energy_df["gdp"].isna()) & (~energy_df["gdp"].eq("")) &
        (~energy_df["low_carbon_elec_per_capita"].isna()) & (~energy_df["low_carbon_elec_per_capita"].eq("")) &
        (~energy_df["fossil_elec_per_capita"].isna()) & (~energy_df["fossil_elec_per_capita"].eq(""))
    ]

    # Create additional variables
    energy_df["gdp_per_capita"] = energy_df["gdp"] / energy_df["population"]
    energy_df["greenhouse_gas_emissions_per_capita"] = (energy_df["greenhouse_gas_emissions"] / energy_df["population"]) * 1000000  # Convert Megatones to tones
    energy_df["electricity_demand_per_capita"] = energy_df["electricity_demand"] / energy_df["population"]

    # Replace NaN with 0
    energy_df = energy_df.fillna(0)

    return energy_df

def table_country(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the country dataset."""

    # Define the list with the variables of interest
    selected_columns = [
        "alpha-3", "region", "sub-region"
    ]
    country_df = df[selected_columns].copy()
    country_df.rename(columns={"alpha-3": "iso_code"}, inplace=True)

    return country_df

def main_table(energy_df: pd.DataFrame, country_df:pd.DataFrame) -> pd.DataFrame:
        
    energy_df = table_energy(energy_df)
    country_df = table_country(country_df)
    main_df = pd.merge(energy_df, country_df, on="iso_code", how="left") 

    # Sort df by year and country
    main_df = main_df.sort_values(by=["country", "year"]).reset_index(drop=True)

    # Convert the categorical variables as 'category'
    main_df['country'] = main_df['country'].astype('category')
    main_df['year'] = main_df['year'].astype('category')
    main_df['region'] = main_df['region'].astype('category')
    main_df['sub-region'] = main_df['sub-region'].astype('category')

    return main_df