import csv
import psutil
import time
import datetime

with open('cpu_utilization.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow(["timestamp", "cpu_utilization"])
    while (True):
        timestamp = datetime.datetime.now()
        cpu = psutil.cpu_percent()

        data = [timestamp, cpu]
        writer.writerow(data)
        time.sleep(1/10)