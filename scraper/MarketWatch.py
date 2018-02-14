#!/usr/bin/python

import re
import scrapy

from datetime import datetime
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import ipdb

class MarketWatchSpider(scrapy.Spider):
    name = 'market watcher'
    start_urls = ['http://www.marketwatch.com/investing/stock/pcln/financials/income/quarter']

    def parse_cell_value(self, cell):
        val, unit = 0, ''
        m = re.search(r'(\(?[-\d.]+[M|B|%]?\)?)', cell)
        if m is None:
            return val, unit

        val = m.group(0)
        if (val == '-'):
            return 0, ''

        if (val[0] == '('):
            val = float('-' + val[1:-1])
        if (val[-1] == 'M' or val[-1] == 'B' or val[-1] == '%'):
            unit = val[-1]
            val = float(val[0:-1])
        else:
            val = float(val)
        return val, unit

            
    def print_report(self, reports):
        print("----------------------------------------------------------------------------------------------------------")
        line = '{:>50}\t'.format('')
        for d in reports["dates"]:
            line += '{:>15}'.format(d.strftime("%b-%d-%Y"))
        print(line)

        for t, vallist in reports.items():
            if (t == "dates"):
                continue
            line = '{:>50}\t'.format(t.rstrip())
            for val, unit in vallist:
                line += '{:>15}'.format('{:.2f}{}'.format(val, unit))
            print(line)


    def parse_table(self, table):
        reports = {'dates': []}
        for thead in table.xpath('.//th[@scope="col"]/text()').extract():
            try:
                reports['dates'].append(datetime.strptime(thead, "%d-%b-%Y"))
            except:
                pass
        for tr in table.xpath('.//tbody/tr'):
            title =  ' '.join([t for t in tr.xpath('.//td[@class="rowTitle"]/text()').re(r'\s*(.*)') if t!= u''])
            reports[title] = []
            for t in tr.xpath('.//td[contains(@class, "valueCell")]/text()').extract():
                val, unit = self.parse_cell_value(t)
                reports[title].append((val, unit))
        self.print_report(reports)


    def parse(self, response):
        print("Start crawling")
        tables = Selector(response=response).xpath('//table[@class="crDataTable"]')
        for table in tables:
            self.parse_table(table)

#if __name__ == "__main__":
