#include company
#don't include if address less than 3 lines
#if address is only 2 lines, and comma, split at first comma

from __future__ import print_function

import cgi
import csv
import os
import re
import sys

import pprint


def warning(*objs):
    print("WARNING:", *objs, file=sys.stderr)


def error(*objs):
    print("ERROR:", *objs, file=sys.stderr)


def fatal(*objs):
    print("FATAL:", *objs, file=sys.stderr)
    sys.exit(1)


def inarray(name, array):
    lname = name.strip().lower()
    for s in array:
        if lname == s.lower():
            return True
    return False


def do_csv(input, output):
    gmap = {}
    """
    fields = [
      'Name',
      'Given Name',
      'Additional Name',
      'Family Name',
      'Address 1 - Type',
      'Address 1 - Formatted',
      'Address 1 - Street',
      'Address 1 - City',
      'Address 1 - PO Box',
      'Address 1 - Region',
      'Address 1 - Postal Code',
      'Address 1 - Country',
      'Address 1 - Extended Address',
      'Address 2 - Type',
      'Address 2 - Formatted',
      'Address 2 - Street',
      'Address 2 - City',
      'Address 2 - PO Box',
      'Address 2 - Region',
      'Address 2 - Postal Code',
      'Address 2 - Country',
      'Address 2 - Extended Address',
    ]
    """

    afields = [
        'Address %d - Street',
        'Address %d - Extended Address',
        'Address %d - PO Box', ]

    cfields = [
        'Address %d - City',
        'Address %d - Region',
        'Address %d - Postal Code', ]
    xml = ''
    header = False
    line_no = 0
    read = 0
    wrote = 0
    with open(input, 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            read += 1
            line_no = line_no + 1
            if not header:
                gfields = row
                for k, v in enumerate(gfields):
                    gmap[v] = k
                header = True
                continue

            #for field in fields:
            #  if field in gmap:
            #    print('%s: %s' % (field, row[gmap[field]]))

            name = row[gmap['Name']].strip()

            if 'Organization 1 - Name' in gmap:
                org = row[gmap['Organization 1 - Name']].strip()
            else:
                org = ''

            if 'Given Name' in gmap:
                first = row[gmap['Given Name']].strip()
            else:
                first = ''

            if 'Family Name' in gmap:
                last = row[gmap['Family Name']].strip()
            else:
                last = ''

            for no in range(1, 20):
                typ = 'Address %s - Type' % no
                if not typ in gmap:
                    break

                faddress = []
                for afield in afields:
                    fname = afield % no
                    line = row[gmap[fname]].strip()

                    if re.search(':::', line):
                        lines = line.split(':::')
                        line = lines[0]

                    line = line.strip()
                    # squash multiple spaces
                    line = line.replace('  ', ' ')
                    if line == '':
                        continue

                    faddress.append(line)

                if len(faddress) < 1:
                    #if org != "":
                    #    print("Skipping address %d: %s/%s: no address" % (no, name, org))
                    continue

                caddress = []
                city_state_zip = ''
                for cfield in cfields:
                    fname = cfield % no
                    line = row[gmap[fname]].strip()

                    if re.search(':::', line):
                        lines = line.split(':::')
                        line = lines[0]

                    line = line.strip()
                    # squash multiple spaces
                    line = line.replace('  ', ' ')
                    if line == '':
                        continue

                    caddress.append(line)

                    if len(caddress) == 3:
                        city_state_zip = "%s, %s  %s" % (caddress[0], caddress[
                            1], caddress[2])
                    if len(caddress) == 2:
                        city_state_zip = "%s, %s" % (caddress[0], caddress[1])
                    if len(caddress) == 1:
                        city_state_zip = caddress[0]

                if city_state_zip != '':
                    faddress.append(city_state_zip)

                fname = 'Address %d - Country' % no
                line = row[gmap[fname]].strip()
                if not re.search('^\s*(u.?s|u.?s.?a|united\s+states)', line, re.IGNORECASE):
                    formatted = 'Address %s - Formatted' % no
                    address = row[gmap[formatted]]
                    addressses = address.split(':::')
                    address = addressses[0]
                    
                    faddress = address.split("\n")

                fileas = name
                
                if name != '':
                    if not inarray(name, faddress):
                        faddress.insert(0, name)
                    if org != '':
                        if not inarray(org, faddress):
                            faddress.insert(1, org)
                else:
                    if org != '':
                        fileas = org
                        if not inarray(org, faddress):
                            faddress.insert(0, org)
                    else:
                        # print("Skipping row %d: no name or org" % line_no)
                        continue

                if row[gmap[typ]]:
                    fileas += ' (' + row[gmap[typ]] + ')'

                #if org != "":
                #    print("%3d: %s" % (line_no, org))
                #    #pprint.pprint(faddress)

                addressdata = '\n'.join(faddress)

                elem = """
\t<AddressEntry>
\t\t<AddressData>%s</AddressData>
\t\t<Name>
\t\t\t<FirstName>%s</FirstName>
\t\t\t<LastName>%s</LastName>
\t\t\t<FileAs>%s</FileAs>
\t\t</Name>
\t</AddressEntry>
"""

                xml += elem % (
                    cgi.escape(addressdata, True), cgi.escape(first, True),
                    cgi.escape(last, True), cgi.escape(fileas, True))
                wrote += 1

    xml2 = """<?xml version="1.0" encoding="utf-8"?>
<AddressBook
\tVersion="8.0"
\tDefaultPermutation="true"
\tFormat="Native">
%s
</AddressBook>
""" % xml

    print(" > Read %d contacts, wrote %d addresses" % (read, wrote))

    with open(output, 'wb') as out:
        out.write(xml2)


if len(sys.argv) < 2:
    sys.exit(
        "Usage: " + sys.argv[0] + " filename.csv|directory [output_directory]")

input = sys.argv[1]
if len(sys.argv) >= 3:
    output = sys.argv[2]
else:
    output = ""

csvs = []
if os.path.isfile(input):
    csvs.append(input)
else:
    for root, dirs, files in os.walk(input):
        for file in files:
            if file.endswith(".csv"):
                f = os.path.join(root, file)
                f = re.sub(r'\\', '/', f)
                csvs.append(f)

for f in csvs:
    abx = os.path.splitext(f)[0] + ".abx"
    print("Processing %s" % f)
    do_csv(f, abx)
