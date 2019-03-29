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
      'Address %d - PO Box',
    ]

    cfields = [
      'Address %d - City',
      'Address %d - Region',
      'Address %d - Postal Code',
    ]
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

        if not row[0]:
          continue
        #print("%s: %s" % (line_no, row[0]))

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
     
          formatted = 'Address %s - Formatted' % no
          address = row[gmap[formatted]]
          fileas = name

          addressses = address.split(':::')
          """
          for afield in afields:
            fname = afield % no
            field = row[gmap[fname]].strip()
            if field == '':
                continue
          """
          if row[gmap[typ]]:
            fileas += ' (' + row[gmap[typ]] + ')'

          for address in addressses:
            lines = address.split("\n")

            faddress = []

            for i, line in enumerate(lines):
              # squash multiple spaces
              line = line.replace('  ', ' ')
              line = line.strip()
              if line == '':
                continue
              if re.search('^\s*(u.?s|u.?s.?a)', line, re.IGNORECASE):
                continue
              if re.search('^\s*united\s+states', line, re.IGNORECASE):
                continue
               
              faddress.append(line)

            if len(faddress) < 1:
              continue

            if len(faddress) == 1:
                faddress = faddress[0].split(',')

            if name != '':
                if not inarray(name, faddress):
                    faddress.insert(0, name)
                if org != '':
                    if not inarray(org, faddress):
                        faddress.insert(1, org)
            else:
                if org != '':
                    if not inarray(org, faddress):
                        faddress.insert(0, org)
                else:
                    continue
            addressdata = '\n'.join(faddress)

            xml += """
\t<AddressEntry>
\t\t<AddressData>%s</AddressData>
\t\t<Name>
\t\t\t<FirstName>%s</FirstName>
\t\t\t<LastName>%s</LastName>
\t\t\t<FileAs>%s</FileAs>
\t\t</Name>
\t</AddressEntry>
""" % (
      cgi.escape(addressdata, True),
      cgi.escape(first, True),
      cgi.escape(last, True),
      cgi.escape(fileas, True)
    )
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
  sys.exit("Usage: " + sys.argv[0] + " filename.csv|directory [output_directory]")

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
