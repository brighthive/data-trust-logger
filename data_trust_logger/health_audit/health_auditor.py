import json
import os
from threading import Thread
from time import sleep
from sqlalchemy import create_engine

from data_trust_logger.config import ConfigurationFactory
from data_trust_logger.health_audit.data_resources_collector import \
    instantiate_data_resources_collector
from data_trust_logger.health_audit.mci_collector import \
    instantiate_mci_collector

config = ConfigurationFactory.from_env()

class HealthAuditor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def audit(self):
        mci_engine = create_engine(config.mci_psql_uri)
        data_resources_engine = create_engine(config.dr_psql_uri)

        while True:
            mci_collector = instantiate_mci_collector(mci_engine)
            mci_metrics = mci_collector.collect_metrics()
            
            data_resources_collector = instantiate_data_resources_collector(data_resources_engine)
            data_resources_metrics = data_resources_collector.collect_metrics()

            metrics_blob = {
                "mci_metrics" : mci_metrics,
                "data_resources_metrics": data_resources_metrics
            }

            with open('/tmp/metrics_blob.json.tmp', 'w+') as f:
                json.dump(metrics_blob, f)
            
            os.replace('/tmp/metrics_blob.json.tmp', '/tmp/metrics_blob.json')

            sleep(60)
