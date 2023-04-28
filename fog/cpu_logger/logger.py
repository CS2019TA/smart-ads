import csv
import psutil
import time

with open('cpu_utilization.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    while (True):
        cpu = [psutil.cpu_percent()]
        writer.writerow(cpu)
        time.sleep(1/10)