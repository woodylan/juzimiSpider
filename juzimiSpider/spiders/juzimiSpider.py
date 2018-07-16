import scrapy

from juzimiSpider.items import JuzimispiderItem

class juzimiSpider(scrapy.Spider):
    name = "juzimi"
    allowed_domains = ['juzimi.com']

    def start_requests(self):
        url = 'https://www.juzimi.com/length/%E7%9F%AD%E5%8F%A5%E5%AD%90'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        juzi_list = response.css('div.view-xqlengthpage').xpath('div/div/div')
        for juzi in juzi_list:
            item = JuzimispiderItem()
            content = juzi.xpath('div/a/text()').extract()[0]
            author = juzi.xpath('div/a/text()').xpath('div[@class="xqjulistwafo"]/a//text()').extract()[0]
            book = juzi.xpath('div/a/text()').xpath('div[@class="xqjulistwafo"]//span/a//text()').extract()[0]
            item['content'] = content
            item['author'] = author
            item['book'] = book
            yield item

        ## 是否还有下一页
        next_pages = response.css('li.pager-next a::attr(href)').extract()[0]

        if next_pages:
            next_page = 'https://www.juzimi.com' + next_pages.extract()
            self.log('page_url: %s' % next_page)
            ## 将 「下一页」的链接传递给自身，并重新分析
            yield scrapy.Request(next_page, callback=self.parse)
