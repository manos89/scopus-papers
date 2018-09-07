import scrapy,json,requests
from scopus.items import ScopusItem
from scrapy.loader import ItemLoader


class QuotesSpider(scrapy.Spider):
    name = "scopus"

    def start_requests(self):
        self.request_counter=0
        self.urls=[]
        self.base_url='https://api.elsevier.com/content/search/scopus?query="{KW}"&apiKey={APIKEY}&httpAccept=application/json&stardindex={i}'
        r=requests.get( self.base_url.replace('{KW}', self.kw).replace('{APIKEY}', self.apikey).replace('{i}',str(0)))
        data=json.loads(r.text)
        finalnumber=int(data['search-results']['opensearch:totalResults'])
        finalnumber=int(finalnumber/finalnumber)+1
        print(str(finalnumber))
        for i in range(0,100,25):
            self.newurl = self.base_url.replace('{KW}', self.kw).replace('{APIKEY}', self.apikey).replace('{i}',str(i))
            self.urls.append(self.newurl)
        for url in   self.urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        l = ItemLoader(item=ScopusItem(), response=response)
        data=json.loads(response.body)
        # print(data)
        print(response.url)
        print(str(self.request_counter))
        self.request_counter+=1
        for d in data['search-results']['entry']:
            l.add_value('entry', d)
            yield l.load_item()


