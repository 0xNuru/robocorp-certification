from robocorp.tasks import task
from RPA.HTTP import HTTP

http = HTTP()

@task
def produce_traffic_data():
    download_traffic_data()
    print("produce")

@task
def consume_traffic_data():
    print("consume")

def download_traffic_data():
    http.download(
        url="https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json",
        target_file="output/traffic.json",
        overwrite=True,
    )