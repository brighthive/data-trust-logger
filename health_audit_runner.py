'''
This script runs the Data Model Manager in its own
thread, separate from the web application that will most likely have multiple
workers.
'''

from threading import Thread

from data_trust_logger.health_audit.health_auditor import HealthAuditor    

health_auditor = HealthAuditor()
health_auditor_thread = Thread(target=health_auditor.audit, args=())
health_auditor_thread.start()