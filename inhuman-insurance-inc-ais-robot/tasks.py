import json
import os

from dotenv import load_dotenv
from robocorp.tasks import task
from RPA.HTTP import HTTP
from RPA.Tables import Tables

load_dotenv()

http = HTTP()
tables = Tables()

@task
def produce_traffic_data():
    http.download(
        url=os.getenv("TRAFFIC_DATA_DOWNLOAD_URL"),
        target_file="output/traffic.json",
        overwrite=True,
    )
    traffic_data_table = load_traffic_data_table()
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


