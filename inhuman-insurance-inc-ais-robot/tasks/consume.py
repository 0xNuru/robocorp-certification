import requests
import os

from robocorp import workitems
from dotenv import load_dotenv

from schema.api import Payload

load_dotenv()


def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    process_traffic_data()

def process_traffic_data():
    for item in workitems.inputs:
        try:
            validated_payload = Payload(**item.payload)
            status, json_response = post_traffic_data_to_sales_system(validated_payload)
            if status == 200:
                item.done()
            else:
                item.fail(
                    exception_type="APPLICATION",
                    code= "TRAFFIC_DATA_POST_FAILED",
                    message=json_response["message"],
                )
        except Exception as e:
            item.fail(
                    exception_type="BUSINESS",
                    code= "INVALID_TRAFFIC_DATA",
                    message=item.payload,
            )
            print(f"Invalid payload: {e}")
            continue

def post_traffic_data_to_sales_system(traffic_data: Payload):
    url = os.getenv("SALES_SYSTEM_API")
    if not url:
        print("Sales system API URL is not set in environment variables.")
        return

    try:
        response = requests.post(url, json=traffic_data.model_dump_json())
        response.raise_for_status()
        print(f"Successfully posted traffic data: {traffic_data}")
    except requests.RequestException as e:
        print(f"Failed to post traffic data: {e}")

    return response.status_code, response.json()