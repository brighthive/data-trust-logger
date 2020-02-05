import json
from time import sleep
import os

from threading import Thread

from data_trust_logger.health_audit.data_resources_collector import \
    instantiate_data_resources_collector
from data_trust_logger.health_audit.mci_collector import \
    instantiate_mci_collector

class HealthAuditor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def audit(self):
        while True:
            mci_collector = instantiate_mci_collector()
            data_resources_collector = instantiate_data_resources_collector()

            mci_metrics = mci_collector.collect_metrics()
            data_resources_metrics = data_resources_collector.collect_metrics()

            metrics_blob = {
                "mci_metrics" : mci_metrics,
                "data_resources_metrics": data_resources_metrics
            }

            this_directory = os.path.abspath(os.path.dirname(__file__))
            with open(f'{this_directory}/metrics_blob.json', 'w') as f:
                json.dump(metrics_blob, f)

            sleep(60)




