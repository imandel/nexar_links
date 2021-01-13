from datetime import date, datetime, timedelta
import csv
import requests
yesterday = int(datetime.timestamp(datetime.combine(date.today()-timedelta(1), datetime.min.time()))) *1000

with open('scripts/h3s.txt', 'r') as inf:
    h3_ints = inf.read().split()

h3_ints = list(h3_ints)
n=300
hunks = [h3_ints[x:x+n] for x in range(0, len(h3_ints), n)]

with open(f'data/{yesterday}.csv', 'w') as of:
    csv_writer = csv.writer(of, delimiter=',')
    csv_writer.writerow(['image_ref', 'timestamp', 'lat','lng'])
    for hunk in hunks:
        url = 'https://live-api.nexar.mobi/api/roadItem/findRawFrames'
        headers = {'Content-Type': 'application/json'}
        filters = {'limit': 10000,'filters': {'h3_indices': {'h3_indices': hunk},
                                                 'start_timestamp': yesterday,
                                                  'end_timestamp': yesterday + int(timedelta(1).total_seconds() * 10000)}}
        response = requests.post(url, headers=headers, json=filters)
        data = response.json()
        if 'raw_frames' in data:
                lines = list(map(lambda frame: [frame['image_ref'],frame['captured_on_ms'],frame['gps_point']['latitude'],frame['gps_point']['longtitude']],data['raw_frames']))
                csv_writer.writerows(lines)