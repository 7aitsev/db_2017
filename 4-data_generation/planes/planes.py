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

writer.writerow(keys1 + keys2[0:2])

print 'Readers and a writer are initialized'

cr1 = []
cr2 = []
for row1 in r1:
    cr1.append([row1[key] for key in keys1]);
for row2 in r2:
    cr2.append([row2[key] for key in keys2])

print 'Cache created'

outrows = []
def add_row(ca):
    man = ca[0].strip()
    mod = ca[1].strip()
    j = 0
    while j < len(outrows):
        if outrows[j][1].lower() == mod.lower():
            if outrows[j][0].lower() != man.lower():
                print 'Warning: model "{}" is the same for differrent manufactures:'.format(ca[1])
                print '\t"{}" and "{}"'.format(outrows[j][0], man)
            return
        j += 1
    outrows.append([man, mod, ca[2], ca[3], ca[4]])
    return

i = 0
limit = 1000000
count = 0
for row1 in cr1:
    if count == limit:
        break

    while i < len(cr2):
        row2 = cr2[i]
        if row1[1].strip().lower() == row2[2].strip().lower():
            if '5' == row2[3]:
                row = row1 + row2[0:2]
                add_row(row)
                count += 1
        i += 1
    i = 0

print 'Found', count, 'matching rows'

for row in outrows:
    writer.writerow(row)

db1.close()
db2.close()
ofile.close()
