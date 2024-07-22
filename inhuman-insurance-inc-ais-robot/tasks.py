import json
import os

from dotenv import load_dotenv
from robocorp.tasks import task
from robocorp import workitems
from RPA.HTTP import HTTP

load_dotenv()

http = HTTP()

RATE_KEY = "NumericValue"
MAX_RATE = 5.0
GENDER_KEY = "Dim1"
COUNTRY_KEY = "SpatialDim"
YEAR_KEY = "TimeDim"
BOTH_GENDERS = "BTSX"

@task
def produce_traffic_data():
    try:
        http.download(
        url=os.getenv("TRAFFIC_DATA_DOWNLOAD_URL"),
        target_file="output/traffic.json",
        overwrite=True,
        )
    except Exception as e:
        print(f"Failed to download traffic data: {e}")
        return

    traffic_data = load_traffic_data_table()
    filtered_and_sorted_traffic_data = filter_and_sort_traffic_data(traffic_data)
    payloads = create_payloads(filtered_and_sorted_traffic_data)
    save_work_item_payloads(payloads)

    print("produce")

@task
def consume_traffic_data():
    print("consume")

def load_traffic_data_table():
    """load traffic data from json into a table"""
    with open(os.getenv("TRAFFIC_DATA_JSON_PATH")) as file:
        data = json.load(file)

    return tables.create_table(data["value"])

def filter_and_sort_traffic_data(data):
    rate_key = "NumericValue"
    max_rate = 5.0
    gender_key = "Dim1"
    both_genders = "BTSX"
    year_key = "TimeDim"
    tables.filter_table_by_column(data, rate_key, "<", max_rate)
    tables.filter_table_by_column(data, gender_key, "==", both_genders)
    tables.sort_table_by_column(data, year_key, False)


