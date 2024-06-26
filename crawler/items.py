# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    company = scrapy.Field()
    address = scrapy.Field()
    salary = scrapy.Field()
    created_at = scrapy.Field()
    end_date = scrapy.Field()
    experience = scrapy.Field()
    degree = scrapy.Field()
    request_genders = scrapy.Field()
    working_form = scrapy.Field()
    quantity = scrapy.Field()
    age = scrapy.Field()
    description = scrapy.Field()
    benefit = scrapy.Field()
    job_requirement = scrapy.Field()
    contact = scrapy.Field()
    job_tag = scrapy.Field()
    position = scrapy.Field()


class Employer(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    career = scrapy.Field()
    company_size = scrapy.Field()
    followers = scrapy.Field()
    description = scrapy.Field()


class Candidate(scrapy.Item):
    name = scrapy.Field()
    birth_date = scrapy.Field()
    gender = scrapy.Field()
    marital_status = scrapy.Field()
    address = scrapy.Field()
    position = scrapy.Field()
    position_recruitment = scrapy.Field()
    salary = scrapy.Field()
    working_form = scrapy.Field()
    career = scrapy.Field()
    target_work_address = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    skill = scrapy.Field()
    language = scrapy.Field()
    achievements = scrapy.Field()
