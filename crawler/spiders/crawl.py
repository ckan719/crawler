from scrapy import Spider
from scrapy.selector import Selector
from crawler.items import Job
from crawler.items import Employer
from crawler.items import Candidate
import os
from dotenv import load_dotenv
from scrapy.http import FormRequest

load_dotenv(dotenv_path="./crawler/.env")


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["huejob.vn"]
    start_urls = os.getenv('START_URL').split(", ")

    def parse(self, response):
        return [
            FormRequest(
                "https://huejob.vn/login",
                formdata={
                    "user[email]": os.getenv('USER'),
                    "user[password]": os.getenv('PASSWORD'),
                    "btn_submit": ''
                },
                callback=self.root_crawler),
        ]

    def root_crawler(self, response):
        if response.css('a.login::attr("href")').get() == "/login/logout":
            print("Login Success !")
        else:
            print("Login Failure !")
            return
        for url in os.getenv('START_URL').split(", "):
            yield response.follow(url, self.sub_crawler)

    def sub_crawler(self, response):
        # Crawl Job
        if response.url == "https://huejob.vn/viec-lam":
            yield response.follow(response.url, self.parse_job)
        # Crawl employer
        if response.url == "https://huejob.vn/nha-tuyen-dung":
            yield response.follow(response.url, self.parse_employer)
        # Crawl candidate
        if response.url == "https://huejob.vn/ung-vien":
            yield response.follow(response.url, self.parse_candidate)

    # Join Data
    def join_data(self, response):
        try:
            return " ".join(response.strip().split())
        except:
            return ""

    # Crawl Job
    def parse_job(self, response):
        for quotes in response.css('div.job-info.yes-logo'):
            yield response.follow(quotes.css('h3 a::attr("href")').get(), self.get_job)

        next_page = response.css(
            'li.paginate_button.next a::attr("href")').get()
        if next_page is not None and next_page != 'javascript:void(0);':
            yield response.follow(next_page, self.parse_job)

    # Crawl employer
    def parse_employer(self, response):
        for quotes in response.css('div.employer-info div.info-top'):
            yield response.follow(quotes.css('h3 a::attr("href")').get(), self.get_employer)

        next_page = response.css(
            'li.paginate_button.next a::attr("href")').get()
        if next_page is not None and next_page != 'javascript:void(0);':
            yield response.follow(next_page, self.parse_employer)

    # Crawl candidate
    def parse_candidate(self, response):
        for quotes in response.css('div.grid-content.candidate-item-search'):
            yield response.follow(quotes.css('a::attr("href")').get(), self.get_candidate)

        next_page = response.css(
            'li.paginate_button.next a::attr("href")').get()
        if next_page is not None and next_page != 'javascript:void(0);':
            yield response.follow(next_page, self.parse_candidate)

    # Crawl Job
    def get_job(self, response):
        item = Job()
        item['title'] = self.join_data(response.css(
            'div.iw-heading-title h1::text').get())
        item['company'] = self.join_data(
            response.css('a.theme-color h2::text').get())
        item['address'] = self.join_data(response.css(
            'span.view-job-tag-place::text').getall())
        item['job_tag'] = self.join_data(response.css(
            'span.view-job-tag-field::text').getall())
        item['salary'] = self.join_data(response.css(
            'div.view-job-div-right.top span:last-child::text').get())
        item['end_date'] = self.join_data(response.css(
            'div.view-job-div-right')[1].css('span:last-child::text').get())
        item['experience'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[0].css('div p::text')[0].get())
        item['degree'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[0].css('div p::text')[1].get())
        item['request_genders'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[0].css('div p::text')[2].get())
        item['working_form'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[1].css('div p::text')[0].get())
        item['position'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[1].css('div p::text')[1].get())
        item['quantity'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
            0].css('div.row div')[1].css('div p::text')[2].get())
        item['description'] = self.join_data(response.css(
            'p.job-detail-description::text')[0].get())
        item['benefit'] = self.join_data(response.css(
            'p.job-detail-description::text')[1].get())
        item['contact'] = self.join_data(response.css(
            'div#other_info::text').getall())
        yield item

    # Crawl employer
    def get_employer(self, response):
        item = Employer()
        item['name'] = self.join_data(response.css(
            'div.employer-info-top div.info-top div.content-right p::text').get())
        item['address'] = self.join_data(response.css('div.iwj-employer-widget-wrap div ul li')[
            0].css('div.content span.map span.detail::text').get())
        item['career'] = self.join_data(response.css(
            'div.iwj-employer-widget-wrap div ul li')[1].css('div.content span a::text').getall())
        item['company_size'] = self.join_data(response.css(
            'div.iwj-employer-widget-wrap div ul li')[2].css('div.content span::text').get())
        item['followers'] = self.join_data(response.css(
            'div.iwj-employer-widget-wrap div ul li')[3].css('div.content span::text').get())
        item['description'] = self.join_data(response.css(
            'div.employer-detail-info div.iwj-employerdl-des div.content p').get())
        yield item

    # Crawl candidate
    def get_candidate(self, response):
        item = Candidate()
        item['name'] = self.join_data(
            response.css('b.txt-candidate-name::text').get())
        item['position_recruitment'] = self.join_data(
            response.css('b.txt-candidate-position::text')[0].get())
        item['experience'] = self.join_data(response.css(
            'b.txt-candidate-position::text')[1].get())
        item['birth_date'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                            0].css('p.job-detail-description')[0].css('span::text').get())
        item['gender'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                        0].css('p.job-detail-description')[1].css('span::text').get())
        item['marital_status'] = self.join_data(response.css(
            'div.job-detail-desc.item.title-job-view-detail-narrow')[0].css('p.job-detail-description')[2].css('span::text').get())
        item['address'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                         0].css('p.job-detail-description')[3].css('span::text').get())
        item['position'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                          2].css('p.job-detail-description')[0].css('span::text').get())
        item['salary'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                        2].css('p.job-detail-description')[1].css('span::text').get())
        item['working_form'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                              2].css('p.job-detail-description')[2].css('span::text').get())
        item['career'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                        2].css('p.job-detail-description')[3].css('span::text').get())
        item['target_work_address'] = self.join_data(response.css(
            'div.job-detail-desc.item.title-job-view-detail-narrow')[2].css('p.job-detail-description')[4].css('span::text').get())
        item['skill'] = self.join_data(response.css(
            'div.job-detail-desc.item.title-job-view-detail-narrow')[4].css('div div p').get())
        item['language'] = self.join_data(response.css(
            'div.job-detail-desc.item.title-job-view-detail-narrow')[5].css('p.job-detail-description').get())
        item['education'] = self.join_data(response.css('div.job-detail-desc.item.title-job-view-detail-narrow')[
                                           6].css('p.job-detail-description')[0].css('span::text').get())
        item['achievements'] = self.join_data(response.css(
            'div.job-detail-desc.item.title-job-view-detail-narrow')[7].css('p').get())
        yield item
