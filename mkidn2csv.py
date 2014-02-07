#!/usr/bin/python
# -*- coding: utf-8

from csv import DictWriter
from lxml import html
from sys import stdin, stdout

table = html.parse(stdin).findall('.//tbody')[0]
headers = ['final', 'org', 'project', 'amount']
lines = []
for row in table:
    values = {
        'final': row[0].text.split()[0].replace(' ', ''),
        'org': row[2].text.encode('utf-8'),
        'project': row[3].text.encode('utf-8'),
    }
    for points in row[3].findall('.//strong'):
        title, amount = points.text.split('-')
        title = title.strip().encode('utf-8')
        values[title.strip()] = amount.replace(' ', '')
        if title not in headers:
            headers.append(title)
    if row[4].text == u'Łącznie: ':
        values['amount'] = row[4][0].text.replace(' ', '')
    else:
        for br in row[4].findall('br'):
            if br.tail == u'Łącznie: ':
                values['amount'] = br.getnext().text.replace(' ', '')
    lines.append(values)

writer = DictWriter(stdout, headers)
writer.writerow({h:h for h in headers})
for line in lines:
    writer.writerow(line)
