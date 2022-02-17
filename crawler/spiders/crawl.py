from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import Job

class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["huejob.vn"]
    start_urls = [
        "https://huejob.vn/viec-lam",
    ]

    def parse(self, response):
        for quotes in response.css('div.job-info.yes-logo'):
            yield response.follow(quotes.css('h3 a::attr("href")').get(),self.get)

        next_page = response.css('li.paginate_button.next a::attr("href")').get()
        if next_page is not None and next_page != 'javascript:void(0);':
            # print("-----", next_page)
            yield response.follow(next_page, self.parse)
    def get(self, response):
        item = Job()
        item['title'] = response.css('div.iw-heading-title h1::text').get()
        item['company'] = response.css('a.theme-color h2::text').get()
        item['address'] = response.css('span.view-job-tag-place::text').getall()
        item['job_tag'] = response.css('span.view-job-tag-field::text').getall()
        item['salary'] = response.css('div.view-job-div-right.top span:last-child::text').get().strip()
        item['end_date'] = response.css('div.view-job-div-right')[1].css('span:last-child::text').get().strip()
        item['experience'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[0].css('div p')[0].css('p::text').get().strip()
        item['degree'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[0].css('div p')[1].css('p::text').get().strip()
        item['request_genders'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[0].css('div p')[2].css('p::text').get().strip()
        item['working_form'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[1].css('div p')[0].css('p::text').get().strip()
        item['position'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[1].css('div p')[1].css('p::text').get().strip()
        item['quantity'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[1].css('div p')[2].css('p::text').get().strip()
        item['age'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('div.row div')[1].css('div p')[3].css('p::text').get().strip()
        item['description'] = response.css('p.job-detail-description::text')[0].get().strip()
        item['benefit'] = response.css('p.job-detail-description::text')[1].get().strip()
        item['contact'] = response.css('div#other_info::text').get().strip()
        yield item
