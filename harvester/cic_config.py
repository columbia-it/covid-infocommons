import logging
import os
import sys

CIC_BASE = "https://cic-apps.datascience.columbia.edu"

logging.basicConfig(filename='cic_harvester.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

CIC_TOKEN = os.getenv('CIC_TOKEN')
if not CIC_TOKEN:
    sys.exit("FATAL! Could not find authentication in CIC_TOKEN")

