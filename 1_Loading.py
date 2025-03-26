"""Loading the files directly from Our World in Data and ISO-3166 repositories by using web scraping techniques."""

import requests
import pandas as pd

def fetch_data(url: str) -> str:
    """Fetch a URL and return the content of the associated HTTP response."""
    if not url.endswith(".csv"):
        raise ValueError("URL must point to a CSV file.")
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    return response.text  # Return the content from the url as text

def read_data(csv_content: str) -> pd.DataFrame:
    """Convert CSV text content into a pandas DataFrame."""
    df = pd.read_csv(csv_content)
    return df

def load_data(url: str) -> pd.DataFrame:
    """Fetch CSV data from URL and return it as a DataFrame."""
    raw_data = fetch_data(url)
    return read_data(raw_data)
