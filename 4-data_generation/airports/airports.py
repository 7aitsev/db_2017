import csv
import sys

ofile = open('out.csv', 'w')
writer = csv.writer(ofile, quoting=csv.QUOTE_ALL);
with open('airports.csv', 'r') as inpf:
    reader = csv.DictReader(inpf);
    
    keys = ['name', 'latitude_deg', 'longitude_deg', 'municipality', 'iso_country']
    writer.writerow(keys)
    
    for row in reader:
        if('RU' == row['iso_country']):
            writer.writerow([row[key] for key in keys[:-1]])

close(ofile)
