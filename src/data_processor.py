import pandas as pd


def load_network_data(file_path: str) -> pd.DataFrame:
    """
    Load network activity data from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    except Exception as error:
        raise RuntimeError(f"Could not load dataset: {error}")


def clean_network_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning and preparation of network data.
    """
    cleaned_data = data.copy()

    # Remove completely empty rows
    cleaned_data = cleaned_data.dropna(how="all")

    # Remove duplicate records
    cleaned_data = cleaned_data.drop_duplicates()

    # Reset row numbering
    cleaned_data = cleaned_data.reset_index(drop=True)

    return cleaned_data
def inspect_network_data(data: pd.DataFrame) -> None:
    """
    Display basic information about the network dataset.
    """
    print("\nDataset Shape:", data.shape)

    print("\nColumns:")
    print(data.columns.tolist())

    print("\nMissing Values:")
    print(data.isnull().sum().sum())

    if "Label" in data.columns:
        print("\nTraffic Labels:")
        print(data["Label"].value_counts())