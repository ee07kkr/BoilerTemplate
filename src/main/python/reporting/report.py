import csv
import logging
import requests

def who_in_space(url):
    if url == 'http://api.open-notify.org/astros.json':
        r = requests.get(url)
        if r.status_code == 200:
            csv_reporting(r.json())
        else:
            raise Exception("Error occureed with response code {}".format(r.status_code))
    else:
        raise Exception("Expected url - http://api.open-notify.org/astros.json")

def csv_reporting(data):

    if not data:
        return None

    if 'people' not in data:
        raise KeyError("Expect Key 'people'")

    with open('report.csv', 'w') as frep:
        csvwriter = csv.writer(frep)
        count = 0
        for item in data['people']:
            if not isinstance(item, dict):
                logging.error("Expected a dictionary, got a %s", type(item))
                raise TypeError('Dictionary expected')
            if count == 0:
                header = item.keys()
                csvwriter.writerow(header)
            count += 1
            csvwriter.writerow(item.values())
