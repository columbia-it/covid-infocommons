import requests
from datetime import datetime
import sched, time

def main(scheduler):
    start1 = datetime.now()
    r = requests.get("https://cic-apps.datascience.columbia.edu/grants/")
    end1 = datetime.now()
    print('/grants took: ')
    print(end1 - start1)
    start2 = datetime.now()
    print(r)
    pi_url = 'https://cic-apps.datascience.columbia.edu/search/facets?field=principal_investigator.full_name'
    r2 = requests.get(pi_url)
    end2 = datetime.now()
    print('PI /facets took: ')
    print(end2 - start2)
    print(r2)

if __name__ == '__main__':
    my_scheduler = sched.scheduler(time.time, time.sleep)
    while True:
        my_scheduler.enter(60, 1, main, (my_scheduler,))
        my_scheduler.run()
