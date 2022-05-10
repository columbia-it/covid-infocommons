import os
import sys

CIC_BASE = "https://cice-dev.paas.cc.columbia.edu"

CIC_TOKEN = os.getenv('CIC_TOKEN')
if not CIC_TOKEN:
    sys.exit("FATAL! Could not find authentication in CIC_TOKEN")

