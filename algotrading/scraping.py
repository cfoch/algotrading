# Algotrading
#
#       src/scraping.py
#
# Copyright (c) 2017, Fabian Orccon <cfoch.fabian@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.
import os
import bs4
import requests
import datetime
import pandas_datareader.data as web
from algotrading.settings import OUT_DIR


def csv_from_ticker(ticker, start=None, end=None):
    filename = ticker.lower() + ".csv"
    csv_path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(csv_path):
        if start is None:
            start = datetime.datetime(2000, 1, 1)
        if end is None:
            end = datetime.datetime.now().replace(second=0, microsecond=0)
        df = web.DataReader(ticker.upper(), 'yahoo', start, end)
        df.to_csv(csv_path)
    return csv_path


def SP500_tickers_from_wikipedia():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    table = soup.find("table", {"class": "wikitable sortable"})
    tickers = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        tickers.append(ticker)
    return tickers
