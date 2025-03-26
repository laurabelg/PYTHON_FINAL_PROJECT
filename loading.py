"""Loading the files directly from Our World in Data and ISO-3166 repositories by using web scraping techniques."""

import requests
import pandas as pd
import io  # Required for StringIO

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
    # Use StringIO to treat the string as a file
    csv_file = io.StringIO(csv_content)
    df = pd.read_csv(csv_file)
    return df

def load_data(url: str) -> pd.DataFrame:
    """Fetch CSV data from URL and return it as a DataFrame."""
    raw_data = fetch_data(url)
    df = read_data(raw_data)
    return df
