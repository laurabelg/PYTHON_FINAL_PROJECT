"""Cleaning the data base"""

def 


#Select the variables of interest
energy_db <- energy %>%
               select("country",
                      "year",
                      "population",
                      "gdp",
                      "carbon_intensity_elec",
                      "electricity_demand",
                      "fossil_elec_per_capita",
                      "greenhouse_gas_emissions",
                      "low_carbon_elec_per_capita",
                      "nuclear_elec_per_capita",
                      "other_renewables_elec_per_capita",
                      "per_capita_electricity",
                      "renewables_elec_per_capita") %>%
              filter(year >= 2005)