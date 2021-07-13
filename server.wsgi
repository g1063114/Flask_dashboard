import sys
import os
sys.path.insert(0,'C:\projects\Flask_dashboard\dashboard')
os.environ['APP_CONFIG_FILE'] = 'C:\projects\Flask_dashboard\config\production.py'

from dashboard import create_app
application = create_app()