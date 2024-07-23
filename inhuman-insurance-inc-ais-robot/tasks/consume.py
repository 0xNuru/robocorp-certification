from robocorp import workitems


def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    process_traffic_data()

def process_traffic_data():
    for item in workitems.inputs:
        print(item)
        traffic_data = item.payload