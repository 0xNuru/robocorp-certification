import json
import os

from dotenv import load_dotenv
from robocorp import workitems
from RPA.HTTP import HTTP

from schema.api import Payload

load_dotenv()

http = HTTP()

RATE_KEY = "NumericValue"
MAX_RATE = 5.0
GENDER_KEY = "Dim1"
COUNTRY_KEY = "SpatialDim"
YEAR_KEY = "TimeDim"
BOTH_GENDERS = "BTSX"

def produce_traffic_data():
    try:
        http.download(
        url=os.getenv("TRAFFIC_DATA_DOWNLOAD_URL"),
        target_file="output/traffic.json",
        overwrite=True,
        )
    except Exception as e:
        print(f"Failed to download traffic data: {e} \n" * 3)
        return

    traffic_data = load_traffic_data_table()
    filtered_and_sorted_traffic_data = filter_and_sort_traffic_data(traffic_data)
    payloads = create_payloads(filtered_and_sorted_traffic_data)
    save_work_item_payloads(payloads)

    print("produce")


def load_traffic_data_table():
    """load traffic data from json into a table"""
    with open(os.getenv("TRAFFIC_DATA_JSON_PATH")) as file:
        data = json.load(file)

    return data["value"]

def filter_and_sort_traffic_data(data):
    data = [item for item in data if item[RATE_KEY] < MAX_RATE and item[GENDER_KEY] == BOTH_GENDERS]
    data = sorted(data, key= lambda x: (-x[YEAR_KEY], x[COUNTRY_KEY]))
    latest_data = {}
    for item in data:
        country = item[COUNTRY_KEY]
        if country not in latest_data:
            latest_data[country] = item
    
    latest_data_list = list(latest_data.values())
    
    return latest_data_list

def create_payloads(data) -> list:
    payloads = []
    for item in data:
        payloads.append({
            "year": item[YEAR_KEY],
            "country": item[COUNTRY_KEY],
            "rate": item[RATE_KEY],
        })
    return payloads

def save_work_item_payloads(payloads):
    for payload in payloads:
        work_item = dict(payload)
        workitems.outputs.create(work_item)
    
        

