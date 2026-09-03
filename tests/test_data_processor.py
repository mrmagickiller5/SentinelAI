import sys
from pathlib import Path

import pandas as pd

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.data_processor import (
    load_network_data,
    clean_network_data,
    inspect_network_data
)

MORNING_FILE = ROOT_DIR / "data" / "Friday-WorkingHours-Morning.pcap_ISCX.csv"
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DDOS_FILE = DATA_DIR / "Friday-WorkingHours-Afternoon-DDos_pcap_ISCX.csv"


def test_load_morning_data():
    data = load_network_data(MORNING_FILE)

    assert isinstance(data, pd.DataFrame)
    assert data.shape[0] > 0
    assert data.shape[1] == 79


def test_load_ddos_data():
    data = load_network_data(DDOS_FILE)

    assert isinstance(data, pd.DataFrame)
    assert data.shape[0] > 0
    assert data.shape[1] == 79


def test_clean_morning_data():
    data = load_network_data(MORNING_FILE)
    cleaned_data = clean_network_data(data)

    assert isinstance(cleaned_data, pd.DataFrame)
    assert cleaned_data.shape[0] > 0


def test_clean_ddos_data():
    data = load_network_data(DDOS_FILE)
    cleaned_data = clean_network_data(data)

    assert isinstance(cleaned_data, pd.DataFrame)
    assert cleaned_data.shape[0] > 0