import sys
import os

# Define the project directory
project_dir = os.path.dirname(__file__)
sys.path.insert(0, project_dir)

# Activate the virtual environment
activate_env = os.path.join(project_dir, 'env', 'bin', 'activate_this.py')
with open(activate_env) as file_:
    exec(file_.read(), dict(__file__=activate_env))

# Set environment variables for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
