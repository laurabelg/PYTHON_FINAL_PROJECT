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
    energy_db = df[selected_columns].copy()

    # Filter by countries with completed data from 2000 to 2022
    energy_db = energy_db[
        (energy_db["year"] > 2000) & 
        (energy_db["iso_code"] != "") &
        (~energy_db["gdp"].isna()) & (~energy_db["gdp"].eq("")) &
        (~energy_db["low_carbon_elec_per_capita"].isna()) & (~energy_db["low_carbon_elec_per_capita"].eq("")) &
        (~energy_db["fossil_elec_per_capita"].isna()) & (~energy_db["fossil_elec_per_capita"].eq(""))
    ]

    # Create additional variables
    energy_db["gdp_per_capita"] = energy_db["gdp"] / energy_db["population"]
    energy_db["greenhouse_gas_emissions_per_capita"] = (energy_db["greenhouse_gas_emissions"] / energy_db["population"]) * 1000000  # Convert Megatones to tones
    energy_db["electricity_demand_per_capita"] = energy_db["electricity_demand"] / energy_db["population"]

    # Replace NaN with 0
    energy_db = energy_db.fillna(0)

    return energy_db

def table_country(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the country dataset."""

    # Define the list with the variables of interest
    selected_columns = [
        "name", "alpha-3", "region", "sub-region"
    ]
    country_db = df[selected_columns].copy()
    country_db.rename(columns={"alpha-3": "iso_code"}, inplace=True)

    return country_db

def main_table(energy_db: pd.DataFrame, country_db:pd.DataFrame) -> pd.DataFrame:
        
    main_db = pd.merge(energy_db, country_db, on="iso_code", how="left") 

    # Sort df by year and country
    main_db = energy_db.sort_values(by=["country", "year"]).reset_index(drop=True)

    return main_db