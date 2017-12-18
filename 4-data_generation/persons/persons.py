import datetime
import random
import csv

start = datetime.date(1910, 1, 1)
end = datetime.date(2018, 1, 1)
def get_bday():
    return start + datetime.timedelta(
        seconds = random.randint(0, int((end - start).total_seconds()))
    )


ofile = open('out.csv', 'w')
writer = csv.writer(ofile, quoting=csv.QUOTE_ALL);
with open('persons.csv', 'r') as inpf:
    reader = csv.DictReader(inpf);
    
    keys = ['first_name', 'last_name', 'phone1', 'bday']
    writer.writerow(keys)
    
    for row in reader:
        row['bday'] = get_bday()
        writer.writerow([row[key] for key in keys])

ofile.close()
