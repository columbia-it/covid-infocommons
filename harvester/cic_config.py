import logging
import os
import sys

CIC_BASE = "https://cice-dev.paas.cc.columbia.edu"
#CIC_BASE= "http://52.44.240.4"

logging.basicConfig(filename='cic_harvester.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

CIC_TOKEN = os.getenv('CIC_TOKEN')
if not CIC_TOKEN:
    sys.exit("FATAL! Could not find authentication in CIC_TOKEN")

