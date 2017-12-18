import csv

ofile = open('out.csv', 'w')
writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)

db1 = open('acrftreg.csv', 'r')
db2 = open('ACFTREF.txt', 'r')

print 'Files are opened'

r1 = csv.DictReader(db1)
r2 = csv.DictReader(db2)

keys1 = ['Manu', 'Model', 'Yearmanu']
keys2 = ['NO-SEATS', 'SPEED', 'MODEL', 'TYPE-ACFT']

writer.writerow(keys1 + keys2)

print 'Readers and a writer are initialized'

limit = 1000
count = 0
for row1 in r1:
    if count == limit:
        break

    for row2 in r2:
        if row1['Model'].strip().lower() == row2['MODEL'].strip().lower():
            if '5' == row2['TYPE-ACFT']:
                row = [row1[key] for key in keys1] + [row2[key] for key in keys2[0:1]]
                writer.writerow(row)
                count += 1
    db2.seek(0)

print 'Found', count, 'matching rows'

db1.close()
db2.close()
ofile.close()
