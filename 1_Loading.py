"""Loading the files directly from Our World in Data repository and  by using webscraping."""

import requests
import pandas as pd

# Define URLs.
url_energy = ("https://github.com/owid/energy-data/blob/master/owid-energy-data.csv")
url_country = ("https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv")


stops = requests.get(f"{base_url}/{stop_suffix}", headers=headers) 



def fetch_data(url: str) -> str:
    """Fetch a URL and the return content of the associated HTTP response."""
    if not url.endswith("csv"):
        raise ValueError(...)
    response = requests.get(url)
    return response.text

def read_data(fetch_url: str) -> pd.DataFrame:
    """Load the csv file from the url and convert it as a pandas dataframe."""
    df = pd.read_csv(fetch_url)
    return df

def load_data(url: str) -> pd.DataFrame:
    raw_data = fetch_data(url)
    read_data(raw_data)
