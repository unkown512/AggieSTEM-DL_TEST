#!/usr/bin/python3
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/FlaskApp/FlaskApp")

from __init__ import app as application 
application.secret_key = os.environ.get('SECRET_KEY') or 'SUPPOSED-to-be-a-secret'

if __name__ == "__main__":
  application.run()
