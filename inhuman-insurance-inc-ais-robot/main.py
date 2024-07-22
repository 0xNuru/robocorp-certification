from robocorp.tasks import task

from tasks.consume import consume_traffic_data
from tasks.produce import produce_traffic_data



@task
def produce():
    produce_traffic_data()

@task
def consume():
    consume_traffic_data()

