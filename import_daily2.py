import subprocess
import sqlite3
import datetime
import sys
import time
from phone_data import *

conn = sqlite3.connect('phone.db')
cur = conn.cursor()

script = "auto_data.acsauto"

queues = {1: 471, 2: 487, 3: 485, 4: 554}
update_script('"' + str(queues[1]) + '"', script)
start_date = datetime.date(year=2017, month=6, day=8)

if len( sys.argv ) > 1:
    try:
        start_date = datetime.date(year=int(sys.argv[1]),month=int(sys.argv[2]), day=int(sys.argv[3]) )
    except (TypeError, ValueError):
        sys.exit("To Specify Start date Override, use syntax: python" + sys.argv[0] + " YYYY MM DD")
else:
    newest_date = get_newest_date(conn)
    start_date = datetime.date(year=int(newest_date[0][0][0:4]),
                               month=int(newest_date[0][0][5:7]),
                               day=int(newest_date[0][0][-2:]))

'''subprocess.run("warmup.acsup", shell=True)
print("Sleeping 30s")
time.sleep(30)'''

for queue_id in range(1, 5):
    rundate = start_date
    if queue_id > 1:
        update_script('"' + str(queues[queue_id]) + '"', script)

    while rundate < (datetime.date.today() - datetime.timedelta(days=1)):
        rundate = rundate + datetime.timedelta(days=1)
        if rundate.isoweekday() in (6,7):
            continue

        update_date(rundate.strftime("%m/%d/%y"), script)
        subprocess.run(script, shell=True)
        time.sleep(3)
        '''subprocess.run("taskkill /IM acs*", shell=True)
        time.sleep(1)'''
        subprocess.run("taskkill /IM acs*", shell=True)
        filename = "daily_phone.txt"
        query, data = read_data(filename, rundate, queue_id)
        cur.executemany(query, data)
        conn.commit()

purge_zero_records(conn)
conn.commit()

