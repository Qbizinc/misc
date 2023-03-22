#!/usr/bin/env python3

from datetime import datetime
from dateutil import relativedelta
import argparse

parser = argparse.ArgumentParser(description='Get delta between two dates')

parser.add_argument('dates', metavar='date', type=str, nargs='+',
                    help='dates (in %%Y-%%m-%%d format by default). Second date is optional (defaults to today)')

parser.add_argument('--format', dest='date_format', action='store',
                    default="%Y-%m-%d",
                    help='optional alternative strptime format')

parser.add_argument('--days', dest='total_days', action='store_const', const=True,
                    help='Show total days rather than years, months, days')

args = parser.parse_args()

d0 = datetime.strptime(args.dates[0], args.date_format)
if len(args.dates) == 1:
    d1 = datetime.now()
else:
    d1 = datetime.strptime(args.dates[1], args.date_format)

delta = relativedelta.relativedelta(d1, d0)
delta_days = d1 - d0

if args.total_days:
    print(f"{delta_days.days} days")
else:
    print(f"{delta.years} years, {delta.months} months, {delta.days} days")


