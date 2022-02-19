from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import Job
from crawler.items import Employer
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./crawler/.env")


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["huejob.vn"]
    start_urls = os.getenv('START_URL').split(", ")

    def parse(self, response):
        # Crawl Job
        if response.url == "https://huejob.vn/viec-lam":
            yield response.follow(response.url, self.parse_job)
        # Crawl employer
        if response.url == "https://huejob.vn/nha-tuyen-dung":
            yield response.follow(response.url, self.parse_employer)

    def parse_job(self, response):
        for quotes in response.css('div.job-info.yes-logo'):
            yield response.follow(quotes.css('h3 a::attr("href")').get(), self.get_job)

        next_page = response.css(
            'li.paginate_button.next a::attr("href")').get()
        if next_page is not None and next_page != 'javascript:void(0);':
            yield response.follow(next_page, self.parse_job)

    def parse_employer(self, response):
        for quotes in response.css('div.employer-info div.info-top'):
            yield response.follow(quotes.css('h3 a::attr("href")').get(), self.get_employer)

        next_page = response.css(
            'li.paginate_button.next a::attr("href")').get()
        if next_page is not None and next_page != 'javascript:void(0);':
            yield response.follow(next_page, self.parse_employer)

    def get_job(self, response):
        item = Job()
        item['title'] = response.css('div.iw-heading-title h1::text').get()
        item['company'] = response.css('a.theme-color h2::text').get()
        item['address'] = response.css(
            'span.view-job-tag-place::text').getall()
        item['job_tag'] = response.css(
            'span.view-job-tag-field::text').getall()
        item['salary'] = response.css(
            'div.view-job-div-right.top span:last-child::text').get().strip()
        item['end_date'] = response.css(
            'div.view-job-div-right')[1].css('span:last-child::text').get().strip()
        item['experience'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[0].css('div p::text')[0].get().strip()
        item['degree'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[0].css('div p::text')[1].get().strip()
        item['request_genders'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[0].css('div p::text')[2].get().strip()
        item['working_form'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[1].css('div p::text')[0].get().strip()
        item['position'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[1].css('div p::text')[1].get().strip()
        item['quantity'] = response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[1].css('div p::text')[2].get().strip()
        item['description'] = response.css(
            'p.job-detail-description::text')[0].get().strip()
        item['benefit'] = response.css(
            'p.job-detail-description::text')[1].get().strip()
        item['contact'] = " ".join(response.css(
            'div#other_info::text').getall()).strip()
        yield item

    def get_employer(self, response):
        item = Employer()
        item['name'] = response.css(
            'div.employer-info-top div.info-top div.content-right p::text').get().strip()
        item['address'] = response.css('div.iwj-employer-widget-wrap div ul li')[
            0].css('div.content span.map span.detail::text').get().strip()
        item['career'] = response.css(
            'div.iwj-employer-widget-wrap div ul li')[1].css('div.content span a::text').getall()
        item['company_size'] = response.css(
            'div.iwj-employer-widget-wrap div ul li')[2].css('div.content span::text').get().strip()
        item['followers'] = response.css(
            'div.iwj-employer-widget-wrap div ul li')[3].css('div.content span::text').get().strip()
        item['description'] = response.css(
            'div.employer-detail-info div.iwj-employerdl-des div.content p').get()
        yield item
