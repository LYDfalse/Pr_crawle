import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.http import Request
from pr.items import PrItem
from pr.items import DcontentItem
from pr.mysqlpipelines.sql import Sql

class PrSpider(scrapy.Spider):
    name = 'pr'
    allowed_dmains = ['www.23us.com']
    bash_url = 'http://www.23us.com/class/'
    bash = '.html'

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bash
            yield Request(url, self.parse)

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink').find_all('a')[-1].get_text()
        bashurl = str(response.url)[:-7]
        for num in range(1, int(max_num)):
            url = bashurl + '_' + str(num) + self.bash
            yield Request(url, callback=self.get_name)

    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor="#FFFFFF")
        for td in tds:
            novelname = td.find_all('a')[1].get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl, callback=self.get_chapterurl, meta={'name': novelname, 'url': novelurl})

    def get_chapterurl(self,response):
        item = PrItem()
        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        category = BeautifulSoup(response.text, 'lxml').table.a.contents[0]
        besh_url = BeautifulSoup(response.text, 'lxml').find('p', class_="btnlinks").a["href"]
        authors = BeautifulSoup(response.text,'lxml').find('table').find_all('td')[1].get_text()
        author = authors[1:-1]
        serialstatuss = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[2].get_text()
        serialstatus = serialstatuss[1:-1]
        serialnumbers = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[4].get_text()
        serialnumber = serialnumbers[1:-1]
        name_id = str(besh_url)[-6:-1].replace('/', '')
        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('/', '')
        item['serialstatus'] = str(serialstatus).replace('/', '')
        item['serialnumber'] = str(serialnumber).replace('/', '')
        item['name_id'] = name_id
        yield item
        yield Request(url=besh_url, callback=self.get_chapter, meta={'name_id': name_id})

    def get_chapter(self, response):
        urls = re.findall(r'<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)
        num = 0
        for url in urls:
            num = num + 1
            chapterurl = response.url + url[0]
            chaptername = url[1]
            rets =  Sql.select_chapter(chapterurl)
            if rets[0] == 1:
                print('章节已经存在了')
                pass
            else:
                yield Request(chapterurl, callback=self.get_chaptercontent, meta={'num': num,
                                                                                'name_id': response.meta['name_id'],
                                                                                'chaptername': chaptername,
                                                                                'chapterurl': chapterurl
                                                                                })
    def get_chaptercontent(self, response):
        item =DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = str(response.meta['chaptername']).replace('\xa0', '')
        item['chapterurl'] = response.meta['chapterurl']
        content = BeautifulSoup(response.text, 'lxml').find('dd', id='contents').get_text()
        item['chaptercontent'] = str(content).replace('\xa0', '')
        return item