from __future__ import print_function

import cgi
import csv
import re
import sys

def warning(*objs):
  print("WARNING:", *objs, file=sys.stderr)

def error(*objs):
  print("ERROR:", *objs, file=sys.stderr)

def fatal(*objs):
  print("FATAL:", *objs, file=sys.stderr)
  sys.exit(1)

if len(sys.argv) != 3:
  sys.exit("Usage: " + sys.argv[0] + " filename.csv output.abx")

input = sys.argv[1]
output = sys.argv[2]

gmap = {}

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

xml = """<?xml version="1.0" encoding="utf-8"?>
<AddressBook
\tVersion="8.0"
\tDefaultPermutation="true"
\tFormat="Native">
"""

header = False
line_no = 0
with open(input, 'rb') as csvfile:
  csvreader = csv.reader(csvfile)
  for row in csvreader:
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

    if name == '':
      continue

    if 'Given Name' in gmap:
      first = row[gmap['Given Name']].strip()
    else:
      first = ''

    if 'Family Name' in gmap:
      last = row[gmap['Family Name']].strip()
    else:
      last = ''

    for no in range(1, 20):
      type = 'Address %s - Type' % no
      if not type in gmap:
        break
      formatted = 'Address %s - Formatted' % no
      address = row[gmap[formatted]]
      fileas = name

      addressses = address.split(':::')

      if row[gmap[type]]:
        fileas += ' (' + row[gmap[type]] + ')'

      for address in addressses:
        lines = address.split("\n")

        addressdata = ''

        for i, line in enumerate(lines):
          line = line.replace('  ', ' ')
          line = line.strip()
          if line == '':
            continue
          if re.search('^\s*(US|USA|U.S.|U.S.A)', line.upper()):
            continue
          if re.search('^\s*UNITEDs+STATES', line.upper()):
            continue

          if addressdata:
            addressdata += "\n"
          addressdata += line

        if not addressdata:
          continue

        addressdata = name + "\n" + addressdata

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

xml += """
</AddressBook>
"""

with open(output, 'wb') as out:
  out.write(xml)
