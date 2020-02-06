'''
This script runs the Health Auditor in its own thread, 
independent of the Flask application. 
But why? The `cmd.sh` script serves the Flask app with multiple gunicorn workers. 
The Health Auditor should not be served by more than one worker (which would put 
unnecessary load on the MCI and DR APIs).
'''

from threading import Thread

from data_trust_logger.health_audit.health_auditor import HealthAuditor    

health_auditor = HealthAuditor()
health_auditor_thread = Thread(target=health_auditor.audit, args=())
health_auditor_thread.start()